-- Keep the LG Display identity; move its location to Binh Duong University.
BEGIN;

UPDATE companies
SET latitude = 10.9902032,
    longitude = 106.6642095
WHERE code = 'lg_display_hp';

-- Refresh profiles using the old default location, preserving custom coordinates.
UPDATE intern_profiles
SET company_lat = 10.9902032,
    company_lng = 106.6642095,
    updated_at = NOW()
WHERE (
    company_id IN (SELECT id FROM companies WHERE code = 'lg_display_hp')
    OR (company_id IS NULL AND company_name IN ('LG Display', 'LG Display Hải Phòng'))
)
AND (
    (ABS(company_lat - 20.8865) < 0.000001
     AND ABS(company_lng - 106.5821) < 0.000001)
    OR (company_lat IS NULL AND company_lng IS NULL)
);

COMMIT;
