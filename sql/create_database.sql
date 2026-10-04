IF DB_ID(N'RideQ') IS NULL
    BEGIN
        CREATE DATABASE [RideQ];
    END


GO
USE [RideQ];


GO
CREATE TABLE [Trips] (
    [trip_id]        SMALLINT       IDENTITY PRIMARY KEY,
    [rwgps_trip_id]  BIGINT         NOT NULL UNIQUE,
    [name]           NVARCHAR (100) NOT NULL,
    [ride_level]     VARCHAR (4)    NULL,
    [description]    NVARCHAR (500) NULL,
    [departed_at]    DATETIMEOFFSET NOT NULL,
    [fit_sport]      TINYINT        NOT NULL,
    [fit_sub_sport]  TINYINT        NOT NULL,
    [is_stationary]  BIT            NOT NULL,
    [distance]       INT            NOT NULL,
    [duration]       INT            NOT NULL,
    [moving_time]    INT            NOT NULL,
    [elevation_gain] SMALLINT       NULL,
    [elevation_loss] SMALLINT       NULL,
    [avg_speed]      DECIMAL (5, 2) NULL,
    [max_speed]      DECIMAL (5, 2) NULL,
    [created_at]     DATETIMEOFFSET NOT NULL,
    [updated_at]     DATETIMEOFFSET NOT NULL
);