select 
  ss.Site as Site,
  ss.SH as GocdbSubmitHost,
  ss.Year as Year,
  ss.Month as Month,
  ss.NJ as GocJobCount,
  sr.NJ as LocalJobCount,
  sr.NJ - ss.NJ as Difference
from (
  select
    Site,
    SUBSTRING_INDEX( SUBSTRING_INDEX( SUBSTRING_INDEX(SubmitHost, '://', -1)  , ':', 1)  , '/', 1)  as SH,
    Year,
    Month,
    sum(NumberOfJobs) as NJ
  from VSuperSummaries
  group by 1,2,3,4
  having
    SH not like 'EMI2%'
    and SH not like 'None')
as ss
join (
  select
     Site,
     SUBSTRING_INDEX( SUBSTRING_INDEX( SUBSTRING_INDEX(SubmitHost, '://', -1)  , ':', 1)  , '/', 1)  as SH,
     Year,
     Month,
     sum(NumberOfJobs) as NJ
  from VSyncRecords
  group by 1,2,3,4
  having
    SH not like 'EMI2%'
    and SH not like 'None')
as sr
using (Site, SH, Year, Month);
