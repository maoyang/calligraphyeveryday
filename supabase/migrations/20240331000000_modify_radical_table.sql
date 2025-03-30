-- 移除 created_at 欄位
alter table public.radical drop column if exists created_at;

-- 新增 stroke_count 欄位
alter table public.radical add column if not exists stroke_count integer not null default 0; 