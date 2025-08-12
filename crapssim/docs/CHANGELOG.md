# Changelog

## v0.3.1

### What's Changed
* **BREAKING**: Rename strategy tools and implement new strategy modes by @skent259 in https://github.com/skent259/crapssim/pull/55
  * Renamed many strategy tools. In addition, breaking change in functionality of BetPlace, and any strategy that uses BetPlace (including PlaceInside, IronCross, Hammerlock, Risk12, Place68DontCome2Odds). To keep old behavior, you need to update to BetPlace(..., strategy_mode=StrategyMode.ADD_IF_POINT_ON) for the corresponding strategy. This will have place bets working during come-out rolls.
  * Fixes PlaceInside strategy is slightly off from table conventions #52
* Add hop bets by @skent259 in https://github.com/skent259/crapssim/pull/56
* Improve printout for verbose table run in 850889453435aa4b2fe09c1abb4b6c0ec6b291ff, #49 
* Fix Simple Bets and BetIfTrue not working on Bets with persistent features (on multi sims) https://github.com/skent259/crapssim/issues/48
* Fix Table does not run properly on second call https://github.com/skent259/crapssim/issues/53
* Add BetAll, BetTall, BetSmall strategies by @skent259 in https://github.com/skent259/crapssim/pull/57
* Improve documentation by @skent259 in https://github.com/skent259/crapssim/pull/50


**Full Changelog**: https://github.com/skent259/crapssim/compare/v0.3.0...v0.3.1

## v0.3.0 (2024/12/01)

This is a major update with breaking changes throughout the package. The changes ensure we can implement new bets and make the strategies much easier for new and old users alike, building for the future of the package. 

### What's Changed
* Changes for Type Hinting by @amortization in https://github.com/skent259/crapssim/pull/3
* Added a Fire bet  by @amortization in https://github.com/skent259/crapssim/pull/12
* Create .gitattributes by @skent259 in https://github.com/skent259/crapssim/pull/15
* Make gitattriuutes by @skent259 in https://github.com/skent259/crapssim/pull/17
* Improve Table Payouts per issue #13 by @amortization in https://github.com/skent259/crapssim/pull/18
* Removed the Python directory as it currently isn't documented or used… by @amortization in https://github.com/skent259/crapssim/pull/9
* Changed how Odds bets work and how Bets are queried by Player by @amortization in https://github.com/skent259/crapssim/pull/20
* Strategy rewrite by @amortization in https://github.com/skent259/crapssim/pull/29
* Bet changes Supersedes #19 by @amortization in https://github.com/skent259/crapssim/pull/30
* Add crapssim development install instructions by @skent259 in https://github.com/skent259/crapssim/pull/22
* Clean up Bet module by @skent259 in https://github.com/skent259/crapssim/pull/36
* Add All, Tall, and Small bets by @skent259 in https://github.com/skent259/crapssim/pull/37
* Add more bet changes by @skent259 in https://github.com/skent259/crapssim/pull/41
* Update dice and table for better randomization. by @skent259 in https://github.com/skent259/crapssim/pull/42
* Clean up strategy module by @skent259 in https://github.com/skent259/crapssim/pull/44
* Incorporate dev updates for version 0.3.0 by @skent259 in https://github.com/skent259/crapssim/pull/45

### New Contributors

* @amortization made their first contribution in https://github.com/skent259/crapssim/pull/3

**Full Changelog**: https://github.com/skent259/crapssim/compare/v0.2.0...v0.3.0

## v0.2.0 (2021/03/07)

v0.2.0 improves on the UI of v0.1.0 by clarifying internal vs external functions, improving documentation, and other minor changes.

## v0.1.1 (2021/03/07)

Small changes in addition to v0.1.1

## v0.1.0

Initial version 