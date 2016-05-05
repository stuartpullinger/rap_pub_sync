select 
  Site, 
  SUBSTRING_INDEX(
    SUBSTRING_INDEX(
      SUBSTRING_INDEX(SubmitHost, '://', -1) -- everything to the right of ‘://’
    , ':', 1) -- everything to the left of ‘:’
  , '/', 1) -- everything to the left of ‘/’
  as GocdbSubmitHost,
  max(LatestEndTime) as LatestPublication
from VSuperSummaries 
group by 1,2 
having
  GocdbSubmitHost not like 'EMI2%' -- Remove migrated data
  and GocdbSubmitHost not like 'None'; -- Remove blank (‘None’) entries

