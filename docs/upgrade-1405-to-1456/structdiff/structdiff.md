# 源码结构 diff:1.4.0.5 (Terarria1405) → 1.4.5.6 (Terarria1456)

- 共同文件:935;1456 新增文件:564;1405 独有(移除/更名/人工添加):47
- 有成员增删的共同文件:386

## 一、1456 新增文件(新系统)

- BCrypt/Net/BCrypt.cs
- Properties/AssemblyInfo.cs
- Terraria/Achievements/AchievementTracker.cs
- Terraria/AdvancedPopupRequest.cs
- Terraria/Audio/ASoundEffectBasedAudioTrack.cs
- Terraria/Audio/AudioTrackPlayCallback.cs
- Terraria/Audio/CueAudioTrack.cs
- Terraria/Audio/DisabledAudioSystem.cs
- Terraria/Audio/IAudioSystem.cs
- Terraria/Audio/IAudioTrack.cs
- Terraria/Audio/LegacyAudioSystem.cs
- Terraria/Audio/MP3AudioTrack.cs
- Terraria/Audio/MusicCueHolder.cs
- Terraria/Audio/OGGAudioTrack.cs
- Terraria/Audio/ProjectileAudioTracker.cs
- Terraria/Audio/SoundPlayOverrides.cs
- Terraria/Audio/VampireSizzleTracker.cs
- Terraria/Audio/WAVAudioTrack.cs
- Terraria/Chat/ChatColors.cs
- Terraria/Chat/Commands/AllDeathCommand.cs
- Terraria/Chat/Commands/AllPVPDeathCommand.cs
- Terraria/Chat/Commands/BossDamageCommand.cs
- Terraria/Chat/Commands/DeathCommand.cs
- Terraria/Chat/Commands/ICommandAliasProvider.cs
- Terraria/Chat/Commands/PVPDeathCommand.cs
- Terraria/Cinematics/DSTFilm.cs
- Terraria/Control.cs
- Terraria/DataStructures/AEntitySource_OnHit.cs
- Terraria/DataStructures/AEntitySource_Tile.cs
- Terraria/DataStructures/ActiveSections.cs
- Terraria/DataStructures/ArmorSetBonus.cs
- Terraria/DataStructures/ArmorSetBonuses.cs
- Terraria/DataStructures/BackgroundVariant.cs
- Terraria/DataStructures/BackgroundVariantSet.cs
- Terraria/DataStructures/CachedProjectileCounterBuffTextHandler.cs
- Terraria/DataStructures/DoubleStack.cs
- Terraria/DataStructures/DrawAnimationScryingOrb.cs
- Terraria/DataStructures/DroneCameraTracker.cs
- Terraria/DataStructures/EntitySource_BossSpawn.cs
- Terraria/DataStructures/EntitySource_Buff.cs
- Terraria/DataStructures/EntitySource_ByItemSourceId.cs
- Terraria/DataStructures/EntitySource_ByProjectileSourceId.cs
- Terraria/DataStructures/EntitySource_CoinRain.cs
- Terraria/DataStructures/EntitySource_DebugCommand.cs
- Terraria/DataStructures/EntitySource_DropAsItem.cs
- Terraria/DataStructures/EntitySource_Film.cs
- Terraria/DataStructures/EntitySource_FishedOut.cs
- Terraria/DataStructures/EntitySource_Gift.cs
- Terraria/DataStructures/EntitySource_ItemOpen.cs
- Terraria/DataStructures/EntitySource_ItemUse.cs
- Terraria/DataStructures/EntitySource_ItemUse_WithAmmo.cs
- Terraria/DataStructures/EntitySource_Loot.cs
- Terraria/DataStructures/EntitySource_Mount.cs
- Terraria/DataStructures/EntitySource_OldOnesArmy.cs
- Terraria/DataStructures/EntitySource_OnHit_ByItemSourceID.cs
- Terraria/DataStructures/EntitySource_OnHit_ByProjectileSourceID.cs
- Terraria/DataStructures/EntitySource_OverfullChest.cs
- Terraria/DataStructures/EntitySource_Parent.cs
- Terraria/DataStructures/EntitySource_RevengeSystem.cs
- Terraria/DataStructures/EntitySource_ShakeTree.cs
- Terraria/DataStructures/EntitySource_SpawnNPC.cs
- Terraria/DataStructures/EntitySource_Sync.cs
- Terraria/DataStructures/EntitySource_TileBreak.cs
- Terraria/DataStructures/EntitySource_TileEntity.cs
- Terraria/DataStructures/EntitySource_TileInteraction.cs
- Terraria/DataStructures/EntitySource_Wiring.cs
- Terraria/DataStructures/EntitySource_WorldEvent.cs
- Terraria/DataStructures/EntitySource_WorldGen.cs
- Terraria/DataStructures/EntryFilterer.cs
- Terraria/DataStructures/EntrySorter.cs
- Terraria/DataStructures/GameDifficultyData.cs
- Terraria/DataStructures/GameDifficultyLevel.cs
- Terraria/DataStructures/GeneralIssueReporter.cs
- Terraria/DataStructures/GetStyleMethod.cs
- Terraria/DataStructures/GuessedPlayerIntention.cs
- Terraria/DataStructures/IBuffTextHandler.cs
- Terraria/DataStructures/IConfigKeyHolder.cs
- Terraria/DataStructures/IEntitySource.cs
- Terraria/DataStructures/IEntryFilter.cs
- Terraria/DataStructures/IEntrySortStep.cs
- Terraria/DataStructures/IFixLoadedData.cs
- Terraria/DataStructures/IProvideReports.cs
- Terraria/DataStructures/IRoomCheckFeedback.cs
- Terraria/DataStructures/IRoomCheckFeedback_Scoring.cs
- Terraria/DataStructures/IRoomCheckFeedback_Spread.cs
- Terraria/DataStructures/ISearchFilter.cs
- Terraria/DataStructures/IssueReport.cs
- Terraria/DataStructures/ItemCreationContext.cs
- Terraria/DataStructures/JourneyDuplicationItemCreationContext.cs
- Terraria/DataStructures/KiteFlyingInfo.cs
- Terraria/DataStructures/MinionRespawner.cs
- Terraria/DataStructures/MinionSpawnFromInventoryItem.cs
- Terraria/DataStructures/MinionSpawnInfo.cs
- Terraria/DataStructures/MultiPointHitbox.cs
- Terraria/DataStructures/NPCDebuffImmunityData.cs
- Terraria/DataStructures/NPCFollowState.cs
- Terraria/DataStructures/NPCKillAttempt.cs
- Terraria/DataStructures/NoRoomCheckFeedback.cs
- Terraria/DataStructures/PlacementDetails.cs
- Terraria/DataStructures/PlayerGetItemLogger.cs
- Terraria/DataStructures/PlayerIntentionGuesser.cs
- Terraria/DataStructures/RecipeItemCreationContext.cs
- Terraria/DataStructures/RejectionMenuInfo.cs
- Terraria/DataStructures/ReturnFromRejectionMenuAction.cs
- Terraria/DataStructures/RichRoomCheckFeedback.cs
- Terraria/DataStructures/SelectionHolder.cs
- Terraria/DataStructures/SettingsForCharacterPreview.cs
- Terraria/DataStructures/SpriteBatchBeginner.cs
- Terraria/DataStructures/SpriteDrawBuffer.cs
- Terraria/DataStructures/TileEntityType.cs
- Terraria/DataStructures/TileReachCheckSettings.cs
- Terraria/DataStructures/TitleLinkButton.cs
- Terraria/DataStructures/TrackedProjectileReference.cs
- Terraria/Enums/FrameSkipMode.cs
- Terraria/EquipmentLoadout.cs
- Terraria/FocusHelper.cs
- Terraria/GameContent/Animations/Actions.cs
- Terraria/GameContent/Animations/GameAnimationSegment.cs
- Terraria/GameContent/Animations/IAnimationSegment.cs
- Terraria/GameContent/Animations/IAnimationSegmentAction.cs
- Terraria/GameContent/Animations/SegmentInforReport.cs
- Terraria/GameContent/Animations/Segments.cs
- Terraria/GameContent/Animations/StardewValleyAnimation.cs
- Terraria/GameContent/BannerSystem.cs
- Terraria/GameContent/Bestiary/BestiaryPortraitBackgroundBasedOnWorldEvilProviderPreferenceInfoElement.cs
- Terraria/GameContent/Bestiary/BestiaryPortraitBackgroundProviderPreferenceInfoElement.cs
- Terraria/GameContent/Bestiary/IBestiaryPrioritizedElement.cs
- Terraria/GameContent/Bestiary/IUpdateBeforeSorting.cs
- Terraria/GameContent/Bestiary/MoonLordPortraitBackgroundProviderBestiaryInfoElement.cs
- Terraria/GameContent/Bestiary/NPCKillCounterInfoElement.cs
- Terraria/GameContent/Biomes/DitherSnake.cs
- Terraria/GameContent/Biomes/DitherSnakePass.cs
- Terraria/GameContent/Biomes/DungeonControlLine.cs
- Terraria/GameContent/Biomes/SpikePitBiome.cs
- Terraria/GameContent/BossDamageTracker.cs
- Terraria/GameContent/ConditionalDialogue.cs
- Terraria/GameContent/CraftingEffectDetails.cs
- Terraria/GameContent/CraftingEffects.cs
- Terraria/GameContent/CraftingRequests.cs
- Terraria/GameContent/DontStarveDarknessDamageDealer.cs
- Terraria/GameContent/DontStarveSeed.cs
- Terraria/GameContent/Drawing/BackgroundArrayGetterMethod.cs
- Terraria/GameContent/Drawing/BackgroundGradientDrawer.cs
- Terraria/GameContent/Drawing/DrawBlackHelper.cs
- Terraria/GameContent/Drawing/EmptyHorizonRenderer.cs
- Terraria/GameContent/Drawing/GetBackgroundDrawWeightMethod.cs
- Terraria/GameContent/Drawing/HorizonHelper.cs
- Terraria/GameContent/Drawing/IHorizonRenderer.cs
- Terraria/GameContent/Drawing/INatureRenderer.cs
- Terraria/GameContent/Drawing/LensFlareElement.cs
- Terraria/GameContent/Drawing/NextHorizonRenderer.cs
- Terraria/GameContent/Drawing/NextNatureRenderer.cs
- Terraria/GameContent/Drawing/OriginalNatureRenderer.cs
- Terraria/GameContent/Drawing/SideFlags.cs
- Terraria/GameContent/Drawing/SunGradients.cs
- Terraria/GameContent/Drawing/TileDrawingBase.cs
- Terraria/GameContent/EmergencyStacking.cs
- Terraria/GameContent/Events/CreditsRollEvent.cs
- Terraria/GameContent/Events/DangerousDungeonCurse.cs
- Terraria/GameContent/ExtraSeatInfo.cs
- Terraria/GameContent/ExtraSpawnPointManager.cs
- Terraria/GameContent/ExtraSpawnSettings.cs
- Terraria/GameContent/ExtraSpawnType.cs
- Terraria/GameContent/ExtractinatorHelper.cs
- Terraria/GameContent/FakeCursorItem.cs
- Terraria/GameContent/FishDropRules/AFishDropRulePopulator.cs
- Terraria/GameContent/FishDropRules/AFishingCondition.cs
- Terraria/GameContent/FishDropRules/FishDropRule.cs
- Terraria/GameContent/FishDropRules/FishDropRuleList.cs
- Terraria/GameContent/FishDropRules/FishPossibilityEntry.cs
- Terraria/GameContent/FishDropRules/FishRarityCondition.cs
- Terraria/GameContent/FishDropRules/FishingConditions.cs
- Terraria/GameContent/FishDropRules/FishingContext.cs
- Terraria/GameContent/FishDropRules/GameContentFishDropPopulator.cs
- Terraria/GameContent/FishDropRules/Roller.cs
- Terraria/GameContent/FlexibleTileWand.cs
- Terraria/GameContent/Generation/Dungeon/DualDungeonUnbreakableWallTiers.cs
- Terraria/GameContent/Generation/Dungeon/DungeonBounds.cs
- Terraria/GameContent/Generation/Dungeon/DungeonColor.cs
- Terraria/GameContent/Generation/Dungeon/DungeonCrawler.cs
- Terraria/GameContent/Generation/Dungeon/DungeonData.cs
- Terraria/GameContent/Generation/Dungeon/DungeonDoorData.cs
- Terraria/GameContent/Generation/Dungeon/DungeonGenVars.cs
- Terraria/GameContent/Generation/Dungeon/DungeonGenerationStyleData.cs
- Terraria/GameContent/Generation/Dungeon/DungeonGenerationStyleID.cs
- Terraria/GameContent/Generation/Dungeon/DungeonGenerationStyles.cs
- Terraria/GameContent/Generation/Dungeon/DungeonLayoutProvider.cs
- Terraria/GameContent/Generation/Dungeon/DungeonLayoutProviderSettings.cs
- Terraria/GameContent/Generation/Dungeon/DungeonPlatformData.cs
- Terraria/GameContent/Generation/Dungeon/DungeonRoomSearchSettings.cs
- Terraria/GameContent/Generation/Dungeon/DungeonShapes.cs
- Terraria/GameContent/Generation/Dungeon/DungeonType.cs
- Terraria/GameContent/Generation/Dungeon/DungeonUtils.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/DomeDungeonEntrance.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/DomeDungeonEntranceSettings.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/DungeonEntrance.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/DungeonEntranceSettings.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/DungeonEntranceType.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/LegacyDungeonEntrance.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/LegacyDungeonEntranceSettings.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/PreGenDungeonEntranceSettings.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/TowerDungeonEntrance.cs
- Terraria/GameContent/Generation/Dungeon/Entrances/TowerDungeonEntranceSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonDropTrap.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonDropTrapSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonDropTrapType.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonFeature.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonFeatureSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalBanners.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalBasicChests.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalBiomeChests.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalBookshelves.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalDoors.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalEarlyDualDungeonFeatures.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalGroundFurniture.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalLateDualDungeonFeatures.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalLights.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalPaintings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalPlatforms.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalSpikes.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalTraps.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonGlobalWallVariants.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonPillar.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonPillarSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonPitTrap.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonPitTrapSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonTileClump.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonTileClumpSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonWindow.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonWindowBasic.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonWindowBasicSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonWindowMosaic.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonWindowMosaicSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/DungeonWindowSettings.cs
- Terraria/GameContent/Generation/Dungeon/Features/GlobalDungeonFeature.cs
- Terraria/GameContent/Generation/Dungeon/Features/IDungeonFeature.cs
- Terraria/GameContent/Generation/Dungeon/Features/PillarType.cs
- Terraria/GameContent/Generation/Dungeon/Halls/DungeonHall.cs
- Terraria/GameContent/Generation/Dungeon/Halls/DungeonHallSettings.cs
- Terraria/GameContent/Generation/Dungeon/Halls/DungeonHallType.cs
- Terraria/GameContent/Generation/Dungeon/Halls/LegacyDungeonHall.cs
- Terraria/GameContent/Generation/Dungeon/Halls/LegacyDungeonHallSettings.cs
- Terraria/GameContent/Generation/Dungeon/Halls/LegacyEntranceDungeonHall.cs
- Terraria/GameContent/Generation/Dungeon/Halls/LegacyEntranceDungeonHallSettings.cs
- Terraria/GameContent/Generation/Dungeon/Halls/RegularDungeonHall.cs
- Terraria/GameContent/Generation/Dungeon/Halls/RegularDungeonHallSettings.cs
- Terraria/GameContent/Generation/Dungeon/Halls/SineDungeonHall.cs
- Terraria/GameContent/Generation/Dungeon/Halls/SineDungeonHallSettings.cs
- Terraria/GameContent/Generation/Dungeon/Halls/StairwellDungeonHall.cs
- Terraria/GameContent/Generation/Dungeon/Halls/StairwellDungeonHallSettings.cs
- Terraria/GameContent/Generation/Dungeon/Halls/StepBasedDungeonHallSettings.cs
- Terraria/GameContent/Generation/Dungeon/LayoutProviders/DualDungeonLayoutProvider.cs
- Terraria/GameContent/Generation/Dungeon/LayoutProviders/DualDungeonLayoutProviderSettings.cs
- Terraria/GameContent/Generation/Dungeon/LayoutProviders/LegacyDungeonLayoutProvider.cs
- Terraria/GameContent/Generation/Dungeon/LayoutProviders/LegacyDungeonLayoutProviderSettings.cs
- Terraria/GameContent/Generation/Dungeon/ProgressionStageCheck.cs
- Terraria/GameContent/Generation/Dungeon/ProtectionType.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/BiomeDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/BiomeDungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/BiomeRuggedDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/BiomeSquareDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/BiomeStructuredDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/ConnectionPointQuality.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/DungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/DungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/DungeonRoomType.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/GenShapeDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/GenShapeDungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/GenShapeType.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/LegacyDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/LegacyDungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/LivingTreeDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/LivingTreeDungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/RegularDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/RegularDungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/StepBasedDungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/WormlikeDungeonRoom.cs
- Terraria/GameContent/Generation/Dungeon/Rooms/WormlikeDungeonRoomSettings.cs
- Terraria/GameContent/Generation/Dungeon/SnakeOrientation.cs
- Terraria/GameContent/Generation/Dungeon/WindowType.cs
- Terraria/GameContent/Generation/PaintingEntry.cs
- Terraria/GameContent/InvasionDamageTracker.cs
- Terraria/GameContent/ItemDropRules/CommonDropScalingWithOnlyBadLuck.cs
- Terraria/GameContent/ItemDropRules/DropBasedOnExtraGel.cs
- Terraria/GameContent/ItemDropRules/DropBasedOnMasterAndExpertMode.cs
- Terraria/GameContent/ItemDropRules/FromOptionsWithoutRepeatsDropRule.cs
- Terraria/GameContent/ItemDropRules/StatueMimicItemDropRule.cs
- Terraria/GameContent/ItemTrader.cs
- Terraria/GameContent/Items/ItemVariant.cs
- Terraria/GameContent/Items/ItemVariantCondition.cs
- Terraria/GameContent/Items/ItemVariants.cs
- Terraria/GameContent/Items/TagEffectState.cs
- Terraria/GameContent/Items/UniqueTagEffect.cs
- Terraria/GameContent/Items/WhipTagEffect.cs
- Terraria/GameContent/Items/WhipTagEffect_DarkHarvest.cs
- Terraria/GameContent/Items/WhipTagEffect_Firecracker.cs
- Terraria/GameContent/Items/WhipTagEffect_Kaleidoscope.cs
- Terraria/GameContent/Items/WhipTagEffect_Possession.cs
- Terraria/GameContent/Items/WhipTagEffect_Starcrash.cs
- Terraria/GameContent/Items/WhipTagEffect_ViolentDisplayOfFlower.cs
- Terraria/GameContent/LeashedEntities/BirdLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/CrawlerLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/CrawlingFlyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/DragonflyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/EmpressButterflyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/FairyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/FireflyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/FishLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/FlyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/FlyerLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/HellButterflyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/JumperLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/LeashedCritter.cs
- Terraria/GameContent/LeashedEntities/LeashedKite.cs
- Terraria/GameContent/LeashedEntities/NormalButterflyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/RunnerLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/ShimmerFlyLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/SnailLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/WalkerLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/WaterStriderLeashedCritter.cs
- Terraria/GameContent/LeashedEntities/WaterfowlLeashedCritter.cs
- Terraria/GameContent/LeashedEntity.cs
- Terraria/GameContent/LightningGenerator.cs
- Terraria/GameContent/Luck.cs
- Terraria/GameContent/LucyAxeMessage.cs
- Terraria/GameContent/NPCDamageTracker.cs
- Terraria/GameContent/NPCInteraction.cs
- Terraria/GameContent/NPCInteractions.cs
- Terraria/GameContent/NearbyChests.cs
- Terraria/GameContent/NetModules/NetDebugModule.cs
- Terraria/GameContent/OneTimeDialogue.cs
- Terraria/GameContent/OutlinedDrawRenderTargetContent.cs
- Terraria/GameContent/Personalities/AShoppingBiome.cs
- Terraria/GameContent/Personalities/AffectionLevel.cs
- Terraria/GameContent/Personalities/BiomePreferenceListTrait.cs
- Terraria/GameContent/Personalities/CorruptionBiome.cs
- Terraria/GameContent/Personalities/CrimsonBiome.cs
- Terraria/GameContent/Personalities/DesertBiome.cs
- Terraria/GameContent/Personalities/DungeonBiome.cs
- Terraria/GameContent/Personalities/ForestBiome.cs
- Terraria/GameContent/Personalities/HallowBiome.cs
- Terraria/GameContent/Personalities/JungleBiome.cs
- Terraria/GameContent/Personalities/MushroomBiome.cs
- Terraria/GameContent/Personalities/NPCPreferenceTrait.cs
- Terraria/GameContent/Personalities/OceanBiome.cs
- Terraria/GameContent/Personalities/PersonalityDatabasePopulator.cs
- Terraria/GameContent/Personalities/SnowBiome.cs
- Terraria/GameContent/Personalities/UndergroundBiome.cs
- Terraria/GameContent/PlayerPettingInfo.cs
- Terraria/GameContent/PopupEffectStyle.cs
- Terraria/GameContent/PositionedChest.cs
- Terraria/GameContent/Prefixes/PrefixLegacy.cs
- Terraria/GameContent/QuickStacking.cs
- Terraria/GameContent/SecretSeedsTracker.cs
- Terraria/GameContent/Shaders/SepiaScreenShaderData.cs
- Terraria/GameContent/ShimmerHelper.cs
- Terraria/GameContent/ShimmerTransforms.cs
- Terraria/GameContent/ShimmerUnstuckHelper.cs
- Terraria/GameContent/Skies/AuroraSky.cs
- Terraria/GameContent/Skies/CreditsRoll/CreditsRollComposer.cs
- Terraria/GameContent/SpecialSeedFeatures.cs
- Terraria/GameContent/Tile_Entities/DisplayDollPoseID.cs
- Terraria/GameContent/Tile_Entities/TECritterAnchor.cs
- Terraria/GameContent/Tile_Entities/TEDeadCellsDisplayJar.cs
- Terraria/GameContent/Tile_Entities/TEKiteAnchor.cs
- Terraria/GameContent/Tile_Entities/TELeashedEntityAnchor.cs
- Terraria/GameContent/Tile_Entities/TELeashedEntityAnchorWithItem.cs
- Terraria/GameContent/UI/BigProgressBar/BigProgressBarCache.cs
- Terraria/GameContent/UI/BigProgressBar/DeerclopsBigProgressBar.cs
- Terraria/GameContent/UI/CharacterCreationTipsProvider.cs
- Terraria/GameContent/UI/Elements/AWorldListItem.cs
- Terraria/GameContent/UI/Elements/GroupOptionButton.cs
- Terraria/GameContent/UI/Elements/UIBestiaryInfoLine.cs
- Terraria/GameContent/UI/Elements/UICreativeItemGrid.cs
- Terraria/GameContent/UI/Elements/UICyclingImage.cs
- Terraria/GameContent/UI/Elements/UIDebugCommandItem.cs
- Terraria/GameContent/UI/Elements/UIIconTextButton.cs
- Terraria/GameContent/UI/Elements/UIImageWithBorder.cs
- Terraria/GameContent/UI/Elements/UIResourcePackInfoButton.cs
- Terraria/GameContent/UI/Elements/UISelectableTextPanel.cs
- Terraria/GameContent/UI/Elements/UITextPanel.cs
- Terraria/GameContent/UI/Elements/UIWorkshopImportWorldListItem.cs
- Terraria/GameContent/UI/Elements/UIWorkshopPublishResourcePackListItem.cs
- Terraria/GameContent/UI/Elements/UIWorkshopPublishWorldListItem.cs
- Terraria/GameContent/UI/Elements/UIWrappedSearchBar.cs
- Terraria/GameContent/UI/GameTipsProvider.cs
- Terraria/GameContent/UI/ITipProvider.cs
- Terraria/GameContent/UI/IssueReportsIndicator.cs
- Terraria/GameContent/UI/Minimap/MinimapFrame.cs
- Terraria/GameContent/UI/Minimap/MinimapFrameManager.cs
- Terraria/GameContent/UI/Minimap/MinimapFrameTemplate.cs
- Terraria/GameContent/UI/NPCChatPanel.cs
- Terraria/GameContent/UI/NewCraftingUI.cs
- Terraria/GameContent/UI/ResourceSets/ClassicPlayerResourcesDisplaySet.cs
- Terraria/GameContent/UI/ResourceSets/CommonResourceBarMethods.cs
- Terraria/GameContent/UI/ResourceSets/FancyClassicPlayerResourcesDisplaySet.cs
- Terraria/GameContent/UI/ResourceSets/HorizontalBarsPlayerResourcesDisplaySet.cs
- Terraria/GameContent/UI/ResourceSets/IPlayerResourcesDisplaySet.cs
- Terraria/GameContent/UI/ResourceSets/PlayerResourceSetsManager.cs
- Terraria/GameContent/UI/ResourceSets/PlayerResourceSetsManager2.cs
- Terraria/GameContent/UI/ResourceSets/PlayerStatsSnapshot.cs
- Terraria/GameContent/UI/ResourceSets/ResourceDrawSettings.cs
- Terraria/GameContent/UI/States/AWorkshopPublishInfoState.cs
- Terraria/GameContent/UI/States/UIDebugCommandsList.cs
- Terraria/GameContent/UI/States/UIReportsPage.cs
- Terraria/GameContent/UI/States/UITextWrappingTest.cs
- Terraria/GameContent/UI/States/UIWorkshopHub.cs
- Terraria/GameContent/UI/States/UIWorkshopSelectResourcePackToPublish.cs
- Terraria/GameContent/UI/States/UIWorkshopSelectWorldToPublish.cs
- Terraria/GameContent/UI/States/UIWorkshopWorldImport.cs
- Terraria/GameContent/UI/States/UIWorldCreationAdvanced.cs
- Terraria/GameContent/UI/States/UIWorldCreationAdvancedSecretSeedsList.cs
- Terraria/GameContent/UI/States/UIWorldGenDebug.cs
- Terraria/GameContent/UI/States/WorkshopPublishInfoStateForResourcePack.cs
- Terraria/GameContent/UI/States/WorkshopPublishInfoStateForWorld.cs
- Terraria/GameContent/UI/TextDisplayCache.cs
- Terraria/GameContent/UI/UIAdvancedPopupRequest.cs
- Terraria/GameContent/UI/UIDust.cs
- Terraria/GameContent/UI/UIPopupText.cs
- Terraria/GameContent/UI/UIPopupTextAlignment.cs
- Terraria/GameContent/UI/UIPopupTextContext.cs
- Terraria/GameContent/UI/UIPopupTextManager.cs
- Terraria/GameContent/UI/WorkshopPublishingIndicator.cs
- Terraria/GameContent/UnbreakableWallScan.cs
- Terraria/GameInput/CursorMode.cs
- Terraria/Graphics/CameraModifiers/CameraInfo.cs
- Terraria/Graphics/CameraModifiers/CameraModifierStack.cs
- Terraria/Graphics/CameraModifiers/ICameraModifier.cs
- Terraria/Graphics/CameraModifiers/PunchCameraModifier.cs
- Terraria/Graphics/Effects/EffectManager.cs
- Terraria/Graphics/GraphicsUtils.cs
- Terraria/Graphics/Light/TileLightScannerOptions.cs
- Terraria/Graphics/LightDiscDrawer.cs
- Terraria/Graphics/Renderers/BloodyExplosionParticle.cs
- Terraria/Graphics/Renderers/FadingPlayerShaderParticle.cs
- Terraria/Graphics/Renderers/FakeFishParticle.cs
- Terraria/Graphics/Renderers/GasParticle.cs
- Terraria/Graphics/Renderers/IParticleRepel.cs
- Terraria/Graphics/Renderers/ItemTransferParticle.cs
- Terraria/Graphics/Renderers/LittleFlyingCritterParticle.cs
- Terraria/Graphics/Renderers/OutlinedTextureRenderer.cs
- Terraria/Graphics/Renderers/ParticlePool.cs
- Terraria/Graphics/Renderers/ParticleRepelDetails.cs
- Terraria/Graphics/Renderers/RoomCheckParticle.cs
- Terraria/Graphics/Renderers/ShockIconParticle.cs
- Terraria/Graphics/Renderers/StormLightningParticle.cs
- Terraria/Graphics/Shaders/EffectParameterExtensions.cs
- Terraria/Graphics/StormLightningDrawer.cs
- Terraria/Graphics/WorldSceneLayerTarget.cs
- Terraria/ID/BiomeConversionID.cs
- Terraria/ID/GameVersionID.cs
- Terraria/ID/GenPassNameID.cs
- Terraria/ID/ImmunityCooldownID.cs
- Terraria/ID/ItemSourceID.cs
- Terraria/ID/LiquidID.cs
- Terraria/ID/MusicID.cs
- Terraria/ID/PaintCoatingID.cs
- Terraria/ID/PlayerItemSlotID.cs
- Terraria/ID/PlayerTeamID.cs
- Terraria/ID/PlayerVoiceID.cs
- Terraria/ID/PlayerVoiceOverrideID.cs
- Terraria/ID/ProjectileDrawLayerID.cs
- Terraria/ID/ProjectileSourceID.cs
- Terraria/ID/RecipeGroups.cs
- Terraria/IEntitySourceTarget.cs
- Terraria/InitData.cs
- Terraria/Initializers/LinkButtonsInitializer.cs
- Terraria/Localization/VariableText.cs
- Terraria/MacLaunch.cs
- Terraria/Map/BossBagMapLayer.cs
- Terraria/Map/MapUpdateQueue.cs
- Terraria/Map/TeamBasedSpawnMapLayer.cs
- Terraria/MapRenderer.cs
- Terraria/NPCSpawningFlagsForDualDungeons.cs
- Terraria/Net/Ping.cs
- Terraria/Net/Sockets/DebugNetworkStream.cs
- Terraria/NewProjectileModifier.cs
- Terraria/NewProjectileModifiers.cs
- Terraria/SceneState.cs
- Terraria/ScriptSandbox.cs
- Terraria/SkyblockIslandID.cs
- Terraria/Social/Base/AWorkshopEntry.cs
- Terraria/Social/Base/AWorkshopProgressReporter.cs
- Terraria/Social/Base/AWorkshopTagsCollection.cs
- Terraria/Social/Base/FoundWorkshopEntryInfo.cs
- Terraria/Social/Base/PlatformSocialModule.cs
- Terraria/Social/Base/TexturePackWorkshopEntry.cs
- Terraria/Social/Base/WorkshopBranding.cs
- Terraria/Social/Base/WorkshopIssueReporter.cs
- Terraria/Social/Base/WorkshopItemPublicSettingId.cs
- Terraria/Social/Base/WorkshopItemPublishSettings.cs
- Terraria/Social/Base/WorkshopSocialModule.cs
- Terraria/Social/Base/WorkshopTagOption.cs
- Terraria/Social/Base/WorldWorkshopEntry.cs
- Terraria/Social/Steam/PlatformSocialModule.cs
- Terraria/Social/Steam/SupportedWorkshopTags.cs
- Terraria/Social/Steam/WorkshopHelper.cs
- Terraria/Social/Steam/WorkshopProgressReporter.cs
- Terraria/Social/Steam/WorkshopSocialModule.cs
- Terraria/Testing/ChatCommands/CommandRequirement.cs
- Terraria/Testing/ChatCommands/DebugCommandAttribute.cs
- Terraria/Testing/ChatCommands/DebugCommandProcessor.cs
- Terraria/Testing/ChatCommands/DebugMessage.cs
- Terraria/Testing/ChatCommands/IDebugCommand.cs
- Terraria/Testing/ChatCommands/ToolkitDebugCommands.cs
- Terraria/Testing/DebugLineDraw.cs
- Terraria/Testing/DebugOptions.cs
- Terraria/Testing/DebugOverrides.cs
- Terraria/Testing/DebugUtils.cs
- Terraria/Testing/DetailedFPS.cs
- Terraria/Testing/GitStatus.cs
- Terraria/Testing/LockstepDebug.cs
- Terraria/Testing/QuickLoad.cs
- Terraria/Testing/WindowsPerformanceDiagnostics.cs
- Terraria/TileColorCache.cs
- Terraria/UI/BannerClaimingUI.cs
- Terraria/UI/Chat/PositionedSnippet.cs
- Terraria/UI/CoinSlot.cs
- Terraria/UI/CraftingUI.cs
- Terraria/UI/ICraftingUI.cs
- Terraria/UI/IHaveBackButtonCommand.cs
- Terraria/UI/IPipsUI.cs
- Terraria/UI/IngameUIWindows.cs
- Terraria/Utilities/BitSet2D.cs
- Terraria/Utilities/Bits64.cs
- Terraria/Utilities/DialogResult.cs
- Terraria/Utilities/EasyDeserializationJsonContractResolver.cs
- Terraria/Utilities/FileBrowser/ExtensionFilter.cs
- Terraria/Utilities/FileBrowser/FileBrowser.cs
- Terraria/Utilities/FileBrowser/IFileBrowser.cs
- Terraria/Utilities/FileBrowser/NativeFileDialog.cs
- Terraria/Utilities/LCG32Random.cs
- Terraria/Utilities/MessageBox.cs
- Terraria/Utilities/MessageBoxButtons.cs
- Terraria/Utilities/MessageBoxIcon.cs
- Terraria/Utilities/NewRuntimeMethods.cs
- Terraria/Utilities/OldAttribute.cs
- Terraria/Utilities/Secrets.cs
- Terraria/Utilities/TileSnapshot.cs
- Terraria/Utilities/Vertical64BitStrips.cs
- Terraria/Utilities/WeightedRandom.cs
- Terraria/WaterfallID.cs
- Terraria/WorldBuilding/AWorldGenerationOption.cs
- Terraria/WorldBuilding/DungeonSide.cs
- Terraria/WorldBuilding/GenPassResult.cs
- Terraria/WorldBuilding/GenVars.cs
- Terraria/WorldBuilding/LandmassData.cs
- Terraria/WorldBuilding/LandmassDataType.cs
- Terraria/WorldBuilding/WorldGenSnapshot.cs
- Terraria/WorldBuilding/WorldGenerationOptions.cs
- Terraria/WorldBuilding/WorldManifest.cs
- Terraria/WorldBuilding/WorldSeedOption_Anniversary.cs
- Terraria/WorldBuilding/WorldSeedOption_DontStarve.cs
- Terraria/WorldBuilding/WorldSeedOption_Drunk.cs
- Terraria/WorldBuilding/WorldSeedOption_Everything.cs
- Terraria/WorldBuilding/WorldSeedOption_ForTheWorthy.cs
- Terraria/WorldBuilding/WorldSeedOption_NoTraps.cs
- Terraria/WorldBuilding/WorldSeedOption_Normal.cs
- Terraria/WorldBuilding/WorldSeedOption_NotTheBees.cs
- Terraria/WorldBuilding/WorldSeedOption_Remix.cs
- Terraria/WorldBuilding/WorldSeedOption_Skyblock.cs
- Terraria/WorldItem.cs
- Terraria/WorldSize.cs
- nativefiledialog.cs

## 二、1405 独有文件(可能是重命名/合并进其他文件)

- Terraria/Achievements/AchievementTracker`1.cs
- Terraria/AssemblyInfo.cs
- Terraria/DataStructures/DoubleStack`1.cs
- Terraria/DataStructures/EntryFilterer`2.cs
- Terraria/DataStructures/EntrySorter`2.cs
- Terraria/DataStructures/GameModeData.cs
- Terraria/DataStructures/IEntryFilter`1.cs
- Terraria/DataStructures/IEntrySortStep`1.cs
- Terraria/DataStructures/ISearchFilter`1.cs
- Terraria/DataStructures/NPCStrengthHelper.cs
- Terraria/DeprecatedClassLeftInForLoading.cs
- Terraria/Enums/TileIDEnum.cs
- Terraria/Extensions/EnumerationExtensions.cs
- Terraria/GameContent/Bestiary/BestiaryPortraitBackgroundBasedOnWorldEvilProvider.cs
- Terraria/GameContent/Bestiary/BestiaryPortraitBackgroundProviderPreferenceInfoEl.cs
- Terraria/GameContent/Bestiary/MoonLordPortraitBackgroundProviderBestiaryInfoElem.cs
- Terraria/GameContent/NPCHeadDrawRenderTargetContent.cs
- Terraria/GameContent/NetModules/NetCreativeUnlocksModule.cs
- Terraria/GameContent/Skies/CreditsRoll/Actions.cs
- Terraria/GameContent/Skies/CreditsRoll/CreditsRollInfo.cs
- Terraria/GameContent/Skies/CreditsRoll/ICreditsRollSegment.cs
- Terraria/GameContent/Skies/CreditsRoll/ICreditsRollSegmentAction`1.cs
- Terraria/GameContent/Skies/CreditsRoll/Segments.cs
- Terraria/GameContent/UI/ClassicPlayerResourcesDisplaySet.cs
- Terraria/GameContent/UI/CommonResourceBarMethods.cs
- Terraria/GameContent/UI/Elements/GroupOptionButton`1.cs
- Terraria/GameContent/UI/Elements/UIBestiaryInfoLine`1.cs
- Terraria/GameContent/UI/Elements/UIResourcePackInfoButton`1.cs
- Terraria/GameContent/UI/Elements/UISelectableTextPanel`1.cs
- Terraria/GameContent/UI/Elements/UITextPanel`1.cs
- Terraria/GameContent/UI/FancyClassicPlayerResourcesDisplaySet.cs
- Terraria/GameContent/UI/HorizontalBarsPlayerReosurcesDisplaySet.cs
- Terraria/GameContent/UI/IPlayerResourcesDisplaySet.cs
- Terraria/GameContent/UI/MinimapFrame.cs
- Terraria/GameContent/UI/PlayerStatsSnapshot.cs
- Terraria/GameContent/UI/ResourceDrawSettings.cs
- Terraria/Graphics/Effects/EffectManager`1.cs
- Terraria/Graphics/Renderers/NPCHeadRenderer.cs
- Terraria/Graphics/Renderers/ParticlePool`1.cs
- Terraria/ID/BiomeID.cs
- Terraria/ID/RecipeGroupID.cs
- Terraria/UI/LegacyNetDiagnosticsUI.cs
- Terraria/Utilities/FileOperationAPIWrapper.cs
- Terraria/Utilities/WeightedRandom`1.cs
- Terraria/WindowsLaunch.cs
- Terraria/World.cs
- Terraria/ZoomContext.cs

## 三、共同文件的成员增删


### Terraria/ID/ItemID.cs (+1164 / -9)
- 新方法(+1): PostSetupContent
- 新字段(+1163): AHorribleNightforAlchemy, AMachineforTerrarians, AbigailsFlower, AcornAxe, AcornSlingshot, AegisCrystal, AegisFruit, AetheriumBathtub, AetheriumBed, AetheriumBookcase, AetheriumCandelabra, AetheriumCandle, AetheriumChair, AetheriumChandelier, AetheriumChest, AetheriumClock, AetheriumDoor, AetheriumDresser, AetheriumLamp, AetheriumLantern, AetheriumPiano, AetheriumPlatform, AetheriumSink, AetheriumSofa, AetheriumTable, AetheriumToilet, AetheriumWorkbench, Ambrosia, AncientBlueDungeonBrick, AncientBlueDungeonBrickWall, AncientCobaltBrick, AncientCobaltBrickWall, AncientCopperBrick, AncientCopperBrickWall, AncientGoldBrick, AncientGoldBrickWall, AncientGreenDungeonBrick, AncientGreenDungeonBrickWall, AncientHellstoneBrick, AncientHellstoneBrickWall, AncientMythrilBrick, AncientMythrilBrickWall, AncientObsidianBrick, AncientObsidianBrickWall, AncientPinkDungeonBrick, AncientPinkDungeonBrickWall, AncientSilverBrick, AncientSilverBrickWall, AntlionEggs, ArcaneCrystal, ArgonMossBlock, ArgonMossBlockWall, ArtisanLoaf, AshGrassSeeds, AshWood, AshWoodBathtub, AshWoodBed, AshWoodBookcase, AshWoodBow, AshWoodBreastplate, AshWoodCandelabra, AshWoodCandle, AshWoodChair, AshWoodChandelier, AshWoodChest, AshWoodClock, AshWoodDoor, AshWoodDresser, AshWoodFence, AshWoodGreaves, AshWoodHammer, AshWoodHelmet, AshWoodLamp, AshWoodLantern, AshWoodPiano, AshWoodPlatform, AshWoodSink, AshWoodSofa, AshWoodSword, AshWoodTable …
- 移除字段(-9): EldMelter, ExpertDamageDealt, ExpertDamageReceived, ItemSpawnDecaySpeed, NewItemSpawnPriority, NormalDamageDealt, NormalDamageReceived, SortingPriorityBossSpawns, healingItemsDecayRate

### Terraria/Player.cs (+608 / -73)
- 新类型(+8): ChannelCancelKey, CraftingGridMode, DashPreference, ItemCheckContext, PlayerInputSyncCache, SelectedItemState, SetMatchRequest, StackToNearbyChestsMode
- 新方法(+299): AddCoinLuck, AdjustRemainingPotionSickness, AllowShimmerDodge, AnimatePlayerAndGetItemFrame, AnyoneToSpectate, ApplyAttackCooldown, ApplyCoating, ApplyHeadOffsetFromMount, ApplyItemPositionOffsetFromMount, ApplyLifeAndOrMana, ApplyMeleeScale, ApplyPaint, ApplyRangeCompensation, ApplyRapidAttackBonus, ApplySetBonus_BeetleDamage, ApplySetBonus_BeetleDefense, ApplySetBonus_Solar, ApplySetBonus_Stardust, ApplyShader, ApplyTouchDamage, ApplyWilsonBeard, BatBat_TryLifeLeeching, BiomeCampfireHoldStyle, BiomeCampfirePlaceStyle, BloodButcherer_TryButchering, CalculateCoinLuck, CanBePushedByWind, CanConsumeConsumableItem, CanDefendWithPaladinsShield, CanDoWireStuffHere, CanFitInSpaceWithSize, CanHitNPCWithMeleeHit, CanItemSlotAcceptPickup, CanPlayerSmashWall, CanShowWireStuffHere, CanSpawnWalkingEffects, CanSpectate, CanUseStressBall, CanWormholeToSpectating, CancelAllBootRunVisualEffects, CapAttackSpeeds, CheckManaPredictWithoutUse, CheckSpawn_Internal, ChestChangeEvents, ChickenBonesWingDust, ClosestSpectatablePlayerTo, CycleQuickStackMode, DashStartAction, Deserialize, DoCommonDashHandle, DoDeadCellsBeheadedParticles, DoDeadCellsGroundPoundEffect, DoEyebrellaRainEffect, DoGlassSlipperSparkles, DoUnbreakableWallScan, DropItemFromExtractinator, EndOngoingTorchGodEvent, FigureOutWhatToPlace, FindItemInInventoryOrOpenVoidBag, FindNewestAI_164Minion, FindPaintOrCoating, FixLoadedData, FixLoadedData_EliminiateDuplicateAccessories, FixLoadedData_Items, GetAdjustedItemScale, GetAnglerRewardRarityMultiplier, GetAnglerReward_Bait, GetAnglerReward_Decoration, GetAnglerReward_MainReward, GetAnglerReward_Money, GetArmorPenetration, GetAutoDoorVelocityContribution, GetBannerBuffEffect, GetBeardDrawOffset, GetBeardOffsetAddonFromHelmet, GetBeardOffsetAddonFromMount, GetClosestRollBadLuck, GetCraftingFilterForTile, GetCurrentContainer, GetFaceDrawOffset …  <!--注意:removed 大概率是 1405 dotPeek 反编译空壳/命名差异造成的假象-->
- 新字段(+301): AFKTimeNeededForAutoKiting, AFKTimeNeededForNoLuckyStars, AFKTimeNeededForNoWormSpawns, ArmorSlotRequested, BaseHeight, BlehOldPositionFixer, Body, CRTMonolithShader, CanUseBootFlyingAbilities, CraftFromNearbyChests, CraftingGridControl, CurrentLoadoutIndex, DashControl, DeadSpectatingLockoutTime, DefaultSize, DefaultTileRangeX, DefaultTileRangeY, Directions, FailedNoSpaceCount, FailedNoSpaceLocation, FlexibleWandCycleOffset, FlexibleWandLastPosition, FlexibleWandRandomSeed, GetItemLogger, HasActiveOverride, HasBufferedChange, HasMinionAttackTargetNPC, HasMinionRestTarget, Head, HeldItem, Hotbar, IntentionGuesser, IsAllowedToHoldItems, ItemAnimationJustStarted, ItemTimeIsZero, Legs, Loadouts, LocalInputCache, Male, MinecartSettings, PaladinsShieldRange, PhilosopherStoneDurationMultiplier, Player, ProjectileIndexExpected, ProjectileTypeExpected, SafeItemAnimationTimeForPreventingExploits, SaveSlotIndex_GuideItem, SaveSlotIndex_TinkererItem, SceneMetrics, Selected, SelectedBinding, ShoppingZone_BelowSurface, SkipItemConsumption, SmartCursorHoldCanReleaseMidUse, SpectatingLingerAfterDeath, StackToChestsPreferredMode, SunScorchGraceTime, SupportedMiscSlotCount, TagEffectState, TileReplacementEnabled, UnbreakableWallRescanDistance, UnbreakableWallRescanPeriod, VisualPosition, _batbatCanHeal, _bloodButchererMax5, _channelShotCache, _framesLeftEligibleForDeadmansChestDeathAchievement, _hallucinationCandidates, _localMinionRespawner, _nextTorchLuckCheckCenter, _pendingRefunds, _sizzleAudioHandle, _spawnBloodButcherer, _spawnMuramasaCut, _spawnTentacleSpikes, _spawnVolcanoExplosion, _tentacleSpikesMax5, _unbreakableWallScanCooldown, _unbreakableWallScanLastPosition, _visualCloneDummyData …
- 移除类型(-1): RandomTeleportationAttemptSettings
- 移除方法(-31): CanItemSlotAccept, CheckForGoodTeleportationSpot, Clone, GetNearbyContainerProjectilesList, GetPettingInfo, GetPrimaryBiome, HandleHotbar, HoneyCollision, InInteractionRange, IsAValidEquipmentSlotForIteration, IsProjectileInteractibleAndInInteractionRange, ItemCheck_CheckCanUse, ItemCheck_CheckFishingBobber_PickAndConsumeBait, ItemCheck_CheckFishingBobbers, ItemCheck_HandleMPItemAnimation, ItemCheck_PayMana, ItemCheck_UseRodOfDiscord, ManageSpecialBiomeVisuals, PlaceThing_Tiles_CheckLavaBlocking, RefreshItemArray, RotatedRelativePointOld, ScrollHotbar, SmartSelect_SelectItem, Spawn_IsAreaAValidWorldSpawn, TryFloatingInWater, UpdateGraveyard, UpdateNearbyInteractibleProjectilesList, WaterCollision, WipeOldestTurret, openPresent …  <!--注意:removed 大概率是 1405 dotPeek 反编译空壳/命名差异造成的假象-->
- 移除字段(-41): HotbarOffset, _blizzardSoundVolume, _insideBlizzardSound, _shaderObstructionInternalValue, _stormShaderObstruction, _strongBlizzardSound, adjWater, attemptsBeforeGivingUp, avoidAnyLiquid, avoidHurtTiles, avoidLava, avoidWalls, brainOfConfusion, cPortalbeStool, coins, disabledBlizzardGraphic, disabledBlizzardSound, discount, flyingPigChest, graveImmediateTime, isPettingAnimal, isTheAnimalBeingPetSmall, itemHeight, itemWidth, launcherWait, manaSickTimeMax, maximumFallDistanceFromOrignalPoint, minecartLeft, mostlySolidFloor, netSkip

### Terraria/WorldGen.cs (+430 / -151)
- 新类型(+5): SecretSeed, Skyblock, TenthAnniversaryWorldInfo, TileMergeCullCache, Variations
- 新方法(+305): ActiveAndWalkableTile, AddBeeLarva, AddLihzahrdAltar, AddManaCrystal, AddMonsterVoiceChangeItemToChest, AddPasses, AddSpikeCaves, AddVoiceChangeItemToChest, AddWire, AddWireFromPointToPoint, AnyLiquidAt, AreAnyTilesInSetNearby, AshTreeGroundTest, AttemptToGeneratePlanteraBulbAt, AttemptToGrowTreeFromSapling, BlockBelowMakesSandConvertIntoHardenedSand, BlockBelowMakesSandFall, BunnyCannonCanFire, Calculate, CanBeClearedDuringGeneration, CanChlorophyteGrow, CanEvilReplace, CanGeneratePressurePlateAt, Check, Check4x4, CheckAchievement_RealEstateAndTownSlimes, CheckAnchor, CheckAndAdjustMultiDirectionalTile, CheckExploitDestroyQueue, CheckForHousesNearAPlayer, CheckInputForSecretSeed, CheckStalactite, CheckStalactiteEcho, CheckStinkbugBlocker, CheckTileBreakability_HasReasonToReturnEarly, CheckVines, ChlorophyteDefense, ClearAllSeeds, ClearPendingLiquid, ClearUnbreakableWallsWithPaintUpTo, ConsideredSolidTileForAnchor, ConvertSkyIslands, ConvertTreeAndGround, ConvertTreeAndGround_Branches, Convert_ActuallyConvertTile, Convert_ActuallyConvertTorch, Convert_ActuallyConvertWall, Cull, DebugLogLightning, Disable, DisablePassesForSpecialSeeds, DoActuallyNoTraps, DoAddTeleporters, DoAddTeleporters_CanPutTeleporterHere, DoAddTeleporters_ClearArea, DoCoatEverythingEcho, DoCoatEverythingIlluminant, DoDigExtraHoles, DoErrorWorldFindChestItem, DoErrorWorldFinish, DoErrorWorldGetRandomBlock, DoErrorWorldShuffleBlocks, DoExtraLiquidAddBubbleBlocks, DoExtraLiquidAddLiquid, DoExtraLiquidFinish, DoHallowOnSurface, DoNoInfection, DoNoSpiderCavesILiedMoreSpiderCaves, DoNoSurface, DoNoSurfaceFillTheTop, DoPaintEverythingGray, DoPaintEverythingNegative, DoPooEverywhere, DoPortalGunInChests, DoRainbowStuff, DoRainsForAYear, DoRandomSpawn, DoRoundLandMasses, DoStartInHardmode, DoSurfaceIsDesert …  <!--注意:removed 大概率是 1405 dotPeek 反编译空壳/命名差异造成的假象-->
- 新字段(+120): AllSecretSeeds, CullBottom, CullBottomLeft, CullBottomRight, CullLeft, CullRight, CullTop, CullTopLeft, CullTopRight, Enabled, ExploitDestroyQueue, GemTree_Sapphire, GoodPrefixIdsForAccessory, GoodPrefixIdsForMagicWeapon, GoodPrefixIdsForMeleeWeapon, GoodPrefixIdsForRangedWeapon, GoodPrefixIdsForSummonerWeapon, InfectionAndGrassSpreadOuterWorldBuffer, ItemSpawnProtectionTime, LastFoundHouse, Localization, Manifest, TextThatWasUsedToUnlock, TransformingWorld, Tree_Ash, WorldSizeLargeX, WorldSizeLargeY, WorldSizeMediumX, WorldSizeMediumY, WorldSizeSmallX, WorldSizeSmallY, _SpawnThunderStorm_SafeSpots, _coatingColors, _code, _enabled, _isRainingBoulders, _plaintext, _preventInfiniteRopeFraming, _roomCheckStack, _sound, _transformingWorld, activeSecretSeedCount, actuallyNoTraps, addTeleporters, anySecretSeedIsActive, biggerAbandonedHouses, bitStrip, builtHouseWithNoFurniture, builtHouseWithNoLight, coatEverythingEcho, coatEverythingIlluminant, currentActiveTiles, denyAllGeneration, digExtraHoles, dontStarveWorldGen, dualDungeons, endlessChristmas, endlessHalloween, errorWorld, everythingWorldGen, extraFloatingIslands, extraLiquid, extraLivingTrees, genRand, generatingRandomEvil, generatingWorldOnThisThread, graveyardBloodmoonStart, growGrassUnderground, hallowOnTheSurface, halloweenGen, hardModeWorldUpdates, hasTile, hasWall, isGeneratingOrLoadingWorld, lowTiles, maxRoomSize, maxRoomTilesForQuery, meteorShowerCount, noAltars, noDungeon …
- 移除方法(-36): CheckAchievement_RealEstate, CheckTight, Chlorophyte, ClearWorld, ConsumePostGenActions, DungeonEnt, DungeonHalls, DungeonPitTrap, DungeonRoom, DungeonStairs, EveryTileFrame, ExplodeMine, FindAHomelessNPC, GetChestItemDrop, GetDresserItemDrop, GrowDungeonTree, GrowDungeonTree_MakePassage, Housing_CheckIfIsCeiling, IsTileReplacable, MakeDungeon, MakeDungeon_Banners, MakeDungeon_GroundFurniture, MakeDungeon_Lights, MakeDungeon_Pictures, MakeDungeon_Traps, PlatformProperSides, QueuePostGenAction, ReplaceTIle_DoActualReplacement, UpdateMapTile, WallDungeon …  <!--注意:removed 大概率是 1405 dotPeek 反编译空壳/命名差异造成的假象-->
- 移除字段(-115): DDoorPos, DDoorX, DDoorY, GemTree_Sappphire, IsGeneratingHardMode, JChestX, JChestY, JungleItemCount, JungleX, LakeX, NUM_SEASHELL_STYLES, StatuesWithTraps, USE_FRAMING_SKIP_FOR_UNIMPORTANT_TILES_IN_WORLDGEN, UndergroundDesertHiveLocation, UndergroundDesertLocation, _genRand, _genRandSeed, _lastSeed, _postGenActions, copperBar, crackedType, currentWorldSeed, dEnteranceX, dMaxX, dMaxY, dMinX, dMinY, dRoomB, dRoomL, dRoomR

### Terraria/Main.cs (+393 / -144)
- 新类型(+5): DialoguePortraitDrawOption, Hacks, IMEPanelAnchor, PipPage, TitleMusicStyle
- 新方法(+186): AddEchoFurnitureTile, AnyPlayerReadyToFightKingSlime, ApplyPendingBackgroundTargetSwap, AssetWatcherUpdateFailed, AssetWatcherValueUpdated, BindSettingsTo, BlackFadeCameraTeleport, CanDryadPlayStardewAnimation, CanPlayCreditsRoll, CanceledGivingServerPassword, CheckForMoonEventsScoreDisplay, ClearHoverItem, ClearWorldSeedFlags, CollectDisplayResolutionsFromAdapter, ComputeScAdj, ContentFileUpdated, CraftItem_GrantItem, CursorHasSpaceToCraftRecipe, CycleFrameSkipMode, CycleNPCPortraitMode, CycleVoiceStyle, DebugCameraPan, DedServ_SeedFlagsMenu, DisplayAndGetFakeItem, DoNPCPortraitHop, DoScrollingInInventory, DoStatefulTickSound, DrawBG_HandleBackgroundTransition, DrawBackground_DirtBackground, DrawBackground_DrawMagmaLayer, DrawBackground_DrawMagmaTransition, DrawBackground_DrawRockLayer, DrawBackground_DrawUnderworldBlackBox, DrawBackground_PickUndergroundBackgroundStyle, DrawBackground_SurfaceTransitionBackground, DrawBackground_UpdateBackgroundStyles, DrawCloud, DrawClouds_Closer, DrawClouds_Closest, DrawClouds_Distant, DrawContinuousTrail, DrawDebugMapOverlays, DrawDebugSectionsOnMap, DrawIMEPanel, DrawInfoAccs_AdjustInfoTextColorsForNPC, DrawInterface_29B_ControlHints, DrawInterface_InstrumentMouseText, DrawLensFlare, DrawLiquid, DrawLoadoutButtons, DrawNPCChatBottomRightItem, DrawNPCDirect_Deerclops, DrawNPCDirect_DeerclopsLeg, DrawNPCDirect_Faeling, DrawNPCMapIcon_CanBeSeen_Townie, DrawNPCMapIcons, DrawNPCMapIcons2, DrawNPCMapIcons3, DrawNPCPortrait, DrawPaladinsShield, DrawPaladinsShieldBoundary, DrawPlayerMapIcon_CanBeSeen, DrawProjDirect, DrawProj_DeadCellsFlintSlash, DrawProj_Excalibur, DrawProj_Flamethrower, DrawProj_Flamethrower_Foxsparks, DrawProj_LightsBane, DrawProj_NightsEdge, DrawProj_Spear, DrawProj_TerraBlade2, DrawProj_TerraBlade2Shot, DrawProj_TheHorsemansBlade, DrawProj_TrueExcalibur, DrawProj_TrueNightsEdge, DrawSocialMediaButtons, DrawSpectatingControlHint, DrawStar, DrawTrail, DrawUnbreakableWallScansOnMap …  <!--注意:removed 大概率是 1405 dotPeek 反编译空壳/命名差异造成的假象-->
- 新字段(+202): AchievementAdvisor, Achievements, BlackFadeDist, CameraModifiers, ChatLineWidthLimit, CollectGen0EveryFrame, CreativeMenuMouseOver, CurrentBackgroundMatrixForCreditsRoll, DelayedProcesses, DelayedProcessesInGame, DialoguePortraitPreference, DoGlowingMouseItemDraw, DroneCameraTracker, EverLastingTicker, FishDropsDB, FlashyEffectsInterface, FlashyEffectsWorld, ForegroundSunlightEffects, GameAskedToQuit, GameUpdateCount, GridToggleMouseOverBanners, GridToggleMouseOverCrafting, HadAnActiveInteractableProjectile, HasInteractableObjectThatIsNotATile, HorizonHelper, HorizonRenderer, InitialMapScale, IsInTheMiddleOfLoadingSettings, IsItAHappyWindyDay, IsItRaining, IsItStorming, IsJourneyMode, IsRainingForever, IssueReporter, IssueReporterIndicator, ItemMapIconRenderer, LastCelestialBodyPosition, LastLoadedResolution, LatestSurfaceBackgroundBeginner, LeinforsBalanceRequestForSlimeRainChance, LocalPlayer, LocalPlayerCreativeTracker, MapPylonTile, MaxWorldViewSize, MaxWorldViewSizeHeight, MaxWorldViewSizeWidth, MinimapFrameManagerInstance, MouseScreen, NoFunctionalSurface, NoPooling, PanTargetMapFullscreen, PanTargetMapFullscreenEnd, ParticleSystem_OverCursor, ParticleSystem_OverInventory, PipsCurrentPage, PipsFastScroll, PipsUseGrid, PlayerSceneMetrics, Position, PreventUpdatingTargets, ReHideCursor, RejectionMenuInfo, ResourceSetsManager, SceneState, ScissorState, ScreenSize, SettingPlayWhenUnfocused, Setting_AssetFileWatcherEnabled, SettingsEnabled_AutoReuseAllItems, ShouldPVPDraw, ShouldPlayRainbowBoulderMusic, SmartCursorDirectionLocks, SmartCursorIsUsed, SmartCursorWanted_GamePad, SmartCursorWanted_Mouse, SupportWideScreen, TARGET_FRAME_TIME, ThickMouse, ThrottleWhenInactive, TitleLinks …
- 移除类型(-1): TextDisplayCache
- 移除方法(-29): CheckMonoliths, CraftItem, DoLightTiles, DrawGuideCraftText_Old, DrawInterface_18_DiagnoseVideo, DrawItemIcon, DrawRainInMenu, DrawToMap, DrawToMap_Section, DrawUnderworldBackgroudLayer, DrawWater, DrawWhipOld, DrawWindowsIMEPanel, FullTile, GetScreenOverdrawOffset, InitMap, LoadContent_Music, LoadMusic, MouseOversTryToClear, OnPlayerSelected, PrepareCache, RenderBlack, SetCameraGamepadLerp, SetRecipeMaterialDisplayName, SetRecommendedZoomContext, TickLoadProcess, TryInteractingWithMoneyTrough2, UpdateParticleSystems, checkMap  <!--注意:removed 大概率是 1405 dotPeek 反编译空壳/命名差异造成的假象-->
- 移除字段(-114): ActiveMinimapFrame, ActiveNetDiagnosticsUI, ActivePlayerResourcesSet, ActiveWorld, BG_STYLES_COUNT, DisableIntenseVisualEffects, HadAnActiveInteractibleProjectile, HasInteractibleObjectThatIsNotATile, LightingEveryFrame, LogicCheckScreenHeight, LogicCheckScreenWidth, MaxBannerTypes, MinimapFrames, MinimumZoomComparerX, MinimumZoomComparerY, MonolithFilterNames, MonolithSkyNames, PlayerResourcesSets, RegisterdGameModes, SceneLocalScreenPositionOffset, SceneMetrics, SettingMusicReplayDelayEnabled, ShaderContentManager, SmartCursorEnabled, TerrariaSaveFolderPath, VertexPixelShaderRef, _MouseOversCanClear, _WeGameReqExit, _artLoaded, _begunMainAsyncLoad

### Terraria/NPC.cs (+313 / -39)
- 新类型(+2): PlayerNetSyncState, Spawner
- 新方法(+173): AI_003_Gnomes_ShouldTurnToStone, AI_007_TownEntities_Shimmer_ScanForBestSpotToLandOn, AI_007_TownEntities_Shimmer_TeleportToLandingSpot, AI_007_TownEntities_TeleportToHome, AI_007_TownEntities_UpdateSavedStates, AI_015_KingSlime, AI_015_KingSlime_FindTeleportSpot, AI_045_Golem, AI_047_GolemFist, AI_120_HallowBoss_DashTo, AI_123_Deerclops, AI_123_Deerclops_FindSpotToSpawnSpike, AI_123_Deerclops_MakeSpikesBothSides, AI_123_Deerclops_MakeSpikesForward, AI_123_Deerclops_Movement, AI_123_Deerclops_ShootRubbleUp, AI_123_Deerclops_TryMakingSpike, AI_123_Deerclops_TryMakingSpike_FindBestY, AI_124_DeerclopsLeg, AI_124_ElderSlimeChest, AI_125_ClumsySlimeBalloon, AI_126_StatueMimic, AI_127_Pal, AI_127_Pal_GiveRewerd, AI_127_Pal_SummonAttacker, AI_127_Pal_TryUnpackNPC, AI_87_BigMimic_FireStuffCannonBurst, AI_87_BigMimic_ShootItem, AI_AttemptToFindTeleportSpot, AI_AttemptToFindTeleportSpotNearBooks, AI_AttemptToFindTeleportSpotNearBooks_SearchWall, AI_FindNearbyBook, AddKingSlimeTeleportCacheTiles, AnyLifeCrystalSlimes, AppearsFriendlyToHunterPotion, ApplyEelWhipDoT, AttemptToConvertNPCToEvil, Boss_CanShootExtraAt, BuildKingSlimeTeleportCache, CanAnyPlayerSeeThisTile, CanApplyHunterPotionEffects, CanShowHomelessText, CanSpawnDevourer, CanSpawnEnemiesNear, CanSpawnInTile, CanSpawnInTiles, CheckActive_WormSegments, CheckDialogue, CheckNotSpawningOnScreen, CheckToSpawnDungeonEnemies, CheckToSpawnRockGolem, CheckToSpawnSpider, CheckToSpawnUndergroundFairy, CheckToSpawnUndergroundGnomes, ConveyorBeltCollision, CurrentlyShimmerTransparent, DoesntDespawnToInactivityAndCountsNPCSlots, FindFrame_Deerclops_GetAttack1Frame, FindFrame_Deerclops_GetAttack2Frame, FindFrame_Deerclops_GetAttack3Frame, FindFrame_FromSequence, FindSpawnTile, GetAttackDamage_CappedAtMaster, GetAttackDamage_ForTownNPC, GetAttackDamage_ScaledByDifficulty, GetAvailableAmountOfNPCsToSpawnUpToSlot, GetAvailableNPCSlot, GetBasicSlimeToSpawn, GetBasicSlimeToSpawn_ChanceToBeHolidaySlime, GetBossSpawnSource, GetDestroyerSegmentsCount, GetGemBunnyToSpawn, GetGemSquirrelToSpawn, GetGnomeChance, GetHurtByDebuff, GetItemSource_Loot, GetItemSource_Misc, GetKnockbackMultiplier_ScaledByDifficulty, GetMagicAuraColor, GetMechQueenCenter …
- 新字段(+138): CanBeReplacedByOtherNPCs, CommonMasterBossLifeReduction, HasGivenName, IsAPortraitDummy, ItemMoonlordCountdownTime, KickOutLookForHomeTimeout, LunarShieldPowerMax, MoonEventRequiredPointsPerWaveLookup, NaturalMoonlordCountdownTime, NetSectionCoordinates, PreventJojaColaDialog, RerollDryadText, SPAWN_SLOT_PROTECTION_TIME, ShimmeredTownNPCs, SupportsNPCTargets, TooWindyForButterflies, TypeName, WhoAmIToTargetingIndex, ZoneCorrupt, ZoneCrimson, ZoneDungeon, ZoneGlowshroom, ZoneGranite, ZoneGraveyard, ZoneHallow, ZoneJungle, ZoneLihzhardTemple, ZoneMarble, ZoneMeteor, ZoneOldOneArmy, ZonePeaceCandle, ZoneSandstorm, ZoneShadowCandle, ZoneSnow, ZoneTowerNebula, ZoneTowerSolar, ZoneTowerStardust, ZoneTowerVortex, ZoneWaterCandle, _deerclopsAttack1Frames, _deerclopsAttack2Frames, _deerclopsAttack3Frames, _nearbyBooks, active, bleeding, bloodButchered, brainOfGravity, brokenArmor, canDisplayBuffs, catchableNPCTempImmunityCounter, combatBookVolumeTwoWasUsed, dayTime, deeperThanRockLayer, deerclopsBoss, defLifeMax, defaultTarget, difficulty, downedDeerclops, dualDungeonsSpawnRules, electricEelCounter, empressRageMode, hardDungeon, hemorrhage, homelessDespawn, ignoreSafeWalls, inDualDungeon, inRemixStartingArea, invaders, isBeach, isOcean, isSpawningInWindDirection, kingSlimePointCache, kingSlimePointCacheSize, kingSlimePointCacheSizeMax, livingTree, lookForHomeTimeout, luck, markedByEelWhip, maximumAmountOfTimesLadyBugRainCanStack, mechQueen …
- 移除方法(-22): AI_120_HallowBoss_CanShootExtraAt, AI_120_HallowBoss_DeprecatedShot, AddIntoPlayersTownNPCSlots, DefaultHeadIndexToType, DropBossBags, GetAttackDamage_LerpBetweenFinalValuesFloat, GetAttackDamage_ScaledByStrength, GetEaterOfWorldsSegmentsCountByGamemode, NPCLootOld, NPCLoot_DropFood, ResetKillCount, ScaleStats_ApplyExpertTweaks, ScaleStats_ApplyGameMode, ScaleStats_ApplyMultiplayerStats, ScaleStats_Old, ScaleStats_UseStrengthMultiplier, SetDefaultsKeepPlayerInteraction, SpawnNPC_CheckToSpawnRockGolem, SpawnNPC_SpawnLavaBaitCritters, SpawnNPC_TryFindingProperGroundTileType, SpawnWithHigherTime, UpdateRGBPeriheralProbe
- 移除字段(-17): AFKTimeNeededForNoWorms, LunarShieldPowerExpert, killCount, markedByBlandWhip, markedByFireWhip, markedByMaceWhip, markedByRainbowWhip, markedBySwordWhip, markedByThornWhip, maxSpawns, netSkip, netUpdate2, spawnRangeX, spawnRangeY, spawnRate, streamPlayer, strengthMultiplier

### Terraria/ID/TileID.cs (+191 / -6)
- 新类型(+2): TileCutIgnore, Wiring
- 新方法(+2): PostSetupContent, Torch
- 新字段(+187): AbigailsFlower, AbigailsFlowerReplica, AllowsSaveCompressionBatching, AncientBlueBrick, AncientCobaltBrick, AncientCopperBrick, AncientGoldBrick, AncientGreenBrick, AncientHellstoneBrick, AncientMythrilBrick, AncientObsidianBrick, AncientPinkBrick, AncientSilverBrick, ArgonMossBlock, AshGrass, AshPlants, AshVines, AshWood, AstraBrick, AttractsStormLightning, BlockMergesWithMergeAllBlock, BlueMacawCage, BooksEcho, BoulderBlock, BoulderThatSpawnsPet, BouncyBoulder, BreaksToys, CRTMonolith, Campfires, CanGrowCrystalShards, CannonBall, ChlorophyteExtractinator, ClosedDoors, CobwebReplica, CorruptBiomeSight, CorruptCountCollection, CorruptJungleGrass, CorruptVines, CosmicEmberBrick, CountsAsChairTypes, CountsAsDoorTypes, CountsAsGemTree, CountsAsTableTypes, CountsAsTorchTypes, CountsAsWaterForCrafting, CrimsonBiomeSight, CrimsonCountCollection, CrimsonJungleGrass, CritterAnchor, CritterCageLidStyle, CryocoreBrick, DamagingSpikeBlock, DarkCelestialBrick, DeadCellsDisplayJar, DeadCellsPotionStation, DemonAltarReplica, DirtiestBlock, DisableSmartCursor, DisableSmartInteract, DoNotAdjustDrawPositionBasedOnTileWidth, DoesNotOpenCraftingMenuOnInteract, DontDrawTileSliced, DontDrawTileSlopes, DontMergeWithSnow, EasterBlock, EchoMonolith, FallenLogEcho, FallenStarBlock, Feywood, FlinxFurBlock, ForbiddenBlock, FrameImportantEchoCulling, Gems, Ghoulder, GlowTulip, GlowTulipReplica, GothicBrick, GrayCockatielCage, HallowBiomeSight, HallowCountCollection …
- 移除字段(-6): BlocksStairsAbove, InteractibleByNPCs, IsSkippedForNPCSpawningGroundTypeCheck, TouchDamageOther, TouchDamageSands, TouchDamageVines

### Terraria/ID/ProjectileID.cs (+181 / -4)
- 新方法(+1): SimpleLoop
- 新字段(+180): AbigailCounter, AbigailMinion, AcornSlingshotAcorn, AllowsContactDamageFromJellyfish, AntlionClaw, AxeFairyPet, Axearang, BerniePet, BirdDroppings, BladeOfGrass, BloodButcherer, BlueChickenPet, BluePhaseblade, BluePhasesaber, BoneWhip, BoulderPet, BoulderThatSpawnsPet, BouncyBoulder, BreaksFromToyBreaker, CanHitPastShimmer, CavelingGardener, CharacterPreviewAnimations, ChesterPet, CobWhip, CobWhipSpider, ConstellationStar, ConstellationWhip, CopiesOwnerAttackCDToLocalImmunityOnSpawn, CorruptWhip, CrimsonWhip, CultistIsResistantTo, CursedFlare, DaybreakExplosion, DeadCellsBarnacle, DeadCellsBarnacleShot, DeadCellsBarrel, DeadCellsFlint, DeadCellsFlintShot, DeadCellsFlintSlash, DeadCellsKillingDeckCard, DeadCellsMushroomBoiMinion, DeadCellsMushroomBoiMinionExplosion, DeadCellsSwarmBiter, DeerclopsIceSpike, DeerclopsPet, DeerclopsRangedProjectile, DirtSpray, DirtiestBlock, DontCancelChannelOnKill, EelWhip, Excalibur, FallingBlockDoesNotFallThroughPlatforms, Fertilizer, FishingBobber, FishingBobberGlowingArgon, FishingBobberGlowingKrypton, FishingBobberGlowingLava, FishingBobberGlowingRainbow, FishingBobberGlowingStar, FishingBobberGlowingViolet, FishingBobberGlowingXenon, FlaironFlail, FlinxMinion, FlowerWhip, FlowerWhipPetal, FreezeBomb, GasTrap, Ghoulder, GlommerPet, GreenPhaseblade, GreenPhasesaber, HiveFive, HorsemanPumpkin, HoundiusShootius, HoundiusShootiusFireball, InsanityShadowFriendly, InsanityShadowHostile, IsABombWithFuse, IsAGravestone, IsAPhaseblade …
- 移除字段(-4): CountsAsHoming, DontAttachHideToAlpha, MinionTargettingFeature, Web

### Terraria/Projectile.cs (+177 / -7)
- 新方法(+143): AI_003_Boomerang, AI_016_Bombs, AI_016_CanAcornPlant, AI_019_Spears_GetExtensionHitbox, AI_019_Spears_GetSpearOffsetRelativeToPlayer, AI_047_MagnetSphere, AI_047_MagnetSphere_TryAttacking, AI_048_GetStartPositionSettingDelay, AI_053_HandleSentryNPCTargeting, AI_066_TryInterceptingTarget, AI_067_FreakingPirates_HitIntention, AI_067_FreakingPirates_TryAssigningHelp, AI_067_FreakingPirates_TryJumpingToTarget, AI_099_1_Counterweights, AI_099_2_Yoyos, AI_105_SporeSac, AI_111_DryadsWard, AI_113_TargetSticker, AI_113_UpdateDrawLayer, AI_156_StartAttack, AI_185_LifeDrain, AI_186_PrincessWeapon, AI_187_ShadowHand, AI_187_ShadowHand_GetVariation, AI_188_LightsBane, AI_189_Volcano, AI_190_NightsEdge, AI_191_TrueNightsEdge, AI_192_GetJuminoFall, AI_192_JuminoAnimation, AI_193_Flamethrower, AI_194_HorsemanPumpkin, AI_195_JimsDrone, AI_196_Petal, AI_197_CeilingAndHoverTurret, AI_197_HandleTileCollision, AI_198_Flint, AI_198_Flint_EmitSpikes, AI_199_MeteorOre, AI_200_BirdDroppings, AI_201_ThrownMelee, AI_202_TorchGodHelper, AI_203_GetLightningColor, AI_203_StormLightning, AI_203_TooFar, AI_204_Digtoise, AI_205_RemoteControlCar, AI_AdjustPlayerItemRotationToFaceProjectile, AI_DisplayDoll, AI_DisplayDoll_Reset, ApplyBuffTo, ApplyStatsFromSource, ApplyWhipDebuffs, BombsHurtPlayers, BoulderExplosion, CheckSectionsInCaseOwnerIsWatching, Chester_IsAnyPlayerTrackingThisProjectile, CopyLocalNPCImmunityTo, CountEnemiesWhoAreImmuneToMeRightNow, CutTilesAt, Damage_CanDealDamage, Damage_EVP, Damage_GetHitbox, Damage_GetProjectileSpecificDamageMultiplier, Damage_PVE, Damage_PVE_Inner, Damage_PVP, Damage_StartIteratingNPC, Damage_StopIteratingNPC, Damage_TryUsingPowders, DecrementLocalImmuneTimeCounters, DefaultToDrillOrChainsaw, DefaultToFlail, DefaultToKite, DefaultToShortsword, DefaultToSpear, DefaultToSpray, DefaultToYoyo, DoLightningKillLambda, DoPalAppearEffect …
- 新字段(+34): MinimumWindStrengthToFlyKite, MinionSpawnInfo, Name, NetSectionCoordinates, StormLightningLiquidDamageRadius, WhipPointsForCollision, _availableFishTypesToShow, _context, _javelinsMax10, _javelinsMax6, _javelinsMax8, _lightningCollisionBounds, _lightningLastHitChainPos, _miningHelperPointsToSkip, _rainbowBoulderTargetsAny, _rainbowBoulderTargetsFar, active, appliesImmunityTimeOnSingleHits, armorPenetration, bannerIdToRespondTo, bonusCritChance, bonusTagDamage, correctSlopeCollision, drawLayer, hostileDamageScaling, isAPreviewDisplayDoll, isAPreviewDummy, kiteSoundPitch, netSyncSkippedForPlayer, reflected, stopsDealingDamageAfterPenetrateHits, tagEffectType, usesOwnerLight, usesOwnerMeleeHitCD
- 移除方法(-6): AI_016, AI_099_1, AI_099_2, CopyLocalNPCImmunityTimes, IsInteractible, ResetImmunity
- 移除字段(-1): _whipPointsForCollision

### Terraria/ID/BuffID.cs (+126 / -54)
- 新字段(+126): AbigailMinion, AddBuffTimeAdditivelyToCap, AmberMinecart, AmberMinecartLegacyUnused, AmethystMinecart, AmethystMinecartLegacyUnused, AxeFairyPet, BatMount, BeeMinecart, BeeMinecartLegacyUnused, BeetleMinecart, BeetleMinecartLegacyUnused, BerniePet, BiomeSight, BloodButcherer, BlueChickenPet, BoneWhipNPCDebuff, BoulderPet, BuffTextHandlers, BuffTimeIsExtendedByDeadCellsPotionStationBuff, BuffTimeIsExtendedWithGameDifficulty, CavelingGardener, ChesterPet, CobWhipNPCDebuff, CobWhipPlayerBuff, CoffinMinecart, CoffinMinecartLegacyUnused, ConstellationWhipNPCDebuff, CoolWhipNPCDebuff, CorruptWhipNPCDebuff, CrimsonWhipNPCDebuff, DeadCellsMushroomBoiMinion, DeadCellsPotionStation, DeadCellsSwarmBiter, DeerclopsPet, DesertMinecart, DesertMinecartLegacyUnused, DiamondMinecart, DiamondMinecartLegacyUnused, DiggingMoleMinecart, DiggingMoleMinecartLegacyUnused, DirtiestBlock, DualSlimePet, EelWhipNPCDebuff, EmeraldMinecart, EmeraldMinecartLegacyUnused, FartMinecart, FartMinecartLegacyUnused, FishMinecart, FishMinecartLegacyUnused, FlinxMinion, FlowerWhipNPCDebuff, FlowerWhipNPCDebuffProc, Frostburn2, GlommerPet, HeartyMeal, HellMinecart, HellMinecartLegacyUnused, Hemorrhage, Hunger, IsAnNPCWhipDebuff, IsFedState, JunimoPet, Kite, LadybugMinecart, LadybugMinecartLegacyUnused, MeowmereMinecart, MeowmereMinecartLegacyUnused, MeteorWhipNPCDebuff, MeteorWhipNPCDebuffProc, Minecart, MinecartLegacyUnused, MinecartMech, MinecartMechLegacyUnused, MinecartWood, MinecartWoodLegacyUnused, MoonLordWhipNPCDebuff, MoonLordWhipNPCDebuffProc, MountType, NeutralHunger …
- 移除类型(-1): BuffMountData
- 移除字段(-53): AmberMinecartLeft, AmberMinecartRight, AmethystMinecartLeft, AmethystMinecartRight, BasicMountData, BeeMinecartLeft, BeeMinecartRight, BeetleMinecartLeft, BeetleMinecartRight, CoffinMinecartLeft, CoffinMinecartRight, DesertMinecartLeft, DesertMinecartRight, DiamondMinecartLeft, DiamondMinecartRight, DiggingMoleMinecartLeft, DiggingMoleMinecartRight, EmeraldMinecartLeft, EmeraldMinecartRight, FishMinecartLeft, FishMinecartRight, HellMinecartLeft, HellMinecartRight, LadybugMinecartLeft, LadybugMinecartRight, MeowmereMinecartLeft, MeowmereMinecartRight, MinecartLeft, MinecartLeftMech, MinecartLeftWood

### Terraria/ID/GoreID.cs (+177 / -0)
- 新字段(+177): ArmsDealerShimmeredArm, ArmsDealerShimmeredHead, ArmsDealerShimmeredLeg, BestiaryGirlShimmeredArm, BestiaryGirlShimmeredArmTransformed, BestiaryGirlShimmeredHead, BestiaryGirlShimmeredHeadTransformed, BestiaryGirlShimmeredLeg, BestiaryGirlShimmeredTail, BlueMacaw1, BlueMacaw2, ClothierShimmeredArm, ClothierShimmeredHead, ClothierShimmeredLeg, Cloud1, Cloud2, Cloud3, CyborgShimmeredArm, CyborgShimmeredHead, CyborgShimmeredLeg, DeerclopsAntler, DeerclopsArm, DeerclopsBody, DeerclopsHead, DeerclopsLeg, DemolitionistShimmeredArm, DemolitionistShimmeredHead, DemolitionistShimmeredHeadParty, DemolitionistShimmeredLeg, DryadShimmeredArm, DryadShimmeredHead, DryadShimmeredLeg, DyeTraderShimmeredArm, DyeTraderShimmeredHead, DyeTraderShimmeredHeadParty, DyeTraderShimmeredLeg, FartCloud1, FartCloud2, FartCloud3, FireImpArm, FireImpHead, FireImpLeg, GoblinTinkererShimmeredArm, GoblinTinkererShimmeredHead, GoblinTinkererShimmeredLeg, GolferShimmeredArm, GolferShimmeredHead, GolferShimmeredLeg, GrayCockatiel1, GrayCockatiel2, GuideShimmeredArm, GuideShimmeredHead, GuideShimmeredLeg, HornetBody, HornetHead, HornetHeadHoney, HornetHeadSpikey, IsDrip, MechanicShimmeredArm, MechanicShimmeredHead, MechanicShimmeredLeg, MerchantShimmeredArm, MerchantShimmeredHead, MerchantShimmeredHeadParty, MerchantShimmeredLeg, MossHornetBody, MossHornetHead, MossZombieChunk1, MossZombieChunk2, MossZombieHead, NurseShimmeredArm, NurseShimmeredHead, NurseShimmeredHeadParty, NurseShimmeredLeg, OldManShimmeredArm, OldManShimmeredHead, OldManShimmeredLeg, OrcaChunk1, OrcaChunk2, OrcaHead …

### Terraria/ID/ArmorIDs.cs (+165 / -2)
- 新类型(+1): Beard
- 新字段(+164): AltFaceHead, AlwaysAnimated, AshWoodBreastplate, AshWoodGreaves, AshWoodHelmet, BlueBikiniBody, BlueBikiniLegs, BoneGlove, BoneHelm, CanDrawOnVelociraptorMount, CapricornChestplate, CapricornLegs, CapricornMask, CapricornTail, ChickenBonesBody, ChickenBonesHead, ChickenBonesLegs, ChickenBonesRobe, ChickenBonesRobeExtension, ChickenBonesRobeExtensionBack, ChickenBonesWings, ChippysBody, ChippysHead, ChippysHeadband, ChippysLegs, ChippysWings, ChlorophyteVisor, DeadCellsBeheadedBody, DeadCellsBeheadedHead, DeadCellsBeheadedLegsFemale, DeadCellsBeheadedLegsMale, DeerclopsMask, DisableBeltAccDraw, DisableHandOnAndOffAccDraw, DizzyHat, DoesNotSupportSittingDraw, DontDrawIfWearingAScarfOrCape, DrawFaceMaskUnderHeadLayer, DrawInBackpackLayer, DrawInFaceFlowerLayer, DrawInFaceHeadLayer, DrawInFaceMaskLayer, DrawInFaceUnderHairLayer, DrawInFrontOfBackArmLayer, DrawInTailLayer, DrawsInNeckLayerRegardlessOfPlayerFrame, Eyebrella, FlinxFurCoat, FlinxFurCoatExtension, FloretProtecterChestplate, FloretProtectorChestplate, FloretProtectorHelmet, FloretProtectorLegs, GarlandHat, GiFemaleExtension, GiMaleExtension, GlassSlipperFemale, GlassSlipperMale, GoblorcEars, GraySwimshorts, GreenSwimshorts, GypsyRobeFemaleExtension, GypsyRobeMaleExtension, HallowedCrown, HandOfCreation, HeroicisBody, HeroicisHead, HeroicisLegs, HeroicisWings, HidesCompositeShoulders, HidesHead, HidesShouldersAsCoat, HorseshoeBundle, IncompatibleWithFrogLeg, IsABelt, IsACape, IsARollerSkate, IsAScarf, JimsCap, JimsDroneVisor …
- 移除字段(-2): Merfolk, UnusedID

### Terraria/TimeLogger.cs (+135 / -31)
- 新类型(+3): DataSeries, FormatPool, StartTimestamp
- 新方法(+22): ABTest, Add, AddTime, Draw, DrawDelta, DrawEntry, DrawEntryData, DrawExtras, DrawString, DrawTimes, DrawValue, Format, FormatTicks, LogAdd, NewCounterEntry, NewEntry, OnNextFrame, PerformanceColor, Quantile, Reset, StartNextFrame, ToggleLogging
- 新字段(+110): ABTestMode, ABTestName, ClothingRacks, ColumnSpacing, DataSeriesHeaders, DrawBackgroundWaterTiles, DrawBlackTiles, DrawFPSGraph, DrawFullscreenMap, DrawNonSolidTiles, DrawOldUndergroundBackground, DrawSolidTiles, DrawTimeLogger, DrawUndergroundBackground, DrawWallTiles, DrawWaterTiles, DrawWireTiles, DrawnEntryNumber, Dust, Elapsed, ElapsedTicks, Filters, FindPaintedTiles, FindingWaterfalls, FlushNonSolidTiles, FlushSolidTiles, FlushWallTiles, FrameCount, GCPause, Gore, HasData, Interface, Items, LeashedEntities, Lighting, LightingByPass, LightingInit, LiquidBackgroundDrawCalls, LiquidDrawCalls, Map, MapChanges, MapSectionUpdate, MapUpdate, MenuDrawTime, NPCs, Nature, NonSolidDrawCalls, Overlays, Particles, PlayerChat, Players, PrepareRequests, Projectiles, Rain, RenderBackgroundLiquid, RenderBlacksAndWalls, RenderLiquid, RenderNonSolidTiles, RenderSolidTiles, RenderUndergroundBackground, SectionFraming, SectionRefresh, SkyBackground, SolidDrawCalls, SplashDrawTime, SunMoonStars, SunVisibility, SurfaceBackground, TableWidth, TileExtras, TotalDraw, TotalDrawAndUpdate, TotalDrawByRenderCount, TotalDrawRenderNow, WallDrawCalls, Waterfalls, _AssignedCPUFormat, _PinnedCPUFormat, _entriesToDraw, _expectedCPUFormat …
- 移除方法(-19): DetailedDrawReset, DetailedDrawTime, DrawTime, GetDetailedDrawTime, GetDetailedDrawTotal, GetDrawTime, GetDrawTotal, GetLightingTime, GetLightingTotal, GetRenderMax, GetRenderTime, Initialize, LightingTime, MapDrawTime, MenuDrawTime, NewDrawFrame, RenderTime, SplashDrawTime, UpdateTime
- 移除字段(-12): detailedDrawTimer, detailedDrawTimes, drawTimes, lastDetailedDrawTime, lightingTimes, logText, maxTimeDelay, renderTimes, resetMaxTime, time, timeMax, usedLastDraw

### Terraria/Audio/LegacySoundPlayer.cs (+76 / -71)
- 新方法(+3): CreateInstance, DoesSoundScaleWithAmbientVolume, Reload
- 新字段(+73): SoundAttenuationDistance, SoundCamera, SoundChat, SoundCoin, SoundCoins, SoundDig, SoundDoorClosed, SoundDoorOpen, SoundDoubleJump, SoundDrip, SoundDrown, SoundFemaleHit, SoundGrab, SoundGrass, SoundInstanceCamera, SoundInstanceChat, SoundInstanceCoin, SoundInstanceCoins, SoundInstanceDig, SoundInstanceDoorClosed, SoundInstanceDoorOpen, SoundInstanceDoubleJump, SoundInstanceDrip, SoundInstanceDrown, SoundInstanceFemaleHit, SoundInstanceGrab, SoundInstanceGrass, SoundInstanceItem, SoundInstanceLiquid, SoundInstanceMaxMana, SoundInstanceMech, SoundInstanceMenuClose, SoundInstanceMenuOpen, SoundInstanceMenuTick, SoundInstanceMoonlordCry, SoundInstanceNpcHit, SoundInstanceNpcKilled, SoundInstancePixie, SoundInstancePlayerHit, SoundInstancePlayerKilled, SoundInstanceResearch, SoundInstanceRoar, SoundInstanceRun, SoundInstanceShatter, SoundInstanceSplash, SoundInstanceThunder, SoundInstanceTink, SoundInstanceUnlock, SoundInstanceZombie, SoundItem, SoundLiquid, SoundMaxMana, SoundMech, SoundMenuClose, SoundMenuOpen, SoundMenuTick, SoundNpcHit, SoundNpcKilled, SoundPixie, SoundPlayerHit, SoundPlayerKilled, SoundResearch, SoundRoar, SoundRun, SoundShatter, SoundSplash, SoundThunder, SoundTink, SoundUnlock, SoundZombie, TrackableSoundInstances, TrackableSounds, _trackedInstances
- 移除字段(-71): _soundCamera, _soundChat, _soundCoin, _soundCoins, _soundDig, _soundDoorClosed, _soundDoorOpen, _soundDoubleJump, _soundDrip, _soundDrown, _soundFemaleHit, _soundGrab, _soundGrass, _soundInstanceCamera, _soundInstanceChat, _soundInstanceCoin, _soundInstanceCoins, _soundInstanceDig, _soundInstanceDoorClosed, _soundInstanceDoorOpen, _soundInstanceDoubleJump, _soundInstanceDrip, _soundInstanceDrown, _soundInstanceFemaleHit, _soundInstanceGrab, _soundInstanceGrass, _soundInstanceItem, _soundInstanceLiquid, _soundInstanceMaxMana, _soundInstanceMech

### Terraria/ID/SoundID.cs (+115 / -1)
- 新字段(+115): AbigailAttack, AbigailCry, AbigailSummon, AbigailUpgrade, BalloonDeath, BalloonHurt, BellHurt, BestReforge, BombFuse, CatHurt, ChesterClose, ChesterOpen, ChickenHurt, ChickenHurtRare, Clown, Cockatiel, CrowHurt, DSTFemaleHurt, DSTMaleHurt, DeadCellsBarrelLauncherExplode, DeadCellsBarrelLauncherFire, DeadCellsFlintCharge, DeadCellsFlintRelease, DeadCellsFlintWave, DeadCellsMushroomExplode, DeadCellsMushroomJump, DeadCellsMushroomLand, DeadCellsMushroomSummon, DeerclopsDeath, DeerclopsHit, DeerclopsIceAttack, DeerclopsRubbleAttack, DeerclopsScream, DeerclopsStep, DefaultPlayerHurt, DogHurt, EOWDiggin, FairyHurt, FishSplash, FoxparksFlame, FrogHurt, GlommerBounce, GoatHurt, GoblinHurt, GuitarBm, Hungry, InstantThunder, Item173, Item174, Item175, Item176, Item177, Item178, Item179, Item180, Item181, Item182, Item183, Item184, Item185, Item186, Item187, Item188, Item189, Item190, Item191, Item192, Item193, Item194, Item195, Item196, Item197, Item198, Item199, JimsDrone, LeafBlower, LucyTheAxeTalk, Macaw, MenuAccept, MeteorShower …
- 移除字段(-1): GuitarF

### Terraria/ID/NPCID.cs (+109 / -2)
- 新类型(+6): BasicNPCPortrait, Entry, LocalBuffID, NPCPortraitProvider, NPCPortraitSelector, NPCVariantChecker
- 新方法(+10): BasicPortrait, Default, Fits, GetDrawData, GetFirstValidatedEntry, PrioritizedPortrait, SelectionCondition, ShimmeredPortraitCondition, VariantPortraitCondition, With
- 新字段(+93): BetsysCurse, BirdThatCanPoop, Bleeding, BloodButcherer, BlueMacaw, BoneJavelin, BoundTownSlimeOld, BoundTownSlimePurple, BoundTownSlimeYellow, CanBeHurtByBees, CanConvertIntoCopperSlimeTownNPC, CanHitPastShimmer, CannotSpawnInSlot0, ChaosBallTim, Condition, Confused, ConveyorBeltCollision, CritterThatCanTurnOnPlayers, CursedInferno, Daybreak, DebuffImmunitySets, Deerclops, DontDropDungeonKeysOrSouls, FrameX, FrameY, Frostburn, Frostburn2, GoldenSlime, GrayCockatiel, Hemorrhage, HorizontalFrames, HunterPotionFriendlyOverride, Ichor, IsGoldCritter, IsTownSlime, LibrarianSkeleton, MossZombie, NPCPortraits, NPCPortraitsCloseUpOffsets, NPCPortraitsFullBodyRetroOffsets, Oiled, OnFire, OnFire3, Orca, OwlMimic, PaddingX, PaddingY, PalworldCattivaDistressed, PalworldFoxsparksDistressed, Poisoned, Portrait, Princess, Pufferfish, ReflectStarShotsInForTheWorthy, ScarletMacaw, SearchSpawnSlotsInReverse, ShadowFlame, ShimmerImmunity, ShimmerSlime, ShimmerTownTransform, ShimmerTransformToItem, ShimmerTransformToNPC, Shimmerfly, ShouldBeCountedAsBossForBestiary, ShouldBeCountedAsBossForRainbowBoulders, SkipUpdateInUnsyncedTiles, SlimeCanContainItems, SpawnOnPlayerCanSpawnInMidairOnSkyblock, StatueMimic, Stinkbug, TentacleSpike, TexturePath, TorchGod, Toucan, TownSlimeBlue, TownSlimeCopper, TownSlimeGreen, TownSlimeOld, TownSlimePurple, TownSlimeRainbow …
- 移除字段(-2): ShouldBeCountedAsBoss, UsesNewTargetting

### Terraria/UI/ItemSlot.cs (+101 / -9)
- 新类型(+4): AlternateClickAction, ItemDisplayKey, ItemTransferInfo, PulseEffect
- 新方法(+48): AddCooldown, AddPulseEffect, AfterItemSwap, AnnounceTransfer, CanBulkBuy, CanDoSimulatedClickAction, CanEquipAccessoryInSlot, CanEquipAccessoryInVanitySlot, CanEquipBothAccessories, CanExecuteCommand, CanSwapEquip, DisplayTransfer_GetItem, DisplayTransfer_OneWay, DisplayTransfer_TwoWay, DrawItemIcon, DrawItem_GetColorAndScale, Equals, EstimateDisplayStack, GetAlternateClickAction, GetBulkBuyAmount, GetBulkCraftAmount, GetColorByLoadout, GetCraftSlotGamepadInstructions, GetDimSlotForMouseItem, GetGamepadPointForSlot, GetHashCode, GetLoadoutColor, GetQuickCraftGamepadInstructions, GetSellOrTrash, GetTimeToAnimate, HasIncompatibleAccessory, HasSameItemInSlot, HoverOverrideClick, IndicateBlockedSlot, ItemTransferEvent, PrepareForChest, RecordLoadoutChange, ResetInventoryStateCounters, SetGlowForChest, ShiftHueByLoadout, ShouldHighlightSlotForMouseItem, SwapVanityEquip, TryDisplayTransfer, TryGetSlotColor, TryItemSwap, TryOpenContainer, TryOpenContainer_GrantItems, TryResearchingItem
- 新字段(+49): BannerClaiming, Context, ControlInUse, CreativeInfiniteLocked, DisableQuickTrash, DisplayDollMount, DisplayDollWeapon, DrawSelectionHighlightForGridSlot, EffectDuration, EquipMiscDye, FromContenxt, HotbarItemSmartSelected, InWorld, InWorldDisplay, IsActive, ItemType, LoadoutSlotColors, NewCraftingUICraftSlot, NewCraftingUIMaterial, NewCraftingUIRecipe, NumPulses, OnItemTransferred, OverdrawGlow, OverdrawGlowColorMultiplier, OverdrawGlowSize, Sell, Slot, ToContext, TransferAmount, TransferFromChest, TransferToBackpack, TransferToChest, Trash, Unequip, VoidItem, _dirtyHack, _lastTimeForVisualEffectsThatLoadoutWasChanged, _nextTickDrawAvailable, canQuickDropAt, color, cursorOverride, dyeSwapCounter, forceClearGlowsOnChest, gamepadHintText, itemInSlot, operator, playerSlotPulseEffects, slotRef, time
- 移除方法(-7): AccCheck, Equippable, GetOverrideInstructions, LeftClick_SellOrTrash, RightClick_FindSpecialActions, SellOrTrash, isEquipLocked
- 移除字段(-2): accSlotToSwapTo, dyeSlotCount

### Terraria/Item.cs (+69 / -33)
- 新方法(+44): BestPrefixValue, CanBeEquipped, CanHavePrefixes, CanPassivelyStackInWorld, CanRollPrefix, CanShimmer, CanStack, ChangeItemType, DefaultToBanner, DefaultToBody, DefaultToBomb, DefaultToInfoAccessory, DefaultToKite, DefaultToLegs, DefaultToMinecart, DefaultToMonolith, DefaultToPlaceableTile, DefaultToPlaceableWall, DefaultToSeaShell, DefaultToSolution, DefaultToVoiceOverrideAccessory, FindDecraftAmount, FixAgainstExploit, GetFlexibleTileWand, GetHoverName, GetItemSource_Misc, GetNPCSource_FromThis, GetPhaseColor, GetPhaseColorDirect, GetPopupRarityColor, GetRandomVoiceItem, GetRollablePrefixes, GetShimmerEquivalentType, GetVisualCritChance, IsConsideredSameItemAsType, IsNetStateDifferent, MakeUsableWithChlorophyteExtractinator, OnCreated, OnlyNeedOneInInventory, ResetPrefix, RollAPrefix, ToWorldItem, TryAddStack, TryGetPrefixStatMultipliersForItem
- 新字段(+25): CommonMaxStack, Name, OriginalDamage, OriginalDefense, OriginalRarity, PickupReplacementTime, SlotsRemainingBeforeEmergencyStackingInMultiplayer, _phaseColors, active, armorPenetration, beardSlot, bonusTagDamage, chlorophyteExtractinatorConsumable, eggnogDelay, foodHeight, foodWidth, hasVanityEffects, height, mushroomDelay, paintCoating, shootsEveryUse, tooltipSlot, useSoundPitch, voiceSlot, width
- 移除方法(-21): BannerToItem, BannerToNPC, CanCombineStackInWorld, CheckLavaDeath, CombineWithNearbyItems, DefaultToMount, DefaultToPlacableTile, DefaultToPlacableWall, DefaultToSeaShelll, DefaultTokite, DespawnIfMeetingConditions, FindOwner, GetPickedUpByMonsters, IsTheSameAs, MoveInWorld, NPCtoBanner, TryCombiningIntoNearbyItems, UpdateItem, UpdateItem_VisualEffects, checkMat, getRect
- 移除字段(-12): beingGrabbed, canBePlacedInVanityRegardlessOfConditions, instanced, keepTime, netID, noGrabDelay, numberOfNewItems, ownIgnore, ownTime, playerIndexTheItemIsReservedFor, timeSinceItemSpawned, timeSinceTheItemHasBeenReservedForSomeone

### Terraria/ID/ExtrasID.cs (+92 / -0)
- 新字段(+92): AcornSlingshotHeldItem, AuroraNoise, AuroraShape, BatMountBody, ChesterOutline, Chillet, ChilletIgnis, ChippysHeadbandTassels, CreditsRollNPC_CyborgUnderRepair, CreditsRollNPC_DryadTurningToTree, CreditsRollNPC_SkeletonMerchantScavenging, CreditsRollNPC_SteampunkerRepairing, CreditsRollObject_Balloons, CreditsRollObject_BonePile, CreditsRollObject_Campfire, CreditsRollObject_FinaleScene, CreditsRollObject_Fireplace, CreditsRollObject_MiniPortal, CreditsRollScene_CampfireBeach, CreditsRollScene_ChristmasTree, CreditsRollScene_DryadInForest, CreditsRollScene_ForestBar, CreditsRollScene_GolfCourse, CreditsRollScene_GuideDoorClosed, CreditsRollScene_GuideDoorOpened, CreditsRollScene_Hallow, CreditsRollScene_Jungle, CreditsRollScene_Mask, CreditsRollScene_MerchantsGuild, CreditsRollScene_SkeletonMerchantCave, CreditsRollScene_SteampunkerWorkshop, CreditsRollScene_SteampunkerWorkshop2, CreditsRollScene_TavernkeepTavern, CreditsRollScene_TinkererWorkshop, CreditsRollScene_TruffleHouse, DeadCellsBarrelExplosion, DeadCellsBeheadedHead, DeerclopsEye, FakeButterfly, FartMinecart, FloretProtectorFrontTube, FoxsparksHeld, GenericCircle, GuideShimmerFrontal, HeroicisHeadMount, HouseCheckBlock, HouseCheckDot, HouseCheckHammer, HouseCheckMarkerChair, HouseCheckMarkerDoor, HouseCheckMarkerLight, HouseCheckMarkerTable, JimCloakShoulder, JimsBreastplateMetal, JimsDroneRadio, JimsHelmetMetal, JimsLeggingsMetal, LibrarianSkeletonCircle, LightDisc, LightningShape, Loadouts, LunaHeadEars, MoonlordWhipEye, PixieMountBackLayer, PixieMountFrontLayer, PlaguebringerFlame, PotionOfReturnGateInOutline, PylonOffscreenIndicator, RainbowBoulderPetAura, RatMountBody, RoamingFly, RubbleMakerIndicator, ShimmeredMechanicWrench, ShimmerflyinaBottle, ShockIcon, StardewValleyPortal, StardewValleyPortalAnimation, StardewValleyPortalMask, SunSunglasses, SuperCartDisabled …

### Terraria/GameContent/Drawing/ParticleOrchestrator.cs (+91 / -0)
- 新方法(+80): BroadcastOrRequestParticleSpawn, BroadcastParticleSpawn, CopperSlimeEffect, ElderSlimeEffect, GetNewBloodyExplosionParticle, GetNewFadingPlayerShaderParticle, GetNewFakeFishParticle, GetNewGasParticle, GetNewItemTransferParticle, GetNewItemTransferParticle_ScreenSpace, GetNewNatureFlyParticle, GetNewPooFlyParticle, GetNewShockIconParticle, GetNewStormLightningParticle, MagnetFakeFish, NerdySlimeEffect, PingFakeFish, PushAwayFakeFish, RepelAt, SpawnHelper_SpawnInLine, SpawnHelper_SpawnSingleLineDust, SpawnLightningExplosionDust, Spawn_BestReforge, Spawn_BlueLightningSmall, Spawn_BlueLightningSmallLong, Spawn_CattivaHit, Spawn_ClassyCane, Spawn_DeadCellsBarnacleShotFiring, Spawn_DeadCellsBarrelExplosion, Spawn_DeadCellsDownDashExplosion, Spawn_DeadCellsFlint, Spawn_DeadCellsHeadEffect, Spawn_DeadCellsMushroomBoiExplosion, Spawn_DeadCellsMushroomBoiTargetFound, Spawn_Digestion, Spawn_Excalibur, Spawn_FakeFish, Spawn_FlyMeal, Spawn_GasTrap, Spawn_HeatRay, Spawn_HeroicisSetSpawnSound, Spawn_InScreenDungeonSpawn, Spawn_ItemTransfer, Spawn_LakeSparkle, Spawn_LeafCrystalPassive, Spawn_LeafCrystalShot, Spawn_LoadOutChange, Spawn_MagnetSphereBolt, Spawn_MoonLordWhip, Spawn_MoonLordWhipEye, Spawn_NatureFly, Spawn_NightsEdge, Spawn_PaladinsHammer, Spawn_PaladinsHammerShockwave, Spawn_PaladinsShieldHit, Spawn_PetExchange, Spawn_PlayerVoiceOverrideSound, Spawn_PooFly, Spawn_PrincessWeapon, Spawn_RainbowBoulder1, Spawn_RainbowBoulder2, Spawn_RainbowBoulder3, Spawn_RainbowBoulder4, Spawn_ShadowOrbExplosion, Spawn_Shadowbeam, Spawn_ShimmerArrow, Spawn_ShimmerBlock, Spawn_ShimmerTownNPC, Spawn_ShimmerTownNPCSend, Spawn_SilverBulletSparkle, Spawn_SlapHand, Spawn_StormLightning, Spawn_StormLightningWindup, Spawn_TerraBlade, Spawn_TownSlimeTransform, Spawn_TrueExcalibur, Spawn_TrueNightsEdge, Spawn_UFOLaser, Spawn_VampireOnFire, Spawn_WaffleIron
- 新字段(+11): ScreenItemParticles, StormLightningParticles, _fakeFish, _mushBoiExplosionSounds, _natureFlies, _poolBloodyExplosion, _poolFadingPlayerShader, _poolFlies, _poolGas, _poolItemTransfer, _poolShockIcon

### Terraria/Recipe.cs (+75 / -16)
- 新类型(+1): RequiredItemEntry
- 新方法(+59): AddAetheriumFurniture, AddAshWoodFurnitureArmorAndItems, AddBalloonFurniture, AddBoulderFurniture, AddCloudFurniture, AddCoralFurniture, AddCrimtaneFurniture, AddCritterStatueRecipe, AddCustomShimmerResult, AddDemoniteFurniture, AddEasterFurniture, AddFakeCountsForItemGroups, AddFallenStarFurniture, AddFeywoodFurniture, AddFlinxFurFurniture, AddForbiddenFurniture, AddGothicFurniture, AddHallowedFurniture, AddHarpyFurniture, AddJellyfishFurniture, AddLibrarianFurniture, AddMissing, AddMoonplateFurniture, AddOfficeFurniture, AddPineFurniture, AddSnowFurniture, AddSpikeFurniture, AddStandardFurnitureSetRecipes, AddStoneFurniture, AddTileCountsAs, AddToAvailableRecipes, AddWaterFurniture, ClearAvailableRecipes, CollectGuideRecipes, CollectItems, CollectItemsFromChests, CollectItemsToCraftWithFrom, CollectedEnoughItemsToCraft, ConsumeOwnedItem, ContainsIngredient, CreateRequiredItemQuickLookups, GetAvailableItemCount, GetIngredientCraftingDiscount, GetIngredientsForOneCraft, GetRequiredTileName, HowManyTimesCanRecipeBeCrafted, Matches, PlayerMeetsEnvironmentConditions, RequiredItemEntry, SetIngredients, SetupTileInheritance, SubtractOwnedItem, TileUsedInRecipeInherited, ToString, TryRefocusingRecipe, UpdateInheritedTilesUsedInRecipes, UpdateItemVariants, UpdateRecipeList, UpdateWhichItemsAreCrafted
- 新字段(+15): IsRecipeGroup, RecipeGroup, TileCountsAs, TileUsedInRecipes, _ownedItems, _recipeChests, corruption, crimson, customShimmerResults, itemIdOrRecipeGroup, needMechdusa, needTorchGodsFavor, notDecraftable, requiredItemQuickLookup, stack
- 移除方法(-10): AcceptedByItemGroups, Create, FindRecipes, GetThroughDelayedFindRecipes, SetIngridients, useFragment, useIronBar, usePressurePlate, useSand, useWood
- 移除字段(-6): _hasDelayedFindRecipes, anyFragment, anyIronBar, anyPressurePlate, anySand, anyWood

### Terraria/Utils.cs (+83 / -1)
- 新类型(+2): ChaseResults, RandomTeleportationAttemptSettings
- 新方法(+58): BottomLeftDouble, BottomRightDouble, BounceEaseOut, CheckForGoodTeleportationSpot, CheckForGoodTeleportationSpot_CheckNoInvalidTiles, Clamp, ClampedInWorld, ConstrainedToPointInRectangle, DoesFitInCone, DoubleIntersect, DrawNotificationIcon, DrawSelectedCraftingBarIndicator, EaseInCirc, EaseOutBounce, EaseOutCirc, FactorAcceleration, FloodFillTile, GetChaseResults, GetDayTimeAs24FloatStartingFromMidnight, GetDayTimeAsDirectionIn24HClock, GetJumpForce, GetJumpTimeToApex, GetPortraitMovement, Including, IntersectsConeFastInaccurate, IntersectsConeSlowMoreAccurate, JustBecameTrue, Lerp, LineRectangleDistance, LineSegmentsIntersect, NextFromRectangle, NextVector2DCircular, NextVector2DCircularEdge, NextVector2DFromRectangle, NextVector2DSquare, NextVector2DUnit, ParseCommandPrefix, PressingAlt, RandomVector2D, Read7BitEncodedInt, RotateUntil, SWTicksToTimeSpan, ScaledBy, ScreenToWorldPosition, ShiftBlueToCyanTheme, ShiftHue, SolveQuadratic, TimeSpanToSWTicks, ToRotationVector2D, ToVector2D, ToVector3, TopLeftDouble, TopRightDouble, TrimLastCharacter, TrimUserString, TryOperateInLock, WordwrapStringLegacy, Write7BitEncodedInt
- 新字段(+23): ChaserVelocity, InterceptionHappens, InterceptionPosition, InterceptionTime, MaxFloatInt, _floodFillBitset, _floodFillQueue1, _floodFillQueue2, allowSolidTopFloor, attemptsBeforeGivingUp, avoidAnyLiquid, avoidHurtTiles, avoidLava, avoidWalls, maximumFallDistanceFromOrignalPoint, mostlySolidFloor, specializedConditions, strictRange, teleporteeGravityDirection, teleporteeSize, teleporteeVelocity, tilesToAvoid, tilesToAvoidRange
- 移除方法(-1): PlotTileArea

### Terraria/SceneMetrics.cs (+75 / -8)
- 新方法(+10): AddPlayerEffects, AggregateTileCounts, AnyNPCs, CalculateZones, Scan, ScanNPCPositions, ScanOnScreenTiles, ScanTiles, UpdateOreFinder, WithinRangeOfNPC
- 新字段(+65): AssumedConstantScreenSize, BelowSurface, BestOreType, CanPlayCreditsRoll, CloseEnoughToDD2LanePortal, CloseEnoughToNebulaTower, CloseEnoughToSolarTower, CloseEnoughToStardustTower, CloseEnoughToVortexTower, ClosestNPCPosition, DesertTileNormalThreshold, DesertTileSkyblockThreshold, DungeonTileThreshold, EnoughTilesForCorruption, EnoughTilesForCrimson, EnoughTilesForDesert, EnoughTilesForDungeon, EnoughTilesForGlowingMushroom, EnoughTilesForGraveyard, EnoughTilesForHallow, EnoughTilesForJungle, EnoughTilesForMeteor, EnoughTilesForShimmer, EnoughTilesForSnow, InTorchGodMinigame, NPCEventZoneRadius, ShimmerTileThreshold, SnowTileNormalThreshold, SnowTileSkyblockThreshold, SurfaceAtmospherics, TownNPCRectSize, UndergroundForShimmering, ZoneBeach, ZoneCorrupt, ZoneCrimson, ZoneDesert, ZoneDirtLayerHeight, ZoneDungeon, ZoneGemCave, ZoneGlowshroom, ZoneGranite, ZoneGraveyard, ZoneHallow, ZoneHive, ZoneJungle, ZoneLihzhardTemple, ZoneMarble, ZoneMeteor, ZoneOverworldHeight, ZonePeaceCandle, ZoneRain, ZoneRockLayerHeight, ZoneSandstorm, ZoneScanPadding, ZoneScanSize, ZoneShadowCandle, ZoneShimmer, ZoneSkyHeight, ZoneSnow, ZoneUndergroundDesert, ZoneUnderworldHeight, ZoneWaterCandle, _bestOreDistSq, _dummyPlayer, _liquidCounts
- 移除方法(-3): ExportTileCountsToMain, ScanAndExportToMain, UpdateOreFinderData
- 移除字段(-5): DesertTileThreshold, SnowTileThreshold, _oreFinderTileLocations, _world, bestOre

### Terraria/ID/GlowMaskID.cs (+78 / -0)
- 新字段(+78): ArgonMossBlock, ArgonMossBlockWall, AshGrass, AshVines, BatMountBody, CRTMonolith, CapricornLegs, CapricornMask, CapricornTail, ChickenBonesHead, ChickenBonesRobeLeg, ChickenBonesRobeTorso, ChickenBonesWings, CyborgShimmered, CyborgShimmeredParty, DeadCellsBarrel, DeadCellsBeheadedHead, DeadCellsFlint, DeadCellsMushroomBoi, DeadCellsPotionStation, EchoMonolith, EelWhip, FireImp, FishingBobberGlowingArgon, FishingBobberGlowingKrypton, FishingBobberGlowingLava, FishingBobberGlowingRainbow, FishingBobberGlowingStar, FishingBobberGlowingViolet, FishingBobberGlowingXenon, FloretProtectorFrontTube, FloretProtectorHelmet, GlowTulip, KazzymodusChestpiece, KazzymodusHood, KryptonMossBlock, KryptonMossBlockWall, LavaCloud, LavaMossBlock, LavaMossBlockWall, LightsBane, LunasHead, Magiluminescence, Moondial, NoirMonolith, PalworldDigtoise, RainbowMoss, RainbowMossBlock, RainbowMossBlockWall, RainbowMossBrick, RainbowPhaseblade, RainbowPhasesaber, RetroMonolith, RoninHat, ShimmerBlock, ShimmerBrick, ShimmerCloakBack, ShimmerCloakFront, ShimmerMonolith, ShimmerMonolithOrb, Shimmerfall, ShimmerfallWall, Sundial, TVHeadMask, TimelessTravelerBottom, TimelessTravelerHood, TreeAsh, TreeAshBranches, TreeAshTop, TrueCopperShortsword, TruffleShimmered, UpgradedMiningHead, VioletMoss, VioletMossBlock, VioletMossBlockWall, VioletMossBrick, XenonMossBlock, XenonMossBlockWall

### Terraria/Mount.cs (+67 / -4)
- 新类型(+2): DismountCheckResult, SelectiveFlyingMountData
- 新方法(+23): AdjustDashDustMethod, ApplyDummyFrameCounters, CanDismount, CanDismountWithResult, CanVisuallyHoldItem, CastSuperCartLaser, DismountsOnItemUse, DoFailedDismountDust, DrillSmartCursor_Blocks, DrillSmartCursor_Walls, FinalizeMountData, GetProjectileSpawnSource, OverridePositionMethod, OverrideSizeMethod, SetAsChillet, SetAsRollerSkate, TryDismount, TryDismountWithResult, TryEarlyDismount, TryPettingMount, TryStabilizingSmallMountPositionBetweenSlopes, UpdateAfterEquips, UpdateFrame_Velociraptor
- 新字段(+42): AbilityActive, AbilityCharge, AbilityCharging, Active, AutoJump, BlockExtraJumps, BodyFrame, BuffType, CanRideMinecartTracks, CanUseWings, DashDust, ExtraFall, FallDamage, FlyTime, Frame, HandPosition, HeightBoost, MinecartJumpingSound, MouthPosition, Origin, PlayerSize, PlayerXOFfset, RunningGraceTime, SuperCartAcceleration, SuperCartDashSpeed, SuperCartJumpHeight, SuperCartJumpSpeed, SuperCartRunSpeed, Type, XOffset, YOffset, _shouldSuperCart, _walkingGraceTimeLeft, allowedToFly, amountOfBeamsAtOnce, dismountsOnItemUse, extraFall, idleFrames_Rat, lastPurpose, playerXOffset, showFlyingFrames, walkingGraceTimeMax
- 移除方法(-1): DrillSmartCursor
- 移除字段(-3): MinecartDirectional, drillBeamCooldownMax, extraBuff

### Terraria/ID/WallID.cs (+65 / -3)
- 新字段(+65): AllowsPlantsToGrow, AllowsUndergroundDesertEnemiesToSpawn, AncientBlueBrickWall, AncientCobaltBrickWall, AncientCopperBrickWall, AncientGoldBrickWall, AncientGreenBrickWall, AncientHellstoneBrickWall, AncientMythrilBrickWall, AncientObsidianBrickWall, AncientPinkBrickWall, AncientSilverBrickWall, ArgonMossBlockWall, AshWood, AshWoodFence, AstraBrickWall, BlendType, BoulderBlockWall, CannotBeReplacedByWallSpread, CosmicEmberBrickWall, CryocoreBrickWall, DarkCelestialBrickWall, DualDungeonsJungleBiomeWalls, EasterBlockWall, EchoWall, FallenStarWall, Fences, FeywoodWall, FlinxFurBlockWall, ForbiddenBlockWall, GothicBrickWall, HallowedBrickWall, HarpyBlockWall, HeavenforgeBrickWall, Ice, JellyfishBlockWall, KryptonMossBlockWall, LavaMossBlockWall, LibrarianBlockWall, LunarRustBrickWall, MercuryBrickWall, MoonplateBlockWall, OfficeBlockWall, PineTreeBlockWall, PineWoodBlockWall, PoopWall, RainbowMossBlockWall, ReefWall, Search, ShimmerBlockWall, ShimmerBrickWall, Shimmerfall, Snow, SpikeBlockWall, SpreadsCorruption, SpreadsCrimson, SpreadsHallow, StarRoyaleBrickWall, StoneUnsafe, UnbreakableBlockWall, VioletMossBlockWall, WallSpreadStopsAtAir, WallTypeToTerrainTileType, WaterBlockWall, XenonMossBlockWall
- 移除字段(-3): Corrupt, Crimson, Hallow

### Terraria/GameContent/UI/States/UICharacterCreation.cs (+61 / -6)
- 新类型(+1): ArmorAssignments
- 新方法(+35): Click_VoiceCycleBack, Click_VoiceCycleForward, Click_VoicePitch, Click_VoicePlay, EquipArmorFormal, EquipArmorFuneral, EquipArmorGold, EquipArmorHallowed, EquipArmorNone, EquipArmorSilver, EquipArmorSwimming, GetPitchSlider, GetPlayerTemplateValues, GetVoicePitchColorAt, GoBack, HandleBackButtonUsage, MakeHairstylesMenu, OnCanceledNaming, PitchChanged, PitchSliderUpdate, PlayVoicePreview, PreparePreview_ClothStyle, PreparePreview_Main, RecordThatHairWasSelected, RemapPitchSliderKnob, SetPitchSlider_GamePad, SetPitchSlider_Keyboard, TryAutoAssigningHair, TryChangingVoice, Update, UpdatePreviewItems, Update_VoiceIconColor, _clothingStylesCategoryButton_OnUpdate, voiceIcon_OnUpdate, voiceNumber_OnUpdate
- 新字段(+25): Accessory1Item, BackupConfirmationState, BodyItem, HeadItem, LegItem, MAX_NAME_LENGTH, _characterPreviewLayers, _defaultHairstylesForClothStyle, _femaleArmor, _lastSelectedHairstyle, _maleArmor, _oldMaleForVoiceAutoSwitch, _pitchAmount, _pitchChanged, _pitchChangedCooldown, _pitchSlider, _playedVoicePreviewThisFrame, _previewArmorButton, _tips, _validVoiceStyles, _voiceNext, _voicePlay, _voicePrevious, dirty, initialState
- 移除方法(-4): Click_CharGenderFemale, Click_CharGenderMale, MakeHairsylesMenu, OnCancledNaming
- 移除字段(-2): _genderFemale, _genderMale

### Terraria/IO/WorldFile.cs (+45 / -22)
- 新类型(+1): TilePacker
- 新方法(+6): ConvertIlluminantPaintToNewField, FixAgainstExploits, FixEndlessRainWorlds, LoadWorld_LastMinuteFixes, SaveNewWorld, _SaveWorld
- 新字段(+38): Header1_1, Header1_10, Header1_18, Header1_2, Header1_20, Header1_4, Header1_40, Header1_8, Header1_80, Header1_C0, Header2_1, Header2_10, Header2_2, Header2_20, Header2_4, Header2_40, Header2_70, Header2_8, Header2_80, Header3_1, Header3_10, Header3_2, Header3_20, Header3_4, Header3_40, Header3_8, Header3_80, Header4_1, Header4_10, Header4_2, Header4_20, Header4_4, Header4_40, Header4_8, Header4_80, VersionNumberForChestRework, _tempCoinRain, _tempMeteorShowerCount
- 移除方法(-2): CacheSaveTime, SetTempToCache
- 移除字段(-20): CachedCelebratingNPCs, OnWorldLoad, _cachedBloodMoon, _cachedCultistDelay, _cachedDayTime, _cachedEclipse, _cachedLanternNightCooldown, _cachedLanternNightGenuine, _cachedLanternNightManual, _cachedLanternNightNextNightIsGenuine, _cachedMoonPhase, _cachedPartyDaysOnCooldown, _cachedPartyGenuine, _cachedPartyManual, _cachedSandstormHappening, _cachedSandstormIntendedSeverity, _cachedSandstormSeverity, _cachedSandstormTimeLeft, _cachedTime, _hasCache

### Terraria/ID/MessageID.cs (+41 / -19)
- 新字段(+41): AddNPCBuff, AddPlayerBuffPvP, AreaTileChange, CrystalInvasionRequestedToSkipWaitTime, DeadCellsDisplayJarTryPlacing, DevCommands, ExtraSpawnSectionLoaded, HostToken, InitialSpawn, ItemPosition, ItemRotationAndAnimation, ItemUseSound, LockAndUnlock, ManaEffect, MiscDataSync, NPCBuffs, NPCDebuffDamage, OpenSignRequest, OpenSignResponse, Ping, PlayerBuffs, RequestLucyPopup, RequestQuestEffect, RequestSection, SetMiscEventValues, ShimmerActions, SpawnBossUseLicenseStartEvent, SpectatePlayer, SyncChestSize, SyncItemCannotBeTakenByEnemies, SyncItemDespawn, SyncItemsWithShimmer, SyncLoadout, SyncProjectileTrackers, SyncTilePaintOrCoating, SyncWallPaintOrCoating, TEDisplayDollDataSync, TELeashedEntityAnchorPlaceItem, TeamChange, TeamChangeFromUI, Unused83
- 移除字段(-19): AddPlayerBuff, Deprecated1, NPCKillCountDeathTally, TEDisplayDollItemSync, Unknown20, Unknown41, Unknown43, Unknown45, Unknown46, Unknown47, Unknown49, Unknown50, Unknown51, Unknown52, Unknown53, Unknown54, Unknown61, Unknown63, Unknown64

### Terraria/ID/DustID.cs (+56 / -0)
- 新字段(+56): Ash, Astra, BirdDroppings, BlueFlare, BlueGreenElectricity, Chlorophyte, CorruptSpray, Corruption, CosmicEmber, Crimson, CrimsonSpray, Cryocore, DarkCelestial, DirtSpray, Eater, Firefly, Flare, Glass, HallowSpray, HeatRay, Heavenforge, IchorSplash, JesterSparkleBlue, JesterSparkleYellow, LavaCloud, LifeCrystal, LunarRust, MartianBlood, Mercury, MoonBoulder, MushroomSpray, MushroomTorch, PinkPhaseblade, PinkStarfury, PlanteraBulb, PlanteraGrass, PlanteraPetal, Poop, PrettyMirror, PureSpray, RainbowCloud, SandSpray, Shadowbeam, ShimmerSpark, ShimmerSplash, ShimmerStream, ShimmerTorch, SnowSpray, SnowflakeIce, SparkForLightDisc, StarCloud, StarRoyale, Terra, TintablePaint, UnderwaterBubble, VioletMoss

### Terraria/GameContent/UI/States/UIWorldCreation.cs (+47 / -7)
- 新方法(+26): AddSeedFromSeedmenu, ClearSeed, ClearSeedText, ClickAdvancedSeedMenu, DrawSeedSystems, DrawSpecialSeedRing, DrawSpecialSeedRingCallback, DrawSpecialSeedRingCallbackWithoutCondition, EnableSecretSeedOptions, FillSeedContent, GetJoinedSecretSeedString, GoBack, HandleBackButtonUsage, OpenSeedInputMenu, PreparePreviouslyUnlockedSecretSeeds, RandomizeSeed, RemoveSeedFromSeedMenu, ResetSpecialSeedRing, SetGoBackTarget, Spawn_BestReforge, Spawn_RainbowRodHit, StripColors, StripWidth, SubmitSeedEvent, ToggleSeedOption, UpdateSpecialSeedRing
- 新字段(+21): HasDisabledSecretSeed, HasEnteredSpecialSeed, SeedDust, SeedParticleSystem, SubmitSeed, _advancedSeedButton, _disabledSecretSeedTextsEntered, _goBackTarget, _isSpecialSeedText, _secretSeedTextsEntered, _vertexStrip, animationSpeed, numSteps, oldPos, oldTangent, opacity, opacity2, ringPoint, saturation, specialSeedIndex, trial
- 移除方法(-3): AssignRandomWorldSeed, ClickRandomizeSeed, ProcessSeed
- 移除字段(-4): MAX_SEED_LENGTH, _optionDifficulty, _optionEvil, _optionSize

### Terraria/GameInput/PlayerInput.cs (+43 / -11)
- 新类型(+2): FastUseItemMemory, SettingsForUI
- 新方法(+14): CanFastUse, Clear, EndFastUse, IsGamepadButtonLockedFromUse, LocalizeKey, LockGamepadButtons, SetCursorMode, SetZoom_Background, ShouldShowInstructionsForGamepad, TryRevertingToMouseMode, TryStartForItemSlot, TryStartForMouse, UpdateCounters, UpdateHousingCursor
- 新字段(+27): AllowExecutionOfGamepadInstructions, CurrentProfile, CurrentlyRebinding, HousingMouseOffset, HousingScreenPosition, InBuildingMode, ListeningTrigger, OriginalScreenSize, PreventCursorModeSwappingToGamepad, PreventFirstMousePositionGrab, PreventHighlightsForGamepad, ProfileGamepadUI, RealScreenHeight, RealScreenWidth, ShouldFastUseItem, SteamDeckIsUsed, UseSteamDeckIfPossible, UsingGamepadUI, _buttonsLocked, _fastUseMemory, _inputMode, _isMouseItem, _itemType, _keysToLocalize, _player, _shouldFastUse, _slot
- 移除方法(-6): GenerateInputTag_ForCurrentGamemode_WithHacks, GenerateInputTags_Gamepad, GenerateInputTags_GamepadUI, SetDesiredZoomContext, SetZoom_Context, SetZoom_Test
- 移除字段(-5): CurrentInputMode, _currentWantedZoom, _fastUseEmpty, _fastUseItemInventorySlot, _fastUseMouseItemSlotType

### Terraria/GameContent/Drawing/TileDrawing.cs (+42 / -7)
- 新方法(+25): CacheSpecialDraws_Part1, CacheSpecialDraws_Part2, ClearSpecialBlockCounts, DistToWanderingCircle, DrawAnyDirectionalGrass, DrawLiquidBehindTiles, DrawNature, DrawNatureGlowmask, DrawTile_BackRope, GetBoulderFurnitureFlameColor, GetCloudFurnitureFlameColor, GetFallenStarFurnitureFlameColor, GetForbiddenFurnitureFlameColor, GetHallowedFurnitureFlameColor, GetLibrarianFurnitureFlameColor, GetWindGridPush2Axis, GetWrappedFurnitureFlameColor, Hash, Hash2, IsVisible, LavaLightA, LinearNoise, LookupCageTopDrawTexture, LookupTileDrawTexture, SmoothStep
- 新字段(+17): Layer_BehindTiles, Layer_LiquidBehindTiles, Layer_OverTiles, Layer_Tiles, _deadCellsDisplayJarTileEntityPositions, _dust, _gore, _lastPaintLookupKey, _lastPaintLookupTexture, _natureRenderer, _perspectivePlayer, _shouldShowInvisibleBlocks_LastFrame, _tileSolid, _tileSolidTop, _violetMossGlow, drawBlackHelper, noise
- 移除方法(-4): CacheSpecialDraws, GetCactusType, IsAlchemyPlantHarvestable, PreDrawTiles
- 移除字段(-3): _currentTileDrawInfo, _currentTileDrawInfoNonThreaded, _localPlayer

### Terraria/Chest.cs (+38 / -6)
- 新类型(+1): ItemTransferVisualizationSettings
- 新方法(+24): AskForChestToEatItem, Assign, Clear, CloneWithSeparateItems, CreateBank, CreateOutOfArray, CreateShop, CreateWorldChest, FillWithEmptyInstances, FixLoadedData, GetNewParticle, IndicateBlockedChest, IsEmpty, IsLockedOrInUse, Lock, RemoveChest, Resize, SetupTravelShop_AddToShop, SetupTravelShop_AdjustSlotRarities, SetupTravelShop_CanAddItemToShop, SetupTravelShop_GetItem, SetupTravelShop_GetPainting, VisualizeChestTransfer, VisualizeChestTransfer_CoinsBatch
- 新字段(+13): AbsoluteMaxItemsWeCanEverReachInAChestForNow, DefaultMaxItems, Fullbright, Hopper, PlayerToChest, RandomizeEndPosition, RandomizeStartPosition, TransitionIn, _chestsByCoords, _itemsGotSet, _particlePool, eatingAnimationTime, index
- 移除方法(-3): FindChestByGuessing, PutItemInNearbyChest, ServerPlaceItem
- 移除字段(-3): chestItemSpawn, chestItemSpawn2, dresserItemSpawn

### Terraria/UI/ItemSorting.cs (+44 / -0)
- 新类型(+2): DamageTypeSortingLayerEntry, MemoryStamp
- 新方法(+8): AddSortingPrioritiesBasedOnPlayerDamage, CompareWithPrioritySet, Descending, Equals, GetHashCode, GetSortingLayer, GetSortingLayerIndex, SortIndicesStable
- 新字段(+34): Index, ItemType, Layer, LayerCount, MiscAcorns, MiscBossBags, MiscCritters, MiscGems, MiscHerbsAndSeeds, MiscJustTheGlowingMushroom, Multiplier, PotionsFood, PotionsJustTheMushroom, Prefix, Stack, ToolsFishing, ToolsGolf, ToolsInstruments, ToolsKeys, ToolsKites, ToolsMisc, _damageRankings, _fillAmmoFromInventory_acceptedAmmoTypes, _fillAmmoFromInventory_emptyAmmoSlots, _layerCount, _layerIndexForItemType, _sortInventory_postStamps, _sortInventory_preStamps, _sort_availableSortingSlots, _sort_counts, _sort_itemsCache, _sort_itemsToSort, _sort_sortedItemIndexes, operator

### Terraria/GameContent/Tile_Entities/TEDisplayDoll.cs (+28 / -14)
- 新类型(+1): DisplayDollPose
- 新方法(+17): AcceptedInWeaponSlot, CanQuickSwapIntoDisplayDoll, ChangePose, DrawSlotMisc, DrawUI, FixLoadedData, GetAccessoryTargetSlot, GetShiftClickAction, IsValidPose, PerformShiftClickAction, ReadData, ReadDummySync, ReadPose, RegisterUsePose, TryChangePose, WriteData, WriteDummySync
- 新字段(+10): Equipment, ItemAimRadians, ItemAnimationPercent, Pose, SupportedUseStylePoses, _equip, _misc, _playerRenderer, _pose, _projectileDummy
- 移除方法(-11): DrawInner, Find, FitsDisplayDoll, GenerateInstance, Kill, NetPlaceEntityAttempt, OverrideItemSlotHover, OverrideItemSlotLeftClick, Place, RegisterTileEntityID, TryGetItemGamepadOverrideInstructions
- 移除字段(-3): _items, _myEntityID, accessoryTargetSlot

### Terraria/Graphics/TileBatch.cs (+40 / -0)
- 新类型(+4): DataSlice, LayerBatch, LayerBatchKey, RecentLayerCacheEntry
- 新方法(+11): CompareTo, CreateBatch, Equals, FillVertexBuffer, FlushLayered, GetHashCode, GetNewSpriteBufferSlice, GetNextSpriteIndex, Restart, SetLayer, SwitchBatch
- 新字段(+25): BatchIndex, Head, LayerStack, Length, MinSliceLength, Next, NextSprite, SortKey, Start, Tail, Texture, _batchCount, _batchData, _batchDataCount, _batchLookup, _batchLookupCache, _batches, _currentBatchIndex, _currentBatchKey, _drawCalls, _layeredSortingEnabled, _nextLayerStack, _passTextureCount, _passTextures, _textureIdLookup

### Terraria/ID/NPCHeadID.cs (+38 / -1)
- 新字段(+38): AnglerShimmered, ArmsDealerShimmered, BestiaryGirlShimmered, ClothierShimmered, CyborgShimmered, DemolitionistShimmered, DryadShimmered, DyeTraderShimmered, GoblinTinkererShimmered, GolferShimmered, GuideShimmered, HeadListOrder, MechanicShimmered, MerchantShimmered, NurseShimmered, PainterShimmered, PartyGirlShimmered, PirateShimmered, Princess, PrincessShimmered, SantaClausShimmered, SlimeBlue, SlimeCopper, SlimeGreen, SlimeOld, SlimePurple, SlimeRainbow, SlimeRed, SlimeYellow, SteampunkerShimmered, StylistShimmered, Tavernkeep, TavernkeepShimmered, TaxCollectorShimmered, TravellingMerchantShimmered, TruffleShimmered, WitchDoctorShimmered, WizardShimmered
- 移除字段(-1): DD2Bartender

### Terraria/WorldBuilding/WorldGenerator.cs (+36 / -1)
- 新类型(+2): Controller, SnapshotFrequency
- 新方法(+20): CheckLatestPassResultAgainstManifest, DeleteAllSnapshots, DeleteSnapshot, ForceUpdateProgress, GetSnapshot, HashWorld, MsSinceLastSnapshot, OnPassCompleted, OnPaused, ReportException, RunPass, SetDebugWorldGenUIVisibility, SetGenerator, TryCreateSnapshot, TryOperateInControlLock, TryReset, TryResetToPreviousPass, TryResetToSnapshot, TryRunToEndOfPass, UpdatePreviousManifest
- 新字段(+14): CurrentController, CurrentPass, OnPassesLoaded, PassResults, Passes, _controlLock, _controller, _currentPass, _generator, _hashTime, _paused, _previousManifest, _progress, _snapshots
- 移除字段(-1): _totalLoadWeight

### Terraria/DelegateMethods.cs (+36 / -0)
- 新类型(+2): CharacterPreview, Mount
- 新方法(+32): BatDashDust, BatPlayerSize, BerniePet, BumperSoundFart, CastLightOpen_StopForSolids, CheckStopForSolids, CompanionCubePet, EtsyPet, Float, FloatAndRotateForwardWhenWalking, FloatAndSpinWhenWalking, JumpingSound, JumpingSoundFart, LandingSoundFart, NoPosition, NotSolidOrPlatforms, PixieDashDust, PixiePlayerSize, RatPlayerSize, RotateForwardWhenWalking, SlimePet, SparksFart, SparksTerraFart, SpawnFartCloud, SpinWhenWalking, SpreadIceBlocksOverWater, SpreadLightOpen_StopForSolids, SpreadPoopPyramid, SpreadTile, VelociraptorMouthPosition, WolfMouthPosition, WormPet
- 新字段(+2): CheckResultOut, tileCutIgnore

### Terraria/ID/AchievementHelperID.cs (+35 / -0)
- 新字段(+35): CompleteBestiary, DeathByDeadmansChest, DefeatMechdusa, DefeatMoonLordInFTW, DefeatedOldOnesArmyDifficulty3, DrinkBottledWaterWhileDrowning, DroneDiedInSpace, FindAFairy, FlyAKiteOnAWindyDay, FlyPastSpace, FoundGraveyard, GainTorchGodsFavor, GetSunBurned, GoLavaFishing, GraveMistake, HousedAllTownSlimes, JojaCola, PetThePet, PlayGuitar, PlayOnASpecialSeed, PurifyEntireWorld, ResearchedManyItems, RideACoffinCart, ShimmerVillager, SpotTheSunOnACoolDay, SpottedRainbowBoulder, SurviveBoulderRain, SurviveHardcoreDeath, TalkToNPCAtMaxHappiness, Terrarist, ThrowAParty, TrainedTownNPCsForCombat, TransmuteItem, TurnGnomeToStatue, WearMoonLordSet

### Terraria/ID/PaintID.cs (+33 / -1)
- 新字段(+33): BlackPaint, BluePaint, BrownPaint, CyanPaint, DeepBluePaint, DeepCyanPaint, DeepGreenPaint, DeepLimePaint, DeepOrangePaint, DeepPinkPaint, DeepPurplePaint, DeepRedPaint, DeepSkyBluePaint, DeepTealPaint, DeepVioletPaint, DeepYellowPaint, GrayPaint, GreenPaint, IlluminantPaint, LimePaint, NegativePaint, None, Old_IlluminantPaint, OrangePaint, PinkPaint, PurplePaint, RedPaint, ShadowPaint, SkyBluePaint, TealPaint, VioletPaint, WhitePaint, YellowPaint
- 移除字段(-1): GLOW_PAINT

### Terraria/Collision.cs (+30 / -3)
- 新类型(+3): HurtTile, TileContact, TileContactSide
- 新方法(+14): AnyCollisionWithSpecificTiles, AnyHurtingTiles, AnyWallOfTypeOnLine, ApplyConveyorBeltMovementToVelocity, BuildTileContacts, CanTileHurt, HitLine, HitLineWall, HitSpecificWallSubstep, HitTilesInACircle, SolidFullTiles, TileCollisionInStepsOf16, TryChangingSizeFromBottomCenter, TryFindingConveyorBeltRising
- 新字段(+13): Overlap, Side, Slope, Type, X, Y, _cacheForConveyorBelts, bottomFluff, contacts, shimmer, type, x, y
- 移除方法(-3): SwitchTilesNew, TupleHitLine, TupleHitLineWall

### Terraria/Map/MapHelper.cs (+28 / -5)
- 新方法(+8): CalcSkyGradient, CaptureSceneState, DecompressChunk, GetBackgroundType, GetTileType, GetWallType, IsBackground, LoadMapVersionCompressed
- 新字段(+20): Header2Color1, Header2Color2, Header2Color3, Header2Color4, Header2Color5, Header2ShimmerBit, Header2_ReadHeader3Bit, Header2_UnusedBit8, Header3_ReservedForHeader4Bit, Header3_UnusudBit2, Header3_UnusudBit3, Header3_UnusudBit4, Header3_UnusudBit5, Header3_UnusudBit6, Header3_UnusudBit7, Header3_UnusudBit8, MapChunkSize, sceneArea, sceneSnowiness, zlibDecompress
- 移除方法(-1): ResetMapData
- 移除字段(-4): maxUpdateTile, numUpdateTile, updateTileX, updateTileY

### Terraria/IO/WorldFileData.cs (+32 / -0)
- 新方法(+12): CopyToLocal, EnableSeedOptions, GetRenameCallback, GetSecretSeedCodes, GetSerializedSeedsSum, GetWorldName, Rename, SetSeedToRandomWithCurrentEvents, TranslateSeed, TryApplyingCopiedSeed, TryParseSecretSeed, TryParseSeedOptionValue
- 新字段(+20): Anniversary, DefeatedMoonlord, DontStarve, ForTheWorthy, HasValidSeed, LastPlayed, LoadException, LoadStatus, MAX_USER_SEED_TEXT_LENGTH, NoTrapsWorld, NotTheBees, RemixWorld, Seed, SeedText, SkyblockWorld, UseGuidAsMapName, WorldId, WorldSizeName, ZenithWorld, seedOptionsInOrder

### Terraria/Tile.cs (+32 / -0)
- 新方法(+20): BlockColorAndCoating, ClearBlockPaintAndCoating, ClearSlope, ClearTileAndPaint, ClearWallPaintAndCoating, CopyPaintAndCoating, UseBlockColors, UseWallColors, WallColorAndCoating, anyHoney, anyLava, anyShimmer, anyWater, anyWire, fullbrightBlock, fullbrightWall, invisibleBlock, invisibleWall, shimmer, water
- 新字段(+12): Bit0, Bit1, Bit15, Bit2, Bit3, Bit4, Bit5, Bit6, Bit7, EitherLavaOrHoney, Liquid_Shimmer, NeitherLavaOrHoney

### Terraria/DataStructures/PlayerDrawSet.cs (+28 / -3)
- 新方法(+5): AdjustmentsForBatMount, AdjustmentsForPixieMount, AdjustmentsForRatMount, AdjustmentsForVelociraptorMount, AdjustmentsForWolfMount
- 新字段(+23): Center, SelectedDrawnProjectile, cAngelHalo, cBackpack, cBalloonFront, cBeard, cCoat, cFaceFlower, cFaceHead, cFaceMask, cFlameWaker, cTail, colorDisplayDollSkin, drawAngelHalo, drawFrontAccInNeckAccLayerAlways, hairBackFrame, hairFrontFrame, hairOffset, hideEntirePlayer, hideEntirePlayerExceptHelmetsAndFaceAccessories, legsOffset, mountDrawsEyelid, mountHandlesHeadDraw
- 移除字段(-3): backPack, hairFrame, heldProjOverHand

### Terraria/GameContent/ItemDropRules/Conditions.cs (+26 / -5)
- 新类型(+21): DontStarveIsNotUp, DontStarveIsUp, DropExtraGel, Easymode, EyeOfCthulhuDefeatedAndNoAltarsInWorld, IsHardmode, MechdusaKill, NotDropExtraGel, NotRemixSeed, NotRemixSeedEasymode, NotRemixSeedHardmode, PumpkinMoonDropGateForTrophies, RedHatSkeletron, RemixSeed, RemixSeedEasymode, RemixSeedHardmode, SkyblockIsNotUp, SkyblockIsUp, SkyblockIsUpNoSickle, TenthAnniversaryIsNotUp, TenthAnniversaryIsUp
- 新字段(+5): _targetList, aiSlotToCheck, neededName, neededWave, valueToMatch
- 移除类型(-1): KOCannon
- 移除字段(-4): _aiSlotToCheck, _neededName, _neededWave, _valueToMatch

### Terraria/UI/Gamepad/GamepadPointID.cs (+29 / -2)
- 新字段(+29): BannerClaimingBig, BannerClaimingSmall, BannerGridToggle, ClothSoundOption, ClothSoundPitch, CraftFromNearbyChestsToggle, CraftGridToggle, CraftsBigCount, Loadout1, Loadout2, Loadout3, NPCChat10, NPCChat11, NPCChat4, NPCChat5, NPCChat6, NPCChat7, NPCChat8, NPCChat9, NewCraftingUI0, NewCraftingUICraftFromNearbyChestsToggle, NewCraftingUICraftSlot, NewCraftingUIElements0, NewCraftingUIEnd, NewCraftingUIGrid0, NewCraftingUIGuideSlot, NewCraftingUIMaterial0, NewCraftingUIMaterialEnd, NewCraftingUIToggle
- 移除字段(-2): ChestToggleVacuum, DisplayDoll15

### Terraria/UI/UIElement.cs (+22 / -8)
- 新方法(+11): DrawEvent, ExecuteRecursively, LeftClick, LeftDoubleClick, LeftMouseDown, LeftMouseUp, RightClick, RightDoubleClick, RightMouseDown, RightMouseUp, UIElementAction
- 新字段(+11): Children, OnDraw, OnLeftClick, OnLeftDoubleClick, OnLeftMouseDown, OnLeftMouseUp, OnRightClick, OnRightDoubleClick, OnRightMouseDown, OnRightMouseUp, PassThroughMouseInteraction
- 移除方法(-4): Click, DoubleClick, MouseDown, MouseUp
- 移除字段(-4): OnClick, OnDoubleClick, OnMouseDown, OnMouseUp

### Terraria/Graphics/Shaders/ScreenShaderData.cs (+28 / -0)
- 新方法(+4): CheckCachedParameters, UseImageSize0, UseSceneOffset, UseSceneSize
- 新字段(+24): CombinedOpacity, Intensity, MultiChunkCapture, UnscaledScreenSize, _effect, _uImageSize0, _uSceneOffset, _uSceneSize, uColor, uDirection, uImageOffset, uImageSize, uIntensity, uMultiChunkScene, uOpacity, uProgress, uSceneOffset, uSceneSize, uScreenPosition, uScreenResolution, uSecondaryColor, uTargetPosition, uTime, uZoom

### Terraria/DataStructures/PlayerDrawLayers.cs (+24 / -3)
- 新方法(+24): DrawHeldProj, DrawLongCoat, DrawPlayer_08_1_Tails, DrawPlayer_08_PlayerVisuallyHasFullArmorSet, DrawPlayer_09_Wings, DrawPlayer_10_BackAcc, DrawPlayer_12_1_BalloonFronts, DrawPlayer_13_ArmorBackCoat, DrawPlayer_21_1_Magiluminescence, DrawPlayer_21_Head_TheFace_Eyelid, DrawPlayer_27_HeldItem_ApplyStealthToColor, DrawPlayer_32_FrontAcc_BackPart, DrawPlayer_32_FrontAcc_FrontPart, DrawPlayer_38_EyebrellaCloud, DrawPlayer_ChippysHeadband, DrawPlayer_GetMountOffsetForFaceAcc, DrawPlayer_Head_GetTVScreen, DrawPlayer_JimsDroneRadio, DrawPlayer_RenderAllLayersSlow, GetChickenBonesGlowColor, GetHatStacks, GetLunaGlowColor, GetMatchingBodyExtension, GetMatchingBodyExtensionBack
- 移除方法(-3): DrawPlayer_09_BackAc, DrawPlayer_10_Wings, DrawPlayer_21_head_GetHatStacks

### Terraria/Initializers/ChromaInitializer.cs (+27 / -0)
- 新类型(+1): EventLocalization
- 新方法(+10): AddGameplayEvents, BindTo, Configuration_OnLoad, Configuration_OnSave, DisableAllDeviceGroups, LoadSpecialRulesForDevices, LoadSpecialRulesFor_GameSense, LoadSpecialRulesFor_GameSense_Keyboard, LoadSpecialRulesFor_SecondaryDevice, UpdateEvents
- 新字段(+16): DefaultDisplayName, Event_BreathPercent, Event_LifePercent, Event_ManaPercent, GAME_NAME_ID, LocalizedNames, _corsairColorProfile, _localizedEvents, _logitechColorProfile, _razerColorProfile, _rgbUpdateRate, _steelSeriesColorProfile, _useCorsair, _useLogitech, _useRazer, _useSteelSeries

### Terraria/Wiring.cs (+27 / -0)
- 新方法(+23): ClearAll, ExplodeMine, Extractinator, GetItemSource, GetNPCSource, GetProjectileSource, Hopper, IsHopperInRangeOf, Toggle2x2Light, ToggleCampFire, ToggleCandle, ToggleChandelier, ToggleFirePlace, ToggleHangingLantern, ToggleHolidayLight, ToggleLamp, ToggleLampPost, ToggleTorch, TryAddingToEmptySlot, TryAddingToStack, TryFindChestForExtractinator, TryMoveCoinsInChest, TryToPutItemInChest
- 新字段(+4): HopperGrabHitboxSize, bunnyCannonCoolDown, cannonCoolDown, snowballCannonCoolDown

### Terraria/GameContent/UI/States/UIManageControls.cs (+24 / -0)
- 新类型(+1): SpecialControls
- 新方法(+2): controllerGlyphButtonClick, controllerGlyphStyle
- 新字段(+21): DisableDoubleTapForDashing, InvertLeftX, InvertLeftY, InvertRightX, InvertRightY, LeftXDeadZone, LeftYDeadZone, MouseHotbarToggle, MouseSnapToggle, ResetGamepad, ResetGamepadAdvanced, ResetGameplay, ResetHotbar, ResetMap, RightXDeadZone, RightYDeadZone, SlidersDeadZone, TicksPerInventoryMovement, TimeBeforeRadial, TriggersDeadZone, _buttonStyle

### Terraria/ID/MountID.cs (+23 / -1)
- 新字段(+23): Bat, CanDash, CanUseHooks, Chillet, ChilletIgnis, DoesNotOverrideBackpackDraw, DoesNotOverrideBodyFrames, DoesNotOverrideLegFrames, DontDismountWhenCCed, DontHoldItems, FartMinecart, IsRollerSkates, IsTransformationMount, Pixie, PlayerIsHidden, Rat, RollerSkates, RollerSkatesGreen, RollerSkatesPink, RollerSkatesWhite, TerraFartMinecart, Velociraptor, Wolf
- 移除字段(-1): FacePlayersVelocity

### Terraria/UI/Gamepad/UILinkPointNavigator.cs (+21 / -3)
- 新方法(+8): ClearSuggestion, ConsumeSuggestion, ConsumeSuggestionSwap, DrawLink, DrawLinks, GetPosition, SuggestUsage, SwapToSuggestion
- 新字段(+13): CRAFT_CurrentIngredientsCount, CurrentPoint, ItemSlotShouldHighlightAsPreviouslySelected, ItemSlotShouldHighlightAsSelected, NPCCHAT_ButtonsCount, NPCCHAT_ButtonsNew, NPCS_HoveredBanner, NPCS_SelectedNPC, NewCraftingUI_MaterialIndex, _preSuggestionPoint, _queue, _suggestedPointID, _visited
- 移除字段(-3): CRAFT_CurrentIngridientsCount, CREATIVE_ItemSlotShouldHighlightAsSelected, NPCS_LastHovered

### Terraria/Graphics/Shaders/MiscShaderData.cs (+22 / -0)
- 新方法(+4): CheckCachedParameters, IsPowerOfTwo, UseSamplerState, UseSpriteTransformMatrix
- 新字段(+18): MatrixTransform, _customSamplerState, _effect, _transformMatrix, _uImage0Tex, _uImage1Tex, _uImage2Tex, uColor, uDrawPosition, uImageSize0, uImageSize1, uImageSize2, uOpacity, uSaturation, uSecondaryColor, uShaderSpecificData, uSourceRect, uTime

### Terraria/UI/UserInterface.cs (+18 / -4)
- 新类型(+1): InputPointerCache
- 新方法(+6): Clear, ClearPointers, HandleClick, ImmediatelyUpdateInputPointers, MouseCaptured, MouseElementEvent
- 新字段(+11): ClickEvent, CurrentState, DoubleClickEvent, LastClicked, LastDown, LastTimeDown, LeftMouse, MouseDownEvent, MouseUpEvent, RightMouse, WasDown
- 移除字段(-4): _lastElementClicked, _lastElementDown, _lastMouseDownTime, _wasMouseDown

### Terraria/PopupText.cs (+21 / -0)
- 新方法(+10): AddToCoinValue, AssignAsSonarText, ClearAll, DrawItemTextPopups, EmitFancyFlashDust, GetTextHitbox, PrepareDisplayText, PrepareEffects, PrepareTextEffects, ResetText
- 新字段(+11): AnyEffect, TargetScale, charColors, charOffsets, displayText, effectIntensity, effectStyle, framesSinceSpawn, freeAdvanced, maxItemText, popupText

### Terraria/GameContent/UI/Elements/UICreativeInfiniteItemsDisplay.cs (+5 / -15)
- 新方法(+4): GoBackFromVirtualKeyboard, SacrificeWhatYouCan, StopPlayingAnimation, UpdateVisualFrame
- 新字段(+1): _itemList
- 移除方法(-8): AddSearchBar, Click_SearchArea, GoBackHere, OnCancledInput, OnEndTakingInput, OnFinishedSettingName, OnStartTakingInput, OpenVirtualKeyboardWhenNeeded
- 移除字段(-7): SnapPointName_InfinitesItemSlot, _itemIdsAvailableToShow, _itemIdsAvailableTotal, _parentUIState, _searchBar, _searchBoxPanel, _searchString

### Terraria/GameContent/Liquid/LiquidRenderer.cs (+17 / -2)
- 新类型(+1): SpecialLiquidDrawCache
- 新方法(+10): DrawNormalLiquids, DrawShimmer, GetShimmerBaseColor, GetShimmerFrame, GetShimmerGlitterColor, GetShimmerGlitterOpacity, GetShimmerWave, SetShimmerVertexColors, SetShimmerVertexColors_Sparkle, SimpleWhiteNoise
- 新字段(+6): Tiles, X, Y, _drawCacheForShimmer, _waterfallAnimationFrame, _waterfallFrameState
- 移除方法(-2): Draw, InternalDraw

### Terraria/GameContent/TextureAssets.cs (+17 / -1)
- 新字段(+17): AccBeard, BannerToggle, BoneArm3, CageTop, ChestCraft, InventoryBack19, InventoryBack20, InventoryBack21, InventoryBack22, InventoryBack23, InventoryBack24, Logo5, Logo6, NPCHappiness, NpcPortraitBackground, SmartCursorArrow, TexturePackButtons
- 移除字段(-1): MiniMinotaur

### Terraria/DataStructures/TileEntity.cs (+13 / -4)
- 新方法(+10): Add, GetShiftClickAction, Kill, OnPlaced, OnRemoved, OnWorldLoaded, PerformShiftClickAction, PerformUpdates, Place, Remove
- 新字段(+3): EntityCreationLock, RequiresUpdates, UpdateEntities
- 移除方法(-4): GetItemGamepadInstructions, OverrideItemSlotHover, OverrideItemSlotLeftClick, TryGetItemGamepadOverrideInstructions

### Terraria/GameContent/Creative/ItemFilters.cs (+15 / -2)
- 新类型(+8): AAccessories, AArmor, AccessoriesCategory, Furniture, MiscAccessories, MiscFallback, Tools, Vanity
- 新方法(+3): IsAnAccessoryOfType, IsAnArmorThatMatchesSocialState, IsMiscEquipment
- 新字段(+4): _fitsFilterByItemType, _itemIdsThatAreAccepted, _unusedColor, otherFiltersToCheckAgainst
- 移除字段(-2): _unusedBadPrefixLines, _unusedPrefixLine

### Terraria/GameContent/Events/DD2Event.cs (+15 / -1)
- 新类型(+1): DamageTracker
- 新方法(+7): AttemptToSkipWaitTime, GetSpawnSource_OldOnesArmy, IncludeDamageFor, IsStandActive, LoseInvasionMessage, RequestToSkipWaitTime, Stop
- 新字段(+7): EnemySpawningIsOnHold, INFO_FAILURE_INVASION_COLOR, KillTimeMessage, Name, ReadyToFindBartender, _damageTracker, _won
- 移除方法(-1): SpawnNPC

### Terraria/GetItemSettings.cs (+10 / -6)
- 新字段(+10): GiftRecieved, LootAllFromBank, LootAllFromChest, NoCoinMerge, NoSound, QuickTransferFromSlot, RefundConsumedItem, ReturnItemFromSlot, ReturnItemShowAsNew, ReturnItemShowAsNewNoCoinMerge
- 移除字段(-6): GetItemInDropItemCheck, InventoryEntityToPlayerInventorySettings, InventoryUIToInventorySettings, InventoryUIToInventorySettingsShowAsNew, LootAllSettings, NPCEntityToPlayerInventorySettings

### Terraria/Graphics/Shaders/ArmorShaderData.cs (+16 / -0)
- 新方法(+1): CheckCachedParameters
- 新字段(+15): _effect, uColor, uDirection, uDrawPosition, uImageSize0, uImageSize1, uLegacyArmorSheetSize, uLegacyArmorSourceRect, uOpacity, uRotation, uSaturation, uSecondaryColor, uSourceRect, uTargetPosition, uTime

### Terraria/ID/PrefixID.cs (+16 / -0)
- 新类型(+1): Sets
- 新字段(+15): Ballistic, Eager, Fabled, Factory, Feeble, Focused, IllTempered, Loyal, Patient, Petty, Rabid, ReducedNaturalChance, Scraggling, Skittish, Worthy

### Terraria/Localization/LanguageManager.cs (+14 / -2)
- 新方法(+11): AddVariant, EstimateWordCount, HotReloadContentFile, IndexedFromCategory, LoadFromContentSources, LoadLanguageFromFileTextCsv, LoadLanguageFromFileTextJson, ReloadLanguage, TryGetVariation, UpdateTextValue, UseSources
- 新字段(+3): VariationSeparatorSign, _contentSources, _textVariations
- 移除方法(-1): LoadLanguageFromFileText
- 移除字段(-1): OnLanguageChanging

### Terraria/RecipeGroup.cs (+13 / -3)
- 新方法(+9): Add, Contains, CountUsableItems, GetGroupFakeItemId, GetPlaceholderItemType, Register, SortDecraftingEntries, ToString, WithDefaultCombineFormat
- 新字段(+4): DecraftItemId, DefaultCombineFormat, FakeItemIdOffset, Items
- 移除方法(-1): RegisterGroup
- 移除字段(-2): IconicItemId, recipeGroupIDs

### Terraria/GameContent/Tile_Entities/TEHatRack.cs (+4 / -11)
- 新方法(+4): CanQuickSwapIntoHatRack, FixLoadedData, GetShiftClickAction, PerformShiftClickAction
- 移除方法(-10): Find, FitsHatRack, GenerateInstance, Kill, NetPlaceEntityAttempt, OverrideItemSlotHover, OverrideItemSlotLeftClick, Place, RegisterTileEntityID, TryGetItemGamepadOverrideInstructions
- 移除字段(-1): _myEntityID

### Terraria/WorldSections.cs (+13 / -2)
- 新方法(+6): SectionNeedsRefresh, SetAllFramedSectionsAsNeedingRefresh, SetAllSectionsLoaded, SetSectionAsRefreshed, SetTilesLoaded, TileLoaded
- 新字段(+7): AnyNeedRefresh, AnyUnfinishedSections, BitIndex_SectionFramed, BitIndex_SectionLoaded, BitIndex_SectionMapDrawn, BitIndex_SectionNeedsRefresh, _sectionsNeedingRefresh
- 移除方法(-2): GetNextTileFrame, SetAllFramesLoaded

### Terraria/GameContent/SmartCursorHelper.cs (+13 / -1)
- 新方法(+9): AllowNormalBlockPlacementBehaviourForItemType, AllowedForContinuity, GetDesiredDirectionFrom, IsHoveringOverAnInteractableTileThatBlocksSmartCursor, IsPlatform, IsValidSpotForTorch, Step_GrassSeeds, Step_Moss, TileTargetDesired
- 新字段(+4): LockedDesiredDirection, _lockedContinuityCoords, _lockedDesiredDirection, paintCoatingLookup
- 移除方法(-1): IsHoveringOverAnInteractibleTileThatBlocksSmartCursor

### Terraria/GameContent/UI/Elements/UIWorldListItem.cs (+12 / -2)
- 新方法(+6): GoBackHere, HasPlayedMouseOver, NewlyGeneratedMouseOver, OnFinishedSettingName, RenameButtonClick, RenameMouseOver
- 新字段(+6): IsFavorite, _buttonRenameTexture, _hasBeenPlayedByActivePlayer, _hasBeenPlayedByActivePlayerTexture, _isNewlyGenerated, _isNewlyGeneratedTexture
- 移除方法(-1): GetIcon
- 移除字段(-1): _data

### Terraria/GameContent/UI/States/UIVirtualKeyboard.cs (+10 / -4)
- 新方法(+6): CacheCanceledInput, PressSpace, RestoreCanceledInput, ShouldShowKeyboard, TextIsValidForSubmit, TryEscapingMenu
- 新字段(+4): CustomTextValidationForSubmit, CustomTextValidationForUpdate, _editingChest, _editingSign
- 移除方法(-2): CacheCancelledInput, RestoreCancelledInput
- 移除字段(-2): _edittingChest, _edittingSign

### Terraria/Graphics/Shaders/HairShaderData.cs (+14 / -0)
- 新方法(+1): CheckCachedParameters
- 新字段(+13): ShaderDisabled, _effect, uColor, uDirection, uDrawPosition, uImageSize0, uImageSize1, uOpacity, uSaturation, uSecondaryColor, uSourceRect, uTargetPosition, uTime

### Terraria/NetMessage.cs (+12 / -2)
- 新方法(+9): ResyncTiles, SendChestContentsTo, SendObjectPlacement, SendPacket, SendPacketToServer, SyncChestContentsForSection, SyncNPCsForSection, SyncOnePlayer_ItemArray, WriteAccessoryVisibility
- 新字段(+3): _compressChestList, _compressEntities, _compressSignList
- 移除方法(-2): SendObjectPlacment, SendTileRange

### Terraria/Netplay.cs (+10 / -4)
- 新方法(+5): AcceptedFamilyType, UpdateClientInMainThread, UpdateDataRates, UpdateInMainThread, UpdateServerInMainThread
- 新字段(+5): DefaultPort, HostToken, IsHostAndPlay, SaveOnServerExit, swTicksLast
- 移除方法(-4): CleanupServer, Update, UpdateClient, UpdateServer

### Terraria/GameContent/Creative/ItemsSacrificedUnlocksTracker.cs (+12 / -1)
- 新方法(+8): ClearNewlyResearchedStatus, CountFullyResearchedItems, DismissNewlyUnlockedFromTeamMatesIcon, ForEachItemWithResearchProgress, IsFullyResearched, IsNewlyResearched, TryGetSacrificeNumbers, TryGetTeammateUnlockCredit
- 新字段(+4): AnyNewUnlocksFromTeammates, _newlyUnlocked, _sacrificesCountByItemIdCache, _unlockedByTeammate
- 移除字段(-1): SacrificesCountByItemIdCache

### Terraria/Utilities/NPCUtils.cs (+13 / -0)
- 新方法(+2): DownwindFromNPC, TargetClosestDownwindFromNPC
- 新字段(+11): AdjustedTankDistance, FoundNPC, FoundTank, FoundTarget, NearestNPCDistance, NearestNPCIndex, NearestTankDistance, NearestTankOwnerIndex, NearestTankType, NearestTargetHitbox, NearestTargetType

### Terraria/GameContent/RGB/CommonConditions.cs (+7 / -5)
- 新类型(+4): PlayerCondition, SceneCondition, SurfaceCondition, UndergroundCondition
- 新方法(+1): IsInFrontOfDirtWall
- 新字段(+2): Deerclops, Shimmer
- 移除类型(-1): ConditionBase
- 移除方法(-4): InDesert, InIce, InTemple, IsPlayerInFrontOfDirtWall

### Terraria/GameContent/UI/States/UIBestiaryTest.cs (+2 / -10)
- 新方法(+1): GoBackFromVirtualKeyboard
- 新字段(+1): searchButtonLink
- 移除方法(-7): AddSearchBar, Click_SearchArea, GoBackHere, OnEndTakingInput, OnFinishedSettingName, OnStartTakingInput, OpenVirtualKeyboardWhenNeeded
- 移除字段(-3): _searchBar, _searchBoxPanel, _searchString

### Terraria/ObjectData/TileObjectData.cs (+12 / -0)
- 新方法(+6): ApplyNaturalObjectRules, GetStyle_Detritus, GetStyle_SmallPiles, GetStyle_Stalactite, TryGetTileBounds, addSubTileRange
- 新字段(+6): AlternatesCount, Style1x1Drip, Style1x1Plant_Height22, Style1x1Plant_Height34, Style4x4, _useGlobalLiquidChecks

### Terraria/WaterfallManager.cs (+12 / -0)
- 新方法(+6): AddLight, BindTo, Configuration_OnLoad, GetAlpha, StylizeColor, TrySparkling
- 新字段(+6): Layer_Rain, Layer_Waterfall, _shouldShowInvisibleBlocksAndWalls, lavaRainFrameBackground, lavaRainFrameCounter, lavaRainFrameForeground

### Terraria/WorldBuilding/Actions.cs (+12 / -0)
- 新类型(+9): ClearTileAndWallPaint, ClearTilePaint, ClearWallPaint, SetTileAndWallPaint, SetTileAndWallRainbowPaint, SetTilePaint, SetWall, SetWallPaint, UpdateBounds
- 新字段(+3): _bounds, _clearTile, paintID

### Terraria/GameContent/Creative/CreativePowers.cs (+11 / -0)
- 新方法(+11): Button_OnMouseOut, Button_OnMouseOver, Click_Expert, Click_Journey, Click_Master, Click_Normal, SetValueKeyboardForced, UpdateMouseOverNoItemText, bottomText_OnClick, middleText_OnClick, topText_OnClick

### Terraria/GameContent/Drawing/WallDrawing.cs (+10 / -1)
- 新方法(+5): DrawOutline, GetWallDrawTexture, LerpVertexColorsWithColor, LookupWallDrawTexture, Update
- 新字段(+5): QuickPaintLookup, _lastPaintLookupKey, _lastPaintLookupTexture, _shouldShowInvisibleWalls, drawBlackHelper
- 移除方法(-1): GetTileDrawTexture

### Terraria/Lang.cs (+10 / -1)
- 新类型(+1): ItemPrefixCombiner
- 新方法(+7): GetGlobalSubstitution, GetPrefixedItemName, GetSlimeType, InitGlobalSubstitutions, PrincessChat, RegisterGlobalSubstitution, SlimeChat
- 新字段(+2): _globalSubstitutions, _prefixFormatText
- 移除方法(-1): CreateDialogSubstitutionObject

### Terraria/Localization/LocalizedText.cs (+10 / -1)
- 新方法(+6): ConditionsMetWith, EqualsCommand, GetPropertyLookupFunc, GetValueIfConditionsMet, ParseCommandPrefix, TryFormatWith
- 新字段(+4): HasValue, UnformattedValue, _propertyLookupCache, _value
- 移除方法(-1): CanFormatWith

### Terraria/GameContent/Achievements/AchievementsHelper.cs (+9 / -1)
- 新方法(+8): CheckResearchAchievement, DoClassicTitleScreenAchievement, MechaMayhem_Clear, MechaMayhem_Kill, MechaMayhem_Start, PlantedAcorn, ScanForMechs, TryGrantingBestiary100PercentAchievement
- 新字段(+1): _lastResearchVersion
- 移除方法(-1): CheckMechaMayhem

### Terraria/GameContent/Biomes/CaveHouse/HouseBuilder.cs (+10 / -0)
- 新方法(+6): PaintSeedHouses, PlaceBiomeSpecificPriorityTool, PotentiallyConvertToRainbowBrick, PotentiallyConvertToRainbowMossBlock, PotentiallyConvertToSeedHouse, RainbowifyOnTenthAnniversaryWorlds
- 新字段(+4): BottomRoom, TopRoom, _random, _tiles

### Terraria/GameContent/ItemDropRules/CommonDrop.cs (+5 / -5)
- 新字段(+5): amountDroppedMaximum, amountDroppedMinimum, chanceDenominator, chanceNumerator, itemId
- 移除字段(-5): _amtDroppedMaximum, _amtDroppedMinimum, _dropsOutOfY, _dropsXoutOfY, _itemId

### Terraria/GameContent/Tile_Entities/TETrainingDummy.cs (+3 / -7)
- 新字段(+3): activationRetryCooldown, npcSlotsFull, playerBoxes
- 移除方法(-5): Find, GenerateInstance, Kill, NetPlaceEntity, Place
- 移除字段(-2): _myEntityID, playerBox

### Terraria/Graphics/Shaders/ShaderData.cs (+9 / -1)
- 新类型(+1): EffectParameter
- 新方法(+3): Get, SetValue, _Create
- 新字段(+5): _cachedParameters, _effect, _hasValue, _setValue, _value
- 移除方法(-1): SwapProgram

### Terraria/ID/SurfaceBackgroundID.cs (+9 / -1)
- 新类型(+1): Sets
- 新字段(+8): CorruptDesert, Count, CrimsonDesert, Factory, HallowDesert, IsDesertVariant, IsForest, Search
- 移除字段(-1): GoodEvilDesert

### Terraria/UI/ChestUI.cs (+6 / -4)
- 新方法(+3): DepositAll_IntoLocalChest, DepositAll_IntoWorldChest, Scroll
- 新字段(+3): LastChestDisplayRectangle, LastHighestChestRow, StartingRowForDrawing
- 移除方法(-3): GetContainerUsageInfo, ToggleVacuum, TryPlacingInPlayer
- 移除字段(-1): ToggleVacuum

### Terraria/GameContent/Tile_Entities/DisplayDollSlot.cs (+7 / -2)
- 新字段(+7): AccCount, ArmorCount, Armor_Body, EquipCount, Equip_Mount, MiscCount, Misc_Weapon
- 移除字段(-2): Armor_Shirt, Count

### Terraria/GameContent/Tile_Entities/TEFoodPlatter.cs (+1 / -8)
- 新方法(+1): FixLoadedData
- 移除方法(-7): Find, GenerateInstance, Kill, NetPlaceEntity, NetPlaceEntityAttempt, Place, RegisterTileEntityID
- 移除字段(-1): _myEntityID

### Terraria/GameContent/Tile_Entities/TEItemFrame.cs (+1 / -8)
- 新方法(+1): FixLoadedData
- 移除方法(-7): Find, GenerateInstance, Kill, NetPlaceEntity, NetPlaceEntityAttempt, Place, RegisterTileEntityID
- 移除字段(-1): _myEntityID

### Terraria/GameContent/UI/Chat/GlyphTagHandler.cs (+8 / -1)
- 新类型(+3): GlyphPSTagHandler, GlyphSwitchTagHandler, GlyphXboxTagHandler
- 新方法(+2): GetAutoRow, GetGlyph
- 新字段(+3): DefaultGlyphStyle, ForcedStyle, GlyphStyle
- 移除方法(-1): GetStringLength

### Terraria/GameContent/UI/Elements/UIScrollbar.cs (+7 / -2)
- 新类型(+1): ColorTheme
- 新方法(+3): GoToBottom, LeftMouseDown, LeftMouseUp
- 新字段(+3): AutoHide, CanScroll, _theme
- 移除方法(-2): MouseDown, MouseUp

### Terraria/Graphics/Camera.cs (+9 / -0)
- 新字段(+9): Center, GameViewMatrix, Rasterizer, Sampler, ScaledPosition, ScaledSize, SpriteBatch, UnscaledPosition, UnscaledSize

### Terraria/Graphics/Capture/CaptureInterface.cs (+7 / -2)
- 新类型(+1): SelectionContext
- 新方法(+5): EndDrawingSelection, FullScreenArea, SetZoom_Context, StartDrawingSelection, UpdateCameraCountdown
- 新字段(+1): _selectionContext
- 移除方法(-1): UpdateCamera
- 移除字段(-1): KeyToggleActive

### Terraria/Graphics/Renderers/PrettySparkleParticle.cs (+9 / -0)
- 新字段(+9): AdditiveAmount, DrawHorizontalAxis, DrawVerticalAxis, FadeInEnd, FadeInNormalizedTime, FadeOutEnd, FadeOutNormalizedTime, FadeOutStart, TimeToLive

### Terraria/ID/ContentSamples.cs (+7 / -2)
- 新类型(+1): DyeShaderIDs
- 新方法(+4): AddItemResearchOverride, AddItemResearchOverride_Inner, FillResearchItemOverrides, FixItemsUsingPlayerColours
- 新字段(+2): CreativeResearchItemPersistentIdOverride, _manualCraftingStations
- 移除类型(-1): CommonlyUsedContentSamples
- 移除方法(-1): PrepareAfterEverythingElseLoaded

### Terraria/RemoteServer.cs (+8 / -1)
- 新方法(+2): IsConnected, ResetSpecialFlags
- 新字段(+6): HideStatusTextPercent, PendingTermination, ReadBufferFull, ServerSpecialFlags, ServerWantsToRunCheckBytesInClientLoopThread, StatusTextHasShadows
- 移除字段(-1): StatusTextFlags

### Terraria/Audio/SoundEngine.cs (+5 / -3)
- 新方法(+2): PlayTrackedLoopedSound, Reload
- 新字段(+3): AreSoundsPaused, LegacySoundPlayer, SoundPlayer
- 移除字段(-3): _areSoundsPaused, _legacyPlayer, _player

### Terraria/DataStructures/PlayerDrawHeadSet.cs (+8 / -0)
- 新字段(+8): cAngelHalo, cBeard, cFaceFlower, cFaceHead, cFaceMask, colorDisplayDollSkin, drawAngelHalo, hairOffset

### Terraria/Dust.cs (+7 / -1)
- 新方法(+5): DrawDebugBox, GetVisualRotation, GetVisualScale, HackFrame, QuickCircle
- 新字段(+2): fullBright, noLightEmittance
- 移除字段(-1): noLightEmittence

### Terraria/GameContent/ItemDropRules/DropOneByOne.cs (+4 / -4)
- 新字段(+4): ChanceDenominator, ChanceNumerator, itemId, parameters
- 移除字段(-4): DropsXOutOfYTimes_TheX, DropsXOutOfYTimes_TheY, _itemId, _parameters

### Terraria/GameContent/ShopHelper.cs (+6 / -2)
- 新方法(+3): BiomeNameByKey, LikePrincess, LoveNPCByTypeName
- 新字段(+3): MaxHappinessAchievementPriceMultiplier, _dangerousBiomes, _database
- 移除方法(-2): BiomeName, BiomeNameKey

### Terraria/GameContent/Skies/CreditsRollSky.cs (+7 / -1)
- 新字段(+7): AmountOfTimeNeededForFullPlay, _composer, _isActive, _opacity, _segmentsInGame, _segmentsInMainMenu, _wantsToBeSeen
- 移除字段(-1): _segments

### Terraria/GameContent/Tile_Entities/TETeleportationPylon.cs (+2 / -6)
- 新方法(+2): OnPlaced, OnRemoved
- 移除方法(-5): Find, GenerateInstance, Kill, Place, RegisterTileEntityID
- 移除字段(-1): _myEntityID

### Terraria/GameContent/Tile_Entities/TEWeaponsRack.cs (+1 / -7)
- 新方法(+1): FixLoadedData
- 移除方法(-6): Find, GenerateInstance, Kill, KillTileDropItem, Place, RegisterTileEntityID
- 移除字段(-1): _myEntityID

### Terraria/GameContent/UI/Elements/UICharacter.cs (+8 / -0)
- 新方法(+4): DrawPets, GetPlayerPosition, PreparePetProjectiles, PreparePetProjectiles_CreatePetProjectileDummy
- 新字段(+4): IsAnimated, NoPets, PrepareAction, _petProjectiles

### Terraria/GameInput/TriggerNames.cs (+8 / -0)
- 新字段(+8): ArmorSetAbility, Dash, Loadout1, Loadout2, Loadout3, NextLoadout, PreviousLoadout, ToggleCameraMode

### Terraria/IO/ResourcePackList.cs (+8 / -0)
- 新方法(+5): CreatePacksFromDirectories, CreatePacksFromSavedJson, CreatePacksFromWorkshopFolders, CreatePacksFromZips, Publishable
- 新字段(+3): AllPacks, DisabledPacks, EnabledPacks

### Terraria/Initializers/AssetInitializer.cs (+2 / -6)
- 新方法(+2): CreatePublishableResourcePacksList, TagAsset
- 移除方法(-6): Configuration_OnSave_MinimapFrame, Configuration_OnSave_PlayerResourcesSet, LoadAssetsWhileInInitialBlackScreen, LoadMinimap, LoadMinimapFrames, LoadPlayerResourceSets

### Terraria/Liquid.cs (+7 / -1)
- 新方法(+7): AttemptToMoveShimmer, CreateLiquidMergeTile, GetLiquidMergeTypes, LiquidCheck, LiquidOverwriteStrip, ShimmerCheck, UndergroundDesertCheck
- 移除方法(-1): UnderGroundDesertCheck

### Terraria/RemoteClient.cs (+6 / -2)
- 新方法(+2): CheckSection_ForClient, IsSectionActive
- 新字段(+4): CheckingSections, NetSectionActivated, ReadBufferFull, TileSectionsCheckTime
- 移除方法(-1): ResetSections
- 移除字段(-1): _pendingSectionFraming

### Terraria/WorldBuilding/Modifiers.cs (+8 / -0)
- 新类型(+5): Checkerboard, IsAboveHeight, IsBelowHeight, NoLiquid, SkipUnbreakableWalledTiles
- 新字段(+3): _inclusive, _percentile, _y

### Terraria/Cinematics/Film.cs (+7 / -0)
- 新字段(+7): AppendPoint, Duration, Event, Frame, FrameCount, IsActive, Start

### Terraria/Cinematics/FrameEventData.cs (+7 / -0)
- 新字段(+7): AbsoluteFrame, Duration, Frame, IsFirstFrame, IsLastFrame, Remaining, Start

### Terraria/GameContent/Bestiary/NPCStatsReportInfoElement.cs (+6 / -1)
- 新方法(+3): RefreshStats, StatAdjustmentStep, UpdateBeforeSorting
- 新字段(+3): HideStats, OnRefreshStats, _instance
- 移除字段(-1): GameMode

### Terraria/GameContent/TilePaintSystemV2.cs (+7 / -0)
- 新类型(+2): CageTopRenderTargetHolder, CageTopVariationkey
- 新方法(+2): RequestCageTop, TryGetCageTopAndRequestIfNotReady
- 新字段(+3): CageStyle, IsReady, _cageTopRenders

### Terraria/GameContent/Tile_Entities/TELogicSensor.cs (+1 / -6)
- 新方法(+1): OnPlaced
- 移除方法(-5): Find, GenerateInstance, NetPlaceEntity, NetPlaceEntityAttempt, Place
- 移除字段(-1): _myEntityID

### Terraria/GameContent/UI/BigProgressBar/BigProgressBarSystem.cs (+7 / -0)
- 新方法(+4): BindTo, Configuration_OnLoad, Configuration_Save, ToggleShowText
- 新字段(+3): ShowText, _deerclopsBar, _preferencesKey

### Terraria/GameContent/UI/Elements/UICharacterListItem.cs (+7 / -0)
- 新方法(+4): GoBackHere, OnFinishedSettingName, RenameButtonClick, RenameMouseOver
- 新字段(+3): IsFavorite, _buttonRenameTexture, _orderInList

### Terraria/GameContent/UI/Elements/UIDynamicItemCollection.cs (+5 / -2)
- 新方法(+2): DrawSlot, GetItem
- 新字段(+3): Count, SnapPointName_ItemSlot, _contents
- 移除字段(-2): _itemIdsAvailableToShow, _itemIdsToLoadTexturesFor

### Terraria/Graphics/Renderers/FadingParticle.cs (+5 / -2)
- 新字段(+5): Delay, followPlayerIndex, fullbright, timeSinceSpawn, timeTolive
- 移除字段(-2): _timeSinceSpawn, _timeTolive

### Terraria/MessageBuffer.cs (+7 / -0)
- 新方法(+4): ReUseTemporaryNPCAI, ReUseTemporaryProjectileAI, ReadAccessoryVisibility, TrySendingItemArray
- 新字段(+3): RemainingReadBufferLength, _temporaryNPCAI, _temporaryProjectileAI

### Terraria/Program.cs (+5 / -2)
- 新方法(+2): LogFNANativeLibVersions, RunGame
- 新字段(+3): IsMono, SavePath, TerrariaSaveFolderPath
- 移除字段(-2): IsDebug, IsServer

### Terraria/Audio/ActiveSound.cs (+6 / -0)
- 新方法(+4): DetermineIntendedVolume, LoopedPlayCondition, PlayLooped, UseOverrides
- 新字段(+2): Condition, Pitch

### Terraria/DataStructures/PlayerDrawHeadLayers.cs (+4 / -2)
- 新方法(+4): DrawPlayer_04_CapricornMask, DrawPlayer_04_DeadCellsBeheadedHead, DrawPlayer_04_HatsWithFullHair, GetHatStacks
- 移除方法(-2): DrawPlayer_04_GetHatStacks, DrawPlayer_04_JungleRose

### Terraria/GameContent/Creative/CreativeUI.cs (+3 / -3)
- 新方法(+3): ResumeMenuFromGamepadSearch, SacrificeItemInSacrificeSlot, StopPlayingSacrificeAnimations
- 移除方法(-1): RefreshAvailableInfiniteItemsList
- 移除字段(-2): GamepadPointIdForInfiniteItemSearchHack, _itemIdsAvailableInfinitely

### Terraria/GameContent/ItemDropRules/OneFromOptionsDropRule.cs (+3 / -3)
- 新字段(+3): chanceDenominator, chanceNumerator, dropIds
- 移除字段(-3): _dropIds, _outOfY, _xoutOfY

### Terraria/GameContent/ItemDropRules/OneFromOptionsNotScaledWithLuckDropRule.cs (+3 / -3)
- 新字段(+3): chanceDenominator, chanceNumerator, dropIds
- 移除字段(-3): _dropIds, _outOfY, _xoutOfY

### Terraria/GameContent/UI/Elements/UISearchBar.cs (+3 / -3)
- 新方法(+1): OnDeactivate
- 新字段(+2): HasContents, _maxInputLength
- 移除方法(-1): MouseDown
- 移除字段(-2): OnCancledTakingInput, isWritingText

### Terraria/GameContent/UI/EmoteID.cs (+6 / -0)
- 新字段(+6): BossDeerclops, Hungry, LucyTheAxe, Peckish, Starving, TownPrincess

### Terraria/GameContent/UI/GameTipsDisplay.cs (+2 / -4)
- 新字段(+2): TipOffsetY, _tipProvider
- 移除字段(-4): _lastTip, _tipsDefault, _tipsGamepad, _tipsKeyboard

### Terraria/GameContent/UI/States/UIWorldSelect.cs (+5 / -1)
- 新方法(+4): CanWorldBeJoinedByActivePlayer, HasWorldBeenPlayedByActivePlayer, IsNewlyGenerated, OnDeactivate
- 新字段(+1): NewlyGeneratedWorld
- 移除方法(-1): CanWorldBePlayed

### Terraria/ID/TorchID.cs (+6 / -0)
- 新类型(+2): Sets, ShimmerTorchLight
- 新字段(+4): Factory, IsABiomeTorch, Mushroom, Shimmer

### Terraria/IO/ResourcePack.cs (+3 / -3)
- 新类型(+1): BrandingType
- 新字段(+2): Branding, IsCompressed
- 移除方法(-1): Refresh
- 移除字段(-2): _isCompressed, _needsReload

### Terraria/Server/Game.cs (+6 / -0)
- 新字段(+6): Components, GraphicsDevice, IsActive, LaunchParameters, Services, Window

### Terraria/UI/ItemTooltip.cs (+2 / -4)
- 新方法(+1): FromHardcodedText
- 新字段(+1): _neverUpdateHack
- 移除方法(-3): AddGlobalProcessor, ClearGlobalProcessors, RemoveGlobalProcessor
- 移除字段(-1): _globalProcessors

### Terraria/Utilities/PlatformUtilities.cs (+1 / -5)
- 新方法(+1): SavePng
- 移除字段(-5): IsFNA, IsLinux, IsOSX, IsWindows, IsXNA

### Terraria/WorldBuilding/GenPass.cs (+2 / -4)
- 新方法(+2): Disable, Enable
- 移除方法(-2): OnBegin, OnComplete
- 移除字段(-2): _onBegin, _onComplete

### Terraria/GameContent/Biomes/CaveHouse/HouseUtils.cs (+4 / -1)
- 新方法(+4): CreateRooms_BigAbandonedHouses, FindRoom_BigAbandonedHouses, GetMaxPossibleRoomsInABigAbandonedHouse, GetRandomizedRoomCountInABigAbandonedHouse
- 移除方法(-1): SortBiomeResults

### Terraria/GameContent/ChromaHotkeyPainter.cs (+4 / -1)
- 新字段(+4): Expired, PotionAlert, WhatIsThisKeyFor, _triggerName
- 移除字段(-1): _trigger

### Terraria/GameContent/Golf/GolfState.cs (+4 / -1)
- 新方法(+2): TryGetCameraTrackingPosition, WorldClear
- 新字段(+2): ScoreAdjustment, ShouldScoreHole
- 移除方法(-1): GetLastBallLocation

### Terraria/GameContent/ItemDropRules/ItemDropDatabase.cs (+5 / -0)
- 新方法(+5): RegisterBoss_Deerclops, RegisterIceMimic, RegisterIceMimic_GetEasyModeItemPool, RegisterToMultipleNPCsNotRemixSeed, RegisterToMultipleNPCsRemixSeed

### Terraria/GameContent/TownNPCProfiles.cs (+5 / -0)
- 新方法(+3): GetHeadIndexSafe, LegacyWithSimpleShimmer, TransformableWithSimpleShimmer
- 新字段(+2): ShimmeredNPCFileFolderPath, SlimeHeadIDs

### Terraria/GameContent/UI/Elements/UIImage.cs (+5 / -0)
- 新字段(+5): AllowResizingDimensions, Frame, Texture, UseTextureSizeForOrigin, _nonReloadingTexture

### Terraria/GameContent/UI/States/UIGamepadHelper.cs (+5 / -0)
- 新方法(+5): GetLinkPoint, LinkHorizontalStripBottomSideToSingle, LinkHorizontalStripUpSideToSingle, RemovePointsOutOfView, TryMakeLinkPoint

### Terraria/GameInput/TriggersSet.cs (+4 / -1)
- 新方法(+2): CloneFrom, IsInputFromGamepad
- 新字段(+2): DirectionsRaw, LatestInputMode
- 移除方法(-1): Clone

### Terraria/Graphics/Light/LegacyLighting.cs (+4 / -1)
- 新字段(+4): CrackedLight, IsColorOrWhiteMode, _lastCameraPosition, _negLight3
- 移除字段(-1): _world

### Terraria/Graphics/Light/TileLightScanner.cs (+3 / -2)
- 新方法(+2): ApplyLiquidLight, LightIsBlocked
- 新字段(+1): _drawInvisibleWalls
- 移除方法(-1): ApplyLavaLight
- 移除字段(-1): _world

### Terraria/ID/AmmoID.cs (+5 / -0)
- 新字段(+5): Acorn, Factory, IsArrow, IsBullet, IsSpecialist

### Terraria/Minecart.cs (+4 / -1)
- 新类型(+1): Customization
- 新字段(+3): Default, MagnetOffset, WheelOffset
- 移除字段(-1): _trackMagnetOffset

### Terraria/Net/Sockets/TcpSocket.cs (+2 / -3)
- 新方法(+1): GetStream
- 新字段(+1): _debugStream
- 移除字段(-3): _callbackBuffer, _messagesInQueue, _packetBuffer

### Terraria/UI/Chat/ChatMessageContainer.cs (+4 / -1)
- 新方法(+1): OnWidthLimitChanged
- 新字段(+3): CanBeShownWhenChatIsClosed, LineCount, Prepared
- 移除方法(-1): MarkToNeedRefresh

### Terraria/UI/NetDiagnosticsUI.cs (+5 / -0)
- 新方法(+2): GetLastSentRecvBytes, RotateSendRecvCounters
- 新字段(+3): bytesRecv, bytesRecvLast, bytesSentLast

### Terraria/DataStructures/PlayerDeathReason.cs (+2 / -2)
- 新方法(+1): TryGetCausingEntity
- 新字段(+1): _sourceProjectileLocalIndex
- 移除方法(-1): LegacyEmpty
- 移除字段(-1): _sourceProjectileIndex

### Terraria/GameContent/ARenderTargetContentByRequest.cs (+3 / -1)
- 新方法(+2): HandleUseRequest, Reset
- 新字段(+1): IsReady
- 移除方法(-1): HandleUseReqest

### Terraria/GameContent/Bestiary/BestiaryDatabaseNPCsPopulator.cs (+4 / -0)
- 新方法(+4): AddDropOverrides, AdjustEaterOfWorldStats, AdjustPirateShipStats, HideStats

### Terraria/GameContent/Events/Sandstorm.cs (+1 / -3)
- 新方法(+1): ShowSandstormVisuals
- 移除方法(-2): HandleEffectAndSky, ShouldSandstormDustPersist
- 移除字段(-1): _effectsUp

### Terraria/GameContent/ItemDropRules/DropBasedOnExpertMode.cs (+2 / -2)
- 新字段(+2): ruleForExpertMode, ruleForNormalMode
- 移除字段(-2): _ruleForExpertMode, _ruleForNormalMode

### Terraria/GameContent/ItemDropRules/DropBasedOnMasterMode.cs (+2 / -2)
- 新字段(+2): ruleForDefault, ruleForMasterMode
- 移除字段(-2): _ruleForDefault, _ruleForMasterMode

### Terraria/GameContent/ItemDropRules/ItemDropRule.cs (+3 / -1)
- 新方法(+3): Gel, OneFromOptionsWithNumerator, ScalingWithOnlyBadLuck
- 移除方法(-1): OneFromOptionsWithX

### Terraria/GameContent/ItemDropRules/OneFromRulesRule.cs (+2 / -2)
- 新字段(+2): chanceDenominator, options
- 移除字段(-2): _options, _outOfY

### Terraria/GameContent/ItemShopSellbackHelper.cs (+2 / -2)
- 新字段(+2): prefix, type
- 移除字段(-2): itemNetID, itemPrefix

### Terraria/GameContent/Profiles.cs (+4 / -0)
- 新类型(+1): StackedNPCProfile
- 新方法(+1): SetPartyTextures
- 新字段(+2): _defaultCredits, _profiles

### Terraria/GameContent/UI/Elements/UIHairStyleButton.cs (+3 / -1)
- 新方法(+2): LeftMouseDown, SkipRenderingContent
- 新字段(+1): _framesToSkip
- 移除方法(-1): MouseDown

### Terraria/GameContent/UI/Elements/UIImageButton.cs (+4 / -0)
- 新字段(+4): BorderColor, Color, _borderFrame, _frame

### Terraria/GameContent/UI/Elements/UIText.cs (+3 / -1)
- 新字段(+3): Text, _shadowColor, _textLayout
- 移除字段(-1): _visibleText

### Terraria/GameContent/UI/States/UICreativePowersMenu.cs (+4 / -0)
- 新方法(+2): SacrificeWhatsInResearchMenu, StopPlayingResearchAnimations
- 新字段(+2): IsShowingResearchMenu, _infiniteItemsButton

### Terraria/GameInput/PlayerInputProfile.cs (+3 / -1)
- 新字段(+3): AllowEditing, HotbarAllowsRadial, ShowName
- 移除字段(-1): AllowEditting

### Terraria/Graphics/Capture/CaptureCamera.cs (+4 / -0)
- 新方法(+3): BeginDrawCapture, EndDrawCapture, _Capture
- 新字段(+1): _waterTarget

### Terraria/Graphics/Effects/FilterManager.cs (+3 / -1)
- 新方法(+3): BindTo, Configuration_OnLoad, Configuration_OnSave
- 移除字段(-1): OnPostDraw

### Terraria/Graphics/VertexStrip.cs (+3 / -1)
- 新方法(+2): AddVertexPair, Reset
- 新字段(+1): VertexDeclaration
- 移除方法(-1): AddVertex

### Terraria/ID/CloudID.cs (+4 / -0)
- 新字段(+4): Rare_DontStarveCharlie, Rare_DontStarveMaxwell, Rare_DontStarveWillow, Rare_DontStarveWilson

### Terraria/ID/TeleportationStyleID.cs (+4 / -0)
- 新字段(+4): MysticFrog, NoEffect, ShellphoneSpawn, ShimmerTownNPCTransform

### Terraria/IO/PlayerFileData.cs (+4 / -0)
- 新方法(+3): MapBelongsToPath, MarkAsServerSide, Rename
- 新字段(+1): LastPlayed

### Terraria/Map/MapOverlayDrawContext.cs (+4 / -0)
- 新方法(+3): DrawClamped, GetClampedDrawRegion, GetUnclampedDrawRegion
- 新字段(+1): _opacity

### Terraria/Net/NetManager.cs (+3 / -1)
- 新方法(+3): EmptyCallback, SendToClientOrLoopback, SendToServerOrBroadcast
- 移除方法(-1): SendCallback

### Terraria/Social/Base/CloudSocialModule.cs (+4 / -0)
- 新方法(+4): BindTo, Configuration_OnLoad, Configuration_OnSave, Forget

### Terraria/WorldBuilding/Conditions.cs (+4 / -0)
- 新类型(+2): BoolCheck, InWorld
- 新字段(+2): _fluff, _theBool

### Terraria/WorldBuilding/GenBase.cs (+4 / -0)
- 新字段(+4): _random, _tiles, _worldHeight, _worldWidth

### Terraria/Achievements/Achievement.cs (+3 / -0)
- 新字段(+3): Category, HasTracker, IsCompleted

### Terraria/Audio/LegacySoundStyle.cs (+3 / -0)
- 新字段(+3): IsTrackable, MaxTrackedInstances, _maxTrackedInstances

### Terraria/Audio/SoundPlayer.cs (+3 / -0)
- 新方法(+3): GetActiveSoundCount, PlayLooped, Reload

### Terraria/Audio/SoundStyle.cs (+3 / -0)
- 新字段(+3): PitchVariance, Type, Volume

### Terraria/Chat/ChatCommandProcessor.cs (+1 / -2)
- 新方法(+1): PrepareAliases
- 移除方法(-2): HasLocalizedCommand, RemoveCommandPrefix

### Terraria/Cloud.cs (+3 / -0)
- 新方法(+2): GetParallax, UpdateCloudParallax
- 新字段(+1): lastCameraCenter

### Terraria/DataStructures/NPCAimedTarget.cs (+3 / -0)
- 新字段(+3): Center, Invalid, Size

### Terraria/Entity.cs (+2 / -1)
- 新字段(+2): VisualPosition, shimmerWet
- 移除字段(-1): active

### Terraria/GameContent/AnOutlinedDrawRenderTargetContent.cs (+1 / -2)
- 新方法(+1): HandleUseRequest
- 移除方法(-1): HandleUseReqest
- 移除字段(-1): _coloringShader

### Terraria/GameContent/Bestiary/BestiaryDatabase.cs (+3 / -0)
- 新字段(+3): Entries, Filters, SortSteps

### Terraria/GameContent/Creative/SortingSteps.cs (+2 / -1)
- 新类型(+2): ByUnlockStatus, PlaceableObjects
- 移除类型(-1): PlacableObjects

### Terraria/GameContent/Drawing/ParticleOrchestraSettings.cs (+1 / -2)
- 新字段(+1): UniqueInfoPiece
- 移除字段(-2): PackedShaderIndex, SerializationSize

### Terraria/GameContent/Drawing/WindGrid.cs (+2 / -1)
- 新字段(+2): DirectionX, DirectionY
- 移除字段(-1): Direction

### Terraria/GameContent/Dyes/ReflectiveArmorShaderData.cs (+3 / -0)
- 新方法(+1): CheckCachedParameters
- 新字段(+2): _effect, uLightSource

### Terraria/GameContent/Golf/GolfHelper.cs (+1 / -2)
- 新字段(+1): PredictionLine
- 移除方法(-1): UpdateDebugDraw
- 移除字段(-1): _predictionLine

### Terraria/GameContent/RGB/GemCaveShader.cs (+3 / -0)
- 新字段(+3): ColorRarity, CycleTime, TimeRate

### Terraria/GameContent/Shaders/WaterShaderData.cs (+3 / -0)
- 新字段(+3): DrawRipples, SourceRectangle, _noDistortionTexture

### Terraria/GameContent/UI/BigProgressBar/EaterOfWorldsProgressBar.cs (+2 / -1)
- 新字段(+2): _cache, _segmentForReference
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/BigProgressBar/LunarPillarBigProgessBar.cs (+1 / -2)
- 新字段(+1): _cache
- 移除字段(-2): _lifePercentToShow, _shieldPercentToShow

### Terraria/GameContent/UI/Chat/RemadeChatMonitor.cs (+1 / -2)
- 新字段(+1): _lastChatWidthLimit
- 移除方法(-1): OnResolutionChange
- 移除字段(-1): _recalculateOnNextUpdate

### Terraria/GameContent/UI/Elements/UICharacterNameButton.cs (+2 / -1)
- 新方法(+2): GetTextDimensions, LeftMouseDown
- 移除方法(-1): MouseDown

### Terraria/GameContent/UI/Elements/UIClothStyleButton.cs (+2 / -1)
- 新方法(+1): LeftMouseDown
- 新字段(+1): PrepareAction
- 移除方法(-1): MouseDown

### Terraria/GameContent/UI/Elements/UIToggleImage.cs (+2 / -1)
- 新方法(+1): LeftClick
- 新字段(+1): IsOn
- 移除方法(-1): Click

### Terraria/GameContent/UI/EmoteBubble.cs (+3 / -0)
- 新方法(+2): DrawTemporaryBubble, MakeLocalPlayerEmote
- 新字段(+1): _temporaryBubble

### Terraria/Graphics/Light/LightingEngine.cs (+1 / -2)
- 新字段(+1): _oldPerFrameLights
- 移除方法(-1): SetWorld
- 移除字段(-1): _timer

### Terraria/Graphics/Renderers/LegacyPlayerRenderer.cs (+3 / -0)
- 新方法(+2): DrawPlayer_UseNormalLayers, PrepareDrawForFrame
- 新字段(+1): OverrideHeldProjectile

### Terraria/Graphics/SpriteViewMatrix.cs (+3 / -0)
- 新字段(+3): PixelPerfectOffset, PixelPerfectSafeZoomLevelStep, RenderZoom

### Terraria/Graphics/VirtualCamera.cs (+3 / -0)
- 新字段(+3): Center, Position, Size

### Terraria/ID/MenuID.cs (+3 / -0)
- 新字段(+3): BetterRejectionMenu, ConfirmDiscardCharacterCreation, CreditsRoll

### Terraria/IO/FileData.cs (+3 / -0)
- 新字段(+3): IsCloudSave, IsFavorite, Path

### Terraria/Initializers/UILinksInitializer.cs (+3 / -0)
- 新方法(+2): CanExecuteInputCommand, TryQuickCrafting
- 新字段(+1): RightStickGlyphBinding

### Terraria/Map/TeleportPylonsMapLayer.cs (+3 / -0)
- 新方法(+2): DrawLine, IsRevealed
- 新字段(+1): BorderSize

### Terraria/Map/WorldMap.cs (+3 / -0)
- 新方法(+3): QueueUpdate, TryGetMapPath, UnlockMapTilePretty

### Terraria/NPCSpawnParams.cs (+1 / -2)
- 新字段(+1): difficultyOverride
- 移除字段(-2): gameModeData, strengthMultiplierOverride

### Terraria/SceneMetricsScanSettings.cs (+2 / -1)
- 新字段(+2): PerspectivePlayer, ScanNPCPositions
- 移除字段(-1): ScanOreFinderData

### Terraria/Social/SocialAPI.cs (+3 / -0)
- 新字段(+3): Mode, Platform, Workshop

### Terraria/UI/Chat/ChatManager.cs (+3 / -0)
- 新方法(+2): LayoutSnippets, MayNeedParsing
- 新字段(+1): DebugCommands

### Terraria/UI/Chat/TextSnippet.cs (+0 / -3)
- 移除方法(-2): GetStringLength, Update
- 移除字段(-1): Scale

### Terraria/UI/Gamepad/GamepadPageID.cs (+3 / -0)
- 新字段(+3): ClaimBannersBig, ClaimBannersSmall, NewCrafting

### Terraria/Utilities/UnifiedRandom.cs (+2 / -1)
- 新方法(+2): Peek, SetSeed
- 移除字段(-1): inextp

### Terraria/WorldBuilding/ShapeData.cs (+3 / -0)
- 新方法(+2): AddBounds, RemoveBounds
- 新字段(+1): Count

### Terraria/WorldBuilding/WorldUtils.cs (+3 / -0)
- 新方法(+3): ClampToWorldBorders, GetWorldPlayArea, WallFrame

### Terraria/Audio/CustomSoundStyle.cs (+2 / -0)
- 新字段(+2): IsTrackable, MaxTrackedInstances

### Terraria/DataStructures/BufferPool.cs (+2 / -0)
- 新字段(+2): HUGE_BUFFER_SIZE, HugeBufferQueue

### Terraria/DataStructures/CachedBuffer.cs (+2 / -0)
- 新字段(+2): IsActive, Length

### Terraria/GameContent/Bestiary/CommonEnemyUICollectionInfoProvider.cs (+2 / -0)
- 新方法(+1): GetKillCountNeeded
- 新字段(+1): _killCountNeededToFullyUnlock

### Terraria/GameContent/CoinLossRevengeSystem.cs (+2 / -0)
- 新字段(+2): RespawnAttemptLocked, UniqueID

### Terraria/GameContent/Creative/CreativeItemSacrificesCatalog.cs (+1 / -1)
- 新字段(+1): SacrificeCountNeededByItemId
- 移除方法(-1): FillListOfItemsThatCanBeObtainedInfinitely

### Terraria/GameContent/ItemDropRules/Chains.cs (+1 / -1)
- 新字段(+1): hideLootReport
- 移除字段(-1): _hideLootReport

### Terraria/GameContent/ItemDropRules/CommonDropWithRerolls.cs (+1 / -1)
- 新字段(+1): timesToRoll
- 移除字段(-1): _timesToRoll

### Terraria/GameContent/ItemDropRules/DropLocalPerClientAndResetsNPCMoneyTo0.cs (+1 / -1)
- 新字段(+1): condition
- 移除字段(-1): _condition

### Terraria/GameContent/ItemDropRules/DropPerPlayerOnThePlayer.cs (+1 / -1)
- 新字段(+1): condition
- 移除字段(-1): _condition

### Terraria/GameContent/ItemDropRules/ItemDropWithConditionRule.cs (+1 / -1)
- 新字段(+1): condition
- 移除字段(-1): _condition

### Terraria/GameContent/ItemDropRules/LeadingConditionRule.cs (+1 / -1)
- 新字段(+1): condition
- 移除字段(-1): _condition

### Terraria/GameContent/ItemDropRules/MechBossSpawnersDropRule.cs (+1 / -1)
- 新字段(+1): dummyCondition
- 移除字段(-1): _dummyCondition

### Terraria/GameContent/Personalities/PersonalityDatabase.cs (+2 / -0)
- 新方法(+1): GetByNPCID
- 新字段(+1): _trashEntry

### Terraria/GameContent/PlayerQueenSlimeMountTextureContent.cs (+1 / -1)
- 新方法(+1): HandleUseRequest
- 移除方法(-1): HandleUseReqest

### Terraria/GameContent/PlayerRainbowWingsTextureContent.cs (+1 / -1)
- 新方法(+1): HandleUseRequest
- 移除方法(-1): HandleUseReqest

### Terraria/GameContent/PlayerSittingHelper.cs (+2 / -0)
- 新方法(+1): TryGetSittingBlock
- 新字段(+1): details

### Terraria/GameContent/PlayerTitaniumStormBuffTextureContent.cs (+1 / -1)
- 新方法(+1): HandleUseRequest
- 移除方法(-1): HandleUseReqest

### Terraria/GameContent/RGB/BlizzardShader.cs (+2 / -0)
- 新字段(+2): _timeScaleX, _timeScaleY

### Terraria/GameContent/Skies/AmbientSky.cs (+2 / -0)
- 新方法(+1): Helper_GetOpacityWithAccountingForBackgroundsOff
- 新字段(+1): SourceRectangle

### Terraria/GameContent/Skies/MoonLordSky.cs (+0 / -2)
- 移除方法(-1): UpdateMoonLordIndex
- 移除字段(-1): _moonLordIndex

### Terraria/GameContent/Skies/PartySky.cs (+0 / -2)
- 移除方法(-1): IsNearParty
- 移除字段(-1): _opacity

### Terraria/GameContent/TeleportPylonsSystem.cs (+2 / -0)
- 新方法(+1): DoesPositionHaveEnoughNPCs
- 新字段(+1): Pylons

### Terraria/GameContent/TreePaintSystemData.cs (+2 / -0)
- 新方法(+1): GetCageTopSettings
- 新字段(+1): TreeAsh

### Terraria/GameContent/UI/BigProgressBar/BrainOfCthuluBigProgressBar.cs (+1 / -1)
- 新字段(+1): _cache
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/BigProgressBar/CommonBossBigProgressBar.cs (+1 / -1)
- 新字段(+1): _cache
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/BigProgressBar/GolemHeadProgressBar.cs (+1 / -1)
- 新字段(+1): _cache
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/BigProgressBar/MartianSaucerBigProgressBar.cs (+1 / -1)
- 新字段(+1): _cache
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/BigProgressBar/MoonLordProgressBar.cs (+1 / -1)
- 新字段(+1): _cache
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/BigProgressBar/PirateShipBigProgressBar.cs (+1 / -1)
- 新字段(+1): _cache
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/BigProgressBar/TwinsBigProgressBar.cs (+1 / -1)
- 新字段(+1): _cache
- 移除字段(-1): _lifePercentToShow

### Terraria/GameContent/UI/Elements/EmoteButton.cs (+1 / -1)
- 新方法(+1): LeftClick
- 移除方法(-1): Click

### Terraria/GameContent/UI/Elements/UICreativeItemsInfiniteFilteringOptions.cs (+2 / -0)
- 新类型(+1): ColorTheme
- 新字段(+1): _theme

### Terraria/GameContent/UI/Elements/UIDifficultyButton.cs (+1 / -1)
- 新方法(+1): LeftMouseDown
- 移除方法(-1): MouseDown

### Terraria/GameContent/UI/States/UIResourcePackSelectionMenu.cs (+2 / -0)
- 新方法(+1): HandleBackButtonUsage
- 新字段(+1): _uiStateToGoBackTo

### Terraria/GameContent/UI/WiresUI.cs (+2 / -0)
- 新字段(+2): HideWires, Open

### Terraria/Graphics/Effects/GameEffect.cs (+2 / -0)
- 新字段(+2): IsLoaded, Priority

### Terraria/Graphics/Renderers/MapHeadRenderer.cs (+2 / -0)
- 新方法(+1): Reset
- 新字段(+1): IsReady

### Terraria/ID/GameModeID.cs (+2 / -0)
- 新方法(+1): IsValid
- 新字段(+1): Count

### Terraria/ID/ItemHoldStyleID.cs (+2 / -0)
- 新字段(+2): HoldOrb, HoldRadio

### Terraria/ID/ItemUseStyleID.cs (+2 / -0)
- 新字段(+2): HoldOrb, PlaySound

### Terraria/Lighting.cs (+2 / -0)
- 新方法(+1): GetColorClamped
- 新字段(+1): UsingNewLighting

### Terraria/Localization/GameCulture.cs (+2 / -0)
- 新字段(+2): IsActive, Name

### Terraria/Localization/Language.cs (+2 / -0)
- 新方法(+1): TryGetVariation
- 新字段(+1): ActiveCulture

### Terraria/Net/NetGroupInfo.cs (+2 / -0)
- 新字段(+2): HasValidInfo, Id

### Terraria/Net/NetPacket.cs (+2 / -0)
- 新字段(+2): Reader, Writer

### Terraria/Rain.cs (+2 / -0)
- 新方法(+2): GetRainFallVelocity, NewRainForced

### Terraria/Social/Steam/CoreSocialModule.cs (+2 / -0)
- 新方法(+1): SetSkipPulsing
- 新字段(+1): _skipPulsing

### Terraria/UI/EmptyDiagnosticsUI.cs (+2 / -0)
- 新方法(+2): GetLastSentRecvBytes, RotateSendRecvCounters

### Terraria/UI/Gamepad/UILinkPage.cs (+2 / -0)
- 新方法(+1): SpecialInteractionsLate
- 新字段(+1): OnSpecialInteractsLate

### Terraria/UI/InGamePopups.cs (+1 / -1)
- 新字段(+1): ShouldBeRemoved
- 移除字段(-1): _displayTextWithoutTime

### Terraria/Utilities/CrashWatcher.cs (+2 / -0)
- 新方法(+1): PrintException
- 新字段(+1): DumpPath

### Terraria/Utilities/Terraria/Utilities/FloatRange.cs (+2 / -0)
- 新方法(+2): Contains, Lerp

### Terraria/WorldBuilding/GenerationProgress.cs (+1 / -1)
- 新字段(+1): _totalWeightedProgress
- 移除字段(-1): _totalProgress

### Terraria/WorldBuilding/SimpleStructure.cs (+2 / -0)
- 新字段(+2): Height, Width

### Terraria/WorldBuilding/WorldGenRange.cs (+2 / -0)
- 新字段(+2): ScaledMaximum, ScaledMinimum

### Terraria/Achievements/AchievementCondition.cs (+1 / -0)
- 新字段(+1): IsCompleted

### Terraria/Achievements/AchievementManager.cs (+1 / -0)
- 新方法(+1): Clear

### Terraria/Chat/Commands/EmojiCommand.cs (+1 / -0)
- 新方法(+1): PrepareAliases

### Terraria/Cinematics/FrameEvent.cs (+0 / -1)
- 移除方法(-1): FrameEvent

### Terraria/CombatText.cs (+1 / -0)
- 新字段(+1): TargetScale

### Terraria/DataStructures/AnchoredEntitiesCollection.cs (+1 / -0)
- 新字段(+1): AnchoredPlayersAmount

### Terraria/DataStructures/EntityShadowInfo.cs (+1 / -0)
- 新字段(+1): HeadgearOffset

### Terraria/DataStructures/FishingAttempt.cs (+1 / -0)
- 新字段(+1): junk

### Terraria/DataStructures/PlacementHook.cs (+1 / -0)
- 新方法(+1): HookFormat

### Terraria/DataStructures/PlayerDrawHelper.cs (+1 / -0)
- 新字段(+1): DISPLAY_DOLL_DEFAULT_SKIN_COLOR

### Terraria/DataStructures/PlayerInteractionAnchor.cs (+1 / -0)
- 新字段(+1): InUse

### Terraria/DataStructures/Point16.cs (+1 / -0)
- 新方法(+1): Point

### Terraria/GameContent/Bestiary/Filters.cs (+1 / -0)
- 新字段(+1): ForcedDisplay

### Terraria/GameContent/Bestiary/NPCKillsTracker.cs (+1 / -0)
- 新字段(+1): _entryCreationLock

### Terraria/GameContent/Bestiary/NPCNetIdBestiaryInfoElement.cs (+1 / -0)
- 新字段(+1): BestiaryDisplayIndex

### Terraria/GameContent/Bestiary/NPCWasChatWithTracker.cs (+1 / -0)
- 新字段(+1): _entryCreationLock

### Terraria/GameContent/Bestiary/NPCWasNearPlayerTracker.cs (+1 / -0)
- 新字段(+1): _entryCreationLock

### Terraria/GameContent/Bestiary/SalamanderShellyDadUICollectionInfoProvider.cs (+1 / -0)
- 新字段(+1): _killCountNeededToFullyUnlock

### Terraria/GameContent/Bestiary/SortingSteps.cs (+1 / -0)
- 新字段(+1): HiddenFromSortOptions

### Terraria/GameContent/Biomes/CaveHouse/WoodHouseBuilder.cs (+1 / -0)
- 新方法(+1): Place

### Terraria/GameContent/Biomes/Desert/SurfaceMap.cs (+1 / -0)
- 新字段(+1): Width

### Terraria/GameContent/Biomes/DunesBiome.cs (+1 / -0)
- 新字段(+1): MaximumWidth

### Terraria/GameContent/Biomes/HoneyPatchBiome.cs (+1 / -0)
- 新方法(+1): TooCloseToImportantLocations

### Terraria/GameContent/Biomes/MarbleBiome.cs (+1 / -0)
- 新字段(+1): IsSolid

### Terraria/GameContent/Biomes/TerrainPass.cs (+1 / -0)
- 新字段(+1): Length

### Terraria/GameContent/Creative/CreativePowerManager.cs (+1 / -0)
- 新方法(+1): ResetPowersForPlayer

### Terraria/GameContent/Events/BirthdayParty.cs (+1 / -0)
- 新方法(+1): CheckForAchievement

### Terraria/GameContent/Events/CultistRitual.cs (+1 / -0)
- 新方法(+1): CheckFloor2

### Terraria/GameContent/Events/ScreenDarkness.cs (+1 / -0)
- 新字段(+1): frontColor

### Terraria/GameContent/Events/ScreenObstruction.cs (+1 / -0)
- 新字段(+1): lastSpeed

### Terraria/GameContent/Generation/WorldGenLegacyMethod.cs (+0 / -1)
- 移除方法(-1): WorldGenLegacyMethod

### Terraria/GameContent/HairstyleUnlocksHelper.cs (+1 / -0)
- 新字段(+1): _defeatedPlantera

### Terraria/GameContent/ItemDropRules/ItemDropRuleResolveAction.cs (+0 / -1)
- 移除方法(-1): ItemDropRuleResolveAction

### Terraria/GameContent/NetModules/NetCreativeUnlocksPlayerReportModule.cs (+0 / -1)
- 移除字段(-1): _requestItemSacrificeId

### Terraria/GameContent/ObjectInteractions/SmartInteractSystem.cs (+1 / -0)
- 新方法(+1): Clear

### Terraria/GameContent/Personalities/AllPersonalitiesModifier.cs (+1 / -0)
- 新方法(+1): ModifyShopPrice_Relationships

### Terraria/GameContent/Personalities/HelperInfo.cs (+0 / -1)
- 移除字段(-1): PrimaryPlayerBiome

### Terraria/GameContent/PortalHelper.cs (+1 / -0)
- 新方法(+1): ResetNPCSlotData

### Terraria/GameContent/PressurePlateHelper.cs (+1 / -0)
- 新字段(+1): EntityCreationLock

### Terraria/GameContent/Skies/LanternSky.cs (+1 / -0)
- 新字段(+1): FloatAdjustedSpeed

### Terraria/GameContent/TeleportHelpers.cs (+1 / -0)
- 新方法(+1): FindClosestTeleportSpotNoSpace

### Terraria/GameContent/TownRoomManager.cs (+1 / -0)
- 新字段(+1): EntityCreationLock

### Terraria/GameContent/TreePaintingSettings.cs (+1 / -0)
- 新方法(+1): ApplyShader

### Terraria/GameContent/TreeTopsInfo.cs (+0 / -1)
- 移除字段(-1): Factory

### Terraria/GameContent/UI/BigProgressBar/BigProgressBarHelper.cs (+1 / -0)
- 新方法(+1): DrawHealthText

### Terraria/GameContent/UI/BigProgressBar/BigProgressBarInfo.cs (+1 / -0)
- 新字段(+1): showText

### Terraria/GameContent/UI/Chat/ItemTagHandler.cs (+0 / -1)
- 移除方法(-1): GetStringLength

### Terraria/GameContent/UI/Chat/LegacyChatMonitor.cs (+0 / -1)
- 移除方法(-1): OnResolutionChange

### Terraria/GameContent/UI/CustomCurrencySystem.cs (+1 / -0)
- 新字段(+1): CurrencyCap

### Terraria/GameContent/UI/Elements/UIBestiaryEntryInfoPage.cs (+1 / -0)
- 新方法(+1): GetIndividualElementPriority

### Terraria/GameContent/UI/Elements/UIColoredImageButton.cs (+1 / -0)
- 新方法(+1): SetImageWithoutSettingSize

### Terraria/GameContent/UI/Elements/UIGenProgressBar.cs (+1 / -0)
- 新字段(+1): _texOuterRandom

### Terraria/GameContent/UI/Elements/UIList.cs (+1 / -0)
- 新字段(+1): Count

### Terraria/GameContent/UI/Elements/UIParticleLayer.cs (+1 / -0)
- 新方法(+1): ClearParticles

### Terraria/GameContent/UI/Elements/UISliderBase.cs (+1 / -0)
- 新方法(+1): EscapeElements

### Terraria/GameContent/UI/Elements/UIVerticalSlider.cs (+0 / -1)
- 移除字段(-1): _blipFunc

### Terraria/GameContent/UI/NewMultiplayerClosePlayersOverlay.cs (+1 / -0)
- 新字段(+1): drawScryingOrb

### Terraria/GameContent/VanillaContentValidator.cs (+1 / -0)
- 新方法(+1): GetValidImageFilePaths

### Terraria/GameContent/WellFedHelper.cs (+1 / -0)
- 新字段(+1): TimeLeft

### Terraria/GameInput/LockOnHelper.cs (+1 / -0)
- 新字段(+1): Enabled

### Terraria/Gore.cs (+1 / -0)
- 新方法(+1): DeactivateIfOutsideOfWorld

### Terraria/Graphics/Capture/CaptureManager.cs (+1 / -0)
- 新方法(+1): Dispose

### Terraria/Graphics/Capture/CaptureSettings.cs (+1 / -0)
- 新字段(+1): CameraSpaceEffects

### Terraria/Graphics/Effects/Overlay.cs (+1 / -0)
- 新字段(+1): Layer

### Terraria/Graphics/Renderers/ParticleRenderer.cs (+1 / -0)
- 新方法(+1): Clear

### Terraria/Graphics/Renderers/ReturnGatePlayerRenderer.cs (+1 / -0)
- 新方法(+1): PrepareDrawForFrame

### Terraria/Graphics/VertexColors.cs (+1 / -0)
- 新方法(+1): VertexColors

### Terraria/Graphics/WindowStateController.cs (+1 / -0)
- 新字段(+1): CanMoveWindowAcrossScreens

### Terraria/ID/GameEventClearedID.cs (+1 / -0)
- 新字段(+1): DefeatedDeerclops

### Terraria/ID/StatusID.cs (+1 / -0)
- 新字段(+1): Search

### Terraria/IO/FavoritesFile.cs (+1 / -0)
- 新字段(+1): _ourEncoder

### Terraria/IO/ResourcePackVersion.cs (+1 / -0)
- 新方法(+1): Create

### Terraria/IngameOptions.cs (+1 / -0)
- 新字段(+1): _canConsumeHover

### Terraria/Initializers/DyeInitializer.cs (+0 / -1)
- 移除方法(-1): FixRecipes

### Terraria/Localization/LanguageChangeCallback.cs (+0 / -1)
- 移除方法(-1): LanguageChangeCallback

### Terraria/Localization/LanguageSearchFilter.cs (+0 / -1)
- 移除方法(-1): LanguageSearchFilter

### Terraria/Localization/NetworkText.cs (+0 / -1)
- 移除方法(-1): GetMaxSerializedSize

### Terraria/Map/PingMapLayer.cs (+1 / -0)
- 新方法(+1): Clear

### Terraria/Modules/TileObjectBaseModule.cs (+1 / -0)
- 新字段(+1): specificRandomStyles

### Terraria/Modules/TileObjectCoordinatesModule.cs (+1 / -0)
- 新字段(+1): drawFrameOffsets

### Terraria/Modules/TilePlacementHooksModule.cs (+1 / -0)
- 新字段(+1): getStyleMethod

### Terraria/Net/Sockets/SocketConnectionAccepted.cs (+0 / -1)
- 移除方法(-1): SocketConnectionAccepted

### Terraria/Net/Sockets/SocketReceiveCallback.cs (+0 / -1)
- 移除方法(-1): SocketReceiveCallback

### Terraria/Net/Sockets/SocketSendCallback.cs (+0 / -1)
- 移除方法(-1): SocketSendCallback

### Terraria/ResolutionChangeEvent.cs (+0 / -1)
- 移除方法(-1): ResolutionChangeEvent

### Terraria/ShoppingSettings.cs (+1 / -0)
- 新字段(+1): NotInShop

### Terraria/Social/Base/ServerJoinRequestEvent.cs (+0 / -1)
- 移除方法(-1): ServerJoinRequestEvent

### Terraria/Social/Steam/CloudSocialModule.cs (+1 / -0)
- 新方法(+1): Forget

### Terraria/Social/Steam/SteamP2PWriter.cs (+0 / -1)
- 移除方法(-1): ClearUser

### Terraria/Social/WeGame/CloudSocialModule.cs (+1 / -0)
- 新方法(+1): Forget

### Terraria/Star.cs (+1 / -0)
- 新字段(+1): velocity

### Terraria/Testing/ChatCommands/ArgumentListResult.cs (+1 / -0)
- 新字段(+1): Count

### Terraria/TileChangeReceivedEvent.cs (+0 / -1)
- 移除方法(-1): TileChangeReceivedEvent

### Terraria/UI/Alignment.cs (+1 / -0)
- 新字段(+1): OffsetMultiplier

### Terraria/UI/GameInterfaceDrawMethod.cs (+0 / -1)
- 移除方法(-1): GameInterfaceDrawMethod

### Terraria/UI/Gamepad/GamepadMainMenuHandler.cs (+1 / -0)
- 新字段(+1): MoveCursorOnNextRun

### Terraria/UI/TooltipProcessor.cs (+0 / -1)
- 移除方法(-1): TooltipProcessor

### Terraria/UI/UIState.cs (+1 / -0)
- 新字段(+1): NoGamepadSupport

### Terraria/Utilities/FileUtilities.cs (+1 / -0)
- 新方法(+1): CopyToLocal

### Terraria/WorldBuilding/Shapes.cs (+1 / -0)
- 新字段(+1): _bottomHalf