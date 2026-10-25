-- RideQ SCHEMA CREATION
-- updated 2026-10-17


--------------------------------------------------------------------------------
-- TABLE INFO
--------------------------------------------------------------------------------

-- Table count: 7

-- Tables
	--	Trip					--	Imported ride data
	--	TripMetadata	--	Ride classifications and local overrides
	--	Organization	--	Club, shop, and event names with org type
	-- 	Ride Level		--	HBC-only for v1; levels with speed ranges
	--	Tag						--	User-defined tags
	-- 	TripTag				--	Trip-to-tag relationships
	--	Source				--	Originating data provider (e.g. RWGPS)

-- Creation order
	-- 	1. Source					--	Needed as FK for Trip
	--	2. Organization		--	Needed as FK for Trip
	--	3. RideLevel			--	Needed as FK for Trip
	--	4. Trip						--	Needed as PK, FK for TripMetadata, TripTag
	--	5. TripMetadata
	--	6. Tag						--	Needed as FK for TripTag
	-- 	7. TripTag



--------------------------------------------------------------------------------
-- TABLE CREATION & CONSTRAINTS
-- Initial data pop for Source, Organization, Ride Level, Tag
--------------------------------------------------------------------------------

USE [RideQ];

CREATE TABLE Source (
    source_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
		shortname VARCHAR(10) NULL UNIQUE
);

INSERT INTO Source (name, shortname)
VALUES ('Ride With GPS', 'RWGPS');

----------------------------------------

CREATE TABLE Organization (
    organization_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(150) NOT NULL UNIQUE,
    abbreviation VARCHAR(20) NULL,
    organization_type VARCHAR(50) NOT NULL
        CHECK (organization_type IN ('Cycling Club', 'Bike Shop', 'Event'))
);

INSERT INTO Organization (name, abbreviation, organization_type)
VALUES
		('Harrisburg Bicycle Club', 'HBC', 'Cycling Club'),
		('Hershey Cycles', 'HC', 'Bike Shop');

----------------------------------------

CREATE TABLE RideLevel (
    ride_level_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    sort_order INT NOT NULL UNIQUE,
    speed_minimum DECIMAL(4,1) NULL
        CHECK (speed_minimum >= 0),
    speed_maximum DECIMAL(4,1) NULL
        CHECK (speed_maximum >= 0),

    CONSTRAINT ck_RideLevel_SpeedRange
        CHECK (
            speed_minimum IS NULL
            OR speed_maximum IS NULL
            OR speed_minimum <= speed_maximum
        )
);

INSERT INTO RideLevel (name, sort_order)
VALUES
    ('C', 1),
    ('C+', 2),
    ('Flex', 3),
    ('B', 4),
    ('B+', 5);

----------------------------------------

CREATE TABLE Trip (
    trip_id INT IDENTITY(1,1) PRIMARY KEY,
    source_id INT NOT NULL
        REFERENCES Source(source_id),
    source_trip_id BIGINT NOT NULL,

    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(500) NULL,
    departed_at DATETIMEOFFSET(7) NOT NULL,

    fit_sport TINYINT NOT NULL,
    fit_sub_sport TINYINT NOT NULL,
    is_stationary BIT NOT NULL,

    distance INT NOT NULL,
    duration INT NOT NULL,
    moving_time INT NOT NULL,

    elevation_gain SMALLINT NULL,
    elevation_loss SMALLINT NULL,
    avg_speed DECIMAL(5,2) NULL,
    max_speed DECIMAL(5,2) NULL,

    created_at DATETIMEOFFSET(7) NOT NULL,
    updated_at DATETIMEOFFSET(7) NOT NULL,
     
    CONSTRAINT uq_Trip_SourceTrip
        UNIQUE (source_id, source_trip_id)
);

----------------------------------------

CREATE TABLE TripMetadata (
    trip_id INT PRIMARY KEY
        REFERENCES Trip(trip_id) ON DELETE CASCADE,

    custom_name NVARCHAR(255) NULL,
    custom_description NVARCHAR(MAX) NULL,

    ride_type VARCHAR(10) NULL
        CHECK (ride_type IN ('Solo', 'Group')),

    organization_id INT NULL
        REFERENCES Organization(organization_id),

    ride_level_id INT NULL
        REFERENCES RideLevel(ride_level_id)
);

----------------------------------------

CREATE TABLE Tag (
    tag_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO Tag (name)
VALUES
    ('Warmup'),
    ('Commute'),
    ('Recovery'),
    ('Training'),
    ('Hilly'),
    ('Flat');

----------------------------------------

CREATE TABLE TripTag (
    trip_id INT NOT NULL
        REFERENCES Trip(trip_id) ON DELETE CASCADE,

    tag_id INT NOT NULL
        REFERENCES Tag(tag_id) ON DELETE CASCADE,

    PRIMARY KEY (trip_id, tag_id)
);

----------------------------------------