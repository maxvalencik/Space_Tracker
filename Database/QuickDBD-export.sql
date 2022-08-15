-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/5anlus
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Users" (
    "id" int   NOT NULL,
    "first_name" string   NOT NULL,
    "last_name" string   NOT NULL,
    "roleID" int   NOT NULL,
    "email" email   NOT NULL,
    "country" string   NULL,
    "description" text   NULL,
    CONSTRAINT "pk_Users" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Roles" (
    "id" int   NOT NULL,
    "type" string   NOT NULL,
    "definition" text   NOT NULL,
    CONSTRAINT "pk_Roles" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Satellites" (
    "id" int   NOT NULL,
    "sat_name" string   NOT NULL,
    "inclination" float   NOT NULL,
    "apogee" float   NOT NULL,
    "perigee" float   NOT NULL,
    "launch_date" date   NULL,
    "launch_site" string   NOT NULL,
    "country" string   NULL,
    CONSTRAINT "pk_Satellites" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Spaceports" (
    "id" int   NOT NULL,
    "site_name" string   NOT NULL,
    "latitude" float   NOT NULL,
    "longitude" float   NOT NULL,
    "max_inclination" float   NOT NULL,
    "min_inclination" float   NOT NULL,
    "operator" string   NULL,
    "country" string   NULL,
    CONSTRAINT "pk_Spaceports" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "User_Satellite" (
    "id" int   NOT NULL,
    "satID" int   NULL,
    "userID" int   NOT NULL,
    CONSTRAINT "pk_User_Satellite" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "User_Spaceport" (
    "id" int   NOT NULL,
    "spaceportID" int   NOT NULL,
    "userID" int   NOT NULL,
    CONSTRAINT "pk_User_Spaceport" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "Users" ADD CONSTRAINT "fk_Users_roleID" FOREIGN KEY("roleID")
REFERENCES "Roles" ("id");

ALTER TABLE "Satellites" ADD CONSTRAINT "fk_Satellites_launch_site" FOREIGN KEY("launch_site")
REFERENCES "Spaceports" ("id");

ALTER TABLE "User_Satellite" ADD CONSTRAINT "fk_User_Satellite_satID" FOREIGN KEY("satID")
REFERENCES "Satellites" ("id");

ALTER TABLE "User_Satellite" ADD CONSTRAINT "fk_User_Satellite_userID" FOREIGN KEY("userID")
REFERENCES "Users" ("id");

ALTER TABLE "User_Spaceport" ADD CONSTRAINT "fk_User_Spaceport_spaceportID" FOREIGN KEY("spaceportID")
REFERENCES "Spaceports" ("id");

ALTER TABLE "User_Spaceport" ADD CONSTRAINT "fk_User_Spaceport_userID" FOREIGN KEY("userID")
REFERENCES "Users" ("id");

