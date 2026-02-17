-- List all distinct DNA values to debug search mismatches
SELECT root_category, sub_category, value, COUNT(*) 
FROM public.client_dna_attributes 
GROUP BY root_category, sub_category, value 
ORDER BY count DESC;
