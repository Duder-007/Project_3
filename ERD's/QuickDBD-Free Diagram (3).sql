-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/TSXoX1
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "baby_names_1910s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" [INT]   NOT NULL,
    CONSTRAINT "pk_baby_names_1910s" PRIMARY KEY (
        "ID"
     )
);

CREATE TABLE "baby_names_1920s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_1930s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_1940s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_1950s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_1960s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_1970s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_1980s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_1990s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_2000s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

CREATE TABLE "baby_names_2010s" (
    "Rank" INT   NOT NULL,
    "Male_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Males" INT   NOT NULL,
    "Female_Name" VARCHAR(75)   NOT NULL,
    "Number_of_Females" INT   NOT NULL,
    "ID" INT   NOT NULL
);

ALTER TABLE "baby_names_1920s" ADD CONSTRAINT "fk_baby_names_1920s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1910s" ("");

ALTER TABLE "baby_names_1930s" ADD CONSTRAINT "fk_baby_names_1930s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1920s" ("");

ALTER TABLE "baby_names_1940s" ADD CONSTRAINT "fk_baby_names_1940s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1930s" ("");

ALTER TABLE "baby_names_1950s" ADD CONSTRAINT "fk_baby_names_1950s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1940s" ("");

ALTER TABLE "baby_names_1960s" ADD CONSTRAINT "fk_baby_names_1960s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1950s" ("");

ALTER TABLE "baby_names_1970s" ADD CONSTRAINT "fk_baby_names_1970s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1960s" ("");

ALTER TABLE "baby_names_1980s" ADD CONSTRAINT "fk_baby_names_1980s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1970s" ("");

ALTER TABLE "baby_names_1990s" ADD CONSTRAINT "fk_baby_names_1990s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1980s" ("");

ALTER TABLE "baby_names_2000s" ADD CONSTRAINT "fk_baby_names_2000s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_1990s" ("");

ALTER TABLE "baby_names_2010s" ADD CONSTRAINT "fk_baby_names_2010s_ID" FOREIGN KEY("ID")
REFERENCES "baby_names_2000s" ("");

