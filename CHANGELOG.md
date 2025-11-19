# Changelog

All notable changes to this project will be documented in this file. 

For an alternative view, connecting these changes to Pull Requests, Issues, and new contributors, see the [GitHub Releases](https://github.com/skent259/crapssim/releases)

The format is moving towards [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) style for new entries, 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]

## [0.4.0] - 2025-11-18

This version hits the milestone to have all major craps bets implemented. 

### Added

* New bets: `Horn`, `World` (Whirl), `Big6`/`Big8`, `Buy`, `Lay`, and `Put` (with or without odds) from [@nova-rey] in [#73], [#81]
  * Corresponding single bet strategies
  * Corresponding odds strategies: `PutOddsAmount`, `PutOddsMultiplier`
  * Corresponding examples strategies: `QuickProps`, `BuySampler`, `LaySampler`, `PutWithOdds`
* Vig policy settings to TableSettings ([#73])
* `WinMultiplier` family of strategies which take a desired win multiple and calculates the correct amount based on the bet amount ([#74])
  * `WinMultiplier` is the general strategy which takes specific bet type argument
  * Convenience strategies for individual bets: `PassLineWinMultiplier`, `ComeWinMultiplier`, `DontPassWinMultiplier`, `DontComeWinMultiplier`, and `PutWinMultiplier` 
* `ThreePointMolly` and `ThreePointDolly` strategies with variable odds/win mutipliers ([#82])
* Stress tests, expanded examples, tools as part of the Vanilla Expansion Project ([#73])

### Changed

* The default printout for bets is now more compact and easy to read (the `__str__` method is defined; instead of only `__repr__`) ([#83])

### Fixed

*  `DontPass` and `DontCome` bets will now "push" on a come-out 12, bringing the bet down and returing the bet amount to the player. `_WinningLosingNumbersBet` gains `get_push_numbers()` method to accomodate ([#76])
*  The `Risk12` strategy will now take down place bets after hitting point (i.e. place bets not working), which is aligned to table conventions ([#78])
*  `OddsMultiplier` `__repr__` logic so that floats, ints, and incomplete dictionaries all work for odds/win multiplier ([#74])
 
## [0.3.2] - 2025-10-11

### What's Changed
* Restrict strategy updates during runout by [@skent259] in [#62]
* Update Risk12 strategy by [@skent259] in [#63]
* Reorder integration tests by [@skent259] in [#64]
* Verbose: print roll and shooter counts by [@JotaGreen] in [#65]
* Fix odds bet having result when the point is off by [@skent259] in [#66]
* Fix ATS bets, ATS strategy, and strategies with persistent bet features by [@skent259] in [#71]


## [0.3.1] - 2025-02-13

### What's Changed
* **BREAKING**: Rename strategy tools and implement new strategy modes by [@skent259] in [#55]
  * Renamed many strategy tools. In addition, breaking change in functionality of BetPlace, and any strategy that uses BetPlace (including PlaceInside, IronCross, Hammerlock, Risk12, Place68DontCome2Odds). To keep old behavior, you need to update to BetPlace(..., strategy_mode=StrategyMode.ADD_IF_POINT_ON) for the corresponding strategy. This will have place bets working during come-out rolls.
  * Fixes PlaceInside strategy is slightly off from table conventions #52
* Add hop bets by [@skent259] in [#56]
* Improve printout for verbose table run in [`8508894`](https://github.com/skent259/crapssim/commit/850889453435aa4b2fe09c1abb4b6c0ec6b291ff), [#49]
* Fix Simple Bets and BetIfTrue not working on Bets with persistent features (on multi sims) [#48]
* Fix Table does not run properly on second call [#53]
* Add BetAll, BetTall, BetSmall strategies by [@skent259] in [#57]
* Improve documentation by [@skent259] in [#50]


## [0.3.0] - 2024-12-01

This is a major update with breaking changes throughout the package. The changes ensure we can implement new bets and make the strategies much easier for new and old users alike, building for the future of the package. 

### What's Changed
* Changes for Type Hinting by [@amortization] in [#3]
* Added a Fire bet  by [@amortization] in [#12]
* Create .gitattributes by [@skent259] in [#15]
* Make gitattriuutes by [@skent259] in [#17]
* Improve Table Payouts per issue #13 by [@amortization] in [#18]
* Removed the Python directory as it currently isn't documented or used… by [@amortization] in [#9]
* Changed how Odds bets work and how Bets are queried by Player by [@amortization] in [#20]
* Strategy rewrite by [@amortization] in [#29]
* Bet changes Supersedes #19 by [@amortization] in [#30]
* Add crapssim development install instructions by [@skent259] in [#22]
* Clean up Bet module by [@skent259] in [#36]
* Add All, Tall, and Small bets by [@skent259] in [#37]
* Add more bet changes by [@skent259] in [#41]
* Update dice and table for better randomization. by [@skent259] in [#42]
* Clean up strategy module by [@skent259] in [#44]
* Incorporate dev updates for version 0.3.0 by [@skent259] in [#45]


## [0.2.0] - 2021-03-07

 - v0.2.0 improves on the UI of v0.1.0 by clarifying internal vs external functions, improving documentation, and other minor changes.

## [0.1.1] - 2021-03-07

 - Small changes in addition to v0.1.1

## 0.1.0 - 2019-03-09

Initial version 


[unreleased]: https://github.com/skent259/crapssim/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/skent259/crapssim/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/skent259/crapssim/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/skent259/crapssim/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/skent259/crapssim/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/skent259/crapssim/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/skent259/crapssim/releases/tag/v0.1.1

[@skent259]: https://github.com/skent259
[@amortization]: https://github.com/amortization
[@JotaGreen]: https://github.com/JotaGreen
[@nova-rey]: https://github.com/nova-rey

[#3]: https://github.com/skent259/crapssim/pull/3
[#9]: https://github.com/skent259/crapssim/pull/9
[#12]: https://github.com/skent259/crapssim/pull/12
[#15]: https://github.com/skent259/crapssim/pull/15
[#17]: https://github.com/skent259/crapssim/pull/17
[#18]: https://github.com/skent259/crapssim/pull/18
[#20]: https://github.com/skent259/crapssim/pull/20
[#22]: https://github.com/skent259/crapssim/pull/22
[#29]: https://github.com/skent259/crapssim/pull/29
[#30]: https://github.com/skent259/crapssim/pull/30
[#36]: https://github.com/skent259/crapssim/pull/36
[#37]: https://github.com/skent259/crapssim/pull/37
[#41]: https://github.com/skent259/crapssim/pull/41
[#42]: https://github.com/skent259/crapssim/pull/42
[#44]: https://github.com/skent259/crapssim/pull/44
[#45]: https://github.com/skent259/crapssim/pull/45
[#49]: https://github.com/skent259/crapssim/pull/49
[#50]: https://github.com/skent259/crapssim/pull/50
[#55]: https://github.com/skent259/crapssim/pull/55
[#56]: https://github.com/skent259/crapssim/pull/56
[#57]: https://github.com/skent259/crapssim/pull/57
[#62]: https://github.com/skent259/crapssim/pull/62
[#63]: https://github.com/skent259/crapssim/pull/63
[#64]: https://github.com/skent259/crapssim/pull/64
[#65]: https://github.com/skent259/crapssim/pull/65
[#66]: https://github.com/skent259/crapssim/pull/66
[#71]: https://github.com/skent259/crapssim/pull/71
[#73]: https://github.com/skent259/crapssim/pull/71
[#74]: https://github.com/skent259/crapssim/pull/71
[#75]: https://github.com/skent259/crapssim/pull/71
[#76]: https://github.com/skent259/crapssim/pull/71
[#78]: https://github.com/skent259/crapssim/pull/71
[#81]: https://github.com/skent259/crapssim/pull/71
[#82]: https://github.com/skent259/crapssim/pull/71
[#83]: https://github.com/skent259/crapssim/pull/71

[#48]: https://github.com/skent259/crapssim/issues/48
[#53]: https://github.com/skent259/crapssim/issues/53
