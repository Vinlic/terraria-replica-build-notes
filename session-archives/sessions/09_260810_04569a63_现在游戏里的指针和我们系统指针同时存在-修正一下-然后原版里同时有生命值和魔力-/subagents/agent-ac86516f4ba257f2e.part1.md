# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T03:54:24.181Z

```
你在分析反编译源码 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs。NPC.AI() 内的 aiStyle 分发链大约在 19774-43233 行结束（aiStyle 0-127）。但 43233 行之后仍有大量代码（可能是同一 AI() 方法后段的 type 特殊处理段，或独立方法如 AI_003 等），其中有很多 Projectile.NewProjectile。名字权威：同目录 ../Terraria.ID/NPCID.cs 和 ProjectileID.cs（grep "= 数字;" 反查名字，不要猜）。

已知该后段的 Projectile.NewProjectile 行号清单：44208, 44297, 44697, 44749, 44770, 44896, 45905, 46039, 46376, 46646, 46655, 46681, 46757, 46788, 46830, 46870, 46970, 47108, 47139, 47179, 47188, 47414, 47770, 47874, 49649, 49650, 49875, 50251, 51005, 51189, 51287, 53147, 54919, 55187, 55225, 55342, 55358, 55374, 55381, 55387, 56733, 57611, 59011, 59266, 59331, 59373, 59460, 59967, 59972, 59978, 59988, 60212, 61104, 61588, 61608, 61643, 61663, 61708, 61743, 61792, 61827, 61849, 62459, 62523, 62862, 62934, 62980, 64415, 64596, 65404, 65420, 65477, 65500, 65555, 65561, 65643, 65837, 66450, 66459, 66468, 66968, 79017, 79090, 80091, 80100, 80109, 80119, 80174, 84042, 84588。

任务：
1. 先用 grep -n "private void AI_\|void AI(\|private void" NPC.cs 找出 43233 行之后的方法边界，判断这些发射点分别落在哪个方法/逻辑段（如 AI_003 战士族段约在 59464-60085）。
2. 重点：59464-60085 据信是 AI_003 战士族的发射段。请找出该段 switch/if-type 结构里覆盖的全部 NPC type 列表（已知 111/214/215/216 在里面，问：还有哪些 type？111/214/215/216 各是什么怪、发什么弹、触发条件、行号）。grep NPCID.cs 核实名字。
3. 对其余发射点，快速判断归属：用 grep -n -B20 该行找最近的 `if (type == N)` 或 `switch (type)`/`case N:` 或 aiStyle 上下文，归到具体 NPC。只展开「常规敌怪」（非 Boss 主体、非 DD2 军团 aiStyle 108-112、非南瓜/霜月 57-62、非火星 72-76/80-82、非星柱 83-85/94-97、非日食 Mothron、非海盗入侵炮弹）。符合的常规敌怪候选：骷髅神射/爆破/战术（491/492/493）、Paladin(494) 圣骑士锤、骷髅法师系、RuneWizard(172)、ChaosElemental(120)（查它瞬移是否伴随攻击/发射）、Mimic(85)、Hornet 族毒刺（210/211/215?，黄蜂 aiStyle 可能是 18 或在本段）、Corruptor(110?)、漂浮眼/僵尸系特殊发射、RaggedCaster 系。
4. Boss/事件的发射点不必展开，但请在表格里给一行「行号 | 归属 NPC | Boss/事件，跳过」的清单（可以合并归类，如「44208 等属 AI_006 Boss 段」），让调用方能对账全部行号。
5. 每个常规敌怪发射点输出一行：NPC id+名字 | 所在 aiStyle/方法 | 弹幕 id+名字（grep ProjectileID.cs 核实）| 触发条件（计时器/距离/视线/expertMode 限定）| 弹速 | 行号。

输出：纯 markdown 表格 + 简短说明，直接文字返回，不要写文件。范围大，优先把「常规敌怪」的行挖透，事件/Boss 的归类可以粗一些。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T03:54:24.182Z

```
- dataviz: Use this skill whenever you are about to create ANY chart, graph, plot, dashboard, or data visualization, in ANY output medium — an HTML or React artifact, inline SVG, plotting code in any library (matplotlib, plotly, d3, Recharts, …), an image/PNG you will render and upload, or a chart shared into Slack. Read it BEFORE writing the first line of chart code, choosing chart colors, building a stat tile / meter / KPI row, or laying out a dashboard. Produces visualizations that read as one system — elegant, accessible, consistent in light and dark — using a brand-neutral placeholder palette you swap for your own. Teaches a design-system-agnostic method: a form heuristic, a color formula with a runnable validator, mark specs, and interaction rules. A validated default palette is documented in `references/palette.md` — swap that file's values for your brand's. Triggers on: "chart", "graph", "plot", "data viz", "visualization", "dashboard", "analytics", "visualize data", "categorical colors", "sequential / diverging palette", "stat tile", "sparkline", "heatmap", "legend", "axis", "tooltip", "chart colors", "color by series".
- update-config: Use this skill to configure the Claude Code harness via settings.json. Automated behaviors ("from now on when X", "each time X", "whenever X", "before/after X") require hooks configured in settings.json - the harness executes these, not Claude, so memory/preferences cannot fulfill them. Also use for: permissions ("allow X", "add permission", "move permission to"), env vars ("set X=Y"), hook troubleshooting, or any changes to settings.json/settings.local.json files. Examples: "allow npm commands", "add bq permission to global settings", "move permission to user settings", "set DEBUG=true", "when claude stops show X". For simple settings like theme/model, suggest the /config command.
- keybindings-help: Use when the user wants to customize keyboard shortcuts, rebind keys, add chord bindings, or modify ~/.claude/keybindings.json. Examples: "rebind ctrl+s", "add a chord shortcut", "change the submit key", "customize keybindings".
- simplify: Review the changed code for reuse, simplification, efficiency, and altitude cleanups, then apply the fixes. Quality only — it does not hunt for bugs; use /code-review for that.
- fewer-permission-prompts: Scan your transcripts for common read-only Bash and MCP tool calls, then add a prioritized allowlist to project .claude/settings.json to reduce permission prompts.
- loop: Run a prompt or slash command on a recurring interval (e.g. /loop 5m /foo, defaults to 10m) - When the user wants to set up a recurring task, poll for status, or run something repeatedly on an interval (e.g. "check the deploy every 5 minutes", "keep running /babysit-prs"). Do NOT invoke for one-off tasks.
- claude-api: Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents, caching, token counting, model migration.
TRIGGER — read BEFORE opening the target file; don't skip because it "looks like a one-liner" — whenever: the prompt names Claude/Anthropic in any form (Claude, Anthropic, Fable, Opus, Sonnet, Haiku, `anthropic`, `@anthropic-ai`, `claude-*`, `us.anthropic.*`, `[1m]`); the user asks about an LLM (pricing/model choice/limits/caching) — never answer from memory; OR the task is LLM-shaped with provider unstated (agent/MCP/tool-definition/multi-agent/RAG/LLM-judge/computer-use; generate/summarize/extract/classify/rewrite/converse over NL; debugging refusals/cutoffs/streaming/tool-calls/tokens).
SKIP only when another provider is being worked on (overrides all triggers): OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama named in the query; OR `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'` over the project hits (run this grep FIRST if no provider named — don't Read the file).
- run: Launch and drive this project's app to see a change working. Use when asked to run, start, or screenshot the app, or to confirm a change works in the real app (not just tests). First looks for a project skill that already covers launching the app; otherwise falls back to built-in patterns per project type (CLI, server, TUI, Electron, browser-driven, library).
- init: Initialize a new CLAUDE.md file with codebase documentation
- review: Review a GitHub pull request; for your working diff use /code-review
- security-review: Complete a security review of the pending changes on the current branch
```


---

## 🤖 Assistant · 2026-08-11T03:54:34.684Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the file structure and finding method boundaries after line 43233 in NPC.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:54:35.303Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void\\|public void\\|internal void\\|void AI(\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1 > 43000' | head -120",
 "description": "Find method boundaries after line 43000"
}
```


---

## 🤖 Assistant · 2026-08-11T03:54:35.578Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Count lines in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:54:47.143Z

**📎 ToolResult**

```
43239:	private void AI_127_Pal()
43341:	private void AI_127_Pal_GiveRewerd()
43371:	private void AddKingSlimeTeleportCacheTiles(int x0, int x1, int y0, int y1)
43436:	private void AI_015_KingSlime()
43760:	private void AI_126_StatueMimic()
44004:	private void AI_124_ElderSlimeChest()
44009:	private void AI_125_ClumsySlimeBalloon()
44142:	private void SpawnStardustMark_StardustTower()
44230:	private void SpawnStardustMark_StardustWorm()
44338:	private void AI_123_Deerclops()
44730:	private void SpawnPassiveShadowHands(float lifePercent, int shadowHandDamage)
44754:	private void AI_123_Deerclops_ShootRubbleUp(ref NPCAimedTarget targetData, ref Point sourceTileCoords, int howMany, int distancedByThisManyTiles, float upBiasPerSpike, int whichOne)
44776:	private void AI_123_Deerclops_MakeSpikesForward(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
44812:	private void AI_123_Deerclops_MakeSpikesBothSides(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
44851:	private void AI_123_Deerclops_FindSpotToSpawnSpike(int howMany, int whichOne, ref int x, ref int y)
44887:	private void AI_123_Deerclops_TryMakingSpike(ref Point sourceTileCoords, int dir, int howMany, int whichOne, int xOffset)
44957:	private void AI_123_Deerclops_Movement(bool haltMovement, bool goHome)
45045:	private void AI_124_DeerclopsLeg()
45142:	private void AI_87_BigMimic_FireStuffCannonBurst()
45152:	private void AI_87_BigMimic_ShootItem(int itemID)
45177:	public void AI_122_PirateGhost()
45219:	public void AI_000_TransformBoundNPC(int playerID, int npcType)
45231:	private void AI_065_Butterflies()
45467:	private void AI_121_QueenSlime_FlyMovement()
45543:	private void AI_121_QueenSlime()
46178:	private void AI_120_HallowBoss_DoMagicEffect(Vector2 spot, int effectType, float progress)
46299:	private void AI_120_HallowBoss()
47304:	private void AI_120_HallowBoss_DashTo(Vector2 targetPosition)
47344:	private void AI_119_Dandelion()
47432:	private void AI_118_Seahorses()
47488:	private void AI_117_BloodNautilus()
47838:	private void BloodNautilus_CallForHelp()
47882:	private void AI_116_WaterStriders()
47944:	private void AI_115_LadyBugs()
48080:	private void AI_114_Dragonflies()
48253:	private void AI_113_WindyBalloon()
48453:	private void AI_112_FairyCritter()
49054:	private void GetBirdFlightRecommendation(int downScanRange, int upRange, Point tCoords, out bool goDownwards, out bool goUpwards)
49143:	private void AI_069_DukeFishron()
50129:	private void AI_037_Destroyer()
50626:	private void AI_005_EaterOfSouls()
51312:	public void CopyInteractions(NPC npc)
51357:	private void AI_006_Worms()
52673:	private void AI_002_FloatingEye()
53132:	private void StingerExplosion()
53195:	private void AI_007_FindGoodRestingSpot(int myTileX, int myTileY, out int floorX, out int floorY)
53264:	private void AI_007_TryForcingSitting(int homeFloorX, int homeFloorY)
53304:	public void UpdateHomeTileState(bool homeless, int x, int y)
53335:	private void AI_007_TownEntities_UpdateSavedStates()
53366:	private void AI_007_TownEntities()
55982:	private void AI_007_TownEntities_Shimmer_TeleportToLandingSpot()
56063:	private void AI_007_TownEntities_TeleportToHome(int homeFloorX, int homeFloorY)
56093:	private void AI_007_TownEntities_GetWalkPrediction(int myTileX, int homeFloorX, bool canBreathUnderWater, bool currentlyDrowning, int tileX, int tileY, out bool keepwalking, out bool avoidFalling)
56172:	private void AI_007_AttemptToPlayIdleAnimationsForPets(int petIdleChance)
56245:	private void AI_003_Fighters()
60735:	private void AI_001_Slimes()
62141:	public void AI_001_SetRainbowSlimeColor()
62266:	private void AI_110_Betsy()
62809:	private void AI_026_Unicorns()
63372:	private void AI_107_ImprovedWalkers()
64921:	private void AI_084_LunaticCultist()
65959:	private void AI_108_DivingFlyer()
66392:	private void AI_109_DarkMage()
66793:	private void AI_111_DD2LightningBug()
67003:	public void ReflectProjectiles(Rectangle myRect)
67025:	public void BloodNautilus_GetMouthPositionAndRotation(out Vector2 mouthPosition, out Vector2 mouthDirection)
67036:	public void ReflectProjectile(Projectile proj)
67197:	public void TweakSwingStats(int swingMax, int swingCurrent, int aimDir, ref Rectangle itemRectangle)
67272:	public void SetFrameSize()
67295:	public void FindFrame()
78100:	public void SimpleFlyMovement(Vector2 desiredVelocity, float moveSpeed)
78136:	public void HealEffect(int healAmount, bool broadcast = true)
78197:	public void BigMimicSpawnSmoke()
78349:	public void FaceTarget()
78355:	public void TargetClosestUpgraded(bool faceTarget = true, Vector2? checkPosition = null)
78456:	public void TargetClosest(bool faceTarget = true)
78472:	public void TargetClosest_WOF(bool faceTarget = true)
78488:	private void TryTrackingTarget(ref float distance, ref float realDist, ref bool t, ref int tankTarget, int j)
78516:	private void SetTargetTrackingValues(bool faceTarget, float realDist, int tankTarget)
78690:	public void CheckActive()
78804:	private void CheckActive_WormSegments()
78828:	public void checkDead()
79067:	public void DropTombstoneTownNPC(NetworkText deathText)
79212:	private void DropEoWLoot(bool fromCheckDead = true)
79243:	private void CheckProgressFrostMoon()
79386:	private void CheckProgressPumpkinMoon()
79628:	public void NPCLoot()
79716:	private void DoDeathEvents_BeforeLoot(Player closestPlayer)
79726:	private void NPCLoot_DropItems(Player closestPlayer)
79746:	private void DoDeathEvents_DropBossPotionsAndHearts()
79819:	private void DoDeathEvents_CelebrateBossDeath()
79837:	private void CreateBrickBoxForWallOfFlesh()
79865:	private void DoDeathEvents_SummonDungeonSpirit(Player closestPlayer)
79881:	private void DoDeathEvents_AdvanceSlimeRain(Player closestPlayer)
79899:	private void NPCLoot_DropHeals(Player closestPlayer)
79998:	private void DoDeathEvents(Player closestPlayer)
80317:	private void ViolentlySpawnNerdySlime()
80332:	private void NPCLoot_DropCommonLifeAndMana(Player closestPlayer)
80351:	private void NPCLoot_DropDungeonStuff()
80377:	private void NPCLoot_DropTempleTraps()
80384:	private void NPCLoot_DropLihzahrdStuff()
80393:	private void NPCLoot_DropAltar()
80406:	private void NPCLoot_DropHellforge()
80412:	private void NPCLoot_DropMoney(Player closestPlayer)
80603:	private void CountKillForBannersAndDropThem()
80626:	private void CountKillForAchievements()
80723:	public void DropItemInstanced(Vector2 Position, Vector2 HitboxSize, int itemType, int itemStack = 1, bool interactionRequired = true)
80749:	public void PlayerInteraction(int player)
80841:	public void ApplyInteraction(int player)
81739:	public void TransformVisuals(int oldType, int newType)
81811:	public void Teleport(Vector2 newPos, int Style = 0, int extraInfo = 0)
81850:	public void Transform(int newType, float ai0 = 0f, float ai1 = 0f, float ai2 = 0f, float ai3 = 0f, bool withReposition = true)
82366:	private void LadyBugLuck(int plr, bool GoldLadyBug = false)
82395:	private void NPCLuck()
82421:	public void HitEffect(int hitDirection = 0, double dmg = 10.0)
90966:	public void AddBuff(int type, int time, bool quiet = false)
91025:	public void RequestBuffRemoval(int buffTypeToRemove)
91042:	public void DelBuff(int buffIndex, bool quiet = false)
91092:	public void moneyPing(Vector2 pos)
91115:	public void IdleSounds()

```


---

## 👤 User(sidechain) · 2026-08-11T03:54:47.161Z

**📎 ToolResult**

```
   96369 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs

```


---

## 🤖 Assistant · 2026-08-11T03:55:09.183Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have method boundaries. Let me map the given line numbers to methods:

- 44208, 44297 → SpawnStardustMark_StardustTower (44142-44230) / SpawnStardustMark_StardustWorm (44230-44338) — Stardust pillar boss/event
- 44697, 44749, 44770 → AI_123_Deerclops (44338-44730) / SpawnPassiveShadowHands (44730) / AI_123_Deerclops_ShootRubbleUp (44754) — Deerclops boss
- 44896 → AI_123_Deerclops_MakeSpikesBothSides (44812-44851) — boss
- 45905, 46039 → AI_121_QueenSlime_FlyMovement (45467-45543) / AI_121_QueenSlime (45543-46178) — boss
- 46376, 46646, 46655, 46681, 46757, 46788, 46830, 46870, 46970, 47108, 47139, 47179, 47188, 47414 → AI_120_HallowBoss (46299-47304) — Empress of Light boss
- 47770, 47874 → AI_117_BloodNautilus (47488-47838) / BloodNautilus_CallForHelp (47838-47882) — Dreadnautilus blood moon event
- 49649, 49650 → AI_069_DukeFishron (49143-50129) — boss
- 49875 → AI_069_DukeFishron — boss
- 50251 → AI_037_Destroyer (50129-50626) — boss
- 51005, 51189, 51287 → AI_005_EaterOfSouls (50626-51312) — eater of souls/Corruptor etc? aiStyle 5. Actually AI_005_EaterOfSouls covers Eater of Souls family + Corruptor? Corruptor is aiStyle 5? Let's check. Corruptor (110) is aiStyle 5? Actually Corruptor uses aiStyle 5 (Eater of Souls AI). Hmm, Corruptor shoots vile spit. But line numbers 51005, 51189, 51287 in AI_005_EaterOfSouls. One of them could be Corruptor's vile spit. Need to check.
- 53147 → StingerExplosion (53132-53195) or AI_002_FloatingEye (52673-53132). 53147 in StingerExplosion.
- 54919, 55187, 55225, 55342, 55358, 55374, 55381, 55387 → AI_007_TownEntities (53366-55982) — town NPCs (Skeleton merchant etc). Not regular enemies.
- 56733 → AI_007_TownEntities* region (56063-56245?) Actually 56733 is in AI_003_Fighters? No, AI_003_Fighters starts at 56245. 56733 is within AI_003_Fighters.
- 57611 → AI_003_Fighters
- 59011, 59266, 59331, 59373, 59460, 59967, 59972, 59978, 59988, 60212 → AI_003_Fighters
- 61104, 61588, 61608, 61643, 61663, 61708, 61743, 61792, 61827, 61849, 62459, 62523 → AI_003_Fighters (ends 60735) — no wait AI_003_Fighters is 56245-60735, AI_001_Slimes 60735-62141. So 61104, 61588... → AI_001_Slimes; 62459, 62523 → AI_110_Betsy? No, AI_001_Slimes ends 62141, AI_110_Betsy is 62266-62809. So 62459, 62523 → AI_110_Betsy (DD2 boss, skip).
- 62862, 62934, 62980 → AI_026_Unicorns (62809-63372) — Unicorns! Regular-ish enemy (hardmode hallow). Line 62862 could be unicorn... need check. Actually AI_026_Unicorns is unicorns only, they don't shoot. Hmm, maybe these are in a switch(type) — AI_026 covers some other NPCs? Let me check.
- 64415, 64596 → AI_107_ImprovedWalkers (63372-64921) — ImprovedWalkers covers wolves, mimics? Actually aiStyle 107? Hmm. AI_107_ImprovedWalkers - covers possessed... let me check.
- 65404, 65420, 65477, 65500, 65555, 65561, 65643, 65837 → AI_084_LunaticCultist (64921-65959) — boss skip
- 66450, 66459, 66468 → AI_109_DarkMage (66392-66793) — DD2 event skip
- 66968 → AI_111_DD2LightningBug (66793-67003) skip
- 79017 → checkDead region? 79017 in DropTombstoneTownNPC (79067)? No, 79017 < 79067, so it's in checkDead (78828-79067). Tombstone spawn probably.
- 79090 → DropTombstoneTownNPC — tombstone
- 80091, 80100, 80109, 80119, 80174 → DoDeathEvents (79998-80317) — boss death events
- 84042, 84588 → HitEffect (82421-...) — visual effects

Also the pre-43233 segment: aiStyle dispatch chain. The task says focus on post-43233.

Now the key focus: AI_003_Fighters (56245-60735), the "warrior family" segment 59464-60085. Let me read that.

Plan:
1. Read 59464-60085 fully to extract type cases.
2. Grep NPCID.cs for names.
3. Check other fighter-segment launch points 56733, 57611, 59011, 59266, 59331, 59373, 59460, 60212.
4. Check AI_005_EaterOfSouls (Corruptor), AI_002_FloatingEye (52673-53132), AI_107_ImprovedWalkers (63372-64921), AI_026_Unicorns (62809-63372), AI_001_Slimes.

Let me read the fighter segment first.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:55:09.442Z · glm-x-preview-260804

```
方法边界已理清。现在读取关键的 AI_003_Fighters 段（59464-60085 附近）。
```


---

## 🤖 Assistant · 2026-08-11T03:55:09.900Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '59440,60100p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_003_Fighters type-switch segment"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:55:09.931Z

**📎 ToolResult**

```
		}
		if (type == 389)
		{
			if (confused)
			{
				ai[2] = -60f;
			}
			else
			{
				if (ai[2] < 20f)
				{
					ai[2] += 1f;
				}
				if (justHit)
				{
					ai[2] = -30f;
				}
				if (ai[2] == 20f && Main.netMode != 1)
				{
					ai[2] = -10 + Main.rand.Next(3) * -10;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y + 8f, direction * 6, 0f, 437, 25, 1f, Main.myPlayer);
				}
			}
		}
		if (type == 110 || type == 111 || type == 206 || type == 214 || type == 215 || type == 216 || type == 290 || type == 291 || type == 292 || type == 293 || type == 350 || type == 379 || type == 380 || type == 381 || type == 382 || (type >= 449 && type <= 452) || type == 468 || type == 481 || type == 411 || type == 409 || (type >= 498 && type <= 506) || type == 424 || type == 426 || type == 520)
		{
			bool flag16 = type == 381 || type == 382 || type == 520;
			bool flag17 = type == 426;
			bool flag18 = true;
			int num161 = -1;
			int num162 = -1;
			if (type == 411)
			{
				flag16 = true;
				num161 = 120;
				num162 = 120;
				if (ai[1] <= 220f)
				{
					flag18 = false;
				}
			}
			if (ai[1] > 0f)
			{
				ai[1] -= 1f;
			}
			bool flag19 = false;
			if (justHit)
			{
				flag19 = ai[2] > 0f;
				ai[1] = 30f;
				ai[2] = 0f;
				netUpdate = true;
			}
			int num163 = 70;
			if (type == 379 || type == 380)
			{
				num163 = 80;
			}
			if (type == 381 || type == 382)
			{
				num163 = 80;
			}
			if (type == 520)
			{
				num163 = 15;
			}
			if (type == 350)
			{
				num163 = 110;
			}
			if (type == 291)
			{
				num163 = 200;
			}
			if (type == 292)
			{
				num163 = 120;
			}
			if (type == 293)
			{
				num163 = 90;
			}
			if (type == 111)
			{
				num163 = 180;
			}
			if (type == 206)
			{
				num163 = 50;
			}
			if (type == 481)
			{
				num163 = 100;
			}
			if (type == 214)
			{
				num163 = 50;
			}
			if (type == 215)
			{
				num163 = 90;
			}
			if (type == 290)
			{
				num163 = 30;
			}
			if (type == 411)
			{
				num163 = 330;
			}
			if (type == 409)
			{
				num163 = 60;
			}
			if (type == 424)
			{
				num163 = 180;
			}
			if (type == 426)
			{
				num163 = 60;
			}
			bool flag20 = false;
			if (type == 216)
			{
				if (localAI[2] >= 20f)
				{
					flag20 = true;
					if (flag19)
					{
						localAI[3] += 1f;
					}
					int num164 = (int)localAI[3];
					num163 = Math.Max(60, 180 - num164 * 20);
				}
				else
				{
					num163 = 9;
				}
			}
			int num165 = num163 / 2;
			if (type == 424)
			{
				num165 = num163 - 1;
			}
			if (type == 426)
			{
				num165 = num163 - 1;
			}
			if (type == 411)
			{
				num165 = 220;
			}
			if (confused)
			{
				ai[2] = 0f;
			}
			if (ai[2] > 0f)
			{
				if (flag18)
				{
					TargetClosest();
				}
				if (ai[1] == (float)num165)
				{
					if (type == 216)
					{
						localAI[2] += 1f;
					}
					float num166 = 11f;
					if (type == 111)
					{
						num166 = 9f;
					}
					if (type == 206)
					{
						num166 = 7f;
					}
					if (type == 290)
					{
						num166 = 9f;
					}
					if (type == 293)
					{
						num166 = 4f;
					}
					if (type == 216)
					{
						num166 = 9f;
						if (flag20)
						{
							num166 = 15f;
						}
					}
					if (type == 214)
					{
						num166 = 10f;
					}
					if (type == 215)
					{
						num166 = 14f;
					}
					if (type == 382)
					{
						num166 = 7f;
					}
					if (type == 520)
					{
						num166 = 8f;
					}
					if (type == 409)
					{
						num166 = 4f;
					}
					if (type >= 449 && type <= 452)
					{
						num166 = 7f;
					}
					if (type == 481)
					{
						num166 = 8f;
					}
					if (type == 468)
					{
						num166 = 7.5f;
					}
					if (type == 411)
					{
						num166 = 1f;
					}
					if (type >= 498 && type <= 506)
					{
						num166 = 7f;
					}
					Vector2 chaserPosition2 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
					if (type == 481)
					{
						chaserPosition2.Y -= 14f;
					}
					if (type == 206)
					{
						chaserPosition2.Y -= 10f;
					}
					if (type == 290)
					{
						chaserPosition2.Y -= 10f;
					}
					if (type == 381 || type == 382)
					{
						chaserPosition2.Y += 6f;
					}
					if (type == 520)
					{
						chaserPosition2.Y = position.Y + 20f;
					}
					if (type >= 498 && type <= 506)
					{
						chaserPosition2.Y -= 8f;
					}
					if (type == 426)
					{
						chaserPosition2 += new Vector2(spriteDirection * 2, -12f);
						num166 = 7f;
					}
					float num167 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - chaserPosition2.X;
					float num168 = Math.Abs(num167) * 0.1f;
					if (type == 291 || type == 292)
					{
						num168 = 0f;
					}
					if (type == 215)
					{
						num168 = Math.Abs(num167) * 0.08f;
					}
					if (type == 214 || (type == 216 && !flag20))
					{
						num168 = 0f;
					}
					_ = type == 216 && flag20;
					if (type == 381 || type == 382 || type == 520)
					{
						num168 = 0f;
					}
					if (type >= 449 && type <= 452)
					{
						num168 = Math.Abs(num167) * (float)Main.rand.Next(10, 50) * 0.01f;
					}
					if (type == 468)
					{
						num168 = Math.Abs(num167) * (float)Main.rand.Next(10, 50) * 0.01f;
					}
					if (type == 481)
					{
						num168 = Math.Abs(num167) * (float)Main.rand.Next(-10, 11) * 0.0035f;
					}
					if (type >= 498 && type <= 506)
					{
						num168 = Math.Abs(num167) * (float)Main.rand.Next(1, 11) * 0.0025f;
					}
					float num169 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - chaserPosition2.Y - num168;
					if (type == 291)
					{
						num167 += (float)Main.rand.Next(-40, 41) * 0.2f;
						num169 += (float)Main.rand.Next(-40, 41) * 0.2f;
					}
					else if (type == 381 || type == 382 || type == 520)
					{
						num167 += (float)Main.rand.Next(-100, 101) * 0.4f;
						num169 += (float)Main.rand.Next(-100, 101) * 0.4f;
						num167 *= (float)Main.rand.Next(85, 116) * 0.01f;
						num169 *= (float)Main.rand.Next(85, 116) * 0.01f;
						if (type == 520)
						{
							num167 += (float)Main.rand.Next(-100, 101) * 0.6f;
							num169 += (float)Main.rand.Next(-100, 101) * 0.6f;
							num167 *= (float)Main.rand.Next(85, 116) * 0.015f;
							num169 *= (float)Main.rand.Next(85, 116) * 0.015f;
						}
					}
					else if (type == 481)
					{
						num167 += (float)Main.rand.Next(-40, 41) * 0.4f;
						num169 += (float)Main.rand.Next(-40, 41) * 0.4f;
					}
					else if (type >= 498 && type <= 506)
					{
						num167 += (float)Main.rand.Next(-40, 41) * 0.3f;
						num169 += (float)Main.rand.Next(-40, 41) * 0.3f;
					}
					else if (type == 426)
					{
						num167 += (float)Main.rand.Next(-30, 31) * 0.3f;
						num169 += (float)Main.rand.Next(-30, 31) * 0.3f;
					}
					else if (type == 214)
					{
						num167 += (float)Main.rand.Next(-45, 46);
						num169 += (float)Main.rand.Next(-45, 46);
					}
					else if (type == 216)
					{
						if (!flag20)
						{
							num167 += (float)Main.rand.Next(-50, 51);
							num169 += (float)Main.rand.Next(-50, 51);
						}
					}
					else if (type != 292)
					{
						num167 += (float)Main.rand.Next(-40, 41);
						num169 += (float)Main.rand.Next(-40, 41);
					}
					float num170 = (float)Math.Sqrt(num167 * num167 + num169 * num169);
					netUpdate = true;
					num170 = num166 / num170;
					num167 *= num170;
					num169 *= num170;
					int num171 = 35;
					int num172 = 82;
					if (type == 111)
					{
						num171 = 11;
					}
					if (type == 206)
					{
						num171 = 37;
					}
					if (type == 379 || type == 380)
					{
						num171 = 40;
					}
					if (type == 350)
					{
						num171 = 45;
					}
					if (type == 468)
					{
						num171 = 50;
					}
					if (type == 111)
					{
						num172 = 81;
					}
					if (type == 379 || type == 380)
					{
						num172 = 81;
					}
					if (type == 381)
					{
						num172 = 436;
						num171 = 24;
					}
					if (type == 382)
					{
						num172 = 438;
						num171 = 30;
					}
					if (type == 520)
					{
						num172 = 592;
						num171 = 35;
					}
					if (type >= 449 && type <= 452)
					{
						num172 = 471;
						num171 = 15;
					}
					if (type >= 498 && type <= 506)
					{
						num172 = 572;
						num171 = 14;
					}
					if (type == 481)
					{
						num172 = 508;
						num171 = 18;
					}
					if (type == 206)
					{
						num172 = 177;
					}
					if (type == 468)
					{
						num172 = 501;
					}
					if (type == 411)
					{
						num172 = 537;
						num171 = GetAttackDamage_ForProjectiles(60f, 45f);
					}
					if (type == 424)
					{
						num172 = 573;
						num171 = GetAttackDamage_ForProjectiles(60f, 45f);
					}
					if (type == 426)
					{
						num172 = 581;
						num171 = GetAttackDamage_ForProjectiles(60f, 45f);
					}
					if (type == 291)
					{
						num172 = 302;
						num171 = 100;
					}
					if (type == 290)
					{
						num172 = 300;
						num171 = 60;
					}
					if (type == 293)
					{
						num172 = 303;
						num171 = 60;
					}
					if (type == 214)
					{
						num172 = 180;
						num171 = 25;
					}
					if (type == 215)
					{
						num172 = 82;
						num171 = 35;
					}
					if (type == 292)
					{
						num171 = 50;
						num172 = 180;
					}
					if (type == 216)
					{
						num172 = 180;
						num171 = 30;
						if (flag20)
						{
							num171 = 100;
							num172 = 240;
							localAI[2] = 0f;
							localAI[3] = 0f;
						}
					}
					Player player3 = Main.player[target];
					Vector2? vector35 = null;
					if (type == 426)
					{
						vector35 = Main.rand.NextVector2FromRectangle(player3.Hitbox);
					}
					if (vector35.HasValue)
					{
						Utils.ChaseResults chaseResults2 = Utils.GetChaseResults(chaserPosition2, num166, vector35.Value, player3.velocity);
						if (chaseResults2.InterceptionHappens)
						{
							Vector2 vector36 = Utils.FactorAcceleration(chaseResults2.ChaserVelocity, chaseResults2.InterceptionTime, new Vector2(0f, 0.1f), 15);
							num167 = vector36.X;
							num169 = vector36.Y;
						}
					}
					chaserPosition2.X += num167;
					chaserPosition2.Y += num169;
					if (type == 214)
					{
						chaserPosition2.X += num167 * 1.5f;
						chaserPosition2.Y += num169 * 1.5f;
					}
					if (type == 290)
					{
						num171 = GetAttackDamage_ForProjectiles(num171, (float)num171 * 0.75f);
					}
					if (type >= 381 && type <= 392)
					{
						num171 = GetAttackDamage_ForProjectiles(num171, (float)num171 * 0.8f);
					}
					if (Main.netMode != 1)
					{
						if (type == 292)
						{
							for (int num173 = 0; num173 < 4; num173++)
							{
								num167 = player3.position.X + (float)player3.width * 0.5f - chaserPosition2.X;
								num169 = player3.position.Y + (float)player3.height * 0.5f - chaserPosition2.Y;
								num170 = (float)Math.Sqrt(num167 * num167 + num169 * num169);
								num170 = 12f / num170;
								num167 = (num167 += (float)Main.rand.Next(-40, 41));
								num169 = (num169 += (float)Main.rand.Next(-40, 41));
								num167 *= num170;
								num169 *= num170;
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer);
							}
						}
						else if (type == 411)
						{
							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer, 0f, whoAmI);
						}
						else if (type == 424)
						{
							for (int num174 = 0; num174 < 4; num174++)
							{
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X - (float)(spriteDirection * 4), base.Center.Y + 6f, (float)(-3 + 2 * num174) * 0.15f, (float)(-Main.rand.Next(0, 3)) * 0.2f - 0.1f, num172, num171, 0f, Main.myPlayer, 0f, whoAmI);
							}
						}
						else if (type == 409)
						{
							int num175 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X, (int)base.Center.Y, 410, whoAmI);
							Main.npc[num175].velocity = new Vector2(num167, -6f + num169);
						}
						else
						{
							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer);
						}
					}
					if (Math.Abs(num169) > Math.Abs(num167) * 2f)
					{
						if (num169 > 0f)
						{
							ai[2] = 1f;
						}
						else
						{
							ai[2] = 5f;
						}
					}
					else if (Math.Abs(num167) > Math.Abs(num169) * 2f)
					{
						ai[2] = 3f;
					}
					else if (num169 > 0f)
					{
						ai[2] = 2f;
					}
					else
					{
						ai[2] = 4f;
					}
				}
				if ((velocity.Y != 0f && !flag17) || ai[1] <= 0f)
				{
					ai[2] = 0f;
					ai[1] = 0f;
				}
				else if (!flag16 || (num161 != -1 && ai[1] >= (float)num161 && ai[1] < (float)(num161 + num162) && (!flag17 || velocity.Y == 0f)))
				{
					velocity.X *= 0.9f;
					spriteDirection = direction;
				}
			}
			if (type == 468 && !Main.eclipse)
			{
				flag16 = true;
			}
			else if ((ai[2] <= 0f || flag16) && (velocity.Y == 0f || flag17) && ai[1] <= 0f && !Main.player[target].dead)
			{
				bool flag21 = Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height);
				if (type == 520)
				{
					flag21 = Collision.CanHitLine(base.Top + new Vector2(0f, 20f), 0, 0, Main.player[target].position, Main.player[target].width, Main.player[target].height);
				}
				if (Main.player[target].stealth == 0f && Main.player[target].itemAnimation == 0)
				{
					flag21 = false;
				}
				if (flag21)
				{
					float num176 = 10f;
					Vector2 vector37 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
					float num177 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector37.X;
					float num178 = Math.Abs(num177) * 0.1f;
					float num179 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector37.Y - num178;
					num177 += (float)Main.rand.Next(-40, 41);
					num179 += (float)Main.rand.Next(-40, 41);
					float num180 = (float)Math.Sqrt(num177 * num177 + num179 * num179);
					float num181 = 700f;
					if (type == 214)
					{
						num181 = 500f;
					}
					if (type == 215)
					{
						num181 = 650f;
					}
					if (type >= 498 && type <= 506)
					{
						num181 = 190f;
					}
					if (type >= 449 && type <= 452)
					{
						num181 = 200f;
					}
					if (type == 481)
					{
						num181 = 400f;
					}
					if (type == 468)
					{
						num181 = 400f;
					}
					if (num180 < num181)
					{
						netUpdate = true;
						velocity.X *= 0.5f;
						num180 = num176 / num180;
						num177 *= num180;
						num179 *= num180;
						ai[2] = 3f;
						ai[1] = num163;
						if (Math.Abs(num179) > Math.Abs(num177) * 2f)
						{
							if (num179 > 0f)
							{
								ai[2] = 1f;
							}
							else
							{
								ai[2] = 5f;
							}
						}
						else if (Math.Abs(num177) > Math.Abs(num179) * 2f)
						{
							ai[2] = 3f;
						}
						else if (num179 > 0f)

```


---

## 🤖 Assistant · 2026-08-11T03:55:15.907Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the big fighter ranged-attack block. The types: 110, 111, 206, 214, 215, 216, 290, 291, 292, 293, 350, 379, 380, 381, 382, 449-452, 468, 481, 411, 409, 498-506, 424, 426, 520.

Also before that: type 389 shoots projectile 437 (that's at ~59464). Wait, the 389 block starts at 59440ish. Line 59460 Projectile.NewProjectile with proj 437 — that's type 389. Which NPC is 389? Probably "Salamander"? No. Let me grep NPCID.cs.

Note type 110 is in this block! 110 = Corruptor? Let me verify. Actually 111 = Corruptor? Let me grep NPCID.cs for all these.

Let me get names for: 110, 111, 206, 214, 215, 216, 290, 291, 292, 293, 350, 379, 380, 381, 382, 389, 449-452, 468, 481, 411, 409, 410, 498-506, 424, 426, 520, and projectiles 437, 436, 438, 592, 471, 572, 508, 177, 501, 537, 573, 581, 302, 300, 303, 180, 82, 240.

Also I need to check where the launch point lines fall. The block I read covers roughly 59464-60100. NewProjectile lines within it: 59460 (type 389 → proj 437), and the main ones at 59967, 59972, 59978, 59988, 60212. Wait the task lists 59967, 59972, 59978, 59988, 60212 in fighters. Let me find exact line numbers of NewProjectile in the fighter method.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:55:16.170Z · glm-x-preview-260804

```
核心段已拿到。现在核实 NPCID/ProjectileID 名字，并定位 AI_003_Fighters 内全部发射行号。
```


---

## 🤖 Assistant · 2026-08-11T03:55:16.677Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Projectile.NewProjectile\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1 >= 56245 && $1 <= 60735'",
 "description": "List NewProjectile lines within AI_003_Fighters"
}
```


---

## 🤖 Assistant · 2026-08-11T03:55:17.667Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 110 111 206 214 215 216 290 291 292 293 350 379 380 381 382 389 409 410 411 424 426 449 450 451 452 468 481 498 506 520; do grep -n \"= $n;\" NPCID.cs | head -3; done",
 "description": "Look up NPC names by id"
}
```


---

## 🤖 Assistant · 2026-08-11T03:55:18.863Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 82 177 180 240 300 302 303 436 437 438 471 501 508 537 572 573 581 592; do grep -n \"= $n;\" ProjectileID.cs | head -3; done",
 "description": "Look up projectile names by id"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:55:20.857Z

**📎 ToolResult**

```
56733:						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center5.X, center5.Y, v.X, v.Y, 909, num20, 1f, Main.myPlayer);
57611:					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, position.Y + (float)(width / 4), vector22.X, vector22.Y, 498, (int)((double)damage * 0.15), 1f, Main.myPlayer);
59011:					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition.X, chaserPosition.Y, vector30.X, vector30.Y, 577, attackDamage_ForProjectiles, 1f, Main.myPlayer);
59266:					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector32.X, vector32.Y, 472, attackDamage_ForProjectiles2, 0f, Main.myPlayer);
59331:				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector33.X, vector33.Y, num137, num138, num141, num140, 0f, Main.myPlayer);
59373:					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector34.X, vector34.Y, num144, num145, num149, num148, 0f, Main.myPlayer);
59460:					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y + 8f, direction * 6, 0f, 437, 25, 1f, Main.myPlayer);
59967:								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer);
59972:							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer, 0f, whoAmI);
59978:								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X - (float)(spriteDirection * 4), base.Center.Y + 6f, (float)(-3 + 2 * num174) * 0.15f, (float)(-Main.rand.Next(0, 3)) * 0.2f - 0.1f, num172, num171, 0f, Main.myPlayer, 0f, whoAmI);
59988:							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer);
60212:					int num187 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector38.X, vector38.Y, num185, num186, 75, 80, 0f, Main.myPlayer);

```


---

## 👤 User(sidechain) · 2026-08-11T03:55:30.174Z

**📎 ToolResult**

```
11285:	public const short SkeletonArcher = 110;
11287:	public const short GoblinArcher = 111;
11477:	public const short IcyMerman = 206;
11493:	public const short PirateDeadeye = 214;
11495:	public const short PirateCrossbower = 215;
11497:	public const short PirateCaptain = 216;
11645:	public const short Paladin = 290;
11647:	public const short SkeletonSniper = 291;
11649:	public const short TacticalSkeleton = 292;
11651:	public const short SkeletonCommando = 293;
11765:	public const short ElfArcher = 350;
11823:	public const short CultistArcherBlue = 379;
11825:	public const short CultistArcherWhite = 380;
11827:	public const short BrainScrambler = 381;
11829:	public const short RayGunner = 382;
11843:	public const short GigaZapper = 389;
11883:	public const short StardustSpiderBig = 409;
11885:	public const short StardustSpiderSmall = 410;
11887:	public const short StardustSoldier = 411;
11911:	public const short NebulaSoldier = 424;
11915:	public const short VortexHornetQueen = 426;
11959:	public const short BoneThrowingSkeleton = 449;
11961:	public const short BoneThrowingSkeleton2 = 450;
11963:	public const short BoneThrowingSkeleton3 = 451;
11965:	public const short BoneThrowingSkeleton4 = 452;
11997:	public const short DrManFly = 468;
12023:	public const short GreekSkeleton = 481;
12057:	public const short Salamander = 498;
12073:	public const short Salamander9 = 506;
12105:	public const short MartianWalker = 520;

```


---

## 👤 User(sidechain) · 2026-08-11T03:55:36.433Z

**📎 ToolResult**

```
524:	public const short FlamingArrow = 82;
714:	public const short IcewaterSpit = 177;
720:	public const short BulletDeadeye = 180;
840:	public const short CannonballHostile = 240;
960:	public const short PaladinsHammerHostile = 300;
964:	public const short SniperBullet = 302;
966:	public const short RocketSkeleton = 303;
1232:	public const short BrainScramblerBolt = 436;
1234:	public const short GigaZapperSpear = 437;
1236:	public const short RayGunnerLaser = 438;
1302:	public const short SkeletonBone = 471;
1362:	public const short DrManFlyFlask = 501;
1376:	public const short JavelinHostile = 508;
1434:	public const short StardustSoldierLaser = 537;
1504:	public const short SalamanderSpit = 572;
1506:	public const short NebulaBolt = 573;
1522:	public const short VortexAcid = 581;
1544:	public const short MartianWalkerLaser = 592;

```


---

## 🤖 Assistant · 2026-08-11T03:55:40.506Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at the other fighter-segment launch lines: 56733, 57611, 59011, 59266, 59331, 59373, 60212. Get context (which type condition).

Also need: 52673-53132 AI_002_FloatingEye; 53147 StingerExplosion; 50626-51312 AI_005_EaterOfSouls (51005, 51189, 51287); 62809-63372 AI_026_Unicorns (62862, 62934, 62980); 63372-64921 AI_107_ImprovedWalkers (64415, 64596); 60735-62141 AI_001_Slimes (61104, 61588...).

Let me get context for these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:55:41.818Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for L in 56733 57611 59011 59266 59331 59373 60212; do echo \"=== $L ===\"; sed -n \"$((L-45)),$((L))p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"type ==\\|case \\|aiStyle\\|== 0\\|type >=\\|for (\\|if (\" | tail -15; done",
 "description": "Context around fighter launch lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:55:48.230Z

**📎 ToolResult**

```
=== 56733 ===
8:			if (ai[2] == 0f)
11:				if (flag2 && Collision.CanHit(player, this))
21:				if (ai[2] < (float)num17)
25:					if ((double)Math.Abs(velocity.X) < 0.001)
29:					if (Math.Abs(velocity.Y) > 1f)
33:					if (ai[2] == (float)(num17 - num18 / 2) && Main.netMode != 1 && !player.Hitbox.Intersects(base.Hitbox) && Collision.CanHit(player, this))
38:						if (vector5.HasNaNs())
=== 57611 ===
6:				if (num68 > 1)
8:					for (int num70 = 0; num70 < 100; num70++)
12:						for (num72 = num71; num72 == num71; num72 = Main.rand.Next(num68))
21:				for (int num74 = 0; num74 < num68; num74++)
28:				for (int num75 = 0; num75 < num67; num75++)
33:					if (num68 > 0)
39:					if (num68 > 0)
=== 59011 ===
4:			if (ai[3] < 0f)
11:			if (ai[3] >= 0f && ai[3] <= (float)num118)
18:			if (ai[3] >= (float)(num118 + 1) && (ai[3] += 1f) >= (float)(num118 + num119))
23:			if (Main.netMode != 1 && ai[3] == (float)num118)
30:				if (vector28.HasNaNs())
36:				if (chaseResults.InterceptionHappens)
43:				for (int num123 = 0; num123 < 4; num123++)
=== 59266 ===
5:		else if (type == 428)
7:			if (velocity.Y == 0f)
16:		if (type == 159 && Main.netMode != 1)
21:			if ((float)Math.Sqrt(num133 * num133 + num134 * num134) > 300f)
26:		if (Main.netMode != 1)
28:			if (Main.expertMode && target >= 0 && (type == 163 || type == 238 || type == 236 || type == 237) && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
31:				if (justHit)
34:					if (localAI[0] < 0f)
39:				if (localAI[0] > (float)Main.rand.Next(180, 900))
=== 59331 ===
1:				case 530:
5:				if (num135 != -1 && NPCCanStickToWalls() && TryMoveToTransformableSpaceInto(num135))
11:		if (type == 243)
13:			if (justHit && Main.rand.Next(3) == 0)
17:			if (ai[2] < 0f)
21:			if (confused)
29:			if (Main.netMode != 1 && ai[2] >= num136 && velocity.Y == 0f && !Main.player[target].dead && !Main.player[target].frozen && ((direction > 0 && base.Center.X < Main.player[target].Center.X) || (direction < 0 && base.Center.X > Main.player[target].Center.X)) && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
=== 59373 ===
8:		if (type == 251)
10:			if (justHit)
14:			if (ai[2] < 0f)
18:			if (confused)
26:			if (Main.netMode != 1 && ai[2] >= num142 && velocity.Y == 0f && !Main.player[target].dead && !Main.player[target].frozen && ((direction > 0 && base.Center.X < Main.player[target].Center.X) || (direction < 0 && base.Center.X > Main.player[target].Center.X)) && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
37:				if (num146 < (float)num147)
=== 60212 ===
5:				else if (velocity.X < num182 && direction == 1)
8:					if (velocity.X > num182)
13:				else if (velocity.X > 0f - num182 && direction == -1)
16:					if (velocity.X < 0f - num182)
22:			if (type == 520)
25:				if (localAI[2] >= 6f)
32:		if (type == 109 && Main.netMode != 1 && !Main.player[target].dead)
34:			if (justHit)
39:			if (ai[2] > 60f)
42:				if (Main.rand.Next(5) != 0 || AnyNPCs(378))

```


---

## 🤖 Assistant · 2026-08-11T03:55:55.561Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Need more specific context. Let me look at each individually with wider windows:

- 56733: find enclosing type condition. Let me grep upward for "type ==" before 56733.
- 57611: same.
- 59011: type 491? Let me check. ai[3] usage... need context.
- 59266: type == 428 (Nailhead?) — 428. And type 159 (Ragged Caster?), 163/238/236/237 (RaggedCaster variants + Necromancer?). Interesting — expertMode Ragged Caster.
- 59331: type 243? and case 530 above. Actually the context grep shows `if (type == 243)` at line 59319ish (line 13 of the 45-line window = 59331-45+13 = 59299). Hmm, that's before. Wait the window was 59286-59331. The `if (type == 243)` is at ~59298, and launch at 59331 is inside that type-243 block. But there's also `case 530:` at 59286. Let me read precisely.
- 59373: type == 251 block (line 59373-45+8 = 59336). So type 251.
- 60212: type == 109 block? At line 60212-45+32 = 60199 `if (type == 109 ...)`. So launch at 60212 is within type 109 block. 109 = Cursed Skull? Let me check: CursedSkull = 109? Hmm. Actually let me grep. Also 56733 etc.

Let me read the specific regions.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:55:56.802Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for L in 56733 57611 59011; do echo \"===== $L =====\"; awk -v L=$L 'NR>=L-200 && NR<=L {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep \"type ==\\|type >=\\|case \\|aiStyle ==\\|Main.pumpkinMoon\\|frostMoon\\|solarEclipse\\|eclipse\" | tail -8; done",
 "description": "Find enclosing type conditions for three launch lines"
}
```


---

## 🤖 Assistant · 2026-08-11T03:55:57.311Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '59266,59380p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read 59266-59380 raw"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:56:02.966Z

**📎 ToolResult**

```
===== 56733 =====
56575: 		if (type == 379 || type == 380)
56616: 		if (type == 383 && ai[2] == 0f && localAI[0] == 0f && Main.netMode != 1)
56625: 		if (type == 383)
56628: 			if (num14 != -1 && Main.npc[num14].active && Main.npc[num14].type == 384)
56646: 		if (type == 482)
56685: 		if (type == 631)
===== 57611 =====
57503: 		case 501:
57504: 		case 502:
57505: 		case 503:
57506: 		case 504:
57507: 		case 505:
57508: 		case 506:
57509: 		case 520:
57547: 		if (type == 463 && Main.netMode != 1)
===== 59011 =====
58814: 		else if (type == 526)
58819: 		else if (type == 527)
58824: 		else if (type == 415)
58829: 				if (Main.npc[num110].active && Main.npc[num110].type == 416 && Main.npc[num110].ai[0] == (float)whoAmI)
58836: 		else if (type == 258)
58865: 		else if (type == 425)
58942: 					if (num117 != whoAmI && Main.npc[num117].active && Main.npc[num117].type == type && Math.Abs(position.X - Main.npc[num117].position.X) + Math.Abs(position.Y - Main.npc[num117].position.Y) < (float)width)

```


---

## 👤 User(sidechain) · 2026-08-11T03:56:03.004Z

**📎 ToolResult**

```
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector32.X, vector32.Y, 472, attackDamage_ForProjectiles2, 0f, Main.myPlayer);
				}
			}
			if (velocity.Y == 0f)
			{
				int num135 = -1;
				switch (type)
				{
				case 164:
					num135 = 165;
					break;
				case 236:
					num135 = 237;
					break;
				case 163:
					num135 = 238;
					break;
				case 239:
					num135 = 240;
					break;
				case 530:
					num135 = 531;
					break;
				}
				if (num135 != -1 && NPCCanStickToWalls() && TryMoveToTransformableSpaceInto(num135))
				{
					Transform(num135, 0f, 0f, 0f, 0f, withReposition: false);
				}
			}
		}
		if (type == 243)
		{
			if (justHit && Main.rand.Next(3) == 0)
			{
				ai[2] -= Main.rand.Next(30);
			}
			if (ai[2] < 0f)
			{
				ai[2] = 0f;
			}
			if (confused)
			{
				ai[2] = 0f;
			}
			ai[2] += 1f;
			float num136 = Main.rand.Next(30, 900);
			num136 *= (float)life / (float)lifeMax;
			num136 += 30f;
			if (Main.netMode != 1 && ai[2] >= num136 && velocity.Y == 0f && !Main.player[target].dead && !Main.player[target].frozen && ((direction > 0 && base.Center.X < Main.player[target].Center.X) || (direction < 0 && base.Center.X > Main.player[target].Center.X)) && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
			{
				Vector2 vector33 = new Vector2(position.X + (float)width * 0.5f, position.Y + 20f);
				vector33.X += 10 * direction;
				float num137 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector33.X;
				float num138 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector33.Y;
				num137 += (float)Main.rand.Next(-40, 41);
				num138 += (float)Main.rand.Next(-40, 41);
				float num139 = (float)Math.Sqrt(num137 * num137 + num138 * num138);
				netUpdate = true;
				num139 = 15f / num139;
				num137 *= num139;
				num138 *= num139;
				int num140 = 32;
				int num141 = 257;
				vector33.X += num137 * 3f;
				vector33.Y += num138 * 3f;
				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector33.X, vector33.Y, num137, num138, num141, num140, 0f, Main.myPlayer);
				ai[2] = 0f;
			}
		}
		if (type == 251)
		{
			if (justHit)
			{
				ai[2] -= Main.rand.Next(30);
			}
			if (ai[2] < 0f)
			{
				ai[2] = 0f;
			}
			if (confused)
			{
				ai[2] = 0f;
			}
			ai[2] += 1f;
			float num142 = Main.rand.Next(60, 1800);
			num142 *= (float)life / (float)lifeMax;
			num142 += 15f;
			if (Main.netMode != 1 && ai[2] >= num142 && velocity.Y == 0f && !Main.player[target].dead && !Main.player[target].frozen && ((direction > 0 && base.Center.X < Main.player[target].Center.X) || (direction < 0 && base.Center.X > Main.player[target].Center.X)) && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
			{
				float num143 = 15f;
				Vector2 vector34 = new Vector2(position.X + (float)width * 0.5f, position.Y + 12f);
				vector34.X += 6 * direction;
				float num144 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector34.X;
				float num145 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector34.Y;
				num144 += (float)Main.rand.Next(-40, 41);
				num145 += (float)Main.rand.Next(-30, 0);
				float num146 = (float)Math.Sqrt(num144 * num144 + num145 * num145);
				int num147 = 700;
				if (num146 < (float)num147)
				{
					num146 = num143 / num146;
					num144 *= num146;
					num145 *= num146;
					int num148 = 30;
					short num149 = 83;
					vector34.X += num144 * 3f;
					vector34.Y += num145 * 3f;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector34.X, vector34.Y, num144, num145, num149, num148, 0f, Main.myPlayer);
					ai[2] = 0f;
					netUpdate = true;
				}
			}
		}
		if (type == 386)
		{

```


---

## 🤖 Assistant · 2026-08-11T03:56:08.963Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now:
- 59331 → type 243, proj 257, speed 15, dmg 32. What is NPC 243? Probably "AngryTrapper"? Let me grep. Actually 243 might be Clinger? Clinger shoots cursed flames. proj 257 = ? Let me check. Actually 257 could be "SpikedBalls"? Hmm. Let me grep.
- 59373 → type 251, proj 83, speed 15, dmg 30. NPC 251? Maybe "ArmoredViking"? Hmm, proj 83? Let's check. 83 = ? ProjectileID: 83 might be "SpikyBall"? Actually let me check.

Now let me look at the earlier contexts:
- 56733: nearest type cond above is `if (type == 631)` at 56685. Let me verify 56733 is inside that. Need to check the block spans. Also proj 909.
- 57611: case 501-506, 520 at 57503-57509 — but launch at 57611 might be in `if (type == 463)` block (57547). Proj 498. Let me check.
- 59011: nearest above: `else if (type == 425)` at 58865. Launch 59011 with proj 577, in ai[3] loop, 4 projectiles. 577 = ? Possibly "BloodSquid"? Hmm. Actually 577 could be... let me check. And type 425 = ? Let me check NPCID: 425 = VortexRifleman! Yes Vortex Rifleman (425) shoots. proj 577 = VortexAmmonite? Hmm. Let me grep.

Also 59266 → type 428 (proj 472), and type 159 (proj ?), and expertMode 163/238/236/237 block. Let me read 59190-59270.

Let me do these reads in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:56:09.308Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '56680,56740p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read 56680-56740"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:56:09.336Z

**📎 ToolResult**

```
			{
				ai[2] = -num16;
				netUpdate = true;
			}
		}
		if (type == 631)
		{
			if (target < 0 || target == 255 || Main.player[target].dead || !Main.player[target].active)
			{
				TargetClosest(ai[2] > 0f);
			}
			Player player = Main.player[target];
			bool flag2 = !player.dead && player.active && base.Center.Distance(player.Center) < 320f;
			int num17 = 100;
			int num18 = 32;
			if (ai[2] == 0f)
			{
				ai[3] = 65f;
				if (flag2 && Collision.CanHit(player, this))
				{
					ai[2] = num17;
					ai[3] = 0f;
					velocity.X = (float)direction * 0.01f;
					netUpdate = true;
				}
			}
			else
			{
				if (ai[2] < (float)num17)
				{
					ai[2] += 1f;
					velocity.X *= 0.9f;
					if ((double)Math.Abs(velocity.X) < 0.001)
					{
						velocity.X = 0f;
					}
					if (Math.Abs(velocity.Y) > 1f)
					{
						ai[2] = 0f;
					}
					if (ai[2] == (float)(num17 - num18 / 2) && Main.netMode != 1 && !player.Hitbox.Intersects(base.Hitbox) && Collision.CanHit(player, this))
					{
						float num19 = 8f;
						Vector2 center5 = base.Center;
						Vector2 vector5 = DirectionTo(Main.player[target].Center) * num19;
						if (vector5.HasNaNs())
						{
							vector5 = new Vector2((float)direction * num19, 0f);
						}
						int num20 = 20;
						Vector2 v = vector5 + Utils.RandomVector2(Main.rand, -0.8f, 0.8f);
						v = v.SafeNormalize(Vector2.Zero);
						v *= num19;
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center5.X, center5.Y, v.X, v.Y, 909, num20, 1f, Main.myPlayer);
					}
					if (ai[2] >= (float)num17)
					{
						ai[2] = num17;
						ai[3] = 0f;
						velocity.X = (float)direction * 0.01f;
						netUpdate = true;

```


---

## 🤖 Assistant · 2026-08-11T03:56:09.662Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '57540,57620p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read 57540-57620"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:56:09.686Z

**📎 ToolResult**

```
				netUpdate = true;
			}
			if (Main.player[target].Hitbox.Intersects(base.Hitbox))
			{
				ai[3] = 0f;
			}
		}
		if (type == 463 && Main.netMode != 1)
		{
			if (localAI[3] > 0f)
			{
				localAI[3] -= 1f;
			}
			if (justHit && localAI[3] <= 0f && Main.rand.Next(3) == 0)
			{
				localAI[3] = 30f;
				int num67 = Main.rand.Next(3, 6);
				int[] array = new int[num67];
				int num68 = 0;
				for (int num69 = 0; num69 < 255; num69++)
				{
					if (Main.player[num69].active && !Main.player[num69].dead && Collision.CanHitLine(position, width, height, Main.player[num69].position, Main.player[num69].width, Main.player[num69].height))
					{
						array[num68] = num69;
						num68++;
						if (num68 == num67)
						{
							break;
						}
					}
				}
				if (num68 > 1)
				{
					for (int num70 = 0; num70 < 100; num70++)
					{
						int num71 = Main.rand.Next(num68);
						int num72;
						for (num72 = num71; num72 == num71; num72 = Main.rand.Next(num68))
						{
						}
						int num73 = array[num71];
						array[num71] = array[num72];
						array[num72] = num73;
					}
				}
				Vector2 vector20 = new Vector2(-1f, -1f);
				for (int num74 = 0; num74 < num68; num74++)
				{
					Vector2 vector21 = Main.npc[array[num74]].Center - base.Center;
					vector21.Normalize();
					vector20 += vector21;
				}
				vector20.Normalize();
				for (int num75 = 0; num75 < num67; num75++)
				{
					float num76 = Main.rand.Next(8, 13);
					Vector2 vector22 = new Vector2(Main.rand.Next(-100, 101), Main.rand.Next(-100, 101));
					vector22.Normalize();
					if (num68 > 0)
					{
						vector22 += vector20;
						vector22.Normalize();
					}
					vector22 *= num76;
					if (num68 > 0)
					{
						num68--;
						vector22 = Main.player[array[num68]].Center - base.Center;
						vector22.Normalize();
						vector22 *= num76;
					}
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, position.Y + (float)(width / 4), vector22.X, vector22.Y, 498, (int)((double)damage * 0.15), 1f, Main.myPlayer);
				}
			}
		}
		if (type == 460)
		{
			if (velocity.Y < 0f - gravity || velocity.Y > gravity)
			{
				knockBackResist = 0f;
			}

```


---

## 🤖 Assistant · 2026-08-11T03:56:09.998Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '59190,59270p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read 59190-59270"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:56:10.025Z

**📎 ToolResult**

```
				int num132 = Utils.SelectRandom<int>(Main.rand, 161, 229);
				Dust obj7 = Main.dust[Dust.NewDust(base.Center + new Vector2((spriteDirection == 1) ? 8 : (-20), -20f), 8, 8, num132, velocity.X, velocity.Y, 100)];
				obj7.velocity = obj7.velocity / 4f + DirectionTo(Main.player[target].Top);
				obj7.scale = 1.2f;
				obj7.noLight = true;
				position -= netOffset;
			}
			if (Main.rand.Next(6) == 0)
			{
				position += netOffset;
				Dust dust5 = Main.dust[Dust.NewDust(base.Center, 2, 2, 229)];
				dust5.position = base.Center + new Vector2((spriteDirection == 1) ? 26 : (-26), 24f);
				dust5.velocity.X = 0f;
				if (dust5.velocity.Y < 0f)
				{
					dust5.velocity.Y = 0f;
				}
				dust5.noGravity = true;
				dust5.scale = 1f;
				dust5.noLight = true;
				position -= netOffset;
			}
		}
		else if (type == 185)
		{
			if (velocity.Y == 0f)
			{
				rotation = 0f;
				localAI[0] = 0f;
			}
			else if (localAI[0] == 1f)
			{
				rotation += velocity.X * 0.05f;
			}
		}
		else if (type == 428)
		{
			if (velocity.Y == 0f)
			{
				rotation = 0f;
			}
			else
			{
				rotation += velocity.X * 0.08f;
			}
		}
		if (type == 159 && Main.netMode != 1)
		{
			Vector2 vector31 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
			float num133 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector31.X;
			float num134 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector31.Y;
			if ((float)Math.Sqrt(num133 * num133 + num134 * num134) > 300f)
			{
				Transform(158);
			}
		}
		if (Main.netMode != 1)
		{
			if (Main.expertMode && target >= 0 && (type == 163 || type == 238 || type == 236 || type == 237) && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
			{
				localAI[0] += 1f;
				if (justHit)
				{
					localAI[0] -= Main.rand.Next(20, 60);
					if (localAI[0] < 0f)
					{
						localAI[0] = 0f;
					}
				}
				if (localAI[0] > (float)Main.rand.Next(180, 900))
				{
					localAI[0] = 0f;
					Vector2 vector32 = Main.player[target].Center - base.Center;
					vector32.Normalize();
					vector32 *= 8f;
					int attackDamage_ForProjectiles2 = GetAttackDamage_ForProjectiles(18f, 18f);
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector32.X, vector32.Y, 472, attackDamage_ForProjectiles2, 0f, Main.myPlayer);
				}
			}
			if (velocity.Y == 0f)
			{

```


---

## 🤖 Assistant · 2026-08-11T03:56:20.618Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
- 56733 → type 631, proj 909, speed 8, dmg 20. NPC 631? Let me grep — probably "BoneSerpent"? No. 631 might be a newer NPC (1.4.4) — maybe "Cochineal Beetle"? Hmm. Let me grep NPCID.cs.
- 57611 → type 463, proj 498 (dmg*0.15), on justHit & localAI[3]<=0 & 1/3 chance, burst 3-6 shots. NPC 463? proj 498 = ? Let me grep. Hmm, NPC 463 might be "Pinky"? No... Let me grep. Actually 463 might be "DuneSplicerHead"? Not sure. proj 498 — could be "SlimeSpike"? Let me grep.
- 59266 → expertMode types 163/238/236/237, proj 472, speed 8, dmg 18(expert GetAttackDamage). NPCs: 163, 236, 237, 238 — RaggedCaster, RaggedCasterOpen, Necromancer, NecromancerOpen? Let me verify.
- 59331 → type 243, proj 257.
- 59373 → type 251, proj 83.
- 59011 → type 425, proj 577.
- 60212 → type 109, proj 75 (80 dmg) — but wait, there's "if (Main.rand.Next(5) != 0 || AnyNPCs(378))" — this is the Cultist spawn! type 109? Hmm, 109 = CultistArcher? No, Cultist Archer is 109? Let me check. Actually line 60199 `if (type == 109 && Main.netMode != 1 && !Main.player[target].dead)` and inside checks AnyNPCs(378) — 378 is CultistBoss? No... Hmm, 109 might be "CultistArcher"? Wait earlier we found CultistArcherBlue=379, White=380. AnyNPCs(378)... 378 = CultistBoss? Actually LunaticCultist = 439. 378 might be "AncientCultistSquidhead"? Hmm.

Wait — proj 75 = ? ProjectileID 75 might be "WaterBolt"? No. Let me think: 75 could be "PinkLaser"? Actually let me just grep. Also the condition AnyNPCs(378) suggests the NPC 109 spawns "Ancient Light" (projectile) when Cultist (439?) exists... Hmm, actually 109 could be "BoneLee"? No, Bone Lee is melee. Let me grep: NPCID 109.

Actually I recall NPCID.CultistArcher... no. Let me check: 109 = "CultistArcher"? The blue/white cultist archers are 379/380. NPC 109 might be "AncientCultist"? Hmm, but the Lunatic Cultist boss is 439. 378 = CultistBoss? Let me grep both.

Let me now grep the IDs.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:56:21.518Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 631 463 163 236 237 238 243 251 425 109 378 158 159 386 428 389 409 468; do grep -n \"= $n;\" NPCID.cs | head -2; done",
 "description": "Look up NPC names for fighter segment types"
}
```


---

## 🤖 Assistant · 2026-08-11T03:56:21.889Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 909 498 472 257 83 577 75; do grep -n \"= $n;\" ProjectileID.cs | head -2; done",
 "description": "Look up projectile names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:56:28.418Z

**📎 ToolResult**

```
12327:	public const short RockGolem = 631;
11987:	public const short Nailhead = 463;
11391:	public const short BlackRecluse = 163;
11537:	public const short JungleCreeper = 236;
11539:	public const short JungleCreeperWall = 237;
11541:	public const short BlackRecluseWall = 238;
11551:	public const short IceGolem = 243;
11567:	public const short Eyezor = 251;
11913:	public const short VortexRifleman = 425;
11283:	public const short Clown = 109;
11821:	public const short ChatteringTeethBomb = 378;
11381:	public const short VampireBat = 158;
11383:	public const short Vampire = 159;
11837:	public const short MartianEngineer = 386;
11919:	public const short VortexLarva = 428;
11843:	public const short GigaZapper = 389;
11883:	public const short StardustSpiderBig = 409;
11997:	public const short DrManFly = 468;

```


---

## 👤 User(sidechain) · 2026-08-11T03:56:37.045Z

**📎 ToolResult**

```
2178:	public const short RockGolemRock = 909;
1356:	public const short Nail = 498;
1304:	public const short WebSpit = 472;
874:	public const short FrostBeam = 257;
526:	public const short EyeLaser = 83;
1514:	public const short VortexLaser = 577;
510:	public const short HappyBomb = 75;

```


---

## 🤖 Assistant · 2026-08-11T03:56:45.152Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now:
- 56733 → Rock Golem (631), proj 909 RockGolemRock, speed 8, dmg 20, range <320px + CanHit, telegraph timer 100/32.
- 57611 → Nailhead (463), proj 498 Nail, burst on justHit (1/3 chance, localAI[3] cooldown 30), speed 8-12, dmg = damage*0.15.
- 59011 → Vortex Rifleman (425), proj 577 VortexLaser, 4 shots, in ai[3] sequence.
- 59266 → Black Recluse (163/238) & Jungle Creeper (236/237), proj 472 WebSpit, speed 8, dmg 18, expertMode only, LOS, timer 180-900.
- 59331 → Ice Golem (243), proj 257 FrostBeam, speed 15, dmg 32, timer ~30-930 scaled by life.
- 59373 → Eyezor (251), proj 83 EyeLaser, speed 15, dmg 30, range<700.
- 59460 → Giga Zapper (389), proj 437 GigaZapperSpear, horizontal speed direction*6, dmg 25.
- 60212 → Clown (109), proj 75 HappyBomb, dmg 80 — need to look at trigger condition: ai[2] > 60 and rand(5)!=0 || AnyNPCs(ChatteringTeethBomb). Let me read that block to confirm.
- 59967/59972/59978/59988 → the big ranged block covering many types.

Now let me also check the remaining type-conditions inside the big block more carefully — done above. But I should also note the 58865 `else if (type == 425)` block for Vortex Rifleman and check the trigger for 59011 (ai[3] >= num118+num119 etc). Let me read 58865-59020 for the trigger.

Also need to check AI_005_EaterOfSouls (51005, 51189, 51287) — likely Corruptor Vile Spit. AI_002_FloatingEye — 52673-53132, no NewProjectile listed in range except 53147 (StingerExplosion). Wait the list has 53147 only in that area. StingerExplosion — used by Hornets? Actually "StingerExplosion" is for Queen Bee. Hmm, but let me check. Also lines 50251 (Destroyer), 49649/49650/49875 (Duke Fishron).

Also AI_107_ImprovedWalkers: 64415, 64596. AI_026_Unicorns: 62862, 62934, 62980. AI_001_Slimes: 61104, 61588, 61608, 61643, 61663, 61708, 61743, 61792, 61827, 61849.

Let me check these.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:56:46.376Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for L in 62862 62934 62980 64415 64596 53147 51005 51189 51287; do echo \"===== $L =====\"; awk -v L=$L 'NR>=L-60 && NR<=L {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep \"type ==\\|case \\|aiStyle\\|NewProjectile\\|void \\|if (Main\" | tail -10; done",
 "description": "Context for unicorn/walker/stinger/eater launch lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:56:57.960Z

**📎 ToolResult**

```
===== 62862 =====
62809: 	private void AI_026_Unicorns()
62821: 		if (type == 546)
62827: 				if (i != whoAmI && Main.npc[i].active && Main.npc[i].type == type && Math.Abs(position.X - Main.npc[i].position.X) + Math.Abs(position.Y - Main.npc[i].position.Y) < (float)width)
62852: 		if (type == 315)
62859: 				if (Main.netMode != 1 && num4 != 255)
62862: 					Projectile.NewProjectile(GetSpawnSourceForNPCFromNPCAI(), base.Center + Main.rand.NextVector2Circular(40f, 40f), new Vector2(velocity.X, Main.rand.NextFloatDirection() * 3f), 1001, attackDamage_ForProjectiles, 0f, Main.myPlayer, num4);
===== 62934 =====
62876: 				if (Main.rand.Next(3) != 0)
62915: 		if (type == 410)
62923: 					if (Main.player[j].active && !Main.player[j].dead && Main.player[j].Distance(base.Center) < 800f && Main.player[j].Center.Y < base.Center.Y && Math.Abs(Main.player[j].Center.X - base.Center.X) < 20f)
62934: 					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, (Main.rand.NextFloat() - 0.5f) * 2f, -4f - 10f * Main.rand.NextFloat(), 538, 50, 0f, Main.myPlayer);
===== 62980 =====
62923: 					if (Main.player[j].active && !Main.player[j].dead && Main.player[j].Distance(base.Center) < 800f && Main.player[j].Center.Y < base.Center.Y && Math.Abs(Main.player[j].Center.X - base.Center.X) < 20f)
62934: 					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, (Main.rand.NextFloat() - 0.5f) * 2f, -4f - 10f * Main.rand.NextFloat(), 538, 50, 0f, Main.myPlayer);
62942: 		else if (type == 423)
62980: 					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * -20), base.Center.Y, spriteDirection * -7, 0f, 575, attackDamage_ForProjectiles2, 0f, Main.myPlayer, target);
===== 64415 =====
64413: 					if (Main.netMode != 1)
64415: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector7, vector6, num12, num11, 0f, Main.myPlayer);
===== 64596 =====
64594: 							if (Main.netMode != 1)
64596: 								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector10, vector11, num12, num11, 0f, Main.myPlayer);
===== 53147 =====
53109: 		if ((type == 2 || type == 133 || type == 190 || type == 191 || type == 192 || type == 193 || type == 194) && Main.rand.Next(40) == 0)
53132: 	private void StingerExplosion()
53142: 			if (type == 176)
53147: 			int num5 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector.X, vector.Y, num4, num3, 0f, Main.myPlayer);
===== 51005 =====
50962: 		if (type == 23)
50975: 		else if (type == 139)
50991: 			if (Main.netMode != 1 && localAI[0] >= num10)
51005: 					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector.X, vector.Y, vector3.X, vector3.Y, num11, attackDamage_ForProjectiles, 0f, Main.myPlayer);
===== 51189 =====
51130: 		if (type == 42 || type == 176 || (type >= 231 && type <= 235))
51150: 			if (Main.netMode != 1)
51153: 				if (type == 176)
51157: 				if (Main.getGoodWorld)
51184: 							if (type == 176)
51189: 							int num26 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector4.X, vector4.Y, num21, num22, num25, num24, 0f, Main.myPlayer);
===== 51287 =====
51235: 		if (Main.netMode != 1)
51237: 			if (Main.getGoodWorld && type == 6 && AnyNPCs(13))
51253: 			if (type == 94 && !flag)
51269: 			if (type == 619 && !flag)
51287: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center, vector5 * 15f, 811, 35, 1f, Main.myPlayer);

```


---

## 🤖 Assistant · 2026-08-11T03:57:03.219Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting. 62862: type 315 — inside AI_026_Unicorns, but type 315 = ? Let me check. 315 could be... hmm, "BartenderUnconscious"? No. Let me grep. Actually 315 = ? In NPCID: 315 might be "SolarCrawltipedeTail"? No that's different. Let me grep.

Wait, AI_026_Unicorns covers multiple types. Let me check which types have aiStyle 26: Unicorns (172?), Wolf(172?)... Hmm. Let me check the code at 62809-62900. type 315, 410, 423, 546. Let me grep names: 315, 410 (StardustSpiderSmall), 423 (AlienHornet? Actually 423 = AlienQueen?), 546.

Also 64415/64596: the NewProjectile call has 5 args without a proj type... `Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector7, vector6, num12, num11, 0f, ...)` — that's 7 args: source, pos, vel, Type, Damage, Knockback, Owner. So proj type = num12, damage = num11. Need wider context to find num12 assignment and enclosing type.

Let me read AI_107_ImprovedWalkers region 64300-64600 selectively, and 62809-62990.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:57:03.571Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '62809,62995p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_026_Unicorns body"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:57:03.598Z

**📎 ToolResult**

```
	private void AI_026_Unicorns()
	{
		int num = 30;
		int num2 = 10;
		bool flag = false;
		bool flag2 = false;
		bool flag3 = false;
		if (velocity.Y == 0f && ((velocity.X > 0f && direction < 0) || (velocity.X < 0f && direction > 0)))
		{
			flag2 = true;
			ai[3] += 1f;
		}
		if (type == 546)
		{
			num2 = 4;
			bool flag4 = velocity.Y == 0f;
			for (int i = 0; i < Main.maxNPCs; i++)
			{
				if (i != whoAmI && Main.npc[i].active && Main.npc[i].type == type && Math.Abs(position.X - Main.npc[i].position.X) + Math.Abs(position.Y - Main.npc[i].position.Y) < (float)width)
				{
					if (position.X < Main.npc[i].position.X)
					{
						velocity.X -= 0.05f;
					}
					else
					{
						velocity.X += 0.05f;
					}
					if (position.Y < Main.npc[i].position.Y)
					{
						velocity.Y -= 0.05f;
					}
					else
					{
						velocity.Y += 0.05f;
					}
				}
			}
			if (flag4)
			{
				velocity.Y = 0f;
			}
		}
		if (type == 315)
		{
			int num3 = 480;
			if (localAI[0]++ >= (float)num3)
			{
				localAI[0] = 0f;
				int num4 = target;
				if (Main.netMode != 1 && num4 != 255)
				{
					int attackDamage_ForProjectiles = GetAttackDamage_ForProjectiles(40f, 30f);
					Projectile.NewProjectile(GetSpawnSourceForNPCFromNPCAI(), base.Center + Main.rand.NextVector2Circular(40f, 40f), new Vector2(velocity.X, Main.rand.NextFloatDirection() * 3f), 1001, attackDamage_ForProjectiles, 0f, Main.myPlayer, num4);
				}
			}
			Lighting.AddLight(base.Center, 0.4f, 0.36f, 0.2f);
			int num5 = frame.Height;
			if (num5 < 1)
			{
				num5 = 1;
			}
			int num6 = frame.Y / num5;
			if (num6 >= 4 && num6 <= 7)
			{
				Vector2 vector = base.Bottom + new Vector2(-30f, -8f);
				Vector2 vector2 = new Vector2(60f, 8f);
				if (Main.rand.Next(3) != 0)
				{
					Dust dust = Dust.NewDustPerfect(vector + new Vector2(Main.rand.NextFloat() * vector2.X, Main.rand.NextFloat() * vector2.Y), 6, velocity);
					dust.scale = 0.6f;
					dust.fadeIn = 1.1f;
					dust.noGravity = true;
					dust.noLight = true;
				}
			}
		}
		if (position.X == oldPosition.X || ai[3] >= (float)num || flag2)
		{
			ai[3] += 1f;
			flag3 = true;
		}
		else if (ai[3] > 0f)
		{
			ai[3] -= 1f;
		}
		if (ai[3] > (float)(num * num2))
		{
			ai[3] = 0f;
		}
		if (justHit)
		{
			ai[3] = 0f;
		}
		if (ai[3] == (float)num)
		{
			netUpdate = true;
		}
		Vector2 vector3 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
		float num7 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector3.X;
		float num8 = Main.player[target].position.Y - vector3.Y;
		float num9 = (float)Math.Sqrt(num7 * num7 + num8 * num8);
		if (num9 < 200f && !flag3)
		{
			ai[3] = 0f;
		}
		if (type == 410)
		{
			ai[1] += 1f;
			bool flag5 = ai[1] >= 240f;
			if (!flag5 && velocity.Y == 0f)
			{
				for (int j = 0; j < 255; j++)
				{
					if (Main.player[j].active && !Main.player[j].dead && Main.player[j].Distance(base.Center) < 800f && Main.player[j].Center.Y < base.Center.Y && Math.Abs(Main.player[j].Center.X - base.Center.X) < 20f)
					{
						flag5 = true;
						break;
					}
				}
			}
			if (flag5 && Main.netMode != 1)
			{
				for (int k = 0; k < 3; k++)
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, (Main.rand.NextFloat() - 0.5f) * 2f, -4f - 10f * Main.rand.NextFloat(), 538, 50, 0f, Main.myPlayer);
				}
				life = 0;
				HitEffect(0, 9999.0);
				active = false;
				return;
			}
		}
		else if (type == 423)
		{
			if (ai[2] == 1f)
			{
				ai[1] += 1f;
				velocity.X *= 0.7f;
				if (ai[1] < 30f)
				{
					Vector2 vector4 = base.Center + Vector2.UnitX * spriteDirection * -20f;
					Dust obj = Main.dust[Dust.NewDust(vector4, 0, 0, 242)];
					Vector2 vector5 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
					obj.position = vector4 + vector5 * 20f;
					obj.velocity = -vector5 * 2f;
					obj.scale = 0.5f + vector5.X * (float)(-spriteDirection);
					obj.fadeIn = 1f;
					obj.noGravity = true;
				}
				else if (ai[1] == 30f)
				{
					for (int l = 0; l < 20; l++)
					{
						Vector2 vector6 = base.Center + Vector2.UnitX * spriteDirection * -20f;
						Dust obj2 = Main.dust[Dust.NewDust(vector6, 0, 0, 242)];
						Vector2 vector7 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
						obj2.position = vector6 + vector7 * 4f;
						obj2.velocity = vector7 * 4f + Vector2.UnitX * Main.rand.NextFloat() * spriteDirection * -5f;
						obj2.scale = 0.5f + vector7.X * (float)(-spriteDirection);
						obj2.fadeIn = 1f;
						obj2.noGravity = true;
					}
				}
				if (velocity.X > -0.5f && velocity.X < 0.5f)
				{
					velocity.X = 0f;
				}
				if (ai[1] == 30f && Main.netMode != 1)
				{
					int attackDamage_ForProjectiles2 = GetAttackDamage_ForProjectiles(50f, 35f);
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * -20), base.Center.Y, spriteDirection * -7, 0f, 575, attackDamage_ForProjectiles2, 0f, Main.myPlayer, target);
				}
				if (ai[1] >= 60f)
				{
					ai[1] = -Main.rand.Next(320, 601);
					ai[2] = 0f;
				}
			}
			else
			{
				ai[1] += 1f;
				if (ai[1] >= 180f && num9 < 500f && velocity.Y == 0f)
				{
					flag = true;
					ai[1] = 0f;
					ai[2] = 1f;

```


---

## 🤖 Assistant · 2026-08-11T03:57:04.493Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=64330 && NR<=64600 {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"type ==\\|num12 =\\|num11 =\\|num13 =\\|case \\|if (\\|for (\" | head -60",
 "description": "Scan AI_107 walker region for type conditions"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:57:08.115Z

**📎 ToolResult**

```
4:64333: 			if (num56 < num28)
15:64344: 		if ((flag12 || flag5) && ai[0] > 0f)
19:64348: 		if (flag12 && ai[1] > 0f)
23:64352: 		if (flag5 && ai[0] > 0f)
27:64356: 		if (flag5)
29:64358: 			if (ai[0] < 0f)
34:64363: 			if (ai[0] == 0f && (velocity.Y == 0f || flag6) && targetData.Type != NPCTargetType.None && (Collision.CanHit(position, width, height, targetData.Position, targetData.Width, targetData.Height) || Collision.CanHitLine(position, width, height, targetData.Position, targetData.Width, targetData.Height)) && (targetData.Center - base.Center).Length() < num4)
39:64368: 			if (ai[0] > 0f)
42:64371: 				if (flag7)
51:64380: 				if (ai[0] == 0f)
58:64387: 		if (flag3 && ai[0] > 0f)
60:64389: 			if (flag15)
65:64394: 			if (ai[0] == (float)num9)
71:64400: 				for (int num57 = 0; num57 < num17; num57++)
75:64404: 					if (vector2.HasValue)
84:64413: 					if (Main.netMode != 1)
91:64420: 		if (flag4 && ai[0] > 0f)
93:64422: 			if (velocity.Y != 0f && ai[0] < (float)num2)
97:64426: 			if (ai[0] == (float)num)
102:64431: 		if (!flag17 && flag18)
104:64433: 			if (velocity.Y == 0f && velocity.X * (float)direction < 0f)
108:64437: 			if (position.X == oldPosition.X || ai[3] >= (float)num21 || flag19)
112:64441: 			else if (Math.Abs(velocity.X) > 0.9f && ai[3] > 0f)
116:64445: 			if (ai[3] > (float)(num21 * 10))
120:64449: 			if (justHit && !flag30)
124:64453: 			if (targetData.Hitbox.Intersects(base.Hitbox))
128:64457: 			if (ai[3] == (float)num21)
131:64460: 				if (flag30)
140:64469: 					if (type == 576 || type == 577)
144:64473: 					for (int num60 = 0; num60 < num58; num60++)
146:64475: 						if (Main.rand.Next(maxValue4) == 0)
161:64490: 		if (!flag20)
163:64492: 			if (ai[3] < (float)num21 && flag21)
165:64494: 				if (num22 > 0 && Main.rand.Next(num22) == 0)
172:64501: 				if (hasValidTarget != HasValidTarget)
177:64506: 			else if (!flag22)
179:64508: 				if (flag23)
183:64512: 				if (velocity.X == 0f)
185:64514: 					if (velocity.Y == 0f)
188:64517: 						if (ai[2] >= 2f)
197:64526: 				else if (ai[2] != 0f)
202:64531: 				if (direction == 0)
208:64537: 		if (!flag24)
210:64539: 			if (velocity.X < 0f - num23 || velocity.X > num23)
212:64541: 				if (velocity.Y == 0f)
217:64546: 			else if ((velocity.X < num23 && direction == 1) || (velocity.X > 0f - num23 && direction == -1))
222:64551: 		if (flag12)
224:64553: 			if (confused)
230:64559: 				if (ai[1] > 0f)
234:64563: 				if (justHit)
239:64568: 				if (ai[0] > 0f)
241:64570: 					if (flag15)
246:64575: 					if (ai[1] == (float)num9)
252:64581: 						for (int num61 = 0; num61 < num17; num61++)
256:64585: 							if (vector2.HasValue)
265:64594: 							if (Main.netMode != 1)
270:64599: 						if (Math.Abs(vector9.Y) > Math.Abs(vector9.X) * 2f)

```


---

## 🤖 Assistant · 2026-08-11T03:57:10.470Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
AI_107_ImprovedWalkers uses flags (flag15, flag12 etc.) determined by type. I need to read the start of AI_107 (63372+) to see which types map to flags and what num12 (projectile type) is. Let me read the beginning of the method.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:57:10.954Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '63372,63560p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_107_ImprovedWalkers head"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:57:10.986Z

**📎 ToolResult**

```
	private void AI_107_ImprovedWalkers()
	{
		//IL_175b: Unknown result type (might be due to invalid IL or missing references)
		//IL_08c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_08ca: Unknown result type (might be due to invalid IL or missing references)
		//IL_08db: Unknown result type (might be due to invalid IL or missing references)
		//IL_08e0: Unknown result type (might be due to invalid IL or missing references)
		//IL_140b: Unknown result type (might be due to invalid IL or missing references)
		//IL_1410: Unknown result type (might be due to invalid IL or missing references)
		//IL_090b: Unknown result type (might be due to invalid IL or missing references)
		//IL_092a: Unknown result type (might be due to invalid IL or missing references)
		//IL_2470: Unknown result type (might be due to invalid IL or missing references)
		//IL_14cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_1f14: Unknown result type (might be due to invalid IL or missing references)
		//IL_19fc: Unknown result type (might be due to invalid IL or missing references)
		//IL_14f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_14fd: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fba: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fbf: Unknown result type (might be due to invalid IL or missing references)
		//IL_0513: Unknown result type (might be due to invalid IL or missing references)
		//IL_0612: Unknown result type (might be due to invalid IL or missing references)
		//IL_05a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_1f40: Unknown result type (might be due to invalid IL or missing references)
		//IL_083e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fe6: Unknown result type (might be due to invalid IL or missing references)
		//IL_0feb: Unknown result type (might be due to invalid IL or missing references)
		//IL_086a: Unknown result type (might be due to invalid IL or missing references)
		//IL_10fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_1035: Unknown result type (might be due to invalid IL or missing references)
		//IL_103a: Unknown result type (might be due to invalid IL or missing references)
		//IL_1060: Unknown result type (might be due to invalid IL or missing references)
		//IL_1065: Unknown result type (might be due to invalid IL or missing references)
		//IL_112a: Unknown result type (might be due to invalid IL or missing references)
		//IL_112f: Unknown result type (might be due to invalid IL or missing references)
		//IL_1150: Unknown result type (might be due to invalid IL or missing references)
		//IL_117c: Unknown result type (might be due to invalid IL or missing references)
		//IL_1181: Unknown result type (might be due to invalid IL or missing references)
		//IL_2cee: Unknown result type (might be due to invalid IL or missing references)
		//IL_0f5d: Unknown result type (might be due to invalid IL or missing references)
		bool flag = velocity.X == 0f && velocity.Y == 0f && !justHit;
		bool flag2 = false;
		bool flag3 = false;
		bool flag4 = false;
		int num = 32;
		int num2 = 15;
		float num3 = 9f;
		bool flag5 = false;
		float num4 = 40f;
		int num5 = 30;
		int num6 = 0;
		bool flag6 = false;
		bool flag7 = true;
		float num7 = 0.9f;
		bool flag8 = false;
		bool flag9 = false;
		bool flag10 = false;
		bool flag11 = false;
		bool flag12 = false;
		bool flag13 = false;
		bool flag14 = false;
		bool flag15 = true;
		int num8 = 70;
		int num9 = num8 / 2;
		float num10 = 11f;
		Vector2 vector = Vector2.Zero;
		int num11 = 1;
		int num12 = 81;
		float num13 = 700f;
		float num14 = 0f;
		float num15 = 0.1f;
		Vector2? vector2 = null;
		float num16 = 0.5f;
		int num17 = 1;
		float num18 = 1f;
		bool flag16 = false;
		float num19 = 30f;
		float num20 = 0f;
		bool flag17 = false;
		bool flag18 = true;
		bool flag19 = false;
		int num21 = 30;
		bool flag20 = false;
		bool flag21 = false;
		bool flag22 = false;
		bool flag23 = false;
		LegacySoundStyle style = null;
		int num22 = 0;
		bool flag24 = false;
		float num23 = 1f;
		float num24 = 0.07f;
		float num25 = 0.8f;
		float num26 = width / 2 + 6;
		bool flag25 = directionY < 0;
		bool flag26 = false;
		int num27 = 1;
		bool flag27 = false;
		float num28 = 5f;
		float num29 = 3f;
		float num30 = 8f;
		float amount = 0.05f;
		float amount2 = 0.04f;
		float amount3 = 0.1f;
		bool flag28 = false;
		float num31 = 0.025f;
		NPCAimedTarget targetData = GetTargetData();
		NPCUtils.NPCTargetingMethod nPCTargetingMethod = NPCUtils.TargetClosestCommon;
		if (NPCID.Sets.BelongsToInvasionOldOnesArmy[type])
		{
			nPCTargetingMethod = NPCUtils.TargetClosestOldOnesInvasion;
		}
		if (targetData.Type == NPCTargetType.NPC && Main.npc[TranslatedTargetIndex].type == 548 && Main.npc[TranslatedTargetIndex].dontTakeDamageFromHostiles)
		{
			nPCTargetingMethod(this, faceTarget: true, null);
			targetData = GetTargetData();
		}
		if (NPCID.Sets.FighterUsesDD2PortalAppearEffect[type])
		{
			if (!targetData.Invalid)
			{
				flag2 = !Collision.CanHit(base.Center, 0, 0, targetData.Center, 0, 0) && (direction == Math.Sign(targetData.Center.X - base.Center.X) || (noGravity && Distance(targetData.Center) > 50f && base.Center.Y > targetData.Center.Y));
			}
			flag2 &= ai[0] <= 0f;
		}
		if (flag2)
		{
			if (velocity.Y == 0f || Math.Abs(targetData.Center.Y - base.Center.Y) > 800f)
			{
				noGravity = true;
				noTileCollide = true;
			}
		}
		else
		{
			noGravity = false;
			noTileCollide = false;
		}
		bool flag29 = NPCID.Sets.FighterUsesDD2PortalAppearEffect[type];
		bool flag30 = true;
		SlotId val;
		switch (type)
		{
		case 576:
		case 577:
			num22 = 700;
			style = SoundID.DD2_OgreRoar;
			num26 -= 32f;
			flag5 = true;
			num6 = 60;
			num4 = 130f;
			num5 = 44;
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			num7 = 0.7f;
			if (localAI[0] > 0f)
			{
				localAI[0] -= 1f;
			}
			if (ai[0] <= 0f)
			{
				float num34 = ai[1];
				float num35 = Distance(targetData.Center);
				if (localAI[3] >= 60f)
				{
					if (num35 <= num4 + 300f && localAI[0] <= 0f)
					{
						ai[1] = 2f;
					}
					else if (num35 > num4 + 30f)
					{
						ai[1] = 1f;
					}
					else if (!(num35 > num4))
					{
						ai[1] = 0f;
						if (num34 == 1f)
						{
							ai[0] = 0f;
						}
					}
				}
				if (num34 != ai[1])
				{
					netUpdate = true;
				}
			}
			else if (ai[1] == 2f)
			{
				localAI[0] = 300f;
			}
			switch ((int)ai[1])

```


---

## 🤖 Assistant · 2026-08-11T03:57:17.205Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
num12 default = 81 (proj type), num11 = 1 (damage). The launch at 64415 is in a block with flag3 (ai[0] > 0). Launch at 64596 is in flag12 block. I need to see the switch cases to know which types set flag3, flag12, num12, num11, num10 (speed).

Let me grep the switch cases within 63560-64100 to find where flag3/flag12/num12/num11/num10 get set.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:57:17.245Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=63560 && NR<=64340 {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"case [0-9]\\|type ==\\|num12 =\\|num11 =\\|num10 =\\|num17 =\\|flag3 =\\|flag12 =\\|flag15 =\\|flag16 =\\|num13 =\\|num19 =\\|flag14 =\\|flag5 =\\|num4 =\\|num9 =\\|num8 =\"",
 "description": "Find case assignments in AI_107 switch"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:57:23.326Z

**📎 ToolResult**

```
3:63562: 			case 0:
10:63569: 			case 2:
12:63571: 				num4 = 250f;
14:63573: 				num11 = GetAttackDamage_ForProjectiles(60f, 40f);
15:63574: 				num9 = 36;
19:63578: 				flag3 = true;
20:63579: 				num12 = 683;
21:63580: 				flag15 = false;
28:63587: 			case 1:
29:63588: 				flag3 = true;
31:63590: 				num4 = 1000f;
33:63592: 				num11 = GetAttackDamage_ForProjectiles(40f, 30f);
34:63593: 				flag15 = false;
36:63595: 				num12 = 676;
48:63607: 		case 552:
49:63608: 		case 553:
50:63609: 		case 554:
53:63612: 			flag5 = true;
55:63614: 			if (type == 553)
60:63619: 			if (type == 554)
70:63629: 		case 570:
71:63630: 		case 571:
74:63633: 			flag12 = true;
75:63634: 			flag15 = ai[1] > 40f;
76:63635: 			num8 = 60;
77:63636: 			num9 = 40;
78:63637: 			if (type == 571 && ai[1] > 10f && ai[1] <= 40f && (int)ai[1] % 6 == 0)
80:63639: 				num9 = (int)ai[1] - 1;
82:63641: 			if (type == 570 && ai[1] > 10f && ai[1] <= 40f && (int)ai[1] % 9 == 0)
84:63643: 				num9 = (int)ai[1] - 1;
86:63645: 			num12 = 671;
90:63649: 			num13 = 600f;
91:63650: 			num10 = 13f;
92:63651: 			num17 = 1;
94:63653: 			if (type == 570)
98:63657: 			num11 = GetAttackDamage_ForProjectiles(35f, 25f);
99:63658: 			if (type == 571)
101:63660: 				num11 = GetAttackDamage_ForProjectiles(60f, 45f);
117:63676: 				num13 = 1f;
121:63680: 		case 572:
122:63681: 		case 573:
251:63810: 				flag5 = true;
253:63812: 				num4 = 64f;
279:63838: 				flag5 = true;
281:63840: 				num4 = 700f;
288:63847: 		case 568:
289:63848: 		case 569:
295:63854: 			flag5 = true;
296:63855: 			num4 = 600f;
378:63937: 		case 561:
379:63938: 		case 562:
380:63939: 		case 563:
391:63950: 			flag12 = true;
392:63951: 			flag15 = ai[1] > 82f;
393:63952: 			num8 = 90;
394:63953: 			num9 = 82;
395:63954: 			num12 = 662;
396:63955: 			if (type == 563)
398:63957: 				num12 = 685;
403:63962: 			num13 = 600f;
404:63963: 			num10 = 13f;
407:63966: 				num13 = 1f;
410:63969: 			if (type == 561)
414:63973: 				num11 = GetAttackDamage_ForProjectiles(15f, 10f);
415:63974: 				num10 = 11.5f;
418:63977: 			if (type == 562)
422:63981: 				num11 = GetAttackDamage_ForProjectiles(30f, 20f);
423:63982: 				num10 = 12.2f;
426:63985: 			if (type == 563)
430:63989: 				num11 = GetAttackDamage_ForProjectiles(45f, 30f);
434:63993: 		case 555:
435:63994: 		case 556:
436:63995: 		case 557:
443:64002: 			flag12 = true;
444:64003: 			flag15 = ai[1] > 18f;
445:64004: 			num8 = 42;
446:64005: 			num9 = 18;
447:64006: 			num12 = 681;
448:64007: 			num11 = 10;
452:64011: 			num13 = 280f;
453:64012: 			num10 = 6f;
456:64015: 				num13 = 1f;
459:64018: 			if (type == 555)
463:64022: 				num11 = GetAttackDamage_ForProjectiles(20f, 15f);
465:64024: 			if (type == 556)
469:64028: 				num11 = GetAttackDamage_ForProjectiles(30f, 25f);
471:64030: 			if (type == 557)
475:64034: 				num11 = GetAttackDamage_ForProjectiles(40f, 35f);
483:64042: 		case 566:
484:64043: 		case 567:
559:64118: 		case 620:
563:64122: 			flag16 = true;
565:64124: 			num19 = 20f;
569:64128: 			flag12 = true;
570:64129: 			flag15 = ai[1] > 40f;
571:64130: 			num8 = 60;
572:64131: 			num9 = 40;
575:64134: 				num9 = (int)ai[1] - 1;
577:64136: 			num12 = 811;
582:64141: 			num13 = 600f;
583:64142: 			num10 = 13f;
584:64143: 			num17 = 1;
586:64145: 			num11 = GetAttackDamage_ForProjectiles(40f, 30f);
639:64198: 				flag12 = false;
678:64237: 				if (num52 != whoAmI && Main.npc[num52].active && Main.npc[num52].type == type && Math.Abs(position.X - Main.npc[num52].position.X) + Math.Abs(position.Y - Main.npc[num52].position.Y) < (float)width)
725:64284: 				if (type == 576 || type == 577)

```


---

## 🤖 Assistant · 2026-08-11T03:57:25.952Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need the type numbers for the switch cases. The cases are numbers. Let me read 63560-63570 to see which type the `case 0/2/1` inner switch belongs to (probably case 576/577 Ogre sub-switch), plus the case values for flag3 sets at 63578/63588. Let me read 63555-63600.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:57:26.990Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '63555,63600p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---- ; sed -n '63660,63680p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ----; sed -n '64035,64045p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read case blocks around flag3 assignments"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:57:27.059Z

**📎 ToolResult**

```
			}
			else if (ai[1] == 2f)
			{
				localAI[0] = 300f;
			}
			switch ((int)ai[1])
			{
			case 0:
				num5 = 44;
				if (ai[0] == 40f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_OgreAttack, base.Center);
				}
				break;
			case 2:
				num5 = 90;
				num4 = 250f;
				flag4 = true;
				num11 = GetAttackDamage_ForProjectiles(60f, 40f);
				num9 = 36;
				num = 56;
				num2 = 41;
				num3 = 13f;
				flag3 = true;
				num12 = 683;
				flag15 = false;
				vector = new Vector2(-direction * 20, height / 2 - 1);
				if (ai[0] == 40f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_OgreGroundPound, base.Center);
				}
				break;
			case 1:
				flag3 = true;
				num5 = 90;
				num4 = 1000f;
				num6 = 240;
				num11 = GetAttackDamage_ForProjectiles(40f, 30f);
				flag15 = false;
				vector = new Vector2(direction * 30, -70f);
				num12 = 676;
				if (ai[0] == 80f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_OgreSpit, base.Center);
				}
				break;
----
				num11 = GetAttackDamage_ForProjectiles(60f, 45f);
			}
			num23 = 0.77f;
			if (ai[0] > 0f)
			{
				if (ai[1] == 40f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_DrakinShot, base.Center);
				}
				else if (ai[1] == 60f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_DrakinBreathIn, base.Center);
				}
			}
			if (!(localAI[3] >= 60f))
			{
				num13 = 1f;
				num24 = 0.01f + localAI[3] / 60f * 0.05f;
			}
			break;
		case 572:
----
			}
			if (ai[1] == (float)num9)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_GoblinBomberThrow, base.Center);
			}
			break;
		}
		case 566:
		case 567:
		{
			DelegateMethods.v3_1 = new Vector3(0.3f, 0.05f, 0.45f) * 1.5f;

```


---

## 🤖 Assistant · 2026-08-11T03:57:38.053Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So:
- 64415 launch is in the flag3 block (ai[0] > 0, ai[0] == num9) — flag3 is only set for type 576/577 (Ogre) in its ai[1]==2 (ground pound, num12=683 = ? probably "DD2OgreSmash" wave? actually projectile 683) and ai[1]==1 (spit, num12=676 = DD2OgreSpit). DD2 Ogre — event, skip. Confirmed both flag3 cases are Ogre only → 64415 is DD2 Ogre (event).
- 64596 launch is in flag12 block — flag12 set for cases 570/571 (Drakin?), 561/562/563 (Dark Mage? no, those are DD2 goblin...), 555/556/557 (Kobold? KoboldFlyer? KoboldWalker), 620. All DD2 event NPCs. So 64596 is DD2 event, skip.

Now check names: 576 = DD2Ogre, 570/571 = DD2Drakin/DarkMage? Let me verify quickly: 561,562,563 = DD2GoblinBomber/Tinkerer? Actually: DD2GoblinBomber=561, DD2GoblinTinkerer=562, DD2GoblinSorcerer=563? and 555,556,557 = DD2KoboldFlyer/KoboldWalker/KoboldGlider? and 570,571 = DD2DarkMageApply?/DD2Drakin? 620 = DD2LightningBug? No, 66968 was DD2LightningBug. 620 = "DD2Betsy"? no Betsy=551. Hmm 620 = "WanderingEyeFish"? Let me grep: 620, 576, 570, 571, 555-557, 561-563, 683, 676, 671, 662, 685, 681, 811, 538, 575, 1001, 315, 423, 546.

Also need to check 60212 Clown block trigger conditions, and 58865-59020 Vortex Rifleman trigger, plus the AI_001_Slimes launches (61104, 61588, 61608, 61643, 61663, 61708, 61743, 61792, 61827, 61849) — Hoppin' Jack? Spiked Slimes (King Slime spawns spikes?). Actually King Slime spikes is aiStyle 49 in main chain, but 61104 etc in AI_001_Slimes — probably spiky slime ball (SpikedSlime 141?) shooting spikes. Let me check.

Also 51005 (type 139 = ?), 51189 (types 42, 176, 231-235), 51287 (type 619). Let me check:
- 50962 `if (type == 23)` (Eater of Worlds head/body - devourer), 50975 `else if (type == 139)` → 139 = ? Perhaps "Corruptor"? Actually 139... let me grep. Hmm, in 1.4, Corruptor is 110? No we found SkeletonArcher=110. Corruptor = 110? No. Let me grep Corruptor.
- 51130 `if (type == 42 || type == 176 || (type >= 231 && type <= 235))` → 42 = Demon/Eye? 42 = Demon. 176 = Queen Bee? No, Queen Bee=222. 176 = "Hornet"? Actually hornets are 42? Let me check: 42 = Demon, 176 = Hornet? Hmm NPCID.Hornet = 42? Let me grep. And 231-235 = BigHornet variants / BigStingy... Also proj used: at 51153 `if (type == 176)`. Need details.
- 51287: type 619, proj 811. And 620 nearby.

Let me grep names.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:57:39.369Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 576 570 571 555 556 557 561 562 563 620 315 423 546 139 42 176 231 235 619 42 2 133 190 194; do grep -n \"= $n;\" NPCID.cs | head -2; done; echo ---; for n in 683 676 671 662 685 681 811 538 575 1001 181 259 260 262; do grep -n \"= $n;\" ProjectileID.cs | head -2; done",
 "description": "Look up remaining NPC and projectile names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:58:09.802Z

**📎 ToolResult**

```
12217:	public const short DD2OgreT2 = 576;
12205:	public const short DD2DrakinT2 = 570;
12207:	public const short DD2DrakinT3 = 571;
12175:	public const short DD2GoblinBomberT1 = 555;
12177:	public const short DD2GoblinBomberT2 = 556;
12179:	public const short DD2GoblinBomberT3 = 557;
12187:	public const short DD2JavelinstT1 = 561;
12189:	public const short DD2JavelinstT2 = 562;
12191:	public const short DD2JavelinstT3 = 563;
12305:	public const short GoblinShark = 620;
11695:	public const short HeadlessHorseman = 315;
11909:	public const short NebulaBeast = 423;
12157:	public const short Tumbleweed = 546;
11343:	public const short Probe = 139;
11149:	public const short Hornet = 42;
11417:	public const short MossHornet = 176;
11527:	public const short HornetFatty = 231;
11535:	public const short HornetStingy = 235;
12303:	public const short BloodSquid = 619;
11149:	public const short Hornet = 42;
11069:	public const short DemonEye = 2;
11331:	public const short WanderingEye = 133;
11445:	public const short CataractEye = 190;
11453:	public const short PurpleEye = 194;
---
1726:	public const short DD2OgreSmash = 683;
1712:	public const short DD2OgreSpit = 676;
1702:	public const short DD2DrakinShot = 671;
1684:	public const short DD2JavelinHostile = 662;
1730:	public const short DD2JavelinHostileT3 = 685;
1722:	public const short DD2GoblinBomb = 681;
1982:	public const short BloodShot = 811;
1436:	public const short Twinkle = 538;
1510:	public const short NebulaSphere = 575;
2362:	public const short HorsemanPumpkin = 1001;
722:	public const short Bee = 181;
878:	public const short EyeBeam = 259;
880:	public const short HeatRay = 260;
884:	public const short GolemFist = 262;

```


---

## 🤖 Assistant · 2026-08-11T03:58:17.748Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now:
- 62862 → Headless Horseman (315), proj 1001 HorsemanPumpkin, timer 480 ticks, dmg GetAttackDamage(40/30), vel = (velocity.X, random*3), ai0 = target player index. Pumpkin Moon event → skip.
- 62934 → StardustSpiderSmall (410), proj 538 Twinkle, 3 shots upward, self-destruct. Stardust pillar event → skip.
- 62980 → NebulaBeast (423), proj 575 NebulaSphere, horizontal spriteDirection*-7. Nebula pillar → skip.
- 64415 → DD2OgreT2 (576) ground-pound/spit, event skip.
- 64596 → DD2 NPCs (Drakin 570/571, Javelinst 561-563, GoblinBomber 555-557, GoblinShark 620), event skip.
- 51005 → Probe (139) — The Destroyer's probes — laser. Boss-related (Destroyer probe). Boss segment skip. Need proj number: read 50975-51010.
- 51189 → Hornet (42), MossHornet (176), HornetFatty..Stingy (231-235) — stinger! proj num25. This is the hornet stinger launch — REGULAR enemy. Need details (speed, trigger).
- 51287 → BloodSquid (619), proj 811 BloodShot — spawned by Dreadnautilus? Actually Blood Squid is Blood Moon enemy (from Dreadnautilus? no, Blood Squid spawns from Blood Nautilus). It's event. Also type 619 in AI_005_EaterOfSouls? Interesting — that's the getGoodWorld block at 51269 `if (type == 619 && !flag)` — Blood Squid shoots BloodShot. Blood Moon event → skip probably. Also 51237 `Main.getGoodWorld && type == 6 && AnyNPCs(13)` (Eater of Worlds ftw). 51253 `if (type == 94 ...)` — 94 = Clown? No. Let me check 94 = "Clinger"? Actually 94... hmm. Not needed unless it has a NewProjectile nearby. 51287 belongs to type 619.

Let me read the Hornet block 51130-51200 fully, plus the Probe block 50975-51010, plus the Clown block 60199-60230, plus Vortex Rifleman 58865-59020, and AI_001_Slimes launch lines.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:58:18.008Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '51130,51200p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read hornet stinger block"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:58:18.040Z

**📎 ToolResult**

```
		if (type == 42 || type == 176 || (type >= 231 && type <= 235))
		{
			if (wet)
			{
				if (velocity.Y > 0f)
				{
					velocity.Y *= 0.95f;
				}
				velocity.Y -= 0.5f;
				if (velocity.Y < -4f)
				{
					velocity.Y = -4f;
				}
				TargetClosest();
			}
			if (ai[1] == 101f)
			{
				SoundEngine.PlaySound(SoundID.Item17, position);
				ai[1] = 0f;
			}
			if (Main.netMode != 1)
			{
				ai[1] += (float)Main.rand.Next(5, 20) * 0.1f * scale;
				if (type == 176)
				{
					ai[1] += (float)Main.rand.Next(5, 20) * 0.1f * scale;
				}
				if (Main.getGoodWorld)
				{
					ai[1] += (float)Main.rand.Next(5, 20) * 0.1f * scale;
				}
				if (targetData.Type == NPCTargetType.Player)
				{
					Player player = Main.player[target];
					if (player != null && player.stealth == 0f && player.itemAnimation == 0)
					{
						ai[1] = 0f;
					}
				}
				if (ai[1] >= 130f)
				{
					if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
					{
						float num20 = 8f;
						Vector2 vector4 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)(height / 2));
						float num21 = targetData.Center.X - vector4.X + (float)Main.rand.Next(-20, 21);
						float num22 = targetData.Center.Y - vector4.Y + (float)Main.rand.Next(-20, 21);
						if ((num21 < 0f && velocity.X < 0f) || (num21 > 0f && velocity.X > 0f))
						{
							float num23 = (float)Math.Sqrt(num21 * num21 + num22 * num22);
							num23 = num20 / num23;
							num21 *= num23;
							num22 *= num23;
							int num24 = (int)(10f * scale);
							if (type == 176)
							{
								num24 = (int)(30f * scale);
							}
							int num25 = 55;
							int num26 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector4.X, vector4.Y, num21, num22, num25, num24, 0f, Main.myPlayer);
							Main.projectile[num26].timeLeft = 300;
							ai[1] = 101f;
							netUpdate = true;
						}
						else
						{
							ai[1] = 0f;
						}
					}
					else
					{

```


---

## 🤖 Assistant · 2026-08-11T03:58:18.302Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '50975,51010p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read Probe laser block"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:58:18.331Z

**📎 ToolResult**

```
		else if (type == 139)
		{
			localAI[0] += 1f;
			if (ai[3] != 0f)
			{
				localAI[0] += 2f;
			}
			if (justHit)
			{
				localAI[0] = 0f;
			}
			float num10 = 120f;
			if (IsMechQueenUp)
			{
				num10 = 360f;
			}
			if (Main.netMode != 1 && localAI[0] >= num10)
			{
				localAI[0] = 0f;
				if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
				{
					int attackDamage_ForProjectiles = GetAttackDamage_ForProjectiles(25f, 22f);
					int num11 = 84;
					Vector2 vector3 = new Vector2(num4, num5);
					if (IsMechQueenUp)
					{
						Vector2 v = targetData.Center - base.Center - targetData.Velocity * 20f;
						float num12 = 8f;
						vector3 = v.SafeNormalize(Vector2.UnitY) * num12;
					}
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector.X, vector.Y, vector3.X, vector3.Y, num11, attackDamage_ForProjectiles, 0f, Main.myPlayer);
				}
			}
			int num13 = (int)position.X + width / 2;
			int num14 = (int)position.Y + height / 2;
			num13 /= 16;

```


---

## 🤖 Assistant · 2026-08-11T03:58:19.270Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for L in 61104 61588 61608 61643 61663 61708 61743 61792 61827 61849; do echo \"===== $L =====\"; awk -v L=$L 'NR>=L-25 && NR<=L {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep \"type ==\\|NewProjectile\\|case \\|if (\\|for (\" | tail -6; done",
 "description": "Context for slime-segment launch lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:58:23.962Z

**📎 ToolResult**

```
===== 61104 =====
61089: 		if (NPCID.Sets.SlimeCanContainItems[type] && ai[1] > 0f)
61091: 			if (ai[1] == 539f && Main.netMode != 1)
61094: 				if (Main.noTrapsWorld)
61098: 				if (Main.getGoodWorld)
61102: 				if (Main.rand.Next(num11) == 0 && target >= 0 && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type] && Collision.CanHit(this, Main.player[target]))
61104: 					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), (int)base.Center.X, base.Center.Y, direction * 12, 0f, 1073, 20, 2f, Main.myPlayer);
===== 61588 =====
61565: 			if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61571: 				if (Main.expertMode && num36 < 120f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61574: 					if (velocity.Y == 0f)
61578: 					if (Main.netMode != 1 && localAI[0] == 0f)
61580: 						for (int k = 0; k < 5; k++)
61588: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector3.X, vector3.Y, vector4.X, vector4.Y, 174, attackDamage_ForProjectiles, 0f, Main.myPlayer);
===== 61608 =====
61588: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector3.X, vector3.Y, vector4.X, vector4.Y, 174, attackDamage_ForProjectiles, 0f, Main.myPlayer);
61593: 				else if (num36 < 200f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61596: 					if (velocity.Y == 0f)
61600: 					if (Main.netMode != 1 && localAI[0] == 0f)
61608: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector3.X, vector3.Y, num34, num35, 174, 9, 0f, Main.myPlayer);
===== 61643 =====
61620: 			if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61626: 				if (Main.expertMode && num39 < 120f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61629: 					if (velocity.Y == 0f)
61633: 					if (Main.netMode != 1 && localAI[0] == 0f)
61635: 						for (int l = 0; l < 5; l++)
61643: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector5.X, vector5.Y, vector6.X, vector6.Y, 605, attackDamage_ForProjectiles2, 0f, Main.myPlayer);
===== 61663 =====
61643: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector5.X, vector5.Y, vector6.X, vector6.Y, 605, attackDamage_ForProjectiles2, 0f, Main.myPlayer);
61648: 				else if (num39 < 200f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61651: 					if (velocity.Y == 0f)
61655: 					if (Main.netMode != 1 && localAI[0] == 0f)
61663: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector5.X, vector5.Y, num37, num38, 605, 9, 0f, Main.myPlayer);
===== 61708 =====
61686: 					if (velocity.Y == 0f)
61690: 					if (Main.netMode != 1 && localAI[0] == 0f)
61692: 						for (int m = 0; m < 3; m++)
61699: 							if (num42 > 350f)
61703: 							else if (num42 > 250f)
61708: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center.X, center.Y, vector7.X, vector7.Y, 920, attackDamage_ForProjectiles_MultiLerp, 0f, Main.myPlayer);
===== 61743 =====
61721: 					if (velocity.Y == 0f)
61725: 					if (Main.netMode != 1 && localAI[0] == 0f)
61731: 						if (num44 > 350f)
61735: 						else if (num44 > 250f)
61743: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center.X, center.Y, num40, num41, 920, attackDamage_ForProjectiles_MultiLerp2, 0f, Main.myPlayer);
===== 61792 =====
61770: 					if (Main.netMode != 1 && localAI[0] == 0f)
61776: 						if (num48 > 350f)
61780: 						else if (num48 > 250f)
61787: 						if (Main.expertMode)
61792: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center2.X, center2.Y, num45, num46, 921, attackDamage_ForProjectiles_MultiLerp3, 0f, Main.myPlayer);
===== 61827 =====
61804: 			if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61810: 				if (Main.expertMode && num51 < 200f && Collision.CanHit(new Vector2(position.X, position.Y - 20f), width, height + 20, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61813: 					if (velocity.Y == 0f)
61817: 					if (Main.netMode != 1 && localAI[0] == 0f)
61819: 						for (int n = 0; n < 5; n++)
61827: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, vector9.X, vector9.Y, 176, attackDamage_ForProjectiles3, 0f, Main.myPlayer);
===== 61849 =====
61827: 							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, vector9.X, vector9.Y, 176, attackDamage_ForProjectiles3, 0f, Main.myPlayer);
61832: 				if (num51 < 400f && Collision.CanHit(new Vector2(position.X, position.Y - 20f), width, height + 20, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61835: 					if (velocity.Y == 0f)
61839: 					if (Main.netMode != 1 && localAI[0] == 0f)
61849: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, num49, num50, 176, 13, 0f, Main.myPlayer);

```


---

## 🤖 Assistant · 2026-08-11T03:58:28.041Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Slime segment launches need enclosing type conditions. Let me find them:
- 61104: SlimeCanContainItems (slimes with items: e.g., item-dropping slimes shoot proj 1073?). Let me see proj 1073 = ? and the context — "ai[1] == 539" hmm. Let me read 61085-61110. proj 1073.
- 61588/61608: proj 174 — spiky slime ball! types: which? Need enclosing `if (type == ...)` — probably SpikedIceSlime (243?) no. Let me search upward.
- 61643/61663: proj 605.
- 61708/61743: proj 920.
- 61792: proj 921.
- 61827/61849: proj 176.

Let me find enclosing type conditions by searching for "if (type ==" above each.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:58:29.164Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for L in 61588 61643 61708 61743 61792 61827 61104; do echo \"== $L ==\"; awk -v L=$L 'NR<=L && (/if \\(type ==/||/SlimeCanContainItems/||/type >=/||/case /) {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | tail -3; done",
 "description": "Find enclosing type conditions for slime launches"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:58:33.376Z

**📎 ToolResult**

```
== 61588 ==
61508: 		if (type == 667)
61527: 		if (type == 676)
61550: 		if (type == 184)
== 61643 ==
61527: 		if (type == 676)
61550: 		if (type == 184)
61613: 		if (type == 535)
== 61708 ==
61550: 		if (type == 184)
61613: 		if (type == 535)
61668: 		if (type == 658)
== 61743 ==
61550: 		if (type == 184)
61613: 		if (type == 535)
61668: 		if (type == 658)
== 61792 ==
61613: 		if (type == 535)
61668: 		if (type == 658)
61748: 		if (type == 659)
== 61827 ==
61668: 		if (type == 658)
61748: 		if (type == 659)
61797: 		if (type == 204)
== 61104 ==
60820: 				else if (type == 537)
60971: 		if (type == 1)
61089: 		if (NPCID.Sets.SlimeCanContainItems[type] && ai[1] > 0f)

```


---

## 🤖 Assistant · 2026-08-11T03:58:40.476Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now get names for NPC types: 184, 535, 658, 659, 204 and projectiles 1073, 174, 605, 920, 921, 176 (NPC proj 176? we looked up 176 as MossHornet; as projectile 176 = ?), plus 546 (Tumbleweed). Also for the 61104 block: SlimeCanContainItems types.

Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:58:40.549Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 184 535 658 659 204 537 1; do grep -n \"= $n;\" NPCID.cs|head -2; done; echo ---; for n in 1073 174 605 920 921 176; do grep -n \"= $n;\" ProjectileID.cs|head -2; done; echo ---; grep -n \"SlimeCanContainItems\" NPCID.cs | head -3",
 "description": "Look up slime NPC and projectile names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:58:49.568Z

**📎 ToolResult**

```
11433:	public const short SpikedIceSlime = 184;
12135:	public const short SlimeSpiked = 535;
12381:	public const short QueenSlimeMinionBlue = 658;
12383:	public const short QueenSlimeMinionPink = 659;
189:			public const int Oiled = 204;
11473:	public const short SpikedJungleSlime = 204;
12139:	public const short SandSlime = 537;
11067:	public const short BlueSlime = 1;
---
2506:	public const short PoisonDartShotFromSlimes = 1073;
708:	public const short IceSpike = 174;
1570:	public const short SpikedSlimeSpike = 605;
2200:	public const short QueenSlimeMinionBlueSpike = 920;
2202:	public const short QueenSlimeMinionPinkBall = 921;
712:	public const short JungleSpike = 176;
---
4791:		public static bool[] SlimeCanContainItems = Factory.CreateBoolSet(1, 59, 147, 184, 537);

```


---

## 🤖 Assistant · 2026-08-11T03:59:01.709Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All slime launches:
- 61104: SlimeCanContainItems slimes (BlueSlime 1, GreenSlime -81? Actually set = 1, 59, 147, 184, 537) → 1=BlueSlime, 59=GreenSlime?, 147=SandSlime? no 537=SandSlime. 59 = Black Slime? 147 = ? Anyway — they shoot PoisonDartShotFromSlimes (1073) when ai[1]==539 — that's when a Poison Dart trap shoots them? Actually the "poison dart" dart trap mechanism: slimes containing items can shoot a dart back. ai[1] == 539 seems to be set when hit by a dart (item 539?). Anyway condition: rand(num11)==0, target valid, LOS, direction*12, dmg 20. num11 depends on noTrapsWorld/getGoodWorld. Let me check line 61089-61104 details: `if (ai[1] == 539f && Main.netMode != 1)` and Main.noTrapsWorld → num11 presumably different. I'll describe: slimes carrying dart trap item (SlimeCanContainItems set {1,59,147,184,537}) reflect a dart. Let me quickly view 61089-61105.
- 61588/61608: SpikedIceSlime (184) → IceSpike (174); expert 5-shot burst within 120px; normal 1 shot within 200px dmg 9.
- 61643/61663: SlimeSpiked (535) → SpikedSlimeSpike (605); same pattern.
- 61708/61743: QueenSlimeMinionBlue (658) → 920; 3 shots, dmg multi-lerp based on distance; boss minion (Queen Slime) → probably boss-related skip? These are Queen Slime minions — boss event. I'd classify as Boss 段.
- 61792: QueenSlimeMinionPink (659) → 921 ball; boss minion.
- 61827/61849: SpikedJungleSlime (204) → JungleSpike (176); expert 5-shot within 200px, normal 1 shot dmg 13 within 400px.

Now remaining fighter details: Clown (60212), Vortex Rifleman (59011) trigger details, and the main ranged block trigger conditions. Also need the type list answered for the big block: full type list. Already have.

Also check: which of 214/215/216 are pirates — PirateDeadeye (214) fires BulletDeadeye 180, PirateCrossbower (215) fires FlamingArrow 82, PirateCaptain (216) fires CannonballHostile 240. But pirates are invasion — the user's task says pirate invasion cannonballs excluded, but the user explicitly asked in item 2 what 111/214/215/216 are and what they shoot. 111 = GoblinArcher → proj default 81? Wait default num172 = 82? Let's check: num171 (dmg) default 35, num172 (proj) default 82 = FlamingArrow. Hmm wait, for type 111 (Goblin Archer) num171=11? Look: `if (type == 111) { num171 = 11; }` — hmm num171 is damage and 11 damage seems low for an arrow. And `num172 = 81` — 81 = ? Let me check ProjectileID 81. Actually 81 might be "WoodenArrowHostile"? And 82 = FlamingArrow. Let me grep 81, 84 (probe laser), 55 (stinger), and confirm.

Wait, careful: `int num171 = 35; int num172 = 82;` — for goblin archer (111): num171=11, num172=81. proj 81 = ? Let me grep. Likely "WoodenArrowHostile" = 81. And default 82 = FlamingArrow used by ElfArcher (350)? Hmm, Elf Archer's num171=45, num172 default 82 = FlamingArrow. Yes Elf Archer shoots flaming arrows.

Let me grep 81, 84, 55.

Also 60212 Clown block: read 60195-60220.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:59:02.650Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 81 84 55 82; do grep -n \"= $n;\" ProjectileID.cs|head -2; done; echo ----; sed -n '60195,60225p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ----; sed -n '61089,61105p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check proj 81/84/55 and Clown/dart blocks"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:59:06.821Z

**📎 ToolResult**

```
522:	public const short WoodenArrowHostile = 81;
528:	public const short PinkLaser = 84;
470:	public const short Stinger = 55;
524:	public const short FlamingArrow = 82;
----
				}
			}
		}
		if (type == 109 && Main.netMode != 1 && !Main.player[target].dead)
		{
			if (justHit)
			{
				ai[2] = 0f;
			}
			ai[2] += 1f;
			if (ai[2] > 60f)
			{
				Vector2 vector38 = new Vector2(position.X + (float)width * 0.5f - (float)(direction * 24), position.Y + 4f);
				if (Main.rand.Next(5) != 0 || AnyNPCs(378))
				{
					int num185 = Main.rand.Next(3, 8) * direction;
					int num186 = Main.rand.Next(-8, -5);
					int num187 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector38.X, vector38.Y, num185, num186, 75, 80, 0f, Main.myPlayer);
					Main.projectile[num187].timeLeft = 300;
					ai[2] = 0f;
				}
				else
				{
					ai[2] = -120f;
					int number = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)vector38.X, (int)vector38.Y, 378);
					NetMessage.SendData(23, -1, -1, null, number);
				}
			}
		}
		if (velocity.Y == 0f || flag)
		{
----
		if (NPCID.Sets.SlimeCanContainItems[type] && ai[1] > 0f)
		{
			if (ai[1] == 539f && Main.netMode != 1)
			{
				int num11 = 300;
				if (Main.noTrapsWorld)
				{
					num11 -= 120;
				}
				if (Main.getGoodWorld)
				{
					num11 -= 120;
				}
				if (Main.rand.Next(num11) == 0 && target >= 0 && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type] && Collision.CanHit(this, Main.player[target]))
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), (int)base.Center.X, base.Center.Y, direction * 12, 0f, 1073, 20, 2f, Main.myPlayer);
				}

```


---

## 🤖 Assistant · 2026-08-11T03:59:08.899Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the Vortex Rifleman trigger (58865-59015). Let me read that block. Also confirm 59011: proj 577 VortexLaser, 4 shots, dmg GetAttackDamage? Let's read.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:59:09.172Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '58865,59015p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read Vortex Rifleman block"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:59:09.202Z

**📎 ToolResult**

```
		else if (type == 425)
		{
			if (localAI[3] == 0f)
			{
				localAI[3] = 1f;
				ai[3] = -120f;
			}
			if (velocity.Y == 0f)
			{
				ai[2] = 0f;
			}
			if (velocity.Y != 0f && ai[2] == 1f)
			{
				TargetClosest();
				spriteDirection = -direction;
				if (Collision.CanHit(base.Center, 0, 0, Main.player[target].Center, 0, 0))
				{
					float num111 = 0.3f;
					float num112 = 8f;
					float num113 = 0.3f;
					float num114 = 7f;
					float num115 = Main.player[target].Center.X - (float)(direction * 300) - base.Center.X;
					float num116 = Main.player[target].Bottom.Y - base.Bottom.Y;
					if (num115 < 0f && velocity.X > 0f)
					{
						velocity.X *= 0.9f;
					}
					else if (num115 > 0f && velocity.X < 0f)
					{
						velocity.X *= 0.9f;
					}
					if (num115 < 0f && velocity.X > 0f - num114)
					{
						velocity.X -= num113;
					}
					else if (num115 > 0f && velocity.X < num114)
					{
						velocity.X += num113;
					}
					if (velocity.X > num114)
					{
						velocity.X = num114;
					}
					if (velocity.X < 0f - num114)
					{
						velocity.X = 0f - num114;
					}
					if (num116 < -20f && velocity.Y > 0f)
					{
						velocity.Y *= 0.8f;
					}
					else if (num116 > 20f && velocity.Y < 0f)
					{
						velocity.Y *= 0.8f;
					}
					if (num116 < -20f && velocity.Y > 0f - num112)
					{
						velocity.Y -= num111;
					}
					else if (num116 > 20f && velocity.Y < num112)
					{
						velocity.Y += num111;
					}
				}
				if (Main.rand.Next(3) == 0)
				{
					position += netOffset;
					Vector2 vector25 = base.Center + new Vector2(direction * -14, -8f) - Vector2.One * 4f;
					Vector2 vector26 = new Vector2(direction * -6, 12f) * 0.2f + Utils.RandomVector2(Main.rand, -1f, 1f) * 0.1f;
					Dust obj5 = Main.dust[Dust.NewDust(vector25, 8, 8, 229, vector26.X, vector26.Y, 100, Color.Transparent, 1f + Main.rand.NextFloat() * 0.5f)];
					obj5.noGravity = true;
					obj5.velocity = vector26;
					obj5.customData = this;
					position -= netOffset;
				}
				for (int num117 = 0; num117 < Main.maxNPCs; num117++)
				{
					if (num117 != whoAmI && Main.npc[num117].active && Main.npc[num117].type == type && Math.Abs(position.X - Main.npc[num117].position.X) + Math.Abs(position.Y - Main.npc[num117].position.Y) < (float)width)
					{
						if (position.X < Main.npc[num117].position.X)
						{
							velocity.X -= 0.15f;
						}
						else
						{
							velocity.X += 0.15f;
						}
						if (position.Y < Main.npc[num117].position.Y)
						{
							velocity.Y -= 0.15f;
						}
						else
						{
							velocity.Y += 0.15f;
						}
					}
				}
			}
			else if (Main.player[target].Center.Y + 100f < position.Y && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
			{
				flag = true;
				velocity.Y = -5f;
				ai[2] = 1f;
			}
			if (ai[3] < 0f)
			{
				ai[3] += 1f;
			}
			int num118 = 30;
			int num119 = 10;
			int num120 = 180;
			if (ai[3] >= 0f && ai[3] <= (float)num118)
			{
				Vector2 vector27 = DirectionTo(Main.player[target].Center);
				bool flag12 = Math.Abs(vector27.Y) <= Math.Abs(vector27.X);
				bool flag13 = Distance(Main.player[target].Center) < 800f && flag12 && Collision.CanHitLine(base.Center, 0, 0, Main.player[target].Center, 0, 0);
				ai[3] = MathHelper.Clamp(ai[3] + (float)flag13.ToDirectionInt(), 0f, num118);
			}
			if (ai[3] >= (float)(num118 + 1) && (ai[3] += 1f) >= (float)(num118 + num119))
			{
				ai[3] = num118 - num120;
				netUpdate = true;
			}
			if (Main.netMode != 1 && ai[3] == (float)num118)
			{
				ai[3] += 1f;
				netUpdate = true;
				int num121 = 20;
				Vector2 chaserPosition = base.Center + new Vector2(direction * 30, 2f);
				Vector2 vector28 = DirectionTo(Main.player[target].Center) * num121;
				if (vector28.HasNaNs())
				{
					vector28 = new Vector2(direction * num121, 0f);
				}
				int num122 = 2;
				Utils.ChaseResults chaseResults = Utils.GetChaseResults(chaserPosition, num121, Main.player[target].Center, Main.player[target].velocity * 0.5f / num122);
				if (chaseResults.InterceptionHappens)
				{
					Vector2 vector29 = chaseResults.ChaserVelocity / num122;
					vector28.X = vector29.X;
					vector28.Y = vector29.Y;
				}
				int attackDamage_ForProjectiles = GetAttackDamage_ForProjectiles(75f, 50f);
				for (int num123 = 0; num123 < 4; num123++)
				{
					Vector2 vector30 = vector28 + Utils.RandomVector2(Main.rand, -0.8f, 0.8f) * ((num123 != 0) ? 1 : 0);
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition.X, chaserPosition.Y, vector30.X, vector30.Y, 577, attackDamage_ForProjectiles, 1f, Main.myPlayer);
				}
			}
		}
		else if (type == 427)

```


---

## 🤖 Assistant · 2026-08-11T03:59:20.092Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have everything for AI_003_Fighters. Also check 58814-58836 (type 526/527/415) — no NewProjectile there so fine.

Now remaining unattributed lines:
- 44208, 44297: SpawnStardustMark (44142-44338) — boss/event (Moon Lord / Stardust pillar support). Actually SpawnStardustMark_StardustTower is called by Stardust Tower boss. Event skip.
- 44697, 44749, 44770: Deerclops (44338-44812) — boss.
- 44896: AI_123_Deerclops_MakeSpikesBothSides — boss.
- 45905, 46039: QueenSlime — boss.
- 46376...47188: Empress of Light (AI_120_HallowBoss) — boss.
- 47414: hmm, 47414 is before AI_117_BloodNautilus (47488). 47414 lies within AI_118_Seahorses (47432)? No, 47414 < 47432. It's in AI_119_Dandelion (47344-47432). NewProjectile in dandelion? Maybe dandelion seeds. Let me check 47414.
- 47770, 47874: BloodNautilus — blood moon event/boss (Dreadnautilus).
- 49649, 49650, 49875: Duke Fishron — boss.
- 50251: Destroyer — boss.
- 51005: Probe laser — mech boss satellite. Boss-related skip (but it's a regular-ish enemy that appears during Destroyer fight). I'll list it in the boss table but note it's Probe.
- 51189: Hornets (42, 176, 231-235) — REGULAR. stinger 55.
- 51287: BloodSquid 619 — blood moon event.
- 53147: StingerExplosion — Queen Bee (type 176 check? no, `if (type == 176)` hmm at 53142 inside StingerExplosion? Wait StingerExplosion starts 53132, and 53142 `if (type == 176)`. But type 176 = MossHornet... Hmm, StingerExplosion is used by Queen Bee (222). The `type == 176` inside... let me look at the StingerExplosion method quickly to determine. Actually Queen Bee type is 222; but the method checks `type == 176`?? Let me read 53132-53195.
- 54919, 55187, 55225, 55342, 55358, 55374, 55381, 55387: AI_007_TownEntities — town NPCs (Skeleton merchant throwing bones? Actually these could be the Skeleton Merchant's bones, and NPC vs NPC). Let me check which.
- 56733 etc — done.
- 61104...61849 — done.
- 62459, 62523: AI_110_Betsy — DD2 boss.
- 62862, 62934, 62980: pumpkin moon / pillar events.
- 64415, 64596: DD2 Ogre / DD2 army.
- 65404...65837: Lunatic Cultist — boss.
- 66450, 66459, 66468: DarkMage — DD2 event.
- 66968: DD2LightningBug — event.
- 79017, 79090: tombstone (checkDead / DropTombstoneTownNPC) — tombstone.
- 80091...80174: DoDeathEvents — boss death (probes? Actually DoDeathEvents spawns e.g. Martian saucer pieces? no, projectiles like "boss death" effects: 80091 etc might be Queen Bee / Moon Lord). Quick check.
- 84042, 84588: HitEffect — gore/visual (e.g., martian probe explosion?). Quick check.

Let me check 47414, 53132-53195, town entity lines, and 84042/84588/80091 contexts quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-11T03:59:20.329Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '53132,53195p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read StingerExplosion"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:59:20.362Z

**📎 ToolResult**

```
	private void StingerExplosion()
	{
		int num = Main.rand.Next(4, 9);
		for (int i = 0; i < num; i++)
		{
			float num2 = 8f;
			Vector2 vector = new Vector2(Main.rand.NextFloat() - 0.5f, Main.rand.NextFloat() - 0.5f);
			vector.Normalize();
			vector *= num2;
			int num3 = (int)(10f * scale);
			if (type == 176)
			{
				num3 = (int)(30f * scale);
			}
			int num4 = 55;
			int num5 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector.X, vector.Y, num4, num3, 0f, Main.myPlayer);
			Main.projectile[num5].timeLeft = 300;
		}
	}

	public static bool DespawnEncouragement_AIStyle2_FloatingEye_IsDiscouraged(int npcID, Vector2 npcPosition, int target = 255)
	{
		if (!Main.player[target].ZoneGraveyard && Main.IsItDay() && (double)npcPosition.Y <= Main.worldSurface * 16.0)
		{
			if (npcID != 2 && npcID != 133 && npcID != 190 && npcID != 191 && npcID != 192 && npcID != 193 && npcID != 194 && npcID != 317)
			{
				return npcID == 318;
			}
			return true;
		}
		return false;
	}

	private bool AI_007_TownEntities_IsInAGoodRestingSpot(int tileX, int tileY, int idealRestX, int idealRestY)
	{
		if (!Main.dayTime && ai[0] == 5f)
		{
			if (Math.Abs(tileX - idealRestX) <= 7)
			{
				return Math.Abs(tileY - idealRestY) <= 7;
			}
			return false;
		}
		if ((type == 361 || type == 445 || type == 687) && wet)
		{
			return false;
		}
		if (tileX == idealRestX)
		{
			return tileY == idealRestY;
		}
		return false;
	}

	private bool SolidOrSlopedTileOrPlatform(Tile tile)
	{
		if (tile != null && tile.active() && ((Main.tileSolid[tile.type] && !Main.tileSolidTop[tile.type]) || TileID.Sets.Platforms[tile.type]))
		{
			return !tile.inActive();
		}
		return false;
	}

	private void AI_007_FindGoodRestingSpot(int myTileX, int myTileY, out int floorX, out int floorY)

```


---

## 🤖 Assistant · 2026-08-11T03:59:21.422Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for L in 47414 54919 55187 55225 55342 55374 79017 80091 84042 84588; do echo \"===== $L =====\"; awk -v L=$L 'NR>=L-30 && NR<=L {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep \"type ==\\|NewProjectile\\|case \\|void \\|if (\\|Main\\.npc\\[\" | tail -6; done",
 "description": "Context for remaining lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T03:59:47.218Z

**📎 ToolResult**

```
===== 47414 =====
47386: 				if (localAI[1] > 80f)
47393: 					if (localAI[1] != 40f)
47400: 						if (num > 0f)
47407: 						if (vector2.Y > -3f)
47414: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector3, vector2, 836, num4, 1f, Main.myPlayer, 0f, target);
===== 54919 =====
54904: 				if (num15 == 1 && spriteDirection == 1 && num17 != -1)
54906: 					vec = DirectionTo(Main.npc[num17].Center + new Vector2(0f, (0f - num48) * MathHelper.Clamp(Distance(Main.npc[num17].Center) / num49, 0f, 1f)));
54908: 				if (num15 == -1 && spriteDirection == -1 && num16 != -1)
54910: 					vec = DirectionTo(Main.npc[num16].Center + new Vector2(0f, (0f - num48) * MathHelper.Clamp(Distance(Main.npc[num16].Center) / num49, 0f, 1f)));
54912: 				if (vec.HasNaNs() || Math.Sign(vec.X) != spriteDirection)
54919: 				num51 = ((type == 124) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer, 0f, whoAmI, townNpcVariationIndex) : ((type != 142) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer) : Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec.X, vec.Y, num43, num44, knockBack, Main.myPlayer, 0f, Main.rand.Next(5))));
===== 55187 =====
55159: 				case 134:
55173: 			if (localAI[3] == (float)num55 && Main.netMode != 1)
55176: 				if (num59 != -1)
55178: 					vec2 = DirectionTo(Main.npc[num59].Center + new Vector2(0f, -num57));
55180: 				if (vec2.HasNaNs() || Math.Sign(vec2.X) != spriteDirection)
55187: 				num60 = ((type != 227) ? Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec2.X, vec2.Y, num52, num53, knockBack2, Main.myPlayer) : Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec2.X, vec2.Y, num52, num53, knockBack2, Main.myPlayer, 0f, (float)Main.rand.Next(12) / 6f));
===== 55225 =====
55208: 		else if (ai[0] == 13f)
55211: 			if ((float)NPCID.Sets.AttackTime[type] == ai[1])
55217: 			if (localAI[3] == 1f && Main.netMode != 1)
55219: 				Vector2 vec3 = DirectionTo(Main.npc[(int)ai[2]].Center + new Vector2(0f, -20f));
55220: 				if (vec3.HasNaNs() || Math.Sign(vec3.X) == -spriteDirection)
55225: 				int num61 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec3.X, vec3.Y, 584, 0, 0f, Main.myPlayer, ai[2]);
===== 55342 =====
55323: 			if (localAI[3] == (float)num65 && Main.netMode != 1)
55326: 				if (num71 != -1)
55328: 					vec4 = DirectionTo(Main.npc[num71].Center + new Vector2(0f, (0f - num67) * MathHelper.Clamp(Distance(Main.npc[num71].Center) / num68, 0f, 1f)));
55330: 				if (vec4.HasNaNs() || Math.Sign(vec4.X) != spriteDirection)
55336: 				if (type == 108)
55342: 						int num74 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * 16), base.Center.Y - 2f, vec4.X + vector5.X, vec4.Y + vector5.Y, num62, num63, knockBack3, Main.myPlayer, 0f, 0f, townNpcVariationIndex);
===== 55374 =====
55358: 						int num76 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector6.X, vector6.Y, 0f, 0f, num62, num63, knockBack3, Main.myPlayer, 0f, 0f, townNpcVariationIndex);
55363: 				else if (type == 663)
55365: 					if (num71 != -1)
55367: 						Vector2 vector7 = Main.npc[num71].position + Main.npc[num71].Size * Utils.RandomVector2(Main.rand, 0f, 1f) * 1f;
55372: 							vector7 = Main.npc[num71].position + Main.npc[num71].Size * Utils.RandomVector2(Main.rand, 0f, 1f) * 1f;
55374: 						int num78 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector7.X, vector7.Y, 0f, 0f, num62, num63, knockBack3, Main.myPlayer, 0f, 0f, townNpcVariationIndex);
===== 79017 =====
78996: 				if (Main.npc[n].active && (Main.npc[n].type == 134 || Main.npc[n].type == 135 || Main.npc[n].type == 136))
78998: 					float num9 = Math.Abs(Main.npc[n].Center.X - center.X) + Math.Abs(Main.npc[n].Center.Y - center.Y);
78999: 					if (num9 < num8)
79002: 						vector2 = Main.npc[n].position;
79015: 		if (Main.getGoodWorld && Main.netMode != 1 && type == 631)
79017: 			Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center, Vector2.Zero, 99, 70, 10f, Main.myPlayer);
===== 80091 =====
80085: 		case 417:
80086: 		case 418:
80087: 		case 419:
80088: 		case 518:
80089: 			if (ShieldStrengthTowerSolar > 0)
80091: 				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, 0f, 0f, 629, 0, 0f, Main.myPlayer, FindFirstNPC(517));
===== 84042 =====
84025: 						if ((num153 < point2.Y - num149 || num153 > point2.Y + num149 || num152 < point2.X - num149 || num152 > point2.X + num149) && (num153 < point.Y - num148 || num153 > point.Y + num148 || num152 < point.X - num148 || num152 > point.X + num148) && !Main.tile[num152, num153].nactive())
84028: 							if (flag3 && Main.tile[num152, num153].lava())
84032: 							if (flag3 && Collision.SolidTiles(num152 - num150, num152 + num150, num153 - num150, num153 + num150))
84036: 							if (flag3 && !Collision.CanHitLine(base.Center, 0, 0, Main.player[target].Center, 0, 0))
84040: 							if (flag3)
84042: 								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), num152 * 16 + 8, num153 * 16 + 8, 0f, 0f, 578, 0, 1f, Main.myPlayer);
===== 84588 =====
84582: 				if (Main.netMode != 1)
84588: 						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector21.X, vector21.Y, 594, 0, 0f, Main.myPlayer);

```


---

## 🤖 Assistant · 2026-08-11T04:00:24.878Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
All those are non-enemy-attack:
- 47414: Dandelion (AI_119) proj 836 — critter/environment.
- 54919/55187/55225/55342/55358/55374/55381/55387: town NPC defense attacks (AI_007_TownEntities) — skip (城镇 NPC 防卫攻击).
- 79017: Rock Golem (631) death spawn — getGoodWorld, proj 99 = ? Let me check quickly (proj 99 = "Boulder"? no, 99 might be "DD2..."). Actually it's in checkDead. proj 99 = ? Let me grep: probably "RollingCactus"? Just note as Rock Golem death.
- 80091-80174: DoDeathEvents tower/projectiles (Solar tower pillar 417-419/518 → proj 629), others.
- 84042: HitEffect, proj 578 = ? (probably "MartianProbe" spawn on death — martian probe summons invasion). 
- 84588: proj 594 = ? probably MartianSaucer spawn? Hmm.

Let me quickly grep proj 99, 629, 578, 594, 836 and check 79017/84042/84588 attribution (they're death events, not attacks).

Also the town NPC launches at 55358 etc. Fine.

One more thing: 53147 StingerExplosion — it's a helper; who calls it? `if ((type == 2 || type == 133 ...)` no that was in AI_002_FloatingEye at 53109 (rand 40 dust). Let me find callers of StingerExplosion: grep. It's probably called by Queen Bee stinger attack in the main aiStyle chain (pre-43233). type==176 check inside is odd — 176 = MossHornet. Hmm, Queen Bee is 222. Wait — maybe StingerExplosion is called when hornet/queen bee dies? Let me grep callers.

Also verify big-block entry for DrManFly (468): eclipse gate — `if (type == 468 && !Main.eclipse)` sets flag16=true meaning it stops attacking outside eclipse; Dr Man Fly is an eclipse enemy → event, skip-ish. But keep in table.

Also need expertMode/hardmode conditions for the main block: standard trigger: requires LOS + target stealth==0 && itemAnimation==0, distance < num181 (700 default), grounded; then ai[1] = cooldown num163 (type-specific), at half cooldown fires. Note the stealth check: `if (Main.player[target].stealth == 0f && Main.player[target].itemAnimation == 0) flag21 = false;` — i.e., target must be hidden (stealth>0) or using an item to shoot. That's the standard "NPC shoots when player is active".

Wait, that seems inverted but it's the vanilla code: enemies only shoot when the player is using an item or has stealth. Yes — vanilla: `flag21 = false` unless player's stealth==0 and itemAnimation==0... Actually the code sets flag21=false when stealth==0 && itemAnimation==0, meaning shooting only allowed when player is using item or stealthed (detected). Correct vanilla behavior.

Now, the per-type data table for the big block. Let me compile per type:
Type / name / cooldown num163 / speed num166 / proj / damage / range num181:
- 110 SkeletonArcher: default cd 70, speed 11, proj 82 FlamingArrow? Wait num172 default = 82 = FlamingArrow. Hmm but Skeleton Archer shoots wooden arrows in vanilla... Actually in vanilla Skeleton Archers shoot "SkeletonBone"? No — they shoot WoodenArrowHostile (81)? Hmm. Let me re-read: `int num171 = 35; int num172 = 82;` — For type 111 GoblinArcher: `num171 = 11; ... num172 = 81`. Hmm, and for 110 no override except... wait `if (type == 111) { num171 = 11; }` at top of the num166 section, and later `if (type == 111) { num172 = 81; }`. And 110 SkeletonArcher has no num166/num172 override → speed 11, proj 82 FlamingArrow, dmg 35, range 700? Hmm but that seems wrong for Skeleton Archer (vanilla shoots WoodenArrowHostile with 9 speed? Actually I recall skeleton archers shoot flaming arrows? No...). 

Hmm wait — check: does the big block include 110? Yes: `if (type == 110 || type == 111 || ...)`. 110 = SkeletonArcher with defaults: speed 11, dmg 35, proj 82 FlamingArrow. Hmm, in vanilla Skeleton Archer shoots arrows (proj 81? or 82?). Actually vanilla SkeletonArcher shoots "FlamingArrow"? I believe Skeleton Archers shoot wooden arrows that deal 30ish. But the decompiled code says default proj = 82 with damage 35. Since the source is authoritative, I'll report as written. Hmm, but wait: is 82 FlamingArrow? Yes per ProjectileID. Hmm, but damage 35... vanilla skeleton archer arrow damage is 9 base * expert. Eh — the NPC's damage stat is separate; num171 here is projectile damage 35. Fine, report as-is.

Hmm, actually let me double check num172 default. In the code: `int num171 = 35; int num172 = 82;` — hmm wait, that was `int num171 = 35;\n int num172 = 82;`? From my read:

```
int num171 = 35;
int num172 = 82;
if (type == 111)
{
    num171 = 11;
}
```
Yes.

And GoblinArcher (111): speed 9 (num166=9), dmg 11, proj 81 WoodenArrowHostile, cd 180, range 700 (default).
- 111 GoblinArcher: cd 180, speed 9, proj 81 WoodenArrowHostile, dmg 11.

Others:
- 206 IcyMerman: cd 50, speed 7, proj 177 IcewaterSpit, dmg 37, muzzle Y-10, aim compensation num168 = |dx|*0.1 (default) → actually num168 default = |num167|*0.1 then num169 = targetY - chaserY - num168. For 291/292 num168=0. OK.
- 214 PirateDeadeye: cd 50, speed 10, proj 180 BulletDeadeye, dmg 25, range 500, spread ±45.
- 215 PirateCrossbower: cd 90, speed 14, proj 82 FlamingArrow, dmg 35, range 650, aim bias 0.08.
- 216 PirateCaptain: cd 30 initially (num163=30)... wait `if (type == 216)` overrides: if localAI[2]>=20 (flag20 phase) num163 = max(60, 180-20*hits); else num163 = 9. Proj 180 BulletDeadeye dmg 30 normally; in flag20 phase proj 240 CannonballHostile dmg 100 speed 15, then resets counters. So PirateCaptain: phase 1: cd 9, speed 9, BulletDeadeye 25... wait dmg 30? `if (type == 216) { num172 = 180; num171 = 30; if (flag20) { num171 = 100; num172 = 240; ...` yes.
- 290 Paladin: cd 30, speed 9, proj 300 PaladinsHammerHostile, dmg 60 (expert*0.75).
- 291 SkeletonSniper: cd 200, speed 4, proj 302 SniperBullet, dmg 100, no aim bias (num168=0), spread ±8 (rand(-40,41)*0.2).
- 292 TacticalSkeleton: cd 120, speed 12 default? num166 default 11; 292 no override → speed 11? Hmm 292 not in num166 list, so 11. But it fires 4 projectiles at speed 12 (`num170 = 12f/num170`) with proj 180 BulletDeadeye dmg 50. Trigger num165 = num163-1 = 119.
- 293 SkeletonCommando: cd 90, speed 4, proj 303 RocketSkeleton, dmg 60.
- 350 ElfArcher: cd 110, speed 11, proj 82 FlamingArrow, dmg 45, range 700. (Pumpkin/Frost moon event enemy — Elf Archer is frost moon.) → event, skip detail but note.
- 379 CultistArcherBlue / 380 CultistArcherWhite: cd 70/80 (379/380 → 80), speed 11, proj 81? no override → proj 82 FlamingArrow dmg 40. Hmm wait `if (type == 379 || type == 380) num163 = 80;` and num171=40, num172 stays 82. Hmm, cultist archers shoot... in vanilla they shoot "FlamingArrow"? Hmm. Actually I don't recall. Fine, report code.
- 381 BrainScrambler: cd 80, speed 7, proj 436 BrainScramblerBolt, dmg 24, rand spread, no gravity compensation, range 700.
- 382 RayGunner: cd 80, speed 7, proj 438 RayGunnerLaser, dmg 30.
- 449-452 BoneThrowingSkeleton: cd 70, speed 7, proj 471 SkeletonBone, dmg 15, range 200, partial aim bias random.
- 468 DrManFly: cd 70, speed 7.5, proj 501 DrManFlyFlask, dmg 50, range 400, requires eclipse (flag16 forced true when !Main.eclipse → won't stop to shoot).
- 481 GreekSkeleton: cd 100, speed 8, proj 508 JavelinHostile, dmg 18, aim lead compensation, range 400, muzzle Y-14.
- 411 StardustSoldier: cd 330, no charge requirement until ai[1] <= 220 (flag18=false if ai[1]<=220 → won't shoot while justHit timer high), speed 1 (slow laser), proj 537 StardustSoldierLaser dmg GetAttackDamage(60,45), fires with ai0=0, ai1=whoAmI. Stardust pillar event.
- 409 StardustSpiderBig: instead of projectile spawns NPC 410 (small spider) with velocity. Note: 59978 line is for type 424. Wait the NewNPC for 409 is at ~59982 (NewNPC, not NewProjectile). So type 409 doesn't have a NewProjectile line — fine.
- 424 NebulaSoldier: cd 180, num165 = 179, fires 4 NebulaBolt 573 dmg GetAttackDamage(60,45) upward as mist at feet (velocity small upward). Trigger at ai[1]==num165 (179). Nebula pillar event.
- 426 VortexHornetQueen: cd 60, num165=59, proj 581 VortexAcid dmg GetAttackDamage(60,45), speed 7, aimed with GetChaseResults at random player hitbox point. Vortex pillar event.
- 498-506 Salamander family: cd 70, speed 7, proj 572 SalamanderSpit, dmg 14, range 190, muzzle Y-8. Regular enemy (cave, 1.4.4).
- 520 MartianWalker: cd 15, num165 default num163/2=7, speed 8, proj 592 MartianWalkerLaser, dmg 35, spawn from base.Bottom+20, random spread bigger. Martian invasion → event.
- 537 SandSlime? No that's slime. 520 MartianWalker.

Also note type 468 eclipse requirement.

Also, the 56733 Rock Golem is in AI_003_Fighters but separate block. Nailhead (463) block. Chaos Elemental (120) — user asked: does its teleport accompany attack? Chaos Elemental aiStyle is 3 (fighter)? Actually ChaosElemental uses aiStyle 3? Hmm — Chaos Elemental has aiStyle 3? I believe ChaosElemental (120) is aiStyle 3 with ChaosElemental teleport handled in AI_003? Let me grep "type == 120" in NPC.cs within fighters. Let me check.

Also RuneWizard (172) — aiStyle? Rune Wizard teleports and fires a magic missile (proj 165?). Let me grep "type == 172".

Also Mimic (85) — doesn't shoot. Corruptor — hmm, user asked Corruptor(110?) — but 110 is SkeletonArcher. Corruptor actual id? Let me grep: NPCID.Corruptor = ? Probably 110 in old versions but here 110=SkeletonArcher. Let me grep Corruptor.

Also user mentioned "骷髅神射/爆破/战术（491/492/493）" — but actual IDs are 291/292/293. I should note that.

Also check types 163/238 (Black Recluse), and user asked about ChaosElemental(120) teleport attack and RuneWizard(172). Let me grep both quickly.
````

</details>


---

## 🤖 Assistant · 2026-08-11T04:00:25.807Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"type == 120\\|type == 172\\|Corruptor =\\|ChaosElemental\\|RuneWizard\\|Mimic = \\|== 85\\b\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -20; echo ---; grep -n \"StingerExplosion\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Locate Chaos Elemental, Rune Wizard, Corruptor, Mimic handling"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:00:25.837Z

**📎 ToolResult**

```
9837:		else if (type == 85)
10385:		else if (type == 120)
11086:		else if (type == 172)
20800:			if (type == 172)
20814:				if (type == 172)
20865:					else if (type == 172)
20927:					else if (type == 172)
20996:			else if (type == 172)
21228:							else if (type == 172)
21279:			else if (type == 172)
38967:		else if (aiStyle == 85)
57431:		if (type == 120)
57468:		if (type == 343 || type == 47 || type == 67 || type == 109 || type == 110 || type == 111 || type == 120 || type == 163 || type == 164 || type == 239 || type == 168 || type == 199 || type == 206 || type == 214 || type == 215 || type == 216 || type == 217 || type == 218 || type == 219 || type == 220 || type == 226 || type == 243 || type == 251 || type == 257 || type == 258 || type == 290 || type == 291 || type == 292 || type == 293 || type == 305 || type == 306 || type == 307 || type == 308 || type == 309 || type == 348 || type == 349 || type == 350 || type == 351 || type == 379 || (type >= 430 && type <= 436) || type == 591 || type == 380 || type == 381 || type == 382 || type == 383 || type == 386 || type == 391 || (type >= 449 && type <= 452) || type == 466 || type == 464 || type == 166 || type == 469 || type == 468 || type == 471 || type == 470 || type == 480 || type == 481 || type == 482 || type == 411 || type == 424 || type == 409 || (type >= 494 && type <= 506) || type == 425 || type == 427 || type == 426 || type == 428 || type == 580 || type == 508 || type == 415 || type == 419 || type == 520 || (type >= 524 && type <= 527) || type == 528 || type == 529 || type == 530 || type == 532 || type == 582 || type == 624 || type == 631)
57916:		else if (type == 120 || type == 166 || type == 213 || type == 258 || type == 528 || type == 529)
60652:				if (type == 120 && velocity.Y < 0f)
60679:		if (Main.netMode != 1 && type == 120 && ai[3] >= (float)num58)
70316:			if (type == 489 || type == 21 || type == 31 || type == 294 || type == 326 || type == 295 || type == 296 || type == 44 || type == 77 || type == 120 || type == 140 || type == 159 || type == 167 || type == 197 || type == 201 || type == 202)
74205:			if (ai[3] == 2f || (IsABestiaryIconDummy && type == 85))
82065:					if (type == 172)
86378:		if (type == 120 || type == 137 || type == 138)
---
53132:	private void StingerExplosion()
78887:			StingerExplosion();

```


---

## 🤖 Assistant · 2026-08-11T04:00:30.356Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
ChaosElemental (120) is handled in AI_003_Fighters: 57431 (gate), 57916 (teleport logic), 60679 (NewNPC teleport spawn — not projectile). So Chaos Elemental teleports but has no projectile launch (60679 is NewNPC). Let me confirm 60679 is NewNPC.

RuneWizard (172) is handled at 10385 (main AI dispatch, aiStyle 4? "else if (type == 172)") — in the pre-43233 chain. Let me check 10385-10420 and 20800 region to see if it fires projectiles — the user asked. Let me check.

Mimic (85): line 9837 in main chain; no NewProjectile nearby presumably. Check quickly.

StingerExplosion is called at 78887 in checkDead — when a hornet/queen bee? Let me see context 78860-78890: probably "if (type == 42 ...)" on death spawn stingers. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:00:31.307Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '60670,60685p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n '78860,78890p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n '10385,10420p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check ChaosElemental, StingerExplosion caller, RuneWizard dispatch"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:00:31.357Z

**📎 ToolResult**

```
					velocity.Y *= 1.1f;
				}
			}
		}
		else if (flag8)
		{
			ai[1] = 0f;
			ai[2] = 0f;
		}
		if (Main.netMode != 1 && type == 120 && ai[3] >= (float)num58)
		{
			int targetTileX = (int)Main.player[target].Center.X / 16;
			int targetTileY = (int)Main.player[target].Center.Y / 16;
			Vector2 chosenTile = Vector2.Zero;
			if (AI_AttemptToFindTeleportSpot(ref chosenTile, targetTileX, targetTileY, 20, 9))
			{
---
		{
			ai[0] = 2f;
			life = lifeMax;
			netUpdate = true;
			dontTakeDamage = true;
			return;
		}
		if ((type == 517 || type == 422 || type == 507 || type == 493) && ai[2] != 1f)
		{
			ai[2] = 1f;
			ai[1] = 0f;
			life = lifeMax;
			dontTakeDamage = true;
			netUpdate = true;
			return;
		}
		if (type == 548 && ai[1] != 1f)
		{
			ai[1] = 1f;
			ai[0] = 0f;
			life = lifeMax;
			dontTakeDamageFromHostiles = true;
			netUpdate = true;
			return;
		}
		if (Main.netMode != 1 && Main.getGoodWorld && (type == 42 || type == 176 || (type >= 231 && type <= 235)))
		{
			StingerExplosion();
		}
		if (Main.netMode != 1 && Main.getGoodWorld)
		{
---
		else if (type == 120)
		{
			width = 18;
			height = 40;
			aiStyle = 3;
			damage = 40;
			defense = 30;
			lifeMax = 370;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath6;
			knockBackResist = 0.4f;
			value = 600f;
		}
		else if (type == 121)
		{
			width = 40;
			height = 30;
			aiStyle = 14;
			damage = 45;
			defense = 20;
			lifeMax = 60;
			HitSound = SoundID.NPCHit1;
			alpha = 55;
			knockBackResist = 0.8f;
			scale = 1.1f;
		}
		else if (type == 122)
		{
			noGravity = true;
			width = 20;
			height = 20;
			aiStyle = 22;
			damage = 60;
			defense = 22;
			lifeMax = 220;
			HitSound = SoundID.NPCHit1;

```


---

## 🤖 Assistant · 2026-08-11T04:00:35.836Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed:
- ChaosElemental (120): aiStyle 3 (fighter). Teleport at 60679 uses NewNPC? It calls `AI_AttemptToFindTeleportSpot` then presumably spawns a teleport NPC — that's a NewNPC not NewProjectile. So no attack projectile; teleport only. Good answer for user question 3.
- StingerExplosion (53147): only called from checkDead at 78887 for getGoodWorld (FTW) hornets (42/176/231-235) — death stinger burst. So line 53147 is a death event helper, not an AI attack.

RuneWizard (172): the type==172 blocks at 10385 etc are SetDefaults (stats). At 20800 region within AI() main chain — let me check whether RuneWizard fires a projectile (user asked). Let me grep NewProjectile near 20800-21300.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:00:36.817Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=20780 && NR<=21340 {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"NewProjectile\\|aiStyle ==\\|type == 172\\|NewNPC\" | head -20; echo ---; grep -n \"= 172;\" NPCID.cs; grep -n \"= 85;\" NPCID.cs",
 "description": "Check RuneWizard AI block for projectiles"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:01:02.112Z

**📎 ToolResult**

```
21:20800: 			if (type == 172)
35:20814: 				if (type == 172)
86:20865: 					else if (type == 172)
148:20927: 					else if (type == 172)
217:20996: 			else if (type == 172)
343:21122: 										Projectile.NewProjectile(GetSpawnSource_ForProjectile(), num98 * 16 + 8, num99 * 16 + 8, 0f, 0f, 596, 0, 1f, Main.myPlayer, target);
357:21136: 						NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2 + direction * 8, (int)position.Y + 20, 25);
402:21181: 							int num106 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector13.X, vector13.Y, num101, num102, num105, num104, 0f, Main.myPlayer);
423:21202: 								NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2, (int)position.Y - 8, 30);
427:21206: 								NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2, (int)position.Y - 8, 665);
431:21210: 								NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2, (int)position.Y - 8, 33, 0, 0f, 0f, 0f, flag4 ? 1 : 0);
447:21226: 								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vec.X, vec.Y, 0f, 0f, 1092, 13, 0f, Main.myPlayer, 0f, 45f, target);
449:21228: 							else if (type == 172)
461:21240: 								int num113 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector14.X, vector14.Y, num108, num109, num112, num111, 0f, Main.myPlayer);
500:21279: 			else if (type == 172)
---
11409:	public const short RuneWizard = 172;
11235:	public const short Mimic = 85;

```


---

## 🤖 Assistant · 2026-08-11T04:01:16.584Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
RuneWizard's projectile is at 21240 (in the pre-43233 chain, aiStyle 4 — Caster AI). Let me read 21226-21245 to get the details. Since it's outside the requested line list but the user asked about RuneWizard(172), I should include it.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:01:16.684Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '21226,21245p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; awk 'NR>=21100 && NR<=21245 {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"aiStyle\\|case \\|type ==\\|num105 =\\|num112 =\" | head",
 "description": "Read RuneWizard projectile block"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:01:42.141Z

**📎 ToolResult**

```
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vec.X, vec.Y, 0f, 0f, 1092, 13, 0f, Main.myPlayer, 0f, 45f, target);
							}
							else if (type == 172)
							{
								float num107 = 10f;
								Vector2 vector14 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
								float num108 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector14.X + (float)Main.rand.Next(-10, 11);
								float num109 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector14.Y + (float)Main.rand.Next(-10, 11);
								float num110 = (float)Math.Sqrt(num108 * num108 + num109 * num109);
								num110 = num107 / num110;
								num108 *= num110;
								num109 *= num110;
								int num111 = 40;
								int num112 = 129;
								int num113 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector14.X, vector14.Y, num108, num109, num112, num111, 0f, Main.myPlayer);
								Main.projectile[num113].timeLeft = 300;
								localAI[0] = 0f;
							}
						}
					}
---
32:21131: 				else if (type == 24)
47:21146: 							if (type == 285 || type == 286)
51:21150: 							if (type == 281 || type == 282)
58:21157: 							if (type == 283 || type == 284)
70:21169: 							int num105 = 290;
71:21170: 							if (type == 285 || type == 286)
73:21172: 								num105 = 291;
76:21175: 							if (type == 281 || type == 282)
78:21177: 								num105 = 293;
84:21183: 							if (num105 == 291)

```


---

## 🤖 Assistant · 2026-08-11T04:01:47.011Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
RuneWizard (172): proj 129 = ? Let me grep. Probably "RuneBlast"? Let me check. Also which aiStyle contains this — 21100 region is in main AI() before 43233; the block around 21122/21136/21181 is likely aiStyle 4 (caster). Let me find the aiStyle guard. grep "aiStyle == 4" near.

Also need Mimic check (85) — the type==85 at 9837 is SetDefaults. aiStyle 85? 38967 `else if (aiStyle == 85)` — Big Mimic special? No, aiStyle 85 is... hmm, mimic aiStyle is 85? Actually BigMimic uses aiStyle 87 (AI_87_BigMimic). aiStyle 85 is likely "Mimic"? Let me not worry. User asked about Mimic(85) — whether it has launches. AI_87_BigMimic_ShootItem at 45152 has Projectile.NewProjectile? Let's check whether 45142-45177 has NewProjectile — not in our list, so no.

Let me check proj 129 name and the aiStyle for the caster block (20800 area is within main AI()).
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:01:48.393Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"= 129;\" ProjectileID.cs; echo ---; awk 'NR>=20600 && NR<=20810 {print NR\": \"$0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"aiStyle ==\" | tail -5; echo ---; grep -n \"aiStyle = 4;\" NPCID.cs | head -2; grep -n \"if (type == 172)\\|type == 172\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | sed -n '1,3p'; grep -n \"else if (aiStyle == 4)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Find proj 129 name and aiStyle 4 dispatch"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:01:59.337Z

**📎 ToolResult**

```
618:	public const short RuneBlast = 129;
---
160:20759: 		if (aiStyle == 5)
165:20764: 		if (aiStyle == 6)
170:20769: 		if (aiStyle == 7)
175:20774: 		if (aiStyle == 8)
---
11086:		else if (type == 172)
20800:			if (type == 172)
20814:				if (type == 172)

```


---

## 🤖 Assistant · 2026-08-11T04:02:02.161Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The aiStyle == N blocks at 20759-20774 set flags, then a big section (20800+) handles things. The RuneWizard block is at 21226-21240. Which aiStyle gate? Let me look above 21100 for the gate. Actually the block at 21122 `Projectile.NewProjectile(..., 596, ...)` and 21181 launches are in some gate. Let me look for the enclosing `if (aiStyle ==` between 20810 and 21100.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:02:02.801Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (aiStyle == \\|switch (aiStyle\\|case 4:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>=19774 && $1<=43233' | head -40",
 "description": "List aiStyle dispatch conditions in main AI chain"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:02:09.495Z

**📎 ToolResult**

```
19774:		if (aiStyle == 0)
19894:		if (aiStyle == 1)
19899:		if (aiStyle == 2)
19904:		if (aiStyle == 3)
19909:		if (aiStyle == 4)
20759:		if (aiStyle == 5)
20764:		if (aiStyle == 6)
20769:		if (aiStyle == 7)
20774:		if (aiStyle == 8)
21349:		if (aiStyle == 9)
21553:		if (aiStyle == 10)
21904:		if (aiStyle == 11)
22289:		if (aiStyle == 12)
22604:		if (aiStyle == 13)
22895:		if (aiStyle == 14)
23544:		if (aiStyle == 15)
23549:		if (aiStyle == 16)
24079:		if (aiStyle == 17)
24210:		if (aiStyle == 18)
24465:		if (aiStyle == 19)
24596:		if (aiStyle == 20)
24674:		else if (aiStyle == 21)
24726:		else if (aiStyle == 22)
25316:		else if (aiStyle == 23)
25396:		else if (aiStyle == 24)
25621:		else if (aiStyle == 25)
25714:		else if (aiStyle == 26)
25718:		else if (aiStyle == 27)
26141:		else if (aiStyle == 28)
26299:		else if (aiStyle == 29)
26497:		else if (aiStyle == 30)
27116:		else if (aiStyle == 31)
27736:		else if (aiStyle == 32)
28055:		else if (aiStyle == 33)
28360:		else if (aiStyle == 34)
28640:		else if (aiStyle == 35)
28876:		else if (aiStyle == 36)
29111:		else if (aiStyle == 37)
29115:		else if (aiStyle == 38)
29257:		else if (aiStyle == 39)

```


---

## 🤖 Assistant · 2026-08-11T04:02:28.730Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So the RuneWizard block (20800-21248) lies within `if (aiStyle == 4)` block (19909-20759)? No — aiStyle==4 block starts 19909 and ends before 20759 (aiStyle==5). 21240 > 20759, so it's after the aiStyle 5/6/7/8 flag lines but... those `if (aiStyle == 5)` at 20759 are probably tiny (SetDefaults-ish flags?). Hmm, the aiStyle==4 block spans 19909 → 20758. But 20800 (type == 172) is beyond.

Wait — the aiStyle 5,6,7,8 "if" blocks are each only ~5 lines (20759→20764→20769→20774), so they're tiny. Then what contains 20800-21348? Maybe the aiStyle==4 block ends later. The listed boundaries: aiStyle 4 starts 19909; next explicit is aiStyle==5 at 20759 but those might be nested. Given the structure, the Caster AI (aiStyle 4) big block with teleports and projectile launches at 21181/21240 is indeed aiStyle 4 — Rune Wizard, Ragged Caster, Necromancer, Tim, Dark Caster, Goblin Sorcerer, Mindflayer, etc. — that's where all caster projectiles are (21181 = generic caster bolt switch). So RuneWizard fires RuneBlast(129) speed 10, dmg 40, within aiStyle 4 caster chain at line 21240.

Good — I have enough. Let me also confirm the gate `if (aiStyle == 4)` at 19909 — read a couple lines to confirm it's the caster. Actually it's fine: the caster AI at ~19909-21348 includes the type-172 special. The user only asked to identify RuneWizard; I'll state "AI() 主链 aiStyle 4（施法者）段，21240 行".

Also let me double check 59978's enclosing — I claimed type 424 (NebulaSoldier). From the earlier read: `else if (type == 424) { for (num174...) NewProjectile(... num172=573 NebulaBolt...)}`. Yes.

And 59972: `else if (type == 411)` → proj 537 with ai0=0, ai1=whoAmI. Yes.
And 59967: type 292 loop (4 bullets). Wait: `if (type == 292) { for num173<4 ... NewProjectile }` at 59967; 59972 = type 411; 59978 = type 424 loop; 59988 = else generic.

So mapping of launch lines in the big block: 59967 (TacticalSkeleton), 59972 (StardustSoldier), 59978 (NebulaSoldier), 59988 (all other types in the set).

Now let me also verify what 57431 gate does vs 57468 gate: 57468 is the big "ranged attacker" gate list which includes the types I found plus more (343, 47, 67, 109, 110, 111, 120, 163, 164, 239, 168, 199, 206, 214-220, 226, 243, 251, 257, 258, 290-293, 305-309, 348-351, 379-380, 430-436, 591, 381-383, 386, 391, 449-452, 466, 464, 166, 469, 468, 471, 470, 480-482, 411, 424, 409, 494-506, 425, 427, 426, 428, 580, 508, 415, 419, 520, 524-527, 528, 529, 530, 532, 582, 624, 631). That's the "ranged fighter" list for opening doors etc. The NewProjectile-bearing subset is the one I extracted.

Note type 591 (in list) — that's in the 57468 gate. Not relevant to projectiles.

I think I have enough to write the report. A few more checks:
1. Confirm 45905/46039 are QueenSlime (they are within 45543-46178 AI_121_QueenSlime / 45467-45543 FlyMovement). 45905 in FlyMovement (45467-45543)? No — 45905 > 45543, so in AI_121_QueenSlime. Both boss.
2. 44896 → AI_123_Deerclops_MakeSpikesBothSides (44812-44851)? 44896 > 44851 — it's in AI_123_Deerclops_FindSpotToSpawnSpike (44851-44887)? No, 44896 > 44887 → AI_123_Deerclops_TryMakingSpike (44887-44957). Deerclops boss spike. Fine — all Deerclops.

Let me also double check 44208/44297: 44208 in SpawnStardustMark_StardustTower (44142-44230); 44297 in SpawnStardustMark_StardustWorm (44230-44338). These are Stardust tower/worm cell spawns — Moon Lord event.

Also check remaining lines: 46376 etc all inside AI_120_HallowBoss (46299-47304). 46376 is in DoMagicEffect (46178-46299)? 46178-46299 is DoMagicEffect; 46299+ HallowBoss. 46376 > 46299 → HallowBoss. Good.

- 47414: AI_119_Dandelion (47344-47432) proj 836. Let me get proj 836 name — probably "DandelionSeed"? no that's an item. Let me grep 836 quickly. Also 79017 proj 99, 80091 proj 629, 84042 proj 578, 84588 proj 594, 51005 proj 84 (PinkLaser - Probe). Quick grep.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:02:29.904Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 836 99 629 578 594 1001; do grep -n \"= $n;\" ProjectileID.cs | head -2; done; echo ---; sed -n '84575,84590p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -20; echo ---; sed -n '84038,84044p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Look up misc projectile names and hit-effect contexts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:02:42.408Z

**📎 ToolResult**

```
2032:	public const short DandelionSeed = 836;
558:	public const short Boulder = 99;
1618:	public const short TowerDamageBolt = 629;
1516:	public const short VortexVortexLightning = 578;
1548:	public const short BlowupSmoke = 594;
2362:	public const short HorsemanPumpkin = 1001;
---
					Dust dust = Main.dust[num197];
					dust.velocity *= 5f;
					num197 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 100, default(Color), 1.5f);
					dust = Main.dust[num197];
					dust.velocity *= 4f;
					Main.dust[num197].noGravity = true;
				}
				if (Main.netMode != 1)
				{
					for (int num198 = 0; num198 < 4; num198++)
					{
						float num199 = (float)(num198 < 2).ToDirectionInt() * (MathF.PI / 8f + MathF.PI / 4f * Main.rand.NextFloat());
						Vector2 vector21 = new Vector2(0f, (0f - Main.rand.NextFloat()) * 0.5f - 0.5f).RotatedBy(num199) * 6f;
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector21.X, vector21.Y, 594, 0, 0f, Main.myPlayer);
					}
				}
---
								flag3 = false;
							}
							if (flag3)
							{
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), num152 * 16 + 8, num153 * 16 + 8, 0f, 0f, 578, 0, 1f, Main.myPlayer);
								flag2 = true;
								break;

```


---

## 🤖 Assistant · 2026-08-11T04:03:19.463Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
84588 proj 594 BlowupSmoke (death effect, HitEffect — Martian Saucer death smoke?). 84042 proj 578 VortexVortexLightning (Vortex pillar death lightning in HitEffect). Good enough — these are death/visual effects, not attacks.

Now I have everything. Let me also verify two details in the big block: the trigger for shooting requires the NPC to be on ground + LOS + target detection (stealth/itemAnimation), distance < num181, and cooldown counts down only while grounded. And each type's ai[1] cooldown num163 listed.

Let me quickly verify Giga Zapper (389) block at 59440-59463: `if (type == 389)` with ai[2] counting to 20 then reset to -10/-20/-30; fires proj 437 at direction*6, dmg 25, needs Main.netMode != 1. Note it's not gated on LOS/ground explicitly in that snippet? Let me re-check lines 59441-59463 — the snippet: `if (type == 389) { if confused ai[2]=-60 else { ai[2]+=1 until 20; justHit → ai[2]=-30; if ai[2]==20 && netMode!=1 → fire }}`. No LOS/ground check in that fragment. OK.

One more: for the answer to question 2, I need to describe the structure: the block at 59469 (`if (type == 110 || ... )`) — the complete list. Also note the pre-block at 57468 (ranged fighter gate) and per-type cooldown values.

Also worth noting lines 56575-56685 etc in fighters before our launch list (no projectiles). Fine.

Also confirm 56733's enclosing gate: type 631 is inside AI_003_Fighters (which starts 56245) — yes, at 56685.

Wait — 56733 is in AI_003_Fighters which starts at 56245? 56685 > 56245 yes. Good.

Now also the user asked about "骷髅法师系" (skeleton mages) — those are casters (aiStyle 4) in main chain, not in our line list. I can mention that they're in the aiStyle-4 chain before 43233, outside scope. Also "漂浮眼/僵尸系特殊发射" — AI_002_FloatingEye has no NewProjectile (only StingerExplosion helper used at death). Zombies: none in list.

Also "Hornet 族毒刺（210/211/215?，黄蜂 aiStyle 可能是 18 或在本段）" — actual hornets: 42, 176 (MossHornet), 231-235 variants, aiStyle 5 (AI_005_EaterOfSouls), launch at 51189. Note 214/215/216 are pirates, not hornets — the user guessed 215; correct them.

Note aiStyle for hornet: they're in AI_005_EaterOfSouls method, which corresponds to aiStyle 5. Good.

Now compose the final answer with tables.

Key: regular-enemy table (focus):

AI_003_Fighters (aiStyle 3 战士族), line 56245 起：
1. Rock Golem 631 | 56733 | proj 909 RockGolemRock | trigger: target within 320px + LOS, ai[2] reaches 68 (100-32) during 100-tick windup; dmg 20; speed 8.
2. Nailhead 463 | 57611 | proj 498 Nail | trigger: justHit && localAI[3]<=0 && 1/3 chance; burst 3-6; dmg = npc.damage*0.15; speed 8-12.
3. Vortex Rifleman 425 | 59011 | proj 577 VortexLaser | ai[3] aim timer reaches 30 (needs target within 800px, roughly horizontal, LOS); fires 4 bullets speed 20 dmg GetAttackDamage(75,50). (Vortex pillar event though — lunar event. Hmm. The user's exclusion list: 星柱 83-85/94-97 excluded — Vortex Rifleman is part of lunar event (NPC 425). Should I exclude? The user's exclusion is "非星柱 83-85/94-97" referring to aiStyle numbers? They wrote aiStyle ranges. Vortex Rifleman aiStyle = 3 actually. But it's a lunar pillar enemy. The user's candidate list doesn't include it. I'll include it in the regular table but flag it as lunar-pillar spawn, so they can decide. Actually to keep clean: I'll put a "边界情况" note.
4. Black Recluse 163/238, Jungle Creeper 236/237 | 59266 | proj 472 WebSpit | expertMode only, LOS, timer 180-900 ticks, speed 8, dmg 18. (Ragged Caster is separate - no. These are spiders. Note: 163=BlackRecluse, 238=BlackRecluseWall, 236=JungleCreeper, 237=JungleCreeperWall.)
5. Ice Golem 243 | 59331 | proj 257 FrostBeam | timer rand(30..900)*lifeRatio+30, grounded + facing player + LOS; speed 15, dmg 32.
6. Eyezor 251 | 59373 | proj 83 EyeLaser | timer rand(60..1800)*lifeRatio+15, grounded+LOS+range<700; speed 15, dmg 30.
7. Giga Zapper 389 | 59460 | proj 437 GigaZapperSpear | ai[2] reaches 20 (justHit resets -30); horizontal direction*6, dmg 25. (Martian invasion enemy.)
8. Big block 59469 gate (line 59967/59972/59978/59988):
   - 110 SkeletonArcher: cd 70, speed 11, FlamingArrow 82, dmg 35, range 700 (default)
   - 111 GoblinArcher: cd 180, speed 9, WoodenArrowHostile 81, dmg 11
   - 206 IcyMerman: cd 50, speed 7, IcewaterSpit 177, dmg 37
   - 214 PirateDeadeye: cd 50, speed 10, BulletDeadeye 180, dmg 25, range 500 (海盗入侵)
   - 215 PirateCrossbower: cd 90, speed 14, FlamingArrow 82, dmg 35, range 650
   - 216 PirateCaptain: cd 9 (phase 1) speed 9 BulletDeadeye 180 dmg 30; after localAI[2]>=20 (后期) cd = max(60,180-20*hits) speed 15 CannonballHostile 240 dmg 100
   - 290 Paladin: cd 30, speed 9, PaladinsHammerHostile 300, dmg 60 (expert ×0.75)
   - 291 SkeletonSniper: cd 200, speed 4, SniperBullet 302, dmg 100
   - 292 TacticalSkeleton: cd 120, fires at 119, 4连发 BulletDeadeye 180 dmg 50 speed 12
   - 293 SkeletonCommando: cd 90, speed 4, RocketSkeleton 303, dmg 60
   - 350 ElfArcher: cd 110, speed 11, FlamingArrow 82, dmg 45 (霜月)
   - 379/380 CultistArcherBlue/White: cd 80, speed 11, FlamingArrow 82, dmg 40 (地牢门口事件怪/拜月教)
   - 381 BrainScrambler: cd 80, speed 7, BrainScramblerBolt 436, dmg 24 (火星)
   - 382 RayGunner: cd 80, speed 7, RayGunnerLaser 438, dmg 30 (火星)
   - 389 GigaZapper: separate block (59460)
   - 449-452 BoneThrowingSkeleton 1-4: cd 70, speed 7, SkeletonBone 471, dmg 15, range 200
   - 468 DrManFly: cd 70, speed 7.5, DrManFlyFlask 501, dmg 50, range 400, 仅日食生效 (!Main.eclipse 时禁射)
   - 481 GreekSkeleton: cd 100, speed 8, JavelinHostile 508, dmg 18, range 400, 带预判修正
   - 409 StardustSpiderBig: 不发射弹幕，改 spawn NPC 410 (小蜘蛛) (~59982 NewNPC)
   - 411 StardustSoldier: cd 330, speed 1, StardustSoldierLaser 537, dmg GetAttackDamage(60,45) (星尘柱)
   - 424 NebulaSoldier: cd 180, 4连 NebulaBolt 573 dmg GetAttackDamage(60,45), 脚下向上喷雾 (星云柱)
   - 426 VortexHornetQueen: cd 60, speed 7, VortexAcid 581 dmg GetAttackDamage(60,45), 预判命中点 (旋涡柱)
   - 498-506 Salamander 族: cd 70, speed 7, SalamanderSpit 572, dmg 14, range 190
   - 520 MartianWalker: cd 15, speed 8, MartianWalkerLaser 592, dmg 35, range 700? (num181 default 700 for 520 — no override) (火星)
   - 109 Clown: 60212 (separate block): proj 75 HappyBomb dmg 80, 每 60 tick 后 4/5 概率扔炸弹否则 spawn ChatteringTeethBomb(378), bomb vel (3-8)*dir, (-8..-5)
   Also gate note: 开火需落地 + LOS + 玩家处于攻击/隐身检测 + 距离 < num181。

AI_005_EaterOfSouls (aiStyle 5):
- Hornets 42/176/231-235 | 51189 | Stinger 55, speed 8, dmg 10*scale (MossHornet 30*scale), timer ai[1]>=130, LOS, 朝移动方向; timeLeft 300.
- Probe 139 | 51005 | PinkLaser 84, dmg GetAttackDamage(25,22), timer 120 (机械皇后在场 360), 速度 8/预判 — 机械 Boss 附属。
- BloodSquid 619 | 51287 | BloodShot 811, dmg 35, speed 15, getGoodWorld — 血月。
- StingerExplosion 53147: checkDead (78887) FTW 死亡毒刺爆散, type 42/176/231-235.

AI_001_Slimes (aiStyle 1):
- SpikedIceSlime 184 | 61588/61608 | IceSpike 174, expert: 5连发 <120px; 普通: 单发 <200px dmg 9
- SlimeSpiked 535 | 61643/61663 | SpikedSlimeSpike 605 同上
- SpikedJungleSlime 204 | 61827/61849 | JungleSpike 176, expert 5连发 <200px; 普通 <400px dmg 13
- 61104: BlueSlime(1)/59/147/184/537 (SlimeCanContainItems) | PoisonDartShotFromSlimes 1073, dmg 20, direction*12 — ai[1]==539 时 (被毒镖陷阱射中后反击), 1/300 概率每 tick
- QueenSlimeMinionBlue 658 / Pink 659 | 61708/61743/61792 | 920/921 — Queen Slime boss 附属

Others:
- RuneWizard 172 | 21240 (aiStyle 4 caster chain, pre-43233) | RuneBlast 129, speed 10, dmg 40, timeLeft 300.
- ChaosElemental 120 | 60679 NewNPC teleport only — no projectile.
- Mimic 85: no NewProjectile in its AI.

Now the boss/event table with all remaining lines.

Mapping:
- 44208, 44297 → SpawnStardustMark_StardustTower/StardustWorm — 月柱/星尘标记
- 44697, 44749, 44770, 44896 → AI_123_Deerclops (+helpers) — Deerclops boss
- 45905, 46039 → AI_121_QueenSlime — Queen Slime boss
- 46376, 46646, 46655, 46681, 46757, 46788, 46830, 46870, 46970, 47108, 47139, 47179, 47188, 47414 — wait 47414 is Dandelion. Others → AI_120_HallowBoss (Empress).
- 47414 → AI_119_Dandelion, DandelionSeed 836 — 小动物/环境
- 47770, 47874 → AI_117_BloodNautilus + CallForHelp — Dreadnautilus 血月
- 49649, 49650, 49875 → AI_069_DukeFishron
- 50251 → AI_037_Destroyer
- 51005 → Probe 激光（机械 Boss 附属，AI_005_EaterOfSouls 内）
- 51287 → BloodSquid（血月，AI_005）
- 53147 → StingerExplosion（FTW 蜂类死亡爆刺）
- 54919, 55187, 55225, 55342, 55358, 55374, 55381, 55387 → AI_007_TownEntities 城镇 NPC 防卫攻击
- 56733, 57611, 59011, 59266, 59331, 59373, 59460, 59967, 59972, 59978, 59988, 60212 → AI_003_Fighters（已展开）
- 61104, 61588, 61608, 61643, 61663, 61827, 61849 → AI_001_Slimes（已展开）
- 61708, 61743, 61792 → Queen Slime minions（AI_001_Slimes 内, Boss 附属）
- 62459, 62523 → AI_110_Betsy (DD2)
- 62862 → HeadlessHorseman (AI_026, 南瓜月)
- 62934 → StardustSpiderSmall 410 (AI_026, 星尘柱)
- 62980 → NebulaBeast 423 (AI_026, 星云柱)
- 64415, 64596 → AI_107_ImprovedWalkers: 64415 = DD2Ogre(576) 冲撞/吐痰; 64596 = DD2 军团 (Drakin 570/571, Javelinst 561-563, GoblinBomber 555-557, GoblinShark 620)
- 65404, 65420, 65477, 65500, 65555, 65561, 65643, 65837 → AI_084_LunaticCultist
- 66450, 66459, 66468 → AI_109_DarkMage (DD2)
- 66968 → AI_111_DD2LightningBug (DD2)
- 79017 → checkDead: RockGolem(631) FTW 死亡落 Boulder(99) dmg 70
- 79090 → DropTombstoneTownNPC 墓碑
- 80091, 80100, 80109, 80119, 80174 → DoDeathEvents（月柱 629 TowerDamageBolt 等 boss 死亡事件）
- 84042 → HitEffect: VortexVortexLightning 578（旋涡柱死亡闪电）
- 84588 → HitEffect: BlowupSmoke 594（爆炸烟雾，视觉）

Verify 79017 — type 631 (Rock Golem) getGoodWorld death boulder. Also the user asked "骷髅神射/爆破/战术（491/492/493）" — correct IDs: 291 SkeletonSniper, 293 SkeletonCommando, 292 TacticalSkeleton. Should mention correction.

Also mention 491-493 don't exist as such. Actually 493 = ? From checkDead we saw type 493 in a list (517/422/507/493). 493 = "MoonLordCore"? Let me quickly grep 491-493 to be accurate in the correction.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:03:19.950Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for n in 491 492 493 59 147 537; do grep -n \"= $n;\" NPCID.cs | head -1; done",
 "description": "Verify IDs 491-493 and slime item set members"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:03:28.301Z

**📎 ToolResult**

```
12043:	public const short PirateShip = 491;
12045:	public const short PirateShipCannon = 492;
12047:	public const short LunarTowerStardust = 493;
11183:	public const short LavaSlime = 59;
11359:	public const short IceSlime = 147;
12139:	public const short SandSlime = 537;

```


---

## 🤖 Assistant · 2026-08-11T04:03:29.953Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. 491/492/493 = PirateShip/PirateShipCannon/LunarTowerStardust — user's guess was wrong; correct are 291/292/293.

Now write the final markdown report.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:04:15.120Z · glm-x-preview-260804

````
# NPC.cs 43233 行后 Projectile.NewProjectile 归属分析

## 一、方法边界（43233 行后与发射点相关的方法）

| 方法 | 行号范围 | 性质 |
|---|---|---|
| AI_123_Deerclops 及辅助 | 44338–45045 | Boss（克苏鲁之眼/鹿角怪 Deerclops） |
| AI_121_QueenSlime | 45467–46178 | Boss（史莱姆皇后） |
| AI_120_HallowBoss | 46299–47344 | Boss（光之女皇） |
| AI_117_BloodNautilus | 47488–47882 | 血月事件（恐惧鹦鹉螺） |
| AI_069_DukeFishron | 49143–50129 | Boss（猪鲨） |
| AI_037_Destroyer | 50129–50626 | Boss（毁灭者） |
| AI_005_EaterOfSouls | 50626–51312 | aiStyle 5（噬魂者/黄蜂/腐蚀者等） |
| AI_002_FloatingEye | 52673–53132 | aiStyle 2（无发射点） |
| StingerExplosion | 53132–53195 | 死亡爆刺辅助（仅 checkDead:78887 调用） |
| AI_007_TownEntities | 53366–55982 | 城镇 NPC 防卫攻击 |
| **AI_003_Fighters** | **56245–60735** | **aiStyle 3 战士族（本次重点）** |
| AI_001_Slimes | 60735–62141 | aiStyle 1 史莱姆族 |
| AI_110_Betsy | 62266–62809 | DD2 Boss |
| AI_026_Unicorns | 62809–63372 | aiStyle 26（独角兽 + 混入的事件怪） |
| AI_107_ImprovedWalkers | 63372–64921 | aiStyle 107（DD2 军团为主） |
| AI_084_LunaticCultist | 64921–65959 | Boss（拜月教邪教徒） |
| AI_109_DarkMage / AI_111_DD2LightningBug | 66392–67003 | DD2 事件 |
| checkDead / DoDeathEvents / HitEffect | 78828+ / 79998+ / 82421+ | 死亡与视觉特效 |

## 二、AI_003_Fighters「通用远程射击大块」(59469 行门控) — 全部 type 清单

门控行 59469：
```csharp
if (type == 110 || 111 || 206 || 214 || 215 || 216 || 290 || 291 || 292 || 293 || 350
 || 379 || 380 || 381 || 382 || (449..452) || 468 || 481 || 411 || 409 || (498..506)
 || 424 || 426 || 520)
```
**除已知 111/214/215/216 外，还覆盖：** 110(骷髅弓手)、206(冰鱼人)、290(圣骑士)、291(骷髅狙击手)、292(战术骷髅)、293(骷髅爆破手)、350(精灵弓手)、379/380(拜月教弓手蓝/白)、381(大脑扰乱器)、382(光线枪手)、449–452(扔骨头骷髅×4)、468(苍蝇博士)、481(希腊骷髅)、409(星尘蜘蛛大)、411(星尘士兵)、424(星云士兵)、426(旋涡蜂后)、498–506(蝾螈族 9 变种)、520(火星步行者)。**389(千兆电击器) 不在此门内，是 59441 行的独立块（59460 发射）。**

**公共触发条件（该块所有成员）**：落地(velocity.Y==0) → 与目标有视线(Collision.CanHit) → 玩家处于"可被察觉"状态(`stealth!=0 || itemAnimation!=0`，否则 60092 行强制取消) → 距离 < 射程阈值(num181) → 进入蓄力 ai[1]=冷却值，蓄力减半时(ai[1]==num163/2)发射；justHit 会打断蓄力(ai[1]=30)。

### 该块逐 type 明细（发射行 59967/59972/59978/59988）

| NPC id+名 | 冷却(帧) | 弹速 | 弹幕 id+名 | 伤害 | 射程/备注 | 行号 |
|---|---|---|---|---|---|---|
| 110 SkeletonArcher 骷髅弓手 | 70 | 11 | 82 FlamingArrow | 35 | 700，默认值 | 59988 |
| **111 GoblinArcher 哥布林弓手** | 180 | 9 | **81 WoodenArrowHostile** | 11 | 700 | 59988 |
| **214 PirateDeadeye 海盗神射手** | 50 | 10 | **180 BulletDeadeye** | 25 | 500，散布±45 | 59988 |
| **215 PirateCrossbower 海盗弩手** | 90 | 14 | **82 FlamingArrow** | 35 | 650，落点补偿 0.08 | 59988 |
| **216 PirateCaptain 海盗船长** | 前期 9 / 后期 max(60, 180-20×被打次数) | 9 / 15 | **180 BulletDeadeye** / **240 CannonballHostile**(localAI[2]≥20 阶段) | 30 / 100 | 散布±50；后期发射完重置计数 | 59988 |
| 206 IcyMerman 冰鱼人 | 50 | 7 | 177 IcewaterSpit | 37 | 出膛点 Y-10 | 59988 |
| 290 Paladin 圣骑士 | 30 | 9 | 300 PaladinsHammerHostile | 60 (expert×0.75) | 700 | 59988 |
| 291 SkeletonSniper 骷髅狙击手 | 200 | 4 | 302 SniperBullet | 100 | 无重力补偿，散布±8 | 59988 |
| 292 TacticalSkeleton 战术骷髅 | 120(在 119 帧发) | 12 | 180 BulletDeadeye ×4 连发 | 50 | 每发重新瞄准+散布±40 | 59967 |
| 293 SkeletonCommando 骷髅爆破手 | 90 | 4 | 303 RocketSkeleton | 60 | 700 | 59988 |
| 350 ElfArcher 精灵弓手（霜月） | 110 | 11 | 82 FlamingArrow | 45 | 700 | 59988 |
| 379/380 CultistArcherBlue/White | 80 | 11 | 82 FlamingArrow | 40 | 700 | 59988 |
| 381 BrainScrambler 大脑扰乱器（火星） | 80 | 7 | 436 BrainScramblerBolt | 24 | 大散布±40×0.4，×0.85–1.16 随机 | 59988 |
| 382 RayGunner 光线枪手（火星） | 80 | 7 | 438 RayGunnerLaser | 30 | 同上 | 59988 |
| 449–452 BoneThrowingSkeleton 1–4 | 70 | 7 | 471 SkeletonBone | 15 | 200，部分随机重力补偿 | 59988 |
| 468 DrManFly 苍蝇博士（日食限定） | 70 | 7.5 | 501 DrManFlyFlask | 50 | 400；`!Main.eclipse` 时禁射(59994) | 59988 |
| 481 GreekSkeleton 希腊骷髅 | 100 | 8 | 508 JavelinHostile | 18 | 400，带目标速度预判(GetChaseResults 类似逻辑外，用随机补偿) | 59988 |
| 409 StardustSpiderBig 星尘蜘蛛大 | — | — | 不发射弹幕；改 spawn NPC 410 小蜘蛛(velocity=(弹速, -6+弹速Y)) | — | 星尘柱事件 | ~59982(NewNPC) |
| 411 StardustSoldier 星尘士兵（星尘柱） | 330 | 1(慢速激光) | 537 StardustSoldierLaser | GetAttackDamage(60,45) | 被打后 220 帧内禁射；ai0=0, ai1=whoAmI | 59972 |
| 424 NebulaSoldier 星云士兵（星云柱） | 180(在 179 帧发) | 向上小速度 | 573 NebulaBolt ×4 | GetAttackDamage(60,45) | 脚下喷雾式，4 连 | 59978 |
| 426 VortexHornetQueen 旋涡蜂后（旋涡柱） | 60(在 59 帧发) | 7 | 581 VortexAcid | GetAttackDamage(60,45) | 瞄玩家 Hitbox 随机点+GetChaseResults 预判 | 59988 |
| 498–506 Salamander 蝾螈族（9 变种） | 70 | 7 | 572 SalamanderSpit | 14 | 190，出膛 Y-8 | 59988 |
| 520 MartianWalker 火星步行者（火星） | 15 | 8 | 592 MartianWalkerLaser | 35 | 700，从脚底+20 发射，大随机散布 | 59988 |

### AI_003_Fighters 内其它独立块发射点

| 行号 | NPC id+名 | 弹幕 id+名 | 触发条件 | 弹速 |
|---|---|---|---|---|
| 56733 | 631 Rock Golem 岩石巨人 | 909 RockGolemRock，dmg 20 | 目标 320px 内 + 视线 → 100 帧前摇，第 68 帧(100-32)发射，且不与玩家碰撞 | 8(±0.8 随机) |
| 57611 | 463 Nailhead 钉子头 | 498 Nail，dmg=damage×0.15 | justHit 且 localAI[3]≤0 且 1/3 概率，爆 3–6 根，朝可见玩家求和方向 | 8–12 |
| 59011 | 425 Vortex Rifleman 旋涡神射手（星旋柱） | 577 VortexLaser ×4，dmg GetAttackDamage(75,50) | ai[3] 瞄准计时满 30（需 <800px、近似水平、视线），之后 10 帧冷却、180 帧循环 | 20(带 GetChaseResults 预判) |
| 59266 | 163/238 Black Recluse(+墙上)，236/237 Jungle Creeper(+墙上) | 472 WebSpit，dmg 18 | **仅 expertMode**，视线，计时 180–900 帧随机 | 8 |
| 59331 | 243 Ice Golem 冰雪巨人 | 257 FrostBeam，dmg 32 | 计时 rand(30..900)×(life/lifeMax)+30，落地+面向玩家+视线 | 15 |
| 59373 | 251 Eyezor 僵尸眼（日食） | 83 EyeLaser，dmg 30 | 计时 rand(60..1800)×(life/lifeMax)+15，落地+视线+距离<700 | 15 |
| 59460 | 389 Giga Zapper 千兆电击器（火星） | 437 GigaZapperSpear，dmg 25 | ai[2] 数到 20（justHit 重置 -30，confused -60） | 水平 direction×6 |
| 60212 | 109 Clown 小丑（血月） | 75 HappyBomb，dmg 80，timeLeft 300 | ai[2]>60 后：4/5 概率丢炸弹，1/5 改 spawn NPC 378 ChatteringTeethBomb 且 ai[2]=-120 | (3–8)×dir, Y(-8..-5) |

## 三、其它常规敌怪发射点

| NPC id+名 | 所在 aiStyle/方法 | 弹幕 id+名 | 触发条件 | 弹速 | 行号 |
|---|---|---|---|---|---|
| 42 Hornet、176 MossHornet、231–235 HornetFatty/Honey/Hornet/Little/Stingy 黄蜂族（aiStyle 5，**不是 18**；215 是海盗弩手，不是黄蜂） | AI_005_EaterOfSouls | 55 Stinger，dmg 10×scale（MossHornet 30×scale），timeLeft 300 | ai[1] 累计(rand(5,20)×0.1×scale，MossHornet/FTW 加速) ≥130，且有视线，且朝向与移动方向一致 | 8 | 51189 |
| 139 Probe 探测器（毁灭者附属，机械战时生成） | AI_005_EaterOfSouls | 84 PinkLaser，dmg GetAttackDamage(25,22) | localAI[0] ≥120（IsMechQueenUp 时 360），视线；机械皇后在场时带目标速度预判 | 8 | 51005 |
| 172 Rune Wizard 符文巫师 | AI() 主链 aiStyle 4（施法者段，43233 行之前） | 129 RuneBlast，dmg 40，timeLeft 300 | 施法者通用计时（localAI[0]），瞬移+施法 | 10 | 21240 |
| 184 SpikedIceSlime 尖刺冰雪史莱姆 | AI_001_Slimes (aiStyle 1) | 174 IceSpike，expert: GetAttackDamage 连发 / 普通 dmg 9 | expert & <120px & 视线 & 落地：5 连发；否则 <200px 单发 | 抛物线扇形 | 61588 / 61608 |
| 535 SlimeSpiked 尖刺史莱姆（王城/地牢周边） | AI_001_Slimes | 605 SpikedSlimeSpike，同上 | 同上 | 同上 | 61643 / 61663 |
| 204 SpikedJungleSlime 尖刺丛林史莱姆 | AI_001_Slimes | 176 JungleSpike，expert 5 连发 dmg GetAttackDamage / 普通 dmg 13 | expert & <200px & 视线；普通 <400px 单发 | 抛物线扇形 | 61827 / 61849 |
| 1/59/147/184/537 可含物品史莱姆（蓝/熔岩/冰/…/沙史莱姆，Set: SlimeCanContainItems） | AI_001_Slimes | 1073 PoisonDartShotFromSlimes，dmg 20 | ai[1]==539（被毒镖陷阱击中的反击标记）时 1/300 每帧（noTrapsWorld/FTW 各 -120），有目标+视线 | direction×12 水平 | 61104 |

用户提的候选核对结果：
- **骷髅神射/爆破/战术**：正确 id 是 **291/293/292**（SkeletonSniper/SkeletonCommando/TacticalSkeleton）；491/492/493 实为 PirateShip/PirateShipCannon/LunarTowerStardust。
- **Paladin 494**：错，是 **290**，弹 300 PaladinsHammerHostile。
- **ChaosElemental 120**：在 AI_003_Fighters 内瞬移（60679 行），但用的是 **NewNPC/Teleport**，**无任何 Projectile.NewProjectile**——瞬移不伴随攻击。
- **Mimic 85**：无发射点（AI_87_BigMimic 的 ShootItem 45152 处也无弹幕调用）。
- **Corruptor**：不在本批行号内（其 aiStyle 5 但本段只覆盖 42/176/231-235/139/619 的发射；腐蚀者的腐蚀唾液逻辑在 43233 之前或未含发射）。注意 **110 是 SkeletonArcher 不是 Corruptor**。
- **骷髅法师系/RaggedCaster 系**：属 AI() 主链 aiStyle 4（43233 之前），不在本批行号中。

## 四、Boss/事件/非攻击发射点对账清单

| 行号 | 归属 | 分类 |
|---|---|---|
| 44208, 44297 | SpawnStardustMark_StardustTower / _StardustWorm | 月柱事件，跳过 |
| 44697, 44749, 44770, 44896 | AI_123_Deerclops 及 spike 辅助方法 | Deerclops Boss，跳过 |
| 45905, 46039 | AI_121_QueenSlime(_FlyMovement) | 史莱姆皇后 Boss，跳过 |
| 46376, 46646, 46655, 46681, 46757, 46788, 46830, 46870, 46970, 47108, 47139, 47179, 47188 | AI_120_HallowBoss | 光之女皇 Boss，跳过 |
| 47414 | AI_119_Dandelion（弹 836 DandelionSeed） | 环境小动物，跳过 |
| 47770, 47874 | AI_117_BloodNautilus + CallForHelp | 血月事件，跳过 |
| 49649, 49650, 49875 | AI_069_DukeFishron | 猪鲨 Boss，跳过 |
| 50251 | AI_037_Destroyer | 毁灭者 Boss，跳过 |
| 51005 | Probe 139 激光（AI_005 内） | 机械 Boss 附属，已在上表展开 |
| 51287 | 619 BloodSquid → 811 BloodShot | 血月事件，跳过 |
| 53147 | StingerExplosion（仅 checkDead:78887，FTW 下蜂类死亡爆刺 4–8 根） | 死亡效果，跳过 |
| 54919, 55187, 55225, 55342, 55358, 55374, 55381, 55387 | AI_007_TownEntities（城镇 NPC 防卫攻击，含 124/142/227/108/663 分支） | 城镇 NPC，跳过 |
| 61708, 61743, 61792 | 658/659 QueenSlimeMinionBlue/Pink → 920/921（在 AI_001_Slimes 内） | 史莱姆皇后附属，跳过 |
| 62459, 62523 | AI_110_Betsy | DD2 Boss，跳过 |
| 62862 | 315 HeadlessHorseman → 1001 HorsemanPumpkin（每 480 帧，dmg GetAttackDamage(40,30)） | 南瓜月事件，跳过 |
| 62934 | 410 StardustSpiderSmall → 538 Twinkle ×3 后自毁 | 星尘柱事件，跳过 |
| 62980 | 423 NebulaBeast → 575 NebulaSphere（ai[1]==30 帧，spriteDir×-7） | 星云柱事件，跳过 |
| 64415 | AI_107 flag3 块 = 576 DD2OgreT2（case ai[1]==2 撞地波 683 DD2OgreSmash / ai[1]==1 吐痰 676 DD2OgreSpit） | DD2 事件，跳过 |
| 64596 | AI_107 flag12 块 = 570/571 DD2Drakin(671)、561–563 DD2Javelinst(662/685)、555–557 DD2GoblinBomber(681)、620 GoblinShark(811) | DD2 事件，跳过 |
| 65404, 65420, 65477, 65500, 65555, 65561, 65643, 65837 | AI_084_LunaticCultist | 拜月教邪教徒 Boss，跳过 |
| 66450, 66459, 66468 | AI_109_DarkMage | DD2 事件，跳过 |
| 66968 | AI_111_DD2LightningBug | DD2 事件，跳过 |
| 79017 | checkDead：631 Rock Golem，FTW(getGoodWorld) 死亡落弹 99 Boulder dmg 70 | 死亡效果，跳过 |
| 79090 | DropTombstoneTownNPC | 墓碑，跳过 |
| 80091, 80100, 80109, 80119, 80174 | DoDeathEvents（如 417–419/518 月柱死亡 → 629 TowerDamageBolt 等） | Boss 死亡事件，跳过 |
| 84042 | HitEffect：旋涡柱死亡闪电 578 VortexVortexLightning | 死亡视觉，跳过 |
| 84588 | HitEffect：594 BlowupSmoke ×4 | 死亡视觉，跳过 |

**边界提示**：381/382/389/520（火星）、468（日食）、214–216（海盗入侵）、350（霜月）、379/380（拜月教门口）、409/411/424/426/59011（星柱）、29266 蜘蛛/243/251 等，虽结构上属 AI_003_Fighters 通用块，但语义上分属各入侵/事件，是否纳入"常规敌怪"由调用方按上述备注裁决。
````
