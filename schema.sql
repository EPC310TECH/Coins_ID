-- ============================================================
-- Coin Inventory Schema (Supabase / Postgres)
-- One row per physical coin. The coin_id follows the coin from
-- flip -> photos -> listing -> sale -> shipment.
-- ============================================================

create table if not exists coins (
    id              bigint generated always as identity primary key,
    coin_id         text not null unique,          -- e.g. 'C0001' (written on the flip)

    -- Identification (from your ID program or manual entry)
    denomination    text,                           -- 'Cent', 'Nickel', 'Dime', 'Quarter', 'Half', 'Dollar'
    series          text,                           -- 'Lincoln Wheat', 'Morgan', 'Mercury', etc.
    year            int,
    mint_mark       text,                           -- '', 'D', 'S', 'CC', 'O', 'W'
    variety         text,                           -- 'DDO', '1955 doubled die', 'small date', etc.
    composition     text,                           -- '90% silver', 'copper', 'clad'

    -- Condition / verification
    grade_est       text,                           -- your estimate: 'G-4', 'VF-20', 'AU-58', 'MS-63'
    graded          boolean default false,          -- sent to PCGS/NGC?
    cert_number     text,                           -- slab cert # if graded
    weight_g        numeric(6,3),                   -- from your 0.01g scale
    diameter_mm     numeric(5,2),
    problems        text,                           -- 'cleaned', 'holed', 'corrosion', null if none

    -- Physical location
    box             text,                           -- 'Box A', 'Red Box 2'
    slot            text,                           -- position/divider within box

    -- Photos
    photo_slate     text,                           -- filename: C0001-slate.jpg
    photo_obv       text,                           -- C0001-obv.jpg
    photo_rev       text,                           -- C0001-rev.jpg
    photos_done     boolean generated always as
                      (photo_obv is not null and photo_rev is not null) stored,

    -- Valuation & listing
    est_value_low   numeric(10,2),
    est_value_high  numeric(10,2),
    lot_group       text,                           -- non-null = part of a bulk lot, e.g. 'LOT-wheat-01'
    ebay_item_id    text,                           -- filled when listed
    list_format     text check (list_format in ('auction','fixed','lot') or list_format is null),
    list_price      numeric(10,2),

    -- Lifecycle status
    status          text not null default 'intake'
                    check (status in ('intake','identified','flipped','photographed',
                                      'listed','sold','shipped','graded_out','keep')),
    sold_price      numeric(10,2),
    sold_at         timestamptz,
    buyer_username  text,
    tracking_number text,

    notes           text,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

-- Auto-bump updated_at
create or replace function touch_updated_at() returns trigger as $$
begin new.updated_at = now(); return new; end;
$$ language plpgsql;

drop trigger if exists coins_touch on coins;
create trigger coins_touch before update on coins
    for each row execute function touch_updated_at();

-- Useful indexes
create index if not exists idx_coins_status on coins(status);
create index if not exists idx_coins_series_year on coins(series, year, mint_mark);
create index if not exists idx_coins_lot on coins(lot_group) where lot_group is not null;

-- ============================================================
-- Views for daily workflow
-- ============================================================

-- What still needs photos
create or replace view v_needs_photos as
select coin_id, series, year, mint_mark, box, slot
from coins
where status in ('identified','flipped') and photo_obv is null
order by coin_id;

-- Ready to list (photographed but no eBay item yet)
create or replace view v_ready_to_list as
select coin_id, series, year, mint_mark, grade_est,
       est_value_low, est_value_high, photo_obv, photo_rev
from coins
where photos_done and ebay_item_id is null
  and status not in ('sold','shipped','keep','graded_out')
order by est_value_high desc nulls last;

-- Candidates for professional grading (high value, still raw)
create or replace view v_grading_candidates as
select coin_id, series, year, mint_mark, grade_est, est_value_high
from coins
where graded = false and est_value_high >= 100
order by est_value_high desc;

-- Sales summary
create or replace view v_sales as
select date_trunc('week', sold_at) as week,
       count(*) as coins_sold,
       sum(sold_price) as gross
from coins where status in ('sold','shipped')
group by 1 order by 1 desc;
