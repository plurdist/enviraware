WITH FieldStats AS (
    SELECT
        CAST(PM1 AS REAL) AS PM1,
        CAST("0.3 to 1.0" AS REAL) AS "0.3_to_1.0",
        CAST("1.0 to 2.5" AS REAL) AS "1.0_to_2.5",
        CAST("2.5 to 4.0" AS REAL) AS "2.5_to_4.0",
        CAST("4.0 to 10.0" AS REAL) AS "4.0_to_10.0",
        CAST(H AS REAL) AS H,
        CAST(T AS REAL) AS T,
        CAST(VOC AS REAL) AS VOC,
        CAST(Nox AS REAL) AS Nox
    FROM air_quality
)

SELECT
    COUNT(*) AS TotalRecords,
    
    AVG(PM1) AS Mean_PM1,
    MIN(PM1) AS Min_PM1,
    MAX(PM1) AS Max_PM1,
    ROUND(AVG(PM1 * PM1) - AVG(PM1) * AVG(PM1), 2) AS Variance_PM1,
    
    AVG("0.3_to_1.0") AS Mean_0_3_to_1_0,
    MIN("0.3_to_1.0") AS Min_0_3_to_1_0,
    MAX("0.3_to_1.0") AS Max_0_3_to_1_0,
    ROUND(AVG("0.3_to_1.0" * "0.3_to_1.0") - AVG("0.3_to_1.0") * AVG("0.3_to_1.0"), 2) AS Variance_0_3_to_1_0,

    AVG("1.0_to_2.5") AS Mean_1_0_to_2_5,
    MIN("1.0_to_2.5") AS Min_1_0_to_2_5,
    MAX("1.0_to_2.5") AS Max_1_0_to_2_5,
    ROUND(AVG("1.0_to_2.5" * "1.0_to_2.5") - AVG("1.0_to_2.5") * AVG("1.0_to_2.5"), 2) AS Variance_1_0_to_2_5,

    AVG("2.5_to_4.0") AS Mean_2_5_to_4_0,
    MIN("2.5_to_4.0") AS Min_2_5_to_4_0,
    MAX("2.5_to_4.0") AS Max_2_5_to_4_0,
    ROUND(AVG("2.5_to_4.0" * "2.5_to_4.0") - AVG("2.5_to_4.0") * AVG("2.5_to_4.0"), 2) AS Variance_2_5_to_4_0,

    AVG("4.0_to_10.0") AS Mean_4_0_to_10_0,
    MIN("4.0_to_10.0") AS Min_4_0_to_10_0,
    MAX("4.0_to_10.0") AS Max_4_0_to_10_0,
    ROUND(AVG("4.0_to_10.0" * "4.0_to_10.0") - AVG("4.0_to_10.0") * AVG("4.0_to_10.0"), 2) AS Variance_4_0_to_10_0,

    AVG(H) AS Mean_H,
    MIN(H) AS Min_H,
    MAX(H) AS Max_H,
    ROUND(AVG(H * H) - AVG(H) * AVG(H), 2) AS Variance_H,

    AVG(T) AS Mean_T,
    MIN(T) AS Min_T,
    MAX(T) AS Max_T,
    ROUND(AVG(T * T) - AVG(T) * AVG(T), 2) AS Variance_T,

    AVG(VOC) AS Mean_VOC,
    MIN(VOC) AS Min_VOC,
    MAX(VOC) AS Max_VOC,
    ROUND(AVG(VOC * VOC) - AVG(VOC) * AVG(VOC), 2) AS Variance_VOC,

    AVG(Nox) AS Mean_Nox,
    MIN(Nox) AS Min_Nox,
    MAX(Nox) AS Max_Nox,
    ROUND(AVG(Nox * Nox) - AVG(Nox) * AVG(Nox), 2) AS Variance_Nox

FROM FieldStats;
