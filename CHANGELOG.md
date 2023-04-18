# Changelog

All notable changes to the extension will be documented in this file.

## [Unreleased]

## [v1.0.0] - 2023-04-08
- Initial release!

## [v1.0.1] - 2023-04-08
- Fixed entity conditions not having a comma after its type.

## [v1.0.2] - 2023-04-08
- Renamed dupe snippets for action/condition so that it now specifies if it is an action or a condition.
- Renamed tooltip snippets based on badge and power types.

## [v1.0.3] - 2023-04-09
- Moved two snippet's properties position to the bottom of the snippet to make "reading" easier.

## [v1.0.4] - 2023-04-09
- Updated README.md.

## [v1.0.5] - 2023-04-15
- Fixed "entity:change_resource" having it's comma in the wrong spot. (Ty ying)
- Renamed dupe snippets for meta:and so that it now specifies if it is an action or a condition. (Ty ying)

## [v1.0.6] - 2023-04-16
- Fixed an issue where an extra comma was appended in single-line snippets.

## [v1.0.7] - 2023-04-18
- Disambiguated certain data and power types with their action or condition counterparts like ingredient and resource.
- Simplified some snippets with keys that do the same thing to only have the array version.

- Fixed an issue where comparison used object instead of string.
- Fixed a comma in power:action_over_time and entity:modify_inventory.
- Fixed entity:drop_inventory.
- Changed meta:delay key positions for brevity.