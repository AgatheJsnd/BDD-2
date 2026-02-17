-- CLEANUP SCRIPT
-- Deletes the 3 specific seed clients.
-- This does NOT touch your uploaded/ingested data.

DELETE FROM public.clients 
WHERE id IN (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', -- Sophie
    'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', -- Marc
    'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33'  -- Hélène
);
