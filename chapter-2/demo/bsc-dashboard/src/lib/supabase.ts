import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://ewgncgyekgmwbznrhiqy.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV3Z25jZ3lla2dtd2J6bnJoaXF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3MTk3NTgsImV4cCI6MjA3NTI5NTc1OH0.cxgF8o6senaSt6kRcbHIBDJe18BLwl50OvnuEHhnlF8'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
