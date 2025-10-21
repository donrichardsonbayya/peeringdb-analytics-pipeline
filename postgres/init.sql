-- Enhanced PeeringDB Data Schema
-- This schema supports queries like "Which ASNs peer at which IXs? Which facilities sit behind the busiest IXs?"

-- Organizations (companies that own networks)
CREATE TABLE IF NOT EXISTS organizations (
    org_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    website TEXT,
    city TEXT,
    country TEXT,
    region_continent TEXT,
    address1 TEXT,
    address2 TEXT,
    zipcode TEXT,
    state TEXT,
    phone TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Internet Exchanges (physical locations where networks peer)
CREATE TABLE IF NOT EXISTS internet_exchanges (
    ix_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    country TEXT,
    region_continent TEXT,
    website TEXT,
    tech_email TEXT,
    policy_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IX LANs (network segments within IXs where peering happens)
CREATE TABLE IF NOT EXISTS ix_lans (
    ixlan_id INTEGER PRIMARY KEY,
    ix_id INTEGER REFERENCES internet_exchanges(ix_id),
    name TEXT,
    descr TEXT,
    mtu INTEGER DEFAULT 1500,
    vlan INTEGER,
    dot1q_support BOOLEAN DEFAULT FALSE,
    rs_asn INTEGER, -- Route Server ASN
    arp_sponge BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Networks (ASNs and their details)
CREATE TABLE IF NOT EXISTS networks (
    network_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    asn INTEGER UNIQUE NOT NULL,
    country TEXT,
    website TEXT,
    org_id INTEGER REFERENCES organizations(org_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Network-IX LAN Connections (peering relationships)
CREATE TABLE IF NOT EXISTS network_ixlan_connections (
    netixlan_id INTEGER PRIMARY KEY,
    net_id INTEGER REFERENCES networks(network_id),
    ixlan_id INTEGER REFERENCES ix_lans(ixlan_id),
    ipaddr4 INET,
    ipaddr6 INET,
    speed INTEGER, -- Speed in Mbps
    asn INTEGER, -- Network's ASN (denormalized for easier queries)
    is_rs_peer BOOLEAN DEFAULT FALSE, -- Connected to route server
    notes TEXT,
    operational BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Facilities (data centers where networks have presence)
CREATE TABLE IF NOT EXISTS asset_facilities (
    facility_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    country TEXT,
    website TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Facility-Network Mappings (which networks are in which facilities)
CREATE TABLE IF NOT EXISTS facility_network_map (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER REFERENCES asset_facilities(facility_id),
    network_id INTEGER REFERENCES networks(network_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(facility_id, network_id)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_networks_asn ON networks(asn);
CREATE INDEX IF NOT EXISTS idx_networks_org_id ON networks(org_id);
CREATE INDEX IF NOT EXISTS idx_ix_lans_ix_id ON ix_lans(ix_id);
CREATE INDEX IF NOT EXISTS idx_netixlan_net_id ON network_ixlan_connections(net_id);
CREATE INDEX IF NOT EXISTS idx_netixlan_ixlan_id ON network_ixlan_connections(ixlan_id);
CREATE INDEX IF NOT EXISTS idx_netixlan_asn ON network_ixlan_connections(asn);
CREATE INDEX IF NOT EXISTS idx_facility_network_facility_id ON facility_network_map(facility_id);
CREATE INDEX IF NOT EXISTS idx_facility_network_network_id ON facility_network_map(network_id);

-- Views for common queries
CREATE OR REPLACE VIEW peering_summary AS
SELECT 
    n.asn,
    n.name as network_name,
    o.name as org_name,
    COUNT(DISTINCT nix.ixlan_id) as ix_count,
    COUNT(DISTINCT nix.netixlan_id) as peering_connections,
    SUM(nix.speed) as total_bandwidth_mbps
FROM networks n
LEFT JOIN organizations o ON n.org_id = o.org_id
LEFT JOIN network_ixlan_connections nix ON n.network_id = nix.net_id
WHERE nix.operational = TRUE
GROUP BY n.asn, n.name, o.name;

CREATE OR REPLACE VIEW ix_traffic_summary AS
SELECT 
    ix.ix_id,
    ix.name as ix_name,
    ix.city,
    ix.country,
    COUNT(DISTINCT nix.net_id) as connected_networks,
    COUNT(nix.netixlan_id) as total_connections,
    SUM(nix.speed) as total_bandwidth_mbps,
    AVG(nix.speed) as avg_connection_speed_mbps
FROM internet_exchanges ix
LEFT JOIN ix_lans ixlan ON ix.ix_id = ixlan.ix_id
LEFT JOIN network_ixlan_connections nix ON ixlan.ixlan_id = nix.ixlan_id
WHERE nix.operational = TRUE OR nix.operational IS NULL
GROUP BY ix.ix_id, ix.name, ix.city, ix.country;
