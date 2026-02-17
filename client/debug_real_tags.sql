-- List distinct tags from real uploads (excluding seed data if possible, though seed doesn't use tags table usually)
SELECT tag_name, COUNT(*) as frequency
FROM public.tags
GROUP BY tag_name
ORDER BY frequency DESC
LIMIT 50;
