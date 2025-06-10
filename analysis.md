# Analysis

## Minimum Required Headers
Testing reveals these headers are required for all endpoints:
- `content-type: application/json` (required)
- `origin: https://rip.ie` (required for CORS)
- `referer: https://rip.ie/*` (required)
- `user-agent` (required)

Optional headers:
- `accept*` headers
- `sec-*` security headers
- `priority`
- `authorization` (appears unused)

## Parameter Analysis

### getCountiesForFilters
- Minimum: `{"input": {}}` returns all counties.
- `page` and `records` control pagination.
- `search` filters counties by name.
- **Response Details:** Returns a JSON object with `total` (number of records) and `records` (an array of objects, each with `id` and `name` for the county).
  Example: `{"data":{"getCountiesForFilters":{"total":32,"records":[{"id":1,"name":"Antrim"},...]}}}`

### getTownsForFilters
- Requires `countyId` parameter.
- Returns error without `countyId`: `{"errors":[{"message":"Variable \"$countyId\" of required type \"Float!\" was not provided."}]}`
- `input` object with `page`, `records`, and `search` controls pagination and filtering by town name.
- **Response Details:** Returns a JSON object with `total` (number of records) and `records` (an array of objects, each with `id` and `name` for the town).
  Example: `{"data":{"getTownsForFilters":{"total":33,"records":[{"id":2436,"name":"Aghalee"},...]}}}`

### searchDeathNoticesForListTableWithoutPhoto
- Requires date range filters (`a.createdAt` with `gte` and `lte` operators).
- Without filters: returns empty array.
- `page` and `records` control pagination.
- `orders` changes sorting (e.g., by `a.createdAtCastToDate` and `a.escapedSurname`).
- `isTiledView` is a boolean flag.
- **Response Details:** Returns a JSON object with `count`, `perPage`, `page`, `nextPage`, and `records` (an array of death notice objects). Each death notice includes `id`, `firstname`, `surname`, `nee`, `createdAt`, `funeralArrangementsLater`, `arrangementsChange`, and nested `county` and `town` objects (each with `id` and `name`).
  Example: `{"data":{"searchDeathNoticesForList":{"count":...,"records":[{"id":...,"firstname":...,"surname":...,"county":{"id":...,"name":...},"town":{"id":...,"name":...}},...]}}}`

### getDeathNoticeFDInfo
- Requires `deathNoticeId` parameter.
- **Response Details:** Returns details about locations and the funeral home associated with a death notice. The `funeralHome` object contains extensive details including `id`, `name`, `addressFirstPart`, `addressSecondPart`, `addressThirdPart`, `city`, `mapUrl`, `websiteUrl`, `email`, `phone`, `mobilePhone`, `county` (`id`, `name`), `funeralHomeAds` (various banner attachments and URLs), and `funeralDirector` (advertisePlaces, isIafd, strapline).
  Example: `{"data":{"previewDeathNotice":{"locations":[],"funeralHome":{"id":944,"name":"O'Halloran Funeral Directors",...}}}}}`

## Endpoint Discovery
Additional endpoints found by modifying operation names:

1. `getCounties`
   - **Description:** Returns a list of all counties. This is the correct operation name for retrieving all counties without filters, as suggested by the API error.
   - **Parameters:** None.
   - **Response Details:** Returns a JSON object with `id` and `name` for each county.
     Example: `{"data":{"getCounties":[{"id":1,"name":"Antrim"},{"id":2,"name":"Armagh"},{"id":3,"name":"Carlow"},{"id":4,"name":"Cavan"},{"id":5,"name":"Clare"},{"id":6,"name":"Cork"},{"id":7,"name":"Derry"},{"id":8,"name":"Donegal"},{"id":9,"name":"Down"},{"id":10,"name":"Dublin"},{"id":11,"name":"Fermanagh"},{"id":12,"name":"Galway"},{"id":13,"name":"Kerry"},{"id":14,"name":"Kildare"},{"id":15,"name":"Kilkenny"},{"id":16,"name":"Laois"},{"id":17,"name":"Leitrim"},{"id":18,"name":"Limerick"},{"id":19,"name":"Longford"},{"id":20,"name":"Louth"},{"id":21,"name":"Mayo"},{"id":22,"name":"Meath"},{"id":23,"name":"Monaghan"},{"id":24,"name":"Offaly"},{"id":25,"name":"Roscommon"},{"id":26,"name":"Sligo"},{"id":27,"name":"Tipperary"},{"id":28,"name":"Tyrone"},{"id":29,"name":"Waterford"},{"id":30,"name":"Westmeath"},{"id":31,"name":"Wexford"},{"id":32,"name":"Wicklow"}]}}`


3. `getDeathNoticeFull`
   - **Description:** Provides comprehensive details for a specific death notice. This is a more detailed version than `getDeathNoticeFDInfo`.
   - **Parameters:** Requires `deathNoticeId` (Float!).
   - **Response Details:** Returns a JSON object containing `id`, `firstname`, `surname`, `nee`, `createdAt`, `funeralArrangementsLater`, `arrangementsChange`, nested `county` and `town` objects, `locations` (array of objects with `id`, `type`, `name`, `latitude`, `longitude`, and nested `town`), and `funeralHome` details (similar to `getDeathNoticeFDInfo` but without the `funeralHomeAds` and `funeralDirector` sub-objects).
     Example: `{"data":{"previewDeathNotice":{"id":596530,"firstname":"Eric","surname":"Holmes","nee":"","createdAt":"2025-06-10T08:08:57.349+01:00","funeralArrangementsLater":false,"arrangementsChange":"NONE","county":{"id":12,"name":"Galway"},"town":{"id":1250,"name":"Eyrecourt"},"locations":[],"funeralHome":{"id":944,"name":"O'Halloran Funeral Directors","addressFirstPart":"Main Street","addressSecondPart":"Corofin","addressThirdPart":"","city":"","mapUrl":"","websiteUrl":"","email":"matohalloran71@gmail.com","phone":"087-6807348","mobilePhone":"087-6807348 or 065-6837628","county":{"id":5,"name":"Clare"}}}}}`

## Key Observations
1. API requires specific referer and origin headers
2. Date ranges are required for death notice searches
3. County ID is required for town/funeral home queries
4. Pagination parameters work consistently across endpoints
