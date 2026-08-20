# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-09T11:48:25.682Z

```
对比泰拉瑞亚 1.4.0.5 与 1.4.5.6 反编译源码中「角色创建 + 玩家外观渲染」部分，找出行为差异：
- 旧版目录：~/Project/GLM/SandboxWorld/Terarria1405/
- 新版目录：~/Project/GLM/SandboxWorld/Terarria1456/（扁平结构：Terraria.GameContent.UI.Elements/、Terraria.GameContent.UI.States/、Terraria.DataStructures/、Player.cs 在根目录附近）

需要对比的文件（两边同名）：
1. UICharacterCreation.cs：_validClothStyles 列表是否变化（旧版 [0,2,1,3,8,4,6,5,7,9]）？分类条（CategoryId）结构？难度按钮（UIDifficultyButton）？HSL 取色面板？随机逻辑？新增了什么（voice/创意模式相关）？
2. UICharacter.cs：59×58 尺寸/动画帧公式 (time/0.07%14+6)*56 是否变化？
3. UICharacterSelect.cs / UICharacterListItem.cs：布局与按钮变化？
4. Player.cs 的默认外观颜色（旧版 199-205 行：hairColor 215,90,55 / skinColor 255,125,90 / eyeColor 105,90,75 / shirtColor 175,165,140 / underShirtColor 160,180,215 / pantsColor 255,230,175 / shoeColor 160,105,60）——新版是否变化？
5. PlayerDrawLayers.cs（旧版 DataStructures/，新版 Terraria.DataStructures/ 或类似）：Players[skinVar, n] 的通道索引→颜色通道映射是否变化（旧版实测：0头/3,5,7,9身/10腿=skin、4,8=undershirt、6,13,14=shirt、11=pants、12=shoes、1=眼白、2=瞳）？皮肤变体 skinVariant 数量上限（旧版 0-11）？发型数量（旧版 228）？
6. UIHairStyleButton.cs / UIClothStyleButton.cs：尺寸（44×44 / 44×80）与行为变化？

输出：「角色系统差异清单」表，每条标【必须改】【可选增强】【无变化】，附行号。我们的移植在 game/src/vui/states/UICharacterCreationState.ts、game/src/player/PaperDoll.ts、Appearance.ts。
```

---

## 📎 Attachment · skill_listing · 2026-08-09T11:48:25.684Z

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

## 🤖 Assistant · 2026-08-09T11:48:28.613Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a comparison of decompiled Terraria source code between 1.4.0.5 and 1.4.5.6 for character creation and player appearance rendering. Let me explore the directories and locate the files.

Let me start with parallel searches to find the relevant files.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:48:29.233Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1405/ 2>/dev/null | head -50; echo \"---NEW---\"; ls ~/Project/GLM/SandboxWorld/Terarria1456/ 2>/dev/null | head -50",
 "description": "List both decompiled source directories"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:29.263Z

**📎 ToolResult**

```
Achievements
Animation.cs
AssemblyInfo.cs
Audio
BitsByte.cs
Chat
Chest.cs
Cinematics
Cloud.cs
Collision.cs
CombatText.cs
DataStructures
DelegateMethods.cs
DeprecatedClassLeftInForLoading.cs
Dust.cs
Entity.cs
Enums
Extensions
FrameSkipTest.cs
Framing.cs
GameContent
GameInput
GetItemSettings.cs
Gore.cs
Graphics
HitTile.cs
ID
IngameOptions.cs
Initializers
IO
Item.cs
ItemSerializationContext.cs
Lang.cs
Libraries
Lighting.cs
Liquid.cs
LiquidBuffer.cs
Localization
Main.cs
Map
MessageBuffer.cs
Microsoft
Minecart.cs
Modules
Mount.cs
Net
NetMessage.cs
Netplay.cs
NPC.145.cs
NPC.cs
---NEW---
app.ico
app.manifest
BCrypt.Net
Microsoft.Xna.Framework.RuntimeProfile
nativefiledialog.cs
Properties
Terraria
Terraria.Achievements
Terraria.Audio
Terraria.Chat
Terraria.Chat.Commands
Terraria.Cinematics
Terraria.csproj
Terraria.DataStructures
Terraria.Enums
Terraria.GameContent
Terraria.GameContent.Achievements
Terraria.GameContent.Ambience
Terraria.GameContent.Animations
Terraria.GameContent.Bestiary
Terraria.GameContent.Biomes
Terraria.GameContent.Biomes.CaveHouse
Terraria.GameContent.Biomes.Desert
Terraria.GameContent.Creative
Terraria.GameContent.Creative.Content.Sacrifices.tsv
Terraria.GameContent.Drawing
Terraria.GameContent.Dyes
Terraria.GameContent.Events
Terraria.GameContent.FishDropRules
Terraria.GameContent.Generation
Terraria.GameContent.Generation.Dungeon
Terraria.GameContent.Generation.Dungeon.Entrances
Terraria.GameContent.Generation.Dungeon.Features
Terraria.GameContent.Generation.Dungeon.Halls
Terraria.GameContent.Generation.Dungeon.LayoutProviders
Terraria.GameContent.Generation.Dungeon.Rooms
Terraria.GameContent.Golf
Terraria.GameContent.ItemDropRules
Terraria.GameContent.Items
Terraria.GameContent.LeashedEntities
Terraria.GameContent.Liquid
Terraria.GameContent.LootSimulation
Terraria.GameContent.LootSimulation.LootSimulatorConditionSetterTypes
Terraria.GameContent.Metadata
Terraria.GameContent.Metadata.MaterialData.Materials.json
Terraria.GameContent.Metadata.MaterialData.Tiles.json
Terraria.GameContent.NetModules
Terraria.GameContent.ObjectInteractions
Terraria.GameContent.Personalities
Terraria.GameContent.Prefixes

```


---

## 🤖 Assistant · 2026-08-09T11:48:29.741Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1405 ~/Project/GLM/SandboxWorld/Terarria1456 -name \"UICharacterCreation.cs\" -o -name \"UICharacter.cs\" -o -name \"UICharacterSelect.cs\" -o -name \"UICharacterListItem.cs\" -o -name \"PlayerDrawLayers.cs\" -o -name \"UIHairStyleButton.cs\" -o -name \"UIClothStyleButton.cs\" -o -name \"UIDifficultyButton.cs\" -o -name \"UIHairColorSlider.cs\" -o -name \"UICharacterListItem.cs\" 2>/dev/null",
 "description": "Find all target comparison files in both versions"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:29.779Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacterListItem.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacter.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIClothStyleButton.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIDifficultyButton.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIHairStyleButton.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterSelect.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterCreation.cs
~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacterListItem.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacter.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIClothStyleButton.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIDifficultyButton.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIHairStyleButton.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterSelect.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterCreation.cs

```


---

## 🤖 Assistant · 2026-08-09T11:48:32.615Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All files located. Let me read the files. First UICharacterCreation.cs in both versions. Let me check sizes.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:48:34.884Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterCreation.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterCreation.cs ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacter.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacter.cs ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIHairStyleButton.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIHairStyleButton.cs ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIClothStyleButton.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIClothStyleButton.cs ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterSelect.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterSelect.cs ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacterListItem.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacterListItem.cs ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs 2>/dev/null || ls ~/Project/GLM/SandboxWorld/Terarria1456/ | grep -i player",
 "description": "Count lines of all target files"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:34.926Z

**📎 ToolResult**

```
    1513 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterCreation.cs
    2386 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterCreation.cs
      88 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacter.cs
     158 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacter.cs
    2771 ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs
    4421 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs
      76 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIHairStyleButton.cs
      97 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIHairStyleButton.cs
      91 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIClothStyleButton.cs
     109 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIClothStyleButton.cs
     290 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterSelect.cs
     311 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterSelect.cs
     299 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacterListItem.cs
     384 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacterListItem.cs
   37306 ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs
   56154 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs
  106454 total

```


---

## 🤖 Assistant · 2026-08-09T11:48:37.018Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Player.cs in new version at Terraria/Player.cs. Let me read files. Start with the smaller ones in parallel using Read.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:48:37.019Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacter.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:48:37.023Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacter.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:37.035Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.UI.Elements.UICharacter
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using ReLogic.Content;
10	using Terraria.UI;
11	
12	namespace Terraria.GameContent.UI.Elements
13	{
14	  public class UICharacter : UIElement
15	  {
16	    private static Item _blankItem = new Item();
17	    private float _characterScale = 1f;
18	    private Player _player;
19	    private Asset<Texture2D> _texture;
20	    private bool _animated;
21	    private bool _drawsBackPanel;
22	    private int _animationCounter;
23	
24	    public UICharacter(Player player, bool animated = false, bool hasBackPanel = true, float characterScale = 1f)
25	    {
26	      this._player = player;
27	      this.Width.Set(59f, 0.0f);
28	      this.Height.Set(58f, 0.0f);
29	      this._texture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/PlayerBackground", (AssetRequestMode) 1);
30	      this.UseImmediateMode = true;
31	      this._animated = animated;
32	      this._drawsBackPanel = hasBackPanel;
33	      this._characterScale = characterScale;
34	      this.OverrideSamplerState = SamplerState.PointClamp;
35	    }
36	
37	    public override void Update(GameTime gameTime)
38	    {
39	      this._player.ResetEffects();
40	      this._player.ResetVisibleAccessories();
41	      this._player.UpdateMiscCounter();
42	      this._player.UpdateDyes();
43	      this._player.PlayerFrame();
44	      if (this._animated)
45	        ++this._animationCounter;
46	      base.Update(gameTime);
47	    }
48	
49	    private void UpdateAnim()
50	    {
51	      if (!this._animated)
52	      {
53	        this._player.bodyFrame.Y = this._player.legFrame.Y = this._player.headFrame.Y = 0;
54	      }
55	      else
56	      {
57	        this._player.bodyFrame.Y = this._player.legFrame.Y = this._player.headFrame.Y = ((int) ((double) Main.GlobalTimeWrappedHourly / 0.0700000002980232) % 14 + 6) * 56;
58	        this._player.WingFrame(false);
59	      }
60	    }
61	
62	    protected override void DrawSelf(SpriteBatch spriteBatch)
63	    {
64	      CalculatedStyle dimensions = this.GetDimensions();
65	      if (this._drawsBackPanel)
66	        spriteBatch.Draw(this._texture.Value, dimensions.Position(), Color.White);
67	      this.UpdateAnim();
68	      Vector2 vector2 = dimensions.Position() + new Vector2(dimensions.Width * 0.5f - (float) (this._player.width >> 1), dimensions.Height * 0.5f - (float) (this._player.height >> 1));
69	      Item obj = this._player.inventory[this._player.selectedItem];
70	      this._player.inventory[this._player.selectedItem] = UICharacter._blankItem;
71	      Main.PlayerRenderer.DrawPlayer(Main.Camera, this._player, vector2 + Main.screenPosition, 0.0f, Vector2.Zero, 0.0f, this._characterScale);
72	      this._player.inventory[this._player.selectedItem] = obj;
73	    }
74	
75	    public void SetAnimated(bool animated)
76	    {
77	      this._animated = animated;
78	    }
79	
80	    public bool IsAnimated
81	    {
82	      get
83	      {
84	        return this._animated;
85	      }
86	    }
87	  }
88	}
89	

```


---

## 👤 User(sidechain) · 2026-08-09T11:48:37.036Z

**📎 ToolResult**

```
1	using System;
2	using Microsoft.Xna.Framework;
3	using Microsoft.Xna.Framework.Graphics;
4	using ReLogic.Content;
5	using Terraria.ID;
6	using Terraria.UI;
7	
8	namespace Terraria.GameContent.UI.Elements;
9	
10	public class UICharacter : UIElement
11	{
12		private Player _player;
13	
14		private Projectile[] _petProjectiles;
15	
16		private Asset<Texture2D> _texture;
17	
18		private static Item _blankItem = new Item();
19	
20		private bool _animated;
21	
22		private bool _drawsBackPanel;
23	
24		private float _characterScale = 1f;
25	
26		private int _animationCounter;
27	
28		public Action PrepareAction;
29	
30		private static readonly Projectile[] NoPets = new Projectile[0];
31	
32		public bool IsAnimated => _animated;
33	
34		public UICharacter(Player player, bool animated = false, bool hasBackPanel = true, float characterScale = 1f, bool useAClone = false)
35		{
36			_player = player;
37			if (useAClone)
38			{
39				_player = player.SerializedClone();
40				_player.dead = false;
41				_player.PlayerFrame();
42			}
43			Width.Set(59f, 0f);
44			Height.Set(58f, 0f);
45			_texture = Main.Assets.Request<Texture2D>("Images/UI/PlayerBackground", (AssetRequestMode)1);
46			UseImmediateMode = true;
47			_animated = animated;
48			_drawsBackPanel = hasBackPanel;
49			_characterScale = characterScale;
50			OverrideSamplerState = SamplerState.PointClamp;
51			_petProjectiles = NoPets;
52			PreparePetProjectiles();
53		}
54	
55		private void PreparePetProjectiles()
56		{
57			if (!_player.hideMisc[0])
58			{
59				Item item = _player.miscEquips[0];
60				if (!item.IsAir)
61				{
62					int shoot = item.shoot;
63					_petProjectiles = new Projectile[1] { PreparePetProjectiles_CreatePetProjectileDummy(shoot) };
64				}
65			}
66		}
67	
68		private Projectile PreparePetProjectiles_CreatePetProjectileDummy(int projectileId)
69		{
70			Projectile projectile = new Projectile();
71			projectile.SetDefaults(projectileId);
72			projectile.isAPreviewDummy = true;
73			return projectile;
74		}
75	
76		public override void Update(GameTime gameTime)
77		{
78			if (_animated)
79			{
80				_animationCounter++;
81			}
82			base.Update(gameTime);
83		}
84	
85		private void UpdateAnim()
86		{
87			if (!_animated)
88			{
89				_player.bodyFrame.Y = (_player.legFrame.Y = (_player.headFrame.Y = 0));
90				return;
91			}
92			int num = (int)(Main.GlobalTimeWrappedHourly / 0.07f) % 14 + 6;
93			_player.bodyFrame.Y = (_player.legFrame.Y = (_player.headFrame.Y = num * 56));
94			_player.WingFrame(wingFlap: false);
95		}
96	
97		protected override void DrawSelf(SpriteBatch spriteBatch)
98		{
99			CalculatedStyle dimensions = GetDimensions();
100			if (_drawsBackPanel)
101			{
102				spriteBatch.Draw(_texture.Value, dimensions.Position(), Color.White);
103			}
104			_player.ResetEffects();
105			_player.ResetVisibleAccessories();
106			_player.UpdateMiscCounter();
107			_player.UpdateDyes();
108			if (PrepareAction != null)
109			{
110				PrepareAction();
111			}
112			_player.PlayerFrame();
113			UpdateAnim();
114			DrawPets(spriteBatch);
115			Vector2 playerPosition = GetPlayerPosition(ref dimensions);
116			Item item = _player.inventory[_player.selectedItem];
117			_player.inventory[_player.selectedItem] = _blankItem;
118			Main.PlayerRenderer.DrawPlayer(Main.Camera, _player, playerPosition + Main.screenPosition, 0f, Vector2.Zero, 0f, _characterScale);
119			_player.inventory[_player.selectedItem] = item;
120		}
121	
122		private Vector2 GetPlayerPosition(ref CalculatedStyle dimensions)
123		{
124			Vector2 result = dimensions.Position() + new Vector2(dimensions.Width * 0.5f - (float)(_player.width >> 1), dimensions.Height * 0.5f - (float)(_player.height >> 1));
125			if (_petProjectiles.Length != 0)
126			{
127				result.X -= 10f;
128			}
129			return result;
130		}
131	
132		public void DrawPets(SpriteBatch spriteBatch)
133		{
134			CalculatedStyle dimensions = GetDimensions();
135			Vector2 playerPosition = GetPlayerPosition(ref dimensions);
136			for (int i = 0; i < _petProjectiles.Length; i++)
137			{
138				Projectile projectile = _petProjectiles[i];
139				Vector2 vector = playerPosition + new Vector2(0f, _player.height) + new Vector2(20f, 0f) + new Vector2(0f, -projectile.height);
140				projectile.position = vector + Main.screenPosition;
141				projectile.velocity = new Vector2(0.1f, 0f);
142				projectile.direction = 1;
143				projectile.owner = Main.myPlayer;
144				ProjectileID.Sets.CharacterPreviewAnimations[projectile.type].ApplyTo(projectile, _animated);
145				Player player = Main.player[Main.myPlayer];
146				Main.player[Main.myPlayer] = _player;
147				Main.instance.DrawProjDirect(projectile);
148				Main.player[Main.myPlayer] = player;
149			}
150			spriteBatch.End();
151			spriteBatch.Begin(SpriteSortMode.Immediate, spriteBatch.GraphicsDevice.BlendState, spriteBatch.GraphicsDevice.SamplerStates[0], spriteBatch.GraphicsDevice.DepthStencilState, spriteBatch.GraphicsDevice.RasterizerState, null, Main.UIScaleMatrix);
152		}
153	
154		public void SetAnimated(bool animated)
155		{
156			_animated = animated;
157		}
158	}
159	

```


---

## 🤖 Assistant · 2026-08-09T11:48:37.629Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIHairStyleButton.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:48:37.631Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIHairStyleButton.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:37.634Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.UI.Elements.UIHairStyleButton
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using ReLogic.Content;
10	using Terraria.Audio;
11	using Terraria.UI;
12	
13	namespace Terraria.GameContent.UI.Elements
14	{
15	  public class UIHairStyleButton : UIImageButton
16	  {
17	    private readonly Player _player;
18	    public readonly int HairStyleId;
19	    private readonly Asset<Texture2D> _selectedBorderTexture;
20	    private readonly Asset<Texture2D> _hoveredBorderTexture;
21	    private bool _hovered;
22	    private bool _soundedHover;
23	
24	    public UIHairStyleButton(Player player, int hairStyleId)
25	      : base((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanel", (AssetRequestMode) 1))
26	    {
27	      this._player = player;
28	      this.HairStyleId = hairStyleId;
29	      this.Width = StyleDimension.FromPixels(44f);
30	      this.Height = StyleDimension.FromPixels(44f);
31	      this._selectedBorderTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode) 1);
32	      this._hoveredBorderTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelBorder", (AssetRequestMode) 1);
33	    }
34	
35	    protected override void DrawSelf(SpriteBatch spriteBatch)
36	    {
37	      if (this._hovered)
38	      {
39	        if (!this._soundedHover)
40	          SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
41	        this._soundedHover = true;
42	      }
43	      else
44	        this._soundedHover = false;
45	      Vector2 vector2 = new Vector2(-5f, -5f);
46	      base.DrawSelf(spriteBatch);
47	      if (this._player.hair == this.HairStyleId)
48	        spriteBatch.Draw(this._selectedBorderTexture.Value, this.GetDimensions().Center() - this._selectedBorderTexture.Size() / 2f, Color.White);
49	      if (this._hovered)
50	        spriteBatch.Draw(this._hoveredBorderTexture.Value, this.GetDimensions().Center() - this._hoveredBorderTexture.Size() / 2f, Color.White);
51	      int hair = this._player.hair;
52	      this._player.hair = this.HairStyleId;
53	      Main.PlayerRenderer.DrawPlayerHead(Main.Camera, this._player, this.GetDimensions().Center() + vector2, 1f, 1f, new Color());
54	      this._player.hair = hair;
55	    }
56	
57	    public override void MouseDown(UIMouseEvent evt)
58	    {
59	      this._player.hair = this.HairStyleId;
60	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
61	      base.MouseDown(evt);
62	    }
63	
64	    public override void MouseOver(UIMouseEvent evt)
65	    {
66	      base.MouseOver(evt);
67	      this._hovered = true;
68	    }
69	
70	    public override void MouseOut(UIMouseEvent evt)
71	    {
72	      base.MouseOut(evt);
73	      this._hovered = false;
74	    }
75	  }
76	}
77	

```


---

## 👤 User(sidechain) · 2026-08-09T11:48:37.635Z

**📎 ToolResult**

```
1	using Microsoft.Xna.Framework;
2	using Microsoft.Xna.Framework.Graphics;
3	using ReLogic.Content;
4	using Terraria.Audio;
5	using Terraria.UI;
6	
7	namespace Terraria.GameContent.UI.Elements;
8	
9	public class UIHairStyleButton : UIImageButton
10	{
11		private readonly Player _player;
12	
13		public readonly int HairStyleId;
14	
15		private readonly Asset<Texture2D> _selectedBorderTexture;
16	
17		private readonly Asset<Texture2D> _hoveredBorderTexture;
18	
19		private bool _hovered;
20	
21		private bool _soundedHover;
22	
23		private int _framesToSkip;
24	
25		public UIHairStyleButton(Player player, int hairStyleId)
26			: base(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanel", (AssetRequestMode)1))
27		{
28			_player = player;
29			HairStyleId = hairStyleId;
30			Width = StyleDimension.FromPixels(44f);
31			Height = StyleDimension.FromPixels(44f);
32			_selectedBorderTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode)1);
33			_hoveredBorderTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelBorder", (AssetRequestMode)1);
34		}
35	
36		public void SkipRenderingContent(int timeInFrames)
37		{
38			_framesToSkip = timeInFrames;
39		}
40	
41		protected override void DrawSelf(SpriteBatch spriteBatch)
42		{
43			if (_hovered)
44			{
45				if (!_soundedHover)
46				{
47					SoundEngine.PlaySound(12);
48				}
49				_soundedHover = true;
50			}
51			else
52			{
53				_soundedHover = false;
54			}
55			Vector2 vector = new Vector2(-5f, -5f);
56			base.DrawSelf(spriteBatch);
57			if (_player.hair == HairStyleId)
58			{
59				spriteBatch.Draw(_selectedBorderTexture.Value, GetDimensions().Center() - _selectedBorderTexture.Size() / 2f, Color.White);
60			}
61			if (_hovered)
62			{
63				spriteBatch.Draw(_hoveredBorderTexture.Value, GetDimensions().Center() - _hoveredBorderTexture.Size() / 2f, Color.White);
64			}
65			if (_framesToSkip > 0)
66			{
67				_framesToSkip--;
68				return;
69			}
70			int head = _player.head;
71			_player.head = -1;
72			int hair = _player.hair;
73			_player.hair = HairStyleId;
74			Main.PlayerRenderer.DrawPlayerHead(Main.Camera, _player, GetDimensions().Center() + vector);
75			_player.hair = hair;
76			_player.head = head;
77		}
78	
79		public override void LeftMouseDown(UIMouseEvent evt)
80		{
81			_player.hair = HairStyleId;
82			SoundEngine.PlaySound(12);
83			base.LeftMouseDown(evt);
84		}
85	
86		public override void MouseOver(UIMouseEvent evt)
87		{
88			base.MouseOver(evt);
89			_hovered = true;
90		}
91	
92		public override void MouseOut(UIMouseEvent evt)
93		{
94			base.MouseOut(evt);
95			_hovered = false;
96		}
97	}
98	

```


---

## 🤖 Assistant · 2026-08-09T11:48:37.636Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIClothStyleButton.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:37.645Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.UI.Elements.UIClothStyleButton
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using ReLogic.Content;
10	using Terraria.Audio;
11	using Terraria.UI;
12	
13	namespace Terraria.GameContent.UI.Elements
14	{
15	  public class UIClothStyleButton : UIElement
16	  {
17	    private readonly Player _player;
18	    public readonly int ClothStyleId;
19	    private readonly Asset<Texture2D> _BasePanelTexture;
20	    private readonly Asset<Texture2D> _selectedBorderTexture;
21	    private readonly Asset<Texture2D> _hoveredBorderTexture;
22	    private readonly UICharacter _char;
23	    private bool _hovered;
24	    private bool _soundedHover;
25	    private int _realSkinVariant;
26	
27	    public UIClothStyleButton(Player player, int clothStyleId)
28	    {
29	      this._player = player;
30	      this.ClothStyleId = clothStyleId;
31	      this.Width = StyleDimension.FromPixels(44f);
32	      this.Height = StyleDimension.FromPixels(80f);
33	      this._BasePanelTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanel", (AssetRequestMode) 1);
34	      this._selectedBorderTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode) 1);
35	      this._hoveredBorderTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelBorder", (AssetRequestMode) 1);
36	      UICharacter uiCharacter = new UICharacter(this._player, false, false, 1f);
37	      uiCharacter.HAlign = 0.5f;
38	      uiCharacter.VAlign = 0.5f;
39	      this._char = uiCharacter;
40	      this.Append((UIElement) this._char);
41	    }
42	
43	    public override void Draw(SpriteBatch spriteBatch)
44	    {
45	      this._realSkinVariant = this._player.skinVariant;
46	      this._player.skinVariant = this.ClothStyleId;
47	      base.Draw(spriteBatch);
48	      this._player.skinVariant = this._realSkinVariant;
49	    }
50	
51	    protected override void DrawSelf(SpriteBatch spriteBatch)
52	    {
53	      if (this._hovered)
54	      {
55	        if (!this._soundedHover)
56	          SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
57	        this._soundedHover = true;
58	      }
59	      else
60	        this._soundedHover = false;
61	      CalculatedStyle dimensions = this.GetDimensions();
62	      Utils.DrawSplicedPanel(spriteBatch, this._BasePanelTexture.Value, (int) dimensions.X, (int) dimensions.Y, (int) dimensions.Width, (int) dimensions.Height, 10, 10, 10, 10, Color.White * 0.5f);
63	      if (this._realSkinVariant == this.ClothStyleId)
64	        Utils.DrawSplicedPanel(spriteBatch, this._selectedBorderTexture.Value, (int) dimensions.X + 3, (int) dimensions.Y + 3, (int) dimensions.Width - 6, (int) dimensions.Height - 6, 10, 10, 10, 10, Color.White);
65	      if (!this._hovered)
66	        return;
67	      Utils.DrawSplicedPanel(spriteBatch, this._hoveredBorderTexture.Value, (int) dimensions.X, (int) dimensions.Y, (int) dimensions.Width, (int) dimensions.Height, 10, 10, 10, 10, Color.White);
68	    }
69	
70	    public override void MouseDown(UIMouseEvent evt)
71	    {
72	      this._player.skinVariant = this.ClothStyleId;
73	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
74	      base.MouseDown(evt);
75	    }
76	
77	    public override void MouseOver(UIMouseEvent evt)
78	    {
79	      base.MouseOver(evt);
80	      this._hovered = true;
81	      this._char.SetAnimated(true);
82	    }
83	
84	    public override void MouseOut(UIMouseEvent evt)
85	    {
86	      base.MouseOut(evt);
87	      this._hovered = false;
88	      this._char.SetAnimated(false);
89	    }
90	  }
91	}
92	

```


---

## 🤖 Assistant · 2026-08-09T11:48:37.703Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIClothStyleButton.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:37.709Z

**📎 ToolResult**

```
1	using System;
2	using Microsoft.Xna.Framework;
3	using Microsoft.Xna.Framework.Graphics;
4	using ReLogic.Content;
5	using Terraria.Audio;
6	using Terraria.UI;
7	
8	namespace Terraria.GameContent.UI.Elements;
9	
10	public class UIClothStyleButton : UIElement
11	{
12		private readonly Player _player;
13	
14		public readonly int ClothStyleId;
15	
16		private readonly Asset<Texture2D> _BasePanelTexture;
17	
18		private readonly Asset<Texture2D> _selectedBorderTexture;
19	
20		private readonly Asset<Texture2D> _hoveredBorderTexture;
21	
22		private readonly UICharacter _char;
23	
24		private bool _hovered;
25	
26		private bool _soundedHover;
27	
28		private int _realSkinVariant;
29	
30		private Action PrepareAction;
31	
32		public UIClothStyleButton(Player player, int clothStyleId, Action prepareAction = null)
33		{
34			_player = player;
35			ClothStyleId = clothStyleId;
36			PrepareAction = prepareAction;
37			Width = StyleDimension.FromPixels(44f);
38			Height = StyleDimension.FromPixels(80f);
39			_BasePanelTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanel", (AssetRequestMode)1);
40			_selectedBorderTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode)1);
41			_hoveredBorderTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelBorder", (AssetRequestMode)1);
42			_char = new UICharacter(_player, animated: false, hasBackPanel: false)
43			{
44				HAlign = 0.5f,
45				VAlign = 0.5f
46			};
47			Append(_char);
48		}
49	
50		public override void Draw(SpriteBatch spriteBatch)
51		{
52			_realSkinVariant = _player.skinVariant;
53			_player.skinVariant = ClothStyleId;
54			int hair = _player.hair;
55			if (PrepareAction != null)
56			{
57				PrepareAction();
58			}
59			_player.PlayerFrame();
60			base.Draw(spriteBatch);
61			_player.skinVariant = _realSkinVariant;
62			_player.hair = hair;
63		}
64	
65		protected override void DrawSelf(SpriteBatch spriteBatch)
66		{
67			if (_hovered)
68			{
69				if (!_soundedHover)
70				{
71					SoundEngine.PlaySound(12);
72				}
73				_soundedHover = true;
74			}
75			else
76			{
77				_soundedHover = false;
78			}
79			CalculatedStyle dimensions = GetDimensions();
80			Utils.DrawSplicedPanel(spriteBatch, _BasePanelTexture.Value, (int)dimensions.X, (int)dimensions.Y, (int)dimensions.Width, (int)dimensions.Height, 10, 10, 10, 10, Color.White * 0.5f);
81			if (_realSkinVariant == ClothStyleId)
82			{
83				Utils.DrawSplicedPanel(spriteBatch, _selectedBorderTexture.Value, (int)dimensions.X + 3, (int)dimensions.Y + 3, (int)dimensions.Width - 6, (int)dimensions.Height - 6, 10, 10, 10, 10, Color.White);
84			}
85			if (_hovered)
86			{
87				Utils.DrawSplicedPanel(spriteBatch, _hoveredBorderTexture.Value, (int)dimensions.X, (int)dimensions.Y, (int)dimensions.Width, (int)dimensions.Height, 10, 10, 10, 10, Color.White);
88			}
89		}
90	
91		public override void LeftMouseDown(UIMouseEvent evt)
92		{
93			base.LeftMouseDown(evt);
94		}
95	
96		public override void MouseOver(UIMouseEvent evt)
97		{
98			base.MouseOver(evt);
99			_hovered = true;
100			_char.SetAnimated(animated: true);
101		}
102	
103		public override void MouseOut(UIMouseEvent evt)
104		{
105			base.MouseOut(evt);
106			_hovered = false;
107			_char.SetAnimated(animated: false);
108		}
109	}
110	

```


---

## 🤖 Assistant · 2026-08-09T11:48:42.549Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting findings so far:

UICharacter.cs:
- 59x58 size unchanged; animation formula unchanged ((time/0.07)%14+6)*56.
- New: pet projectiles preview, PrepareAction, useAClone, draw order changes (ResetEffects moved into DrawSelf), GetPlayerPosition shifts X by -10 when pets.
- Update() no longer calls ResetEffects/PlayerFrame.

UIHairStyleButton.cs:
- size unchanged 44x44. New: _framesToSkip / SkipRenderingContent; sets _player.head = -1 before drawing head so helmet doesn't hide hair preview; DrawPlayerHead call now without rotation/scale/color args (new signature).

UIClothStyleButton.cs:
- size unchanged 44x80. New: PrepareAction param; LeftMouseDown no longer sets skinVariant directly (interesting — click handling moved? Actually old set _player.skinVariant = ClothStyleId; new only calls base.LeftMouseDown — so the parent must handle setting skinVariant via different mechanism, probably in UICharacterCreation with GetHoverImage or a click handler... need to check). Also Draw() now calls PrepareAction() and _player.PlayerFrame().

Now read UICharacterCreation.cs both. Big files 1513 and 2386. Read both fully.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:48:42.550Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterCreation.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:42.698Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.UI.States.UICharacterCreation
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using Newtonsoft.Json;
10	using ReLogic.Content;
11	using ReLogic.OS;
12	using System;
13	using System.Collections.Generic;
14	using System.Globalization;
15	using System.Linq;
16	using Terraria.Audio;
17	using Terraria.GameContent.Creative;
18	using Terraria.GameContent.UI.Elements;
19	using Terraria.GameInput;
20	using Terraria.ID;
21	using Terraria.Initializers;
22	using Terraria.IO;
23	using Terraria.Localization;
24	using Terraria.UI;
25	using Terraria.UI.Gamepad;
26	
27	namespace Terraria.GameContent.UI.States
28	{
29	  public class UICharacterCreation : UIState
30	  {
31	    private int[] _validClothStyles = new int[10]
32	    {
33	      0,
34	      2,
35	      1,
36	      3,
37	      8,
38	      4,
39	      6,
40	      5,
41	      7,
42	      9
43	    };
44	    private List<int> _foundPoints = new List<int>();
45	    private readonly Player _player;
46	    private UIColoredImageButton[] _colorPickers;
47	    private UICharacterCreation.CategoryId _selectedPicker;
48	    private Vector3 _currentColorHSL;
49	    private UIColoredImageButton _clothingStylesCategoryButton;
50	    private UIColoredImageButton _hairStylesCategoryButton;
51	    private UIColoredImageButton _charInfoCategoryButton;
52	    private UIElement _topContainer;
53	    private UIElement _middleContainer;
54	    private UIElement _hslContainer;
55	    private UIElement _hairstylesContainer;
56	    private UIElement _clothStylesContainer;
57	    private UIElement _infoContainer;
58	    private UIText _hslHexText;
59	    private UIText _difficultyDescriptionText;
60	    private UIElement _copyHexButton;
61	    private UIElement _pasteHexButton;
62	    private UIElement _randomColorButton;
63	    private UIElement _copyTemplateButton;
64	    private UIElement _pasteTemplateButton;
65	    private UIElement _randomizePlayerButton;
66	    private UIColoredImageButton _genderMale;
67	    private UIColoredImageButton _genderFemale;
68	    private UICharacterNameButton _charName;
69	    private UIText _helpGlyphLeft;
70	    private UIText _helpGlyphRight;
71	    private UIGamepadHelper _helper;
72	
73	    public UICharacterCreation(Player player)
74	    {
75	      this._player = player;
76	      this._player.difficulty = (byte) 3;
77	      this.BuildPage();
78	    }
79	
80	    private void BuildPage()
81	    {
82	      this.RemoveAllChildren();
83	      int num = 4;
84	      UIElement uiElement1 = new UIElement()
85	      {
86	        Width = StyleDimension.FromPixels(500f),
87	        Height = StyleDimension.FromPixels((float) (380 + num)),
88	        Top = StyleDimension.FromPixels(220f),
89	        HAlign = 0.5f,
90	        VAlign = 0.0f
91	      };
92	      uiElement1.SetPadding(0.0f);
93	      this.Append(uiElement1);
94	      UIPanel uiPanel = new UIPanel();
95	      uiPanel.Width = StyleDimension.FromPercent(1f);
96	      uiPanel.Height = StyleDimension.FromPixels(uiElement1.Height.Pixels - 150f - (float) num);
97	      uiPanel.Top = StyleDimension.FromPixels(50f);
98	      uiPanel.BackgroundColor = new Color(33, 43, 79) * 0.8f;
99	      UIPanel container = uiPanel;
100	      container.SetPadding(0.0f);
101	      uiElement1.Append((UIElement) container);
102	      this.MakeBackAndCreatebuttons(uiElement1);
103	      this.MakeCharPreview(container);
104	      UIElement uiElement2 = new UIElement()
105	      {
106	        Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f),
107	        Height = StyleDimension.FromPixelsAndPercent(50f, 0.0f)
108	      };
109	      uiElement2.SetPadding(0.0f);
110	      uiElement2.PaddingTop = 4f;
111	      uiElement2.PaddingBottom = 0.0f;
112	      container.Append(uiElement2);
113	      UIElement uiElement3 = new UIElement()
114	      {
115	        Top = StyleDimension.FromPixelsAndPercent(uiElement2.Height.Pixels + 6f, 0.0f),
116	        Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f),
117	        Height = StyleDimension.FromPixelsAndPercent(container.Height.Pixels - 70f, 0.0f)
118	      };
119	      uiElement3.SetPadding(0.0f);
120	      uiElement3.PaddingTop = 3f;
121	      uiElement3.PaddingBottom = 0.0f;
122	      container.Append(uiElement3);
123	      this._topContainer = uiElement2;
124	      this._middleContainer = uiElement3;
125	      this.MakeInfoMenu(uiElement3);
126	      this.MakeHSLMenu(uiElement3);
127	      this.MakeHairsylesMenu(uiElement3);
128	      this.MakeClothStylesMenu(uiElement3);
129	      this.MakeCategoriesBar(uiElement2);
130	      this.Click_CharInfo((UIMouseEvent) null, (UIElement) null);
131	    }
132	
133	    private void MakeCharPreview(UIPanel container)
134	    {
135	      float num1 = 70f;
136	      for (float num2 = 0.0f; (double) num2 <= 1.0; ++num2)
137	      {
138	        UICharacter uiCharacter1 = new UICharacter(this._player, true, false, 1.5f);
139	        uiCharacter1.Width = StyleDimension.FromPixels(80f);
140	        uiCharacter1.Height = StyleDimension.FromPixelsAndPercent(80f, 0.0f);
141	        uiCharacter1.Top = StyleDimension.FromPixelsAndPercent(-num1, 0.0f);
142	        uiCharacter1.VAlign = 0.0f;
143	        uiCharacter1.HAlign = 0.5f;
144	        UICharacter uiCharacter2 = uiCharacter1;
145	        container.Append((UIElement) uiCharacter2);
146	      }
147	    }
148	
149	    private void MakeHairsylesMenu(UIElement middleInnerPanel)
150	    {
151	      Main.Hairstyles.UpdateUnlocks();
152	      UIElement element = new UIElement()
153	      {
154	        Width = StyleDimension.FromPixelsAndPercent(-10f, 1f),
155	        Height = StyleDimension.FromPixelsAndPercent(0.0f, 1f),
156	        HAlign = 0.5f,
157	        VAlign = 0.5f,
158	        Top = StyleDimension.FromPixels(6f)
159	      };
160	      middleInnerPanel.Append(element);
161	      element.SetPadding(0.0f);
162	      UIList uiList1 = new UIList();
163	      uiList1.Width = StyleDimension.FromPixelsAndPercent(-18f, 1f);
164	      uiList1.Height = StyleDimension.FromPixelsAndPercent(-6f, 1f);
165	      UIList uiList2 = uiList1;
166	      uiList2.SetPadding(4f);
167	      element.Append((UIElement) uiList2);
168	      UIScrollbar uiScrollbar = new UIScrollbar();
169	      uiScrollbar.HAlign = 1f;
170	      uiScrollbar.Height = StyleDimension.FromPixelsAndPercent(-30f, 1f);
171	      uiScrollbar.Top = StyleDimension.FromPixels(10f);
172	      UIScrollbar scrollbar = uiScrollbar;
173	      scrollbar.SetView(100f, 1000f);
174	      uiList2.SetScrollbar(scrollbar);
175	      element.Append((UIElement) scrollbar);
176	      int count = Main.Hairstyles.AvailableHairstyles.Count;
177	      UIElement uiElement = new UIElement()
178	      {
179	        Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f),
180	        Height = StyleDimension.FromPixelsAndPercent((float) (48 * (count / 10 + (count % 10 == 0 ? 0 : 1))), 0.0f)
181	      };
182	      uiList2.Add(uiElement);
183	      uiElement.SetPadding(0.0f);
184	      for (int id = 0; id < count; ++id)
185	      {
186	        UIHairStyleButton uiHairStyleButton1 = new UIHairStyleButton(this._player, Main.Hairstyles.AvailableHairstyles[id]);
187	        uiHairStyleButton1.Left = StyleDimension.FromPixels((float) ((double) (id % 10) * 46.0 + 6.0));
188	        uiHairStyleButton1.Top = StyleDimension.FromPixels((float) ((double) (id / 10) * 48.0 + 1.0));
189	        UIHairStyleButton uiHairStyleButton2 = uiHairStyleButton1;
190	        uiHairStyleButton2.SetSnapPoint("Middle", id, new Vector2?(), new Vector2?());
191	        uiElement.Append((UIElement) uiHairStyleButton2);
192	      }
193	      this._hairstylesContainer = element;
194	    }
195	
196	    private void MakeClothStylesMenu(UIElement middleInnerPanel)
197	    {
198	      UIElement element1 = new UIElement()
199	      {
200	        Width = StyleDimension.FromPixelsAndPercent(-10f, 1f),
201	        Height = StyleDimension.FromPixelsAndPercent(0.0f, 1f),
202	        HAlign = 0.5f,
203	        VAlign = 0.5f
204	      };
205	      middleInnerPanel.Append(element1);
206	      element1.SetPadding(0.0f);
207	      int num1 = 15;
208	      for (int id = 0; id < this._validClothStyles.Length; ++id)
209	      {
210	        int num2 = 0;
211	        if (id >= this._validClothStyles.Length / 2)
212	          num2 = 20;
213	        UIClothStyleButton clothStyleButton1 = new UIClothStyleButton(this._player, this._validClothStyles[id]);
214	        clothStyleButton1.Left = StyleDimension.FromPixels((float) ((double) id * 46.0 + (double) num2 + 6.0));
215	        clothStyleButton1.Top = StyleDimension.FromPixels((float) num1);
216	        UIClothStyleButton clothStyleButton2 = clothStyleButton1;
217	        clothStyleButton2.OnMouseDown += new UIElement.MouseEvent(this.Click_CharClothStyle);
218	        clothStyleButton2.SetSnapPoint("Middle", id, new Vector2?(), new Vector2?());
219	        element1.Append((UIElement) clothStyleButton2);
220	      }
221	      for (int index = 0; index < 2; ++index)
222	      {
223	        int num2 = 0;
224	        if (index >= 1)
225	          num2 = 20;
226	        UIHorizontalSeparator horizontalSeparator1 = new UIHorizontalSeparator(2, true);
227	        horizontalSeparator1.Left = StyleDimension.FromPixels((float) ((double) index * 230.0 + (double) num2 + 6.0));
228	        horizontalSeparator1.Top = StyleDimension.FromPixels((float) (num1 + 86));
229	        horizontalSeparator1.Width = StyleDimension.FromPixelsAndPercent(230f, 0.0f);
230	        horizontalSeparator1.Color = Color.Lerp(Color.White, new Color(63, 65, 151, (int) byte.MaxValue), 0.85f) * 0.9f;
231	        UIHorizontalSeparator horizontalSeparator2 = horizontalSeparator1;
232	        element1.Append((UIElement) horizontalSeparator2);
233	        UIColoredImageButton pickerWithoutClick = this.CreatePickerWithoutClick(UICharacterCreation.CategoryId.Clothing, "Images/UI/CharCreation/" + (index == 0 ? "ClothStyleMale" : "ClothStyleFemale"), 0.0f, 0.0f);
234	        pickerWithoutClick.Top = StyleDimension.FromPixelsAndPercent((float) (num1 + 92), 0.0f);
235	        pickerWithoutClick.Left = StyleDimension.FromPixels((float) ((double) index * 230.0 + 92.0 + (double) num2 + 6.0));
236	        pickerWithoutClick.HAlign = 0.0f;
237	        pickerWithoutClick.VAlign = 0.0f;
238	        element1.Append((UIElement) pickerWithoutClick);
239	        if (index == 0)
240	        {
241	          pickerWithoutClick.OnMouseDown += new UIElement.MouseEvent(this.Click_CharGenderMale);
242	          this._genderMale = pickerWithoutClick;
243	        }
244	        else
245	        {
246	          pickerWithoutClick.OnMouseDown += new UIElement.MouseEvent(this.Click_CharGenderFemale);
247	          this._genderFemale = pickerWithoutClick;
248	        }
249	        pickerWithoutClick.SetSnapPoint("Low", index * 4, new Vector2?(), new Vector2?());
250	      }
251	      UIElement element2 = new UIElement()
252	      {
253	        Width = StyleDimension.FromPixels(130f),
254	        Height = StyleDimension.FromPixels(50f),
255	        HAlign = 0.5f,
256	        VAlign = 1f
257	      };
258	      element1.Append(element2);
259	      UIColoredImageButton coloredImageButton1 = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Copy", (AssetRequestMode) 1), true);
260	      coloredImageButton1.VAlign = 0.5f;
261	      coloredImageButton1.HAlign = 0.0f;
262	      coloredImageButton1.Left = StyleDimension.FromPixelsAndPercent(0.0f, 0.0f);
263	      UIColoredImageButton coloredImageButton2 = coloredImageButton1;
264	      coloredImageButton2.OnMouseDown += new UIElement.MouseEvent(this.Click_CopyPlayerTemplate);
265	      element2.Append((UIElement) coloredImageButton2);
266	      this._copyTemplateButton = (UIElement) coloredImageButton2;
267	      UIColoredImageButton coloredImageButton3 = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Paste", (AssetRequestMode) 1), true);
268	      coloredImageButton3.VAlign = 0.5f;
269	      coloredImageButton3.HAlign = 0.5f;
270	      UIColoredImageButton coloredImageButton4 = coloredImageButton3;
271	      coloredImageButton4.OnMouseDown += new UIElement.MouseEvent(this.Click_PastePlayerTemplate);
272	      element2.Append((UIElement) coloredImageButton4);
273	      this._pasteTemplateButton = (UIElement) coloredImageButton4;
274	      UIColoredImageButton coloredImageButton5 = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Randomize", (AssetRequestMode) 1), true);
275	      coloredImageButton5.VAlign = 0.5f;
276	      coloredImageButton5.HAlign = 1f;
277	      UIColoredImageButton coloredImageButton6 = coloredImageButton5;
278	      coloredImageButton6.OnMouseDown += new UIElement.MouseEvent(this.Click_RandomizePlayer);
279	      element2.Append((UIElement) coloredImageButton6);
280	      this._randomizePlayerButton = (UIElement) coloredImageButton6;
281	      coloredImageButton2.SetSnapPoint("Low", 1, new Vector2?(), new Vector2?());
282	      coloredImageButton4.SetSnapPoint("Low", 2, new Vector2?(), new Vector2?());
283	      coloredImageButton6.SetSnapPoint("Low", 3, new Vector2?(), new Vector2?());
284	      this._clothStylesContainer = element1;
285	    }
286	
287	    private void MakeCategoriesBar(UIElement categoryContainer)
288	    {
289	      float xPositionStart = -240f;
290	      float xPositionPerId = 48f;
291	      this._colorPickers = new UIColoredImageButton[10];
292	      categoryContainer.Append((UIElement) this.CreateColorPicker(UICharacterCreation.CategoryId.HairColor, "Images/UI/CharCreation/ColorHair", xPositionStart, xPositionPerId));
293	      categoryContainer.Append((UIElement) this.CreateColorPicker(UICharacterCreation.CategoryId.Eye, "Images/UI/CharCreation/ColorEye", xPositionStart, xPositionPerId));
294	      categoryContainer.Append((UIElement) this.CreateColorPicker(UICharacterCreation.CategoryId.Skin, "Images/UI/CharCreation/ColorSkin", xPositionStart, xPositionPerId));
295	      categoryContainer.Append((UIElement) this.CreateColorPicker(UICharacterCreation.CategoryId.Shirt, "Images/UI/CharCreation/ColorShirt", xPositionStart, xPositionPerId));
296	      categoryContainer.Append((UIElement) this.CreateColorPicker(UICharacterCreation.CategoryId.Undershirt, "Images/UI/CharCreation/ColorUndershirt", xPositionStart, xPositionPerId));
297	      categoryContainer.Append((UIElement) this.CreateColorPicker(UICharacterCreation.CategoryId.Pants, "Images/UI/CharCreation/ColorPants", xPositionStart, xPositionPerId));
298	      categoryContainer.Append((UIElement) this.CreateColorPicker(UICharacterCreation.CategoryId.Shoes, "Images/UI/CharCreation/ColorShoes", xPositionStart, xPositionPerId));
299	      this._colorPickers[4].SetMiddleTexture((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/ColorEyeBack", (AssetRequestMode) 1));
300	      this._clothingStylesCategoryButton = this.CreatePickerWithoutClick(UICharacterCreation.CategoryId.Clothing, "Images/UI/CharCreation/ClothStyleMale", xPositionStart, xPositionPerId);
301	      this._clothingStylesCategoryButton.OnMouseDown += new UIElement.MouseEvent(this.Click_ClothStyles);
302	      this._clothingStylesCategoryButton.SetSnapPoint("Top", 1, new Vector2?(), new Vector2?());
303	      categoryContainer.Append((UIElement) this._clothingStylesCategoryButton);
304	      this._hairStylesCategoryButton = this.CreatePickerWithoutClick(UICharacterCreation.CategoryId.HairStyle, "Images/UI/CharCreation/HairStyle_Hair", xPositionStart, xPositionPerId);
305	      this._hairStylesCategoryButton.OnMouseDown += new UIElement.MouseEvent(this.Click_HairStyles);
306	      this._hairStylesCategoryButton.SetMiddleTexture((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/HairStyle_Arrow", (AssetRequestMode) 1));
307	      this._hairStylesCategoryButton.SetSnapPoint("Top", 2, new Vector2?(), new Vector2?());
308	      categoryContainer.Append((UIElement) this._hairStylesCategoryButton);
309	      this._charInfoCategoryButton = this.CreatePickerWithoutClick(UICharacterCreation.CategoryId.CharInfo, "Images/UI/CharCreation/CharInfo", xPositionStart, xPositionPerId);
310	      this._charInfoCategoryButton.OnMouseDown += new UIElement.MouseEvent(this.Click_CharInfo);
311	      this._charInfoCategoryButton.SetSnapPoint("Top", 0, new Vector2?(), new Vector2?());
312	      categoryContainer.Append((UIElement) this._charInfoCategoryButton);
313	      this.UpdateColorPickers();
314	      UIHorizontalSeparator horizontalSeparator1 = new UIHorizontalSeparator(2, true);
315	      horizontalSeparator1.Width = StyleDimension.FromPixelsAndPercent(-20f, 1f);
316	      horizontalSeparator1.Top = StyleDimension.FromPixels(6f);
317	      horizontalSeparator1.VAlign = 1f;
318	      horizontalSeparator1.HAlign = 0.5f;
319	      horizontalSeparator1.Color = Color.Lerp(Color.White, new Color(63, 65, 151, (int) byte.MaxValue), 0.85f) * 0.9f;
320	      UIHorizontalSeparator horizontalSeparator2 = horizontalSeparator1;
321	      categoryContainer.Append((UIElement) horizontalSeparator2);
322	      int num = 21;
323	      UIText uiText1 = new UIText(PlayerInput.GenerateInputTag_ForCurrentGamemode(false, "HotbarMinus"), 1f, false);
324	      uiText1.Left = new StyleDimension((float) -num, 0.0f);
325	      uiText1.VAlign = 0.5f;
326	      uiText1.Top = new StyleDimension(-4f, 0.0f);
327	      UIText uiText2 = uiText1;
328	      categoryContainer.Append((UIElement) uiText2);
329	      UIText uiText3 = new UIText(PlayerInput.GenerateInputTag_ForCurrentGamemode(false, "HotbarMinus"), 1f, false);
330	      uiText3.HAlign = 1f;
331	      uiText3.Left = new StyleDimension((float) (12 + num), 0.0f);
332	      uiText3.VAlign = 0.5f;
333	      uiText3.Top = new StyleDimension(-4f, 0.0f);
334	      UIText uiText4 = uiText3;
335	      categoryContainer.Append((UIElement) uiText4);
336	      this._helpGlyphLeft = uiText2;
337	      this._helpGlyphRight = uiText4;
338	      categoryContainer.OnUpdate += new UIElement.ElementEvent(this.UpdateHelpGlyphs);
339	    }
340	
341	    private void UpdateHelpGlyphs(UIElement element)
342	    {
343	      string text1 = "";
344	      string text2 = "";
345	      if (PlayerInput.UsingGamepad)
346	      {
347	        text1 = PlayerInput.GenerateInputTag_ForCurrentGamemode(false, "HotbarMinus");
348	        text2 = PlayerInput.GenerateInputTag_ForCurrentGamemode(false, "HotbarPlus");
349	      }
350	      this._helpGlyphLeft.SetText(text1);
351	      this._helpGlyphRight.SetText(text2);
352	    }
353	
354	    private UIColoredImageButton CreateColorPicker(
355	      UICharacterCreation.CategoryId id,
356	      string texturePath,
357	      float xPositionStart,
358	      float xPositionPerId)
359	    {
360	      UIColoredImageButton coloredImageButton = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>(texturePath, (AssetRequestMode) 1), false);
361	      this._colorPickers[(int) id] = coloredImageButton;
362	      coloredImageButton.VAlign = 0.0f;
363	      coloredImageButton.HAlign = 0.0f;
364	      coloredImageButton.Left.Set(xPositionStart + (float) id * xPositionPerId, 0.5f);
365	      coloredImageButton.OnMouseDown += new UIElement.MouseEvent(this.Click_ColorPicker);
366	      coloredImageButton.SetSnapPoint("Top", (int) id, new Vector2?(), new Vector2?());
367	      return coloredImageButton;
368	    }
369	
370	    private UIColoredImageButton CreatePickerWithoutClick(
371	      UICharacterCreation.CategoryId id,
372	      string texturePath,
373	      float xPositionStart,
374	      float xPositionPerId)
375	    {
376	      UIColoredImageButton coloredImageButton = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>(texturePath, (AssetRequestMode) 1), false);
377	      coloredImageButton.VAlign = 0.0f;
378	      coloredImageButton.HAlign = 0.0f;
379	      coloredImageButton.Left.Set(xPositionStart + (float) id * xPositionPerId, 0.5f);
380	      return coloredImageButton;
381	    }
382	
383	    private void MakeInfoMenu(UIElement parentContainer)
384	    {
385	      UIElement element1 = new UIElement()
386	      {
387	        Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f),
388	        Height = StyleDimension.FromPixelsAndPercent(0.0f, 1f),
389	        HAlign = 0.5f,
390	        VAlign = 0.0f
391	      };
392	      element1.SetPadding(10f);
393	      element1.PaddingBottom = 0.0f;
394	      element1.PaddingTop = 0.0f;
395	      parentContainer.Append(element1);
396	      UICharacterNameButton characterNameButton = new UICharacterNameButton(Language.GetText("UI.WorldCreationName"), Language.GetText("UI.PlayerEmptyName"), (LocalizedText) null);
397	      characterNameButton.Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f);
398	      characterNameButton.HAlign = 0.5f;
399	      element1.Append((UIElement) characterNameButton);
400	      this._charName = characterNameButton;
401	      characterNameButton.OnMouseDown += new UIElement.MouseEvent(this.Click_Naming);
402	      characterNameButton.SetSnapPoint("Middle", 0, new Vector2?(), new Vector2?());
403	      float num1 = 4f;
404	      float num2 = 0.0f;
405	      float percent = 0.4f;
406	      UIElement element2 = new UIElement()
407	      {
408	        HAlign = 0.0f,
409	        VAlign = 1f,
410	        Width = StyleDimension.FromPixelsAndPercent(-num1, percent),
411	        Height = StyleDimension.FromPixelsAndPercent(-50f, 1f)
412	      };
413	      element2.SetPadding(0.0f);
414	      element1.Append(element2);
415	      UISlicedImage uiSlicedImage1 = new UISlicedImage((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode) 1));
416	      uiSlicedImage1.HAlign = 1f;
417	      uiSlicedImage1.VAlign = 1f;
418	      uiSlicedImage1.Width = StyleDimension.FromPixelsAndPercent((float) (-(double) num1 * 2.0), 1f - percent);
419	      uiSlicedImage1.Left = StyleDimension.FromPixels(-num1);
420	      uiSlicedImage1.Height = StyleDimension.FromPixelsAndPercent(element2.Height.Pixels, element2.Height.Precent);
421	      UISlicedImage uiSlicedImage2 = uiSlicedImage1;
422	      uiSlicedImage2.SetSliceDepths(10);
423	      uiSlicedImage2.Color = Color.LightGray * 0.7f;
424	      element1.Append((UIElement) uiSlicedImage2);
425	      float num3 = 4f;
426	      UIDifficultyButton difficultyButton1 = new UIDifficultyButton(this._player, Lang.menu[26], Lang.menu[31], (byte) 0, Color.Cyan);
427	      difficultyButton1.HAlign = 0.0f;
428	      difficultyButton1.VAlign = (float) (1.0 / ((double) num3 - 1.0));
429	      difficultyButton1.Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f);
430	      difficultyButton1.Height = StyleDimension.FromPixelsAndPercent(-num2, 1f / num3);
431	      UIDifficultyButton difficultyButton2 = difficultyButton1;
432	      UIDifficultyButton difficultyButton3 = new UIDifficultyButton(this._player, Lang.menu[25], Lang.menu[30], (byte) 1, Main.mcColor);
433	      difficultyButton3.HAlign = 0.0f;
434	      difficultyButton3.VAlign = (float) (2.0 / ((double) num3 - 1.0));
435	      difficultyButton3.Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f);
436	      difficultyButton3.Height = StyleDimension.FromPixelsAndPercent(-num2, 1f / num3);
437	      UIDifficultyButton difficultyButton4 = difficultyButton3;
438	      UIDifficultyButton difficultyButton5 = new UIDifficultyButton(this._player, Lang.menu[24], Lang.menu[29], (byte) 2, Main.hcColor);
439	      difficultyButton5.HAlign = 0.0f;
440	      difficultyButton5.VAlign = 1f;
441	      difficultyButton5.Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f);
442	      difficultyButton5.Height = StyleDimension.FromPixelsAndPercent(-num2, 1f / num3);
443	      UIDifficultyButton difficultyButton6 = difficultyButton5;
444	      UIDifficultyButton difficultyButton7 = new UIDifficultyButton(this._player, Language.GetText("UI.Creative"), Language.GetText("UI.CreativeDescriptionPlayer"), (byte) 3, Main.creativeModeColor);
445	      difficultyButton7.HAlign = 0.0f;
446	      difficultyButton7.VAlign = 0.0f;
447	      difficultyButton7.Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f);
448	      difficultyButton7.Height = StyleDimension.FromPixelsAndPercent(-num2, 1f / num3);
449	      UIDifficultyButton difficultyButton8 = difficultyButton7;
450	      UIText uiText1 = new UIText(Lang.menu[26], 1f, false);
451	      uiText1.HAlign = 0.0f;
452	      uiText1.VAlign = 0.5f;
453	      uiText1.Width = StyleDimension.FromPixelsAndPercent(0.0f, 1f);
454	      uiText1.Height = StyleDimension.FromPixelsAndPercent(0.0f, 1f);
455	      uiText1.Top = StyleDimension.FromPixelsAndPercent(15f, 0.0f);
456	      uiText1.IsWrapped = true;
457	      UIText uiText2 = uiText1;
458	      uiText2.PaddingLeft = 20f;
459	      uiText2.PaddingRight = 20f;
460	      uiSlicedImage2.Append((UIElement) uiText2);
461	      element2.Append((UIElement) difficultyButton2);
462	      element2.Append((UIElement) difficultyButton4);
463	      element2.Append((UIElement) difficultyButton6);
464	      element2.Append((UIElement) difficultyButton8);
465	      this._infoContainer = element1;
466	      this._difficultyDescriptionText = uiText2;
467	      difficultyButton2.OnMouseDown += new UIElement.MouseEvent(this.UpdateDifficultyDescription);
468	      difficultyButton4.OnMouseDown += new UIElement.MouseEvent(this.UpdateDifficultyDescription);
469	      difficultyButton6.OnMouseDown += new UIElement.MouseEvent(this.UpdateDifficultyDescription);
470	      difficultyButton8.OnMouseDown += new UIElement.MouseEvent(this.UpdateDifficultyDescription);
471	      this.UpdateDifficultyDescription((UIMouseEvent) null, (UIElement) null);
472	      difficultyButton2.SetSnapPoint("Middle", 1, new Vector2?(), new Vector2?());
473	      difficultyButton4.SetSnapPoint("Middle", 2, new Vector2?(), new Vector2?());
474	      difficultyButton6.SetSnapPoint("Middle", 3, new Vector2?(), new Vector2?());
475	      difficultyButton8.SetSnapPoint("Middle", 4, new Vector2?(), new Vector2?());
476	    }
477	
478	    private void UpdateDifficultyDescription(UIMouseEvent evt, UIElement listeningElement)
479	    {
480	      LocalizedText text = Lang.menu[31];
481	      switch (this._player.difficulty)
482	      {
483	        case 0:
484	          text = Lang.menu[31];
485	          break;
486	        case 1:
487	          text = Lang.menu[30];
488	          break;
489	        case 2:
490	          text = Lang.menu[29];
491	          break;
492	        case 3:
493	          text = Language.GetText("UI.CreativeDescriptionPlayer");
494	          break;
495	      }
496	      this._difficultyDescriptionText.SetText(text);
497	    }
498	
499	    private void MakeHSLMenu(UIElement parentContainer)
500	    {
501	      UIElement element1 = new UIElement()
502	      {
503	        Width = StyleDimension.FromPixelsAndPercent(220f, 0.0f),
504	        Height = StyleDimension.FromPixelsAndPercent(158f, 0.0f),
505	        HAlign = 0.5f,
506	        VAlign = 0.0f
507	      };
508	      element1.SetPadding(0.0f);
509	      parentContainer.Append(element1);
510	      UIPanel uiPanel1 = new UIPanel();
511	      uiPanel1.Width = StyleDimension.FromPixelsAndPercent(220f, 0.0f);
512	      uiPanel1.Height = StyleDimension.FromPixelsAndPercent(104f, 0.0f);
513	      uiPanel1.HAlign = 0.5f;
514	      uiPanel1.VAlign = 0.0f;
515	      uiPanel1.Top = StyleDimension.FromPixelsAndPercent(10f, 0.0f);
516	      UIElement element2 = (UIElement) uiPanel1;
517	      element2.SetPadding(0.0f);
518	      element2.PaddingTop = 3f;
519	      element1.Append(element2);
520	      element2.Append((UIElement) this.CreateHSLSlider(UICharacterCreation.HSLSliderId.Hue));
521	      element2.Append((UIElement) this.CreateHSLSlider(UICharacterCreation.HSLSliderId.Saturation));
522	      element2.Append((UIElement) this.CreateHSLSlider(UICharacterCreation.HSLSliderId.Luminance));
523	      UIPanel uiPanel2 = new UIPanel();
524	      uiPanel2.VAlign = 1f;
525	      uiPanel2.HAlign = 1f;
526	      uiPanel2.Width = StyleDimension.FromPixelsAndPercent(100f, 0.0f);
527	      uiPanel2.Height = StyleDimension.FromPixelsAndPercent(32f, 0.0f);
528	      UIPanel uiPanel3 = uiPanel2;
529	      UIText uiText1 = new UIText("FFFFFF", 1f, false);
530	      uiText1.VAlign = 0.5f;
531	      uiText1.HAlign = 0.5f;
532	      UIText uiText2 = uiText1;
533	      uiPanel3.Append((UIElement) uiText2);
534	      element1.Append((UIElement) uiPanel3);
535	      UIColoredImageButton coloredImageButton1 = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Copy", (AssetRequestMode) 1), true);
536	      coloredImageButton1.VAlign = 1f;
537	      coloredImageButton1.HAlign = 0.0f;
538	      coloredImageButton1.Left = StyleDimension.FromPixelsAndPercent(0.0f, 0.0f);
539	      UIColoredImageButton coloredImageButton2 = coloredImageButton1;
540	      coloredImageButton2.OnMouseDown += new UIElement.MouseEvent(this.Click_CopyHex);
541	      element1.Append((UIElement) coloredImageButton2);
542	      this._copyHexButton = (UIElement) coloredImageButton2;
543	      UIColoredImageButton coloredImageButton3 = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Paste", (AssetRequestMode) 1), true);
544	      coloredImageButton3.VAlign = 1f;
545	      coloredImageButton3.HAlign = 0.0f;
546	      coloredImageButton3.Left = StyleDimension.FromPixelsAndPercent(40f, 0.0f);
547	      UIColoredImageButton coloredImageButton4 = coloredImageButton3;
548	      coloredImageButton4.OnMouseDown += new UIElement.MouseEvent(this.Click_PasteHex);
549	      element1.Append((UIElement) coloredImageButton4);
550	      this._pasteHexButton = (UIElement) coloredImageButton4;
551	      UIColoredImageButton coloredImageButton5 = new UIColoredImageButton((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Randomize", (AssetRequestMode) 1), true);
552	      coloredImageButton5.VAlign = 1f;
553	      coloredImageButton5.HAlign = 0.0f;
554	      coloredImageButton5.Left = StyleDimension.FromPixelsAndPercent(80f, 0.0f);
555	      UIColoredImageButton coloredImageButton6 = coloredImageButton5;
556	      coloredImageButton6.OnMouseDown += new UIElement.MouseEvent(this.Click_RandomizeSingleColor);
557	      element1.Append((UIElement) coloredImageButton6);
558	      this._randomColorButton = (UIElement) coloredImageButton6;
559	      this._hslContainer = element1;
560	      this._hslHexText = uiText2;
561	      coloredImageButton2.SetSnapPoint("Low", 0, new Vector2?(), new Vector2?());
562	      coloredImageButton4.SetSnapPoint("Low", 1, new Vector2?(), new Vector2?());
563	      coloredImageButton6.SetSnapPoint("Low", 2, new Vector2?(), new Vector2?());
564	    }
565	
566	    private UIColoredSlider CreateHSLSlider(UICharacterCreation.HSLSliderId id)
567	    {
568	      UIColoredSlider sliderButtonBase = this.CreateHSLSliderButtonBase(id);
569	      sliderButtonBase.VAlign = 0.0f;
570	      sliderButtonBase.HAlign = 0.0f;
571	      sliderButtonBase.Width = StyleDimension.FromPixelsAndPercent(-10f, 1f);
572	      sliderButtonBase.Top.Set((float) (30 * (int) id), 0.0f);
573	      sliderButtonBase.OnMouseDown += new UIElement.MouseEvent(this.Click_ColorPicker);
574	      sliderButtonBase.SetSnapPoint("Middle", (int) id, new Vector2?(), new Vector2?(new Vector2(0.0f, 20f)));
575	      return sliderButtonBase;
576	    }
577	
578	    private UIColoredSlider CreateHSLSliderButtonBase(
579	      UICharacterCreation.HSLSliderId id)
580	    {
581	      UIColoredSlider uiColoredSlider;
582	      switch (id)
583	      {
584	        case UICharacterCreation.HSLSliderId.Saturation:
585	          uiColoredSlider = new UIColoredSlider(LocalizedText.Empty, (Func<float>) (() => this.GetHSLSliderPosition(UICharacterCreation.HSLSliderId.Saturation)), (Action<float>) (x => this.UpdateHSLValue(UICharacterCreation.HSLSliderId.Saturation, x)), new Action(this.UpdateHSL_S), (Func<float, Color>) (x => this.GetHSLSliderColorAt(UICharacterCreation.HSLSliderId.Saturation, x)), Color.Transparent);
586	          break;
587	        case UICharacterCreation.HSLSliderId.Luminance:
588	          uiColoredSlider = new UIColoredSlider(LocalizedText.Empty, (Func<float>) (() => this.GetHSLSliderPosition(UICharacterCreation.HSLSliderId.Luminance)), (Action<float>) (x => this.UpdateHSLValue(UICharacterCreation.HSLSliderId.Luminance, x)), new Action(this.UpdateHSL_L), (Func<float, Color>) (x => this.GetHSLSliderColorAt(UICharacterCreation.HSLSliderId.Luminance, x)), Color.Transparent);
589	          break;
590	        default:
591	          uiColoredSlider = new UIColoredSlider(LocalizedText.Empty, (Func<float>) (() => this.GetHSLSliderPosition(UICharacterCreation.HSLSliderId.Hue)), (Action<float>) (x => this.UpdateHSLValue(UICharacterCreation.HSLSliderId.Hue, x)), new Action(this.UpdateHSL_H), (Func<float, Color>) (x => this.GetHSLSliderColorAt(UICharacterCreation.HSLSliderId.Hue, x)), Color.Transparent);
592	          break;
593	      }
594	      return uiColoredSlider;
595	    }
596	
597	    private void UpdateHSL_H()
598	    {
599	      this.UpdateHSLValue(UICharacterCreation.HSLSliderId.Hue, UILinksInitializer.HandleSliderHorizontalInput(this._currentColorHSL.X, 0.0f, 1f, PlayerInput.CurrentProfile.InterfaceDeadzoneX, 0.35f));
600	    }
601	
602	    private void UpdateHSL_S()
603	    {
604	      this.UpdateHSLValue(UICharacterCreation.HSLSliderId.Saturation, UILinksInitializer.HandleSliderHorizontalInput(this._currentColorHSL.Y, 0.0f, 1f, PlayerInput.CurrentProfile.InterfaceDeadzoneX, 0.35f));
605	    }
606	
607	    private void UpdateHSL_L()
608	    {
609	      this.UpdateHSLValue(UICharacterCreation.HSLSliderId.Luminance, UILinksInitializer.HandleSliderHorizontalInput(this._currentColorHSL.Z, 0.0f, 1f, PlayerInput.CurrentProfile.InterfaceDeadzoneX, 0.35f));
610	    }
611	
612	    private float GetHSLSliderPosition(UICharacterCreation.HSLSliderId id)
613	    {
614	      switch (id)
615	      {
616	        case UICharacterCreation.HSLSliderId.Hue:
617	          return this._currentColorHSL.X;
618	        case UICharacterCreation.HSLSliderId.Saturation:
619	          return this._currentColorHSL.Y;
620	        case UICharacterCreation.HSLSliderId.Luminance:
621	          return this._currentColorHSL.Z;
622	        default:
623	          return 1f;
624	      }
625	    }
626	
627	    private void UpdateHSLValue(UICharacterCreation.HSLSliderId id, float value)
628	    {
629	      switch (id)
630	      {
631	        case UICharacterCreation.HSLSliderId.Hue:
632	          this._currentColorHSL.X = value;
633	          break;
634	        case UICharacterCreation.HSLSliderId.Saturation:
635	          this._currentColorHSL.Y = value;
636	          break;
637	        case UICharacterCreation.HSLSliderId.Luminance:
638	          this._currentColorHSL.Z = value;
639	          break;
640	      }
641	      Color rgb = UICharacterCreation.ScaledHslToRgb(this._currentColorHSL.X, this._currentColorHSL.Y, this._currentColorHSL.Z);
642	      this.ApplyPendingColor(rgb);
643	      this._colorPickers[(int) this._selectedPicker]?.SetColor(rgb);
644	      if (this._selectedPicker == UICharacterCreation.CategoryId.HairColor)
645	        this._hairStylesCategoryButton.SetColor(rgb);
646	      this.UpdateHexText(rgb);
647	    }
648	
649	    private Color GetHSLSliderColorAt(UICharacterCreation.HSLSliderId id, float pointAt)
650	    {
651	      switch (id)
652	      {
653	        case UICharacterCreation.HSLSliderId.Hue:
654	          return UICharacterCreation.ScaledHslToRgb(pointAt, 1f, 0.5f);
655	        case UICharacterCreation.HSLSliderId.Saturation:
656	          return UICharacterCreation.ScaledHslToRgb(this._currentColorHSL.X, pointAt, this._currentColorHSL.Z);
657	        case UICharacterCreation.HSLSliderId.Luminance:
658	          return UICharacterCreation.ScaledHslToRgb(this._currentColorHSL.X, this._currentColorHSL.Y, pointAt);
659	        default:
660	          return Color.White;
661	      }
662	    }
663	
664	    private void ApplyPendingColor(Color pendingColor)
665	    {
666	      switch (this._selectedPicker)
667	      {
668	        case UICharacterCreation.CategoryId.HairColor:
669	          this._player.hairColor = pendingColor;
670	          break;
671	        case UICharacterCreation.CategoryId.Eye:
672	          this._player.eyeColor = pendingColor;
673	          break;
674	        case UICharacterCreation.CategoryId.Skin:
675	          this._player.skinColor = pendingColor;
676	          break;
677	        case UICharacterCreation.CategoryId.Shirt:
678	          this._player.shirtColor = pendingColor;
679	          break;
680	        case UICharacterCreation.CategoryId.Undershirt:
681	          this._player.underShirtColor = pendingColor;
682	          break;
683	        case UICharacterCreation.CategoryId.Pants:
684	          this._player.pantsColor = pendingColor;
685	          break;
686	        case UICharacterCreation.CategoryId.Shoes:
687	          this._player.shoeColor = pendingColor;
688	          break;
689	      }
690	    }
691	
692	    private void UpdateHexText(Color pendingColor)
693	    {
694	      this._hslHexText.SetText(UICharacterCreation.GetHexText(pendingColor));
695	    }
696	
697	    private static string GetHexText(Color pendingColor)
698	    {
699	      return "#" + pendingColor.Hex3().ToUpper();
700	    }
701	
702	    private void MakeBackAndCreatebuttons(UIElement outerContainer)
703	    {
704	      UITextPanel<LocalizedText> uiTextPanel1 = new UITextPanel<LocalizedText>(Language.GetText("UI.Back"), 0.7f, true);
705	      uiTextPanel1.Width = StyleDimension.FromPixelsAndPercent(-10f, 0.5f);
706	      uiTextPanel1.Height = StyleDimension.FromPixels(50f);
707	      uiTextPanel1.VAlign = 1f;
708	      uiTextPanel1.HAlign = 0.0f;
709	      uiTextPanel1.Top = StyleDimension.FromPixels(-45f);
710	      UITextPanel<LocalizedText> uiTextPanel2 = uiTextPanel1;
711	      uiTextPanel2.OnMouseOver += new UIElement.MouseEvent(this.FadedMouseOver);
712	      uiTextPanel2.OnMouseOut += new UIElement.MouseEvent(this.FadedMouseOut);
713	      uiTextPanel2.OnMouseDown += new UIElement.MouseEvent(this.Click_GoBack);
714	      uiTextPanel2.SetSnapPoint("Back", 0, new Vector2?(), new Vector2?());
715	      outerContainer.Append((UIElement) uiTextPanel2);
716	      UITextPanel<LocalizedText> uiTextPanel3 = new UITextPanel<LocalizedText>(Language.GetText("UI.Create"), 0.7f, true);
717	      uiTextPanel3.Width = StyleDimension.FromPixelsAndPercent(-10f, 0.5f);
718	      uiTextPanel3.Height = StyleDimension.FromPixels(50f);
719	      uiTextPanel3.VAlign = 1f;
720	      uiTextPanel3.HAlign = 1f;
721	      uiTextPanel3.Top = StyleDimension.FromPixels(-45f);
722	      UITextPanel<LocalizedText> uiTextPanel4 = uiTextPanel3;
723	      uiTextPanel4.OnMouseOver += new UIElement.MouseEvent(this.FadedMouseOver);
724	      uiTextPanel4.OnMouseOut += new UIElement.MouseEvent(this.FadedMouseOut);
725	      uiTextPanel4.OnMouseDown += new UIElement.MouseEvent(this.Click_NamingAndCreating);
726	      uiTextPanel4.SetSnapPoint("Create", 0, new Vector2?(), new Vector2?());
727	      outerContainer.Append((UIElement) uiTextPanel4);
728	    }
729	
730	    private void Click_GoBack(UIMouseEvent evt, UIElement listeningElement)
731	    {
732	      SoundEngine.PlaySound(11, -1, -1, 1, 1f, 0.0f);
733	      Main.OpenCharacterSelectUI();
734	    }
735	
736	    private void FadedMouseOver(UIMouseEvent evt, UIElement listeningElement)
737	    {
738	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
739	      ((UIPanel) evt.Target).BackgroundColor = new Color(73, 94, 171);
740	      ((UIPanel) evt.Target).BorderColor = Colors.FancyUIFatButtonMouseOver;
741	    }
742	
743	    private void FadedMouseOut(UIMouseEvent evt, UIElement listeningElement)
744	    {
745	      ((UIPanel) evt.Target).BackgroundColor = new Color(63, 82, 151) * 0.8f;
746	      ((UIPanel) evt.Target).BorderColor = Color.Black;
747	    }
748	
749	    private void Click_ColorPicker(UIMouseEvent evt, UIElement listeningElement)
750	    {
751	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
752	      for (int index = 0; index < this._colorPickers.Length; ++index)
753	      {
754	        if (this._colorPickers[index] == evt.Target)
755	        {
756	          this.SelectColorPicker((UICharacterCreation.CategoryId) index);
757	          break;
758	        }
759	      }
760	    }
761	
762	    private void Click_ClothStyles(UIMouseEvent evt, UIElement listeningElement)
763	    {
764	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
765	      this.UnselectAllCategories();
766	      this._selectedPicker = UICharacterCreation.CategoryId.Clothing;
767	      this._middleContainer.Append(this._clothStylesContainer);
768	      this._clothingStylesCategoryButton.SetSelected(true);
769	      this.UpdateSelectedGender();
770	    }
771	
772	    private void Click_HairStyles(UIMouseEvent evt, UIElement listeningElement)
773	    {
774	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
775	      this.UnselectAllCategories();
776	      this._selectedPicker = UICharacterCreation.CategoryId.HairStyle;
777	      this._middleContainer.Append(this._hairstylesContainer);
778	      this._hairStylesCategoryButton.SetSelected(true);
779	    }
780	
781	    private void Click_CharInfo(UIMouseEvent evt, UIElement listeningElement)
782	    {
783	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
784	      this.UnselectAllCategories();
785	      this._selectedPicker = UICharacterCreation.CategoryId.CharInfo;
786	      this._middleContainer.Append(this._infoContainer);
787	      this._charInfoCategoryButton.SetSelected(true);
788	    }
789	
790	    private void Click_CharClothStyle(UIMouseEvent evt, UIElement listeningElement)
791	    {
792	      this._clothingStylesCategoryButton.SetImage((Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/" + (this._player.Male ? "ClothStyleMale" : "ClothStyleFemale"), (AssetRequestMode) 1));
793	      this.UpdateSelectedGender();
794	    }
795	
796	    private void Click_CharGenderMale(UIMouseEvent evt, UIElement listeningElement)
797	    {
798	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
799	      this._player.Male = true;
800	      this.Click_CharClothStyle(evt, listeningElement);
801	      this.UpdateSelectedGender();
802	    }
803	
804	    private void Click_CharGenderFemale(UIMouseEvent evt, UIElement listeningElement)
805	    {
806	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
807	      this._player.Male = false;
808	      this.Click_CharClothStyle(evt, listeningElement);
809	      this.UpdateSelectedGender();
810	    }
811	
812	    private void UpdateSelectedGender()
813	    {
814	      this._genderMale.SetSelected(this._player.Male);
815	      this._genderFemale.SetSelected(!this._player.Male);
816	    }
817	
818	    private void Click_CopyHex(UIMouseEvent evt, UIElement listeningElement)
819	    {
820	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
821	      ((IClipboard) Platform.Get<IClipboard>()).Value = this._hslHexText.Text;
822	    }
823	
824	    private void Click_PasteHex(UIMouseEvent evt, UIElement listeningElement)
825	    {
826	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
827	      Vector3 hsl;
828	      if (!this.GetHexColor(((IClipboard) Platform.Get<IClipboard>()).Value, out hsl))
829	        return;
830	      this.ApplyPendingColor(UICharacterCreation.ScaledHslToRgb(hsl.X, hsl.Y, hsl.Z));
831	      this._currentColorHSL = hsl;
832	      this.UpdateHexText(UICharacterCreation.ScaledHslToRgb(hsl.X, hsl.Y, hsl.Z));
833	      this.UpdateColorPickers();
834	    }
835	
836	    private void Click_CopyPlayerTemplate(UIMouseEvent evt, UIElement listeningElement)
837	    {
838	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
839	      Dictionary<string, object> dictionary = new Dictionary<string, object>();
840	      dictionary.Add("version", (object) 1);
841	      dictionary.Add("hairStyle", (object) this._player.hair);
842	      dictionary.Add("clothingStyle", (object) this._player.skinVariant);
843	      dictionary.Add("hairColor", (object) UICharacterCreation.GetHexText(this._player.hairColor));
844	      dictionary.Add("eyeColor", (object) UICharacterCreation.GetHexText(this._player.eyeColor));
845	      dictionary.Add("skinColor", (object) UICharacterCreation.GetHexText(this._player.skinColor));
846	      dictionary.Add("shirtColor", (object) UICharacterCreation.GetHexText(this._player.shirtColor));
847	      dictionary.Add("underShirtColor", (object) UICharacterCreation.GetHexText(this._player.underShirtColor));
848	      dictionary.Add("pantsColor", (object) UICharacterCreation.GetHexText(this._player.pantsColor));
849	      dictionary.Add("shoeColor", (object) UICharacterCreation.GetHexText(this._player.shoeColor));
850	      JsonSerializerSettings serializerSettings = new JsonSerializerSettings();
851	      serializerSettings.TypeNameHandling = (TypeNameHandling) 4;
852	      serializerSettings.MetadataPropertyHandling = (MetadataPropertyHandling) 1;
853	      serializerSettings.Formatting = (Formatting) 1;
854	      string text = JsonConvert.SerializeObject((object) dictionary, serializerSettings);
855	      PlayerInput.PrettyPrintProfiles(ref text);
856	      ((IClipboard) Platform.Get<IClipboard>()).Value = text;
857	    }
858	
859	    private void Click_PastePlayerTemplate(UIMouseEvent evt, UIElement listeningElement)
860	    {
861	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
862	      try
863	      {
864	        string str1 = ((IClipboard) Platform.Get<IClipboard>()).Value;
865	        int startIndex = str1.IndexOf("{");
866	        if (startIndex == -1)
867	          return;
868	        string str2 = str1.Substring(startIndex);
869	        int num1 = str2.LastIndexOf("}");
870	        if (num1 == -1)
871	          return;
872	        Dictionary<string, object> dictionary1 = (Dictionary<string, object>) JsonConvert.DeserializeObject<Dictionary<string, object>>(str2.Substring(0, num1 + 1));
873	        if (dictionary1 == null)
874	          return;
875	        Dictionary<string, object> dictionary2 = new Dictionary<string, object>();
876	        foreach (KeyValuePair<string, object> keyValuePair in dictionary1)
877	          dictionary2[keyValuePair.Key.ToLower()] = keyValuePair.Value;
878	        object obj;
879	        if (dictionary2.TryGetValue("version", out obj))
880	        {
881	          long num2 = (long) obj;
882	        }
883	        if (dictionary2.TryGetValue("hairstyle", out obj))
884	        {
885	          int num3 = (int) (long) obj;
886	          if (Main.Hairstyles.AvailableHairstyles.Contains(num3))
887	            this._player.hair = num3;
888	        }
889	        if (dictionary2.TryGetValue("clothingstyle", out obj))
890	        {
891	          int num3 = (int) (long) obj;
892	          if (((IEnumerable<int>) this._validClothStyles).Contains<int>(num3))
893	            this._player.skinVariant = num3;
894	        }
895	        Vector3 hsl;
896	        if (dictionary2.TryGetValue("haircolor", out obj) && this.GetHexColor((string) obj, out hsl))
897	          this._player.hairColor = UICharacterCreation.ScaledHslToRgb(hsl);
898	        if (dictionary2.TryGetValue("eyecolor", out obj) && this.GetHexColor((string) obj, out hsl))
899	          this._player.eyeColor = UICharacterCreation.ScaledHslToRgb(hsl);
900	        if (dictionary2.TryGetValue("skincolor", out obj) && this.GetHexColor((string) obj, out hsl))
901	          this._player.skinColor = UICharacterCreation.ScaledHslToRgb(hsl);
902	        if (dictionary2.TryGetValue("shirtcolor", out obj) && this.GetHexColor((string) obj, out hsl))
903	          this._player.shirtColor = UICharacterCreation.ScaledHslToRgb(hsl);
904	        if (dictionary2.TryGetValue("undershirtcolor", out obj) && this.GetHexColor((string) obj, out hsl))
905	          this._player.underShirtColor = UICharacterCreation.ScaledHslToRgb(hsl);
906	        if (dictionary2.TryGetValue("pantscolor", out obj) && this.GetHexColor((string) obj, out hsl))
907	          this._player.pantsColor = UICharacterCreation.ScaledHslToRgb(hsl);
908	        if (dictionary2.TryGetValue("shoecolor", out obj) && this.GetHexColor((string) obj, out hsl))
909	          this._player.shoeColor = UICharacterCreation.ScaledHslToRgb(hsl);
910	        this.Click_CharClothStyle((UIMouseEvent) null, (UIElement) null);
911	        this.UpdateColorPickers();
912	      }
913	      catch
914	      {
915	      }
916	    }
917	
918	    private void Click_RandomizePlayer(UIMouseEvent evt, UIElement listeningElement)
919	    {
920	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
921	      Player player = this._player;
922	      int index = Main.rand.Next(Main.Hairstyles.AvailableHairstyles.Count);
923	      player.hair = Main.Hairstyles.AvailableHairstyles[index];
924	      while ((int) player.eyeColor.R + (int) player.eyeColor.G + (int) player.eyeColor.B > 300)
925	        player.eyeColor = UICharacterCreation.ScaledHslToRgb(UICharacterCreation.GetRandomColorVector());
926	      float num = (float) Main.rand.Next(60, 120) * 0.01f;
927	      if ((double) num > 1.0)
928	        num = 1f;
929	      player.skinColor.R = (byte) ((double) Main.rand.Next(240, (int) byte.MaxValue) * (double) num);
930	      player.skinColor.G = (byte) ((double) Main.rand.Next(110, 140) * (double) num);
931	      player.skinColor.B = (byte) ((double) Main.rand.Next(75, 110) * (double) num);
932	      player.hairColor = UICharacterCreation.ScaledHslToRgb(UICharacterCreation.GetRandomColorVector());
933	      player.shirtColor = UICharacterCreation.ScaledHslToRgb(UICharacterCreation.GetRandomColorVector());
934	      player.underShirtColor = UICharacterCreation.ScaledHslToRgb(UICharacterCreation.GetRandomColorVector());
935	      player.pantsColor = UICharacterCreation.ScaledHslToRgb(UICharacterCreation.GetRandomColorVector());
936	      player.shoeColor = UICharacterCreation.ScaledHslToRgb(UICharacterCreation.GetRandomColorVector());
937	      player.skinVariant = this._validClothStyles[Main.rand.Next(this._validClothStyles.Length)];
938	      switch (player.hair + 1)
939	      {
940	        case 5:
941	        case 6:
942	        case 7:
943	        case 10:
944	        case 12:
945	        case 19:
946	        case 22:
947	        case 23:
948	        case 26:
949	        case 27:
950	        case 30:
951	        case 33:
952	          player.Male = false;
953	          break;
954	        default:
955	          player.Male = true;
956	          break;
957	      }
958	      this.Click_CharClothStyle((UIMouseEvent) null, (UIElement) null);
959	      this.UpdateSelectedGender();
960	      this.UpdateColorPickers();
961	    }
962	
963	    private void Click_Naming(UIMouseEvent evt, UIElement listeningElement)
964	    {
965	      SoundEngine.PlaySound(10, -1, -1, 1, 1f, 0.0f);
966	      this._player.name = "";
967	      Main.clrInput();
968	      UIVirtualKeyboard uiVirtualKeyboard = new UIVirtualKeyboard(Lang.menu[45].Value, "", new UIVirtualKeyboard.KeyboardSubmitEvent(this.OnFinishedNaming), new Action(this.OnCancledNaming), 0, true);
969	      uiVirtualKeyboard.SetMaxInputLength(20);
970	      Main.MenuUI.SetState((UIState) uiVirtualKeyboard);
971	    }
972	
973	    private void Click_NamingAndCreating(UIMouseEvent evt, UIElement listeningElement)
974	    {
975	      SoundEngine.PlaySound(10, -1, -1, 1, 1f, 0.0f);
976	      if (string.IsNullOrEmpty(this._player.name))
977	      {
978	        this._player.name = "";
979	        Main.clrInput();
980	        UIVirtualKeyboard uiVirtualKeyboard = new UIVirtualKeyboard(Lang.menu[45].Value, "", new UIVirtualKeyboard.KeyboardSubmitEvent(this.OnFinishedNamingAndCreating), new Action(this.OnCancledNaming), 0, false);
981	        uiVirtualKeyboard.SetMaxInputLength(20);
982	        Main.MenuUI.SetState((UIState) uiVirtualKeyboard);
983	      }
984	      else
985	        this.FinishCreatingCharacter();
986	    }
987	
988	    private void OnFinishedNaming(string name)
989	    {
990	      this._player.name = name.Trim();
991	      Main.MenuUI.SetState((UIState) this);
992	      this._charName.SetContents(this._player.name);
993	    }
994	
995	    private void OnCancledNaming()
996	    {
997	      Main.MenuUI.SetState((UIState) this);
998	    }
999	
1000	    private void OnFinishedNamingAndCreating(string name)
1001	    {
1002	      this._player.name = name.Trim();
1003	      Main.MenuUI.SetState((UIState) this);
1004	      this._charName.SetContents(this._player.name);
1005	      this.FinishCreatingCharacter();
1006	    }
1007	
1008	    private void FinishCreatingCharacter()
1009	    {
1010	      this.SetupPlayerStatsAndInventoryBasedOnDifficulty();
1011	      PlayerFileData.CreateAndSave(this._player);
1012	      Main.LoadPlayers();
1013	      Main.menuMode = 1;
1014	    }
1015	
1016	    private void SetupPlayerStatsAndInventoryBasedOnDifficulty()
1017	    {
1018	      int index1 = 0;
1019	      int num1;
1020	      if (this._player.difficulty == (byte) 3)
1021	      {
1022	        this._player.statLife = this._player.statLifeMax = 100;
1023	        this._player.statMana = this._player.statManaMax = 20;
1024	        this._player.inventory[index1].SetDefaults(6);
1025	        Item[] inventory1 = this._player.inventory;
1026	        int index2 = index1;
1027	        int index3 = index2 + 1;
1028	        inventory1[index2].Prefix(-1);
1029	        this._player.inventory[index3].SetDefaults(1);
1030	        Item[] inventory2 = this._player.inventory;
1031	        int index4 = index3;
1032	        int index5 = index4 + 1;
1033	        inventory2[index4].Prefix(-1);
1034	        this._player.inventory[index5].SetDefaults(10);
1035	        Item[] inventory3 = this._player.inventory;
1036	        int index6 = index5;
1037	        int index7 = index6 + 1;
1038	        inventory3[index6].Prefix(-1);
1039	        this._player.inventory[index7].SetDefaults(7);
1040	        Item[] inventory4 = this._player.inventory;
1041	        int index8 = index7;
1042	        int index9 = index8 + 1;
1043	        inventory4[index8].Prefix(-1);
1044	        this._player.inventory[index9].SetDefaults(4281);
1045	        Item[] inventory5 = this._player.inventory;
1046	        int index10 = index9;
1047	        int index11 = index10 + 1;
1048	        inventory5[index10].Prefix(-1);
1049	        this._player.inventory[index11].SetDefaults(8);
1050	        Item[] inventory6 = this._player.inventory;
1051	        int index12 = index11;
1052	        int index13 = index12 + 1;
1053	        inventory6[index12].stack = 100;
1054	        this._player.inventory[index13].SetDefaults(965);
1055	        Item[] inventory7 = this._player.inventory;
1056	        int index14 = index13;
1057	        int num2 = index14 + 1;
1058	        inventory7[index14].stack = 100;
1059	        Item[] inventory8 = this._player.inventory;
1060	        int index15 = num2;
1061	        num1 = index15 + 1;
1062	        inventory8[index15].SetDefaults(50);
1063	        this._player.armor[3].SetDefaults(4978);
1064	        this._player.armor[3].Prefix(-1);
1065	        this._player.AddBuff(216, 3600, true, false);
1066	      }
1067	      else
1068	      {
1069	        this._player.inventory[index1].SetDefaults(3507);
1070	        Item[] inventory1 = this._player.inventory;
1071	        int index2 = index1;
1072	        int index3 = index2 + 1;
1073	        inventory1[index2].Prefix(-1);
1074	        this._player.inventory[index3].SetDefaults(3509);
1075	        Item[] inventory2 = this._player.inventory;
1076	        int index4 = index3;
1077	        int index5 = index4 + 1;
1078	        inventory2[index4].Prefix(-1);
1079	        this._player.inventory[index5].SetDefaults(3506);
1080	        Item[] inventory3 = this._player.inventory;
1081	        int index6 = index5;
1082	        num1 = index6 + 1;
1083	        inventory3[index6].Prefix(-1);
1084	      }
1085	      if (Main.runningCollectorsEdition)
1086	      {
1087	        Item[] inventory = this._player.inventory;
1088	        int index2 = num1;
1089	        int num2 = index2 + 1;
1090	        inventory[index2].SetDefaults(603);
1091	      }
1092	      this._player.savedPerPlayerFieldsThatArentInThePlayerClass = new Player.SavedPlayerDataWithAnnoyingRules();
1093	      CreativePowerManager.Instance.ResetDataForNewPlayer(this._player);
1094	    }
1095	
1096	    private bool GetHexColor(string hexString, out Vector3 hsl)
1097	    {
1098	      if (hexString.StartsWith("#"))
1099	        hexString = hexString.Substring(1);
1100	      uint result;
1101	      if (hexString.Length <= 6 && uint.TryParse(hexString, NumberStyles.HexNumber, (IFormatProvider) CultureInfo.CurrentCulture, out result))
1102	      {
1103	        uint num1 = result & (uint) byte.MaxValue;
1104	        uint num2 = result >> 8 & (uint) byte.MaxValue;
1105	        uint num3 = result >> 16 & (uint) byte.MaxValue;
1106	        hsl = UICharacterCreation.RgbToScaledHsl(new Color((int) num3, (int) num2, (int) num1));
1107	        return true;
1108	      }
1109	      hsl = Vector3.Zero;
1110	      return false;
1111	    }
1112	
1113	    private void Click_RandomizeSingleColor(UIMouseEvent evt, UIElement listeningElement)
1114	    {
1115	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
1116	      Vector3 randomColorVector = UICharacterCreation.GetRandomColorVector();
1117	      this.ApplyPendingColor(UICharacterCreation.ScaledHslToRgb(randomColorVector.X, randomColorVector.Y, randomColorVector.Z));
1118	      this._currentColorHSL = randomColorVector;
1119	      this.UpdateHexText(UICharacterCreation.ScaledHslToRgb(randomColorVector.X, randomColorVector.Y, randomColorVector.Z));
1120	      this.UpdateColorPickers();
1121	    }
1122	
1123	    private static Vector3 GetRandomColorVector()
1124	    {
1125	      return new Vector3(Main.rand.NextFloat(), Main.rand.NextFloat(), Main.rand.NextFloat());
1126	    }
1127	
1128	    private void UnselectAllCategories()
1129	    {
1130	      foreach (UIColoredImageButton colorPicker in this._colorPickers)
1131	        colorPicker?.SetSelected(false);
1132	      this._clothingStylesCategoryButton.SetSelected(false);
1133	      this._hairStylesCategoryButton.SetSelected(false);
1134	      this._charInfoCategoryButton.SetSelected(false);
1135	      this._hslContainer.Remove();
1136	      this._hairstylesContainer.Remove();
1137	      this._clothStylesContainer.Remove();
1138	      this._infoContainer.Remove();
1139	    }
1140	
1141	    private void SelectColorPicker(UICharacterCreation.CategoryId selection)
1142	    {
1143	      this._selectedPicker = selection;
1144	      switch (selection)
1145	      {
1146	        case UICharacterCreation.CategoryId.CharInfo:
1147	          this.Click_CharInfo((UIMouseEvent) null, (UIElement) null);
1148	          break;
1149	        case UICharacterCreation.CategoryId.Clothing:
1150	          this.Click_ClothStyles((UIMouseEvent) null, (UIElement) null);
1151	          break;
1152	        case UICharacterCreation.CategoryId.HairStyle:
1153	          this.Click_HairStyles((UIMouseEvent) null, (UIElement) null);
1154	          break;
1155	        default:
1156	          this.UnselectAllCategories();
1157	          this._middleContainer.Append(this._hslContainer);
1158	          for (int index = 0; index < this._colorPickers.Length; ++index)
1159	          {
1160	            if (this._colorPickers[index] != null)
1161	              this._colorPickers[index].SetSelected((UICharacterCreation.CategoryId) index == selection);
1162	          }
1163	          Vector3 vector3 = Vector3.One;
1164	          switch (this._selectedPicker)
1165	          {
1166	            case UICharacterCreation.CategoryId.HairColor:
1167	              vector3 = UICharacterCreation.RgbToScaledHsl(this._player.hairColor);
1168	              break;
1169	            case UICharacterCreation.CategoryId.Eye:
1170	              vector3 = UICharacterCreation.RgbToScaledHsl(this._player.eyeColor);
1171	              break;
1172	            case UICharacterCreation.CategoryId.Skin:
1173	              vector3 = UICharacterCreation.RgbToScaledHsl(this._player.skinColor);
1174	              break;
1175	            case UICharacterCreation.CategoryId.Shirt:
1176	              vector3 = UICharacterCreation.RgbToScaledHsl(this._player.shirtColor);
1177	              break;
1178	            case UICharacterCreation.CategoryId.Undershirt:
1179	              vector3 = UICharacterCreation.RgbToScaledHsl(this._player.underShirtColor);
1180	              break;
1181	            case UICharacterCreation.CategoryId.Pants:
1182	              vector3 = UICharacterCreation.RgbToScaledHsl(this._player.pantsColor);
1183	              break;
1184	            case UICharacterCreation.CategoryId.Shoes:
1185	              vector3 = UICharacterCreation.RgbToScaledHsl(this._player.shoeColor);
1186	              break;
1187	          }
1188	          this._currentColorHSL = vector3;
1189	          this.UpdateHexText(UICharacterCreation.ScaledHslToRgb(vector3.X, vector3.Y, vector3.Z));
1190	          break;
1191	      }
1192	    }
1193	
1194	    private void UpdateColorPickers()
1195	    {
1196	      int selectedPicker = (int) this._selectedPicker;
1197	      this._colorPickers[3].SetColor(this._player.hairColor);
1198	      this._hairStylesCategoryButton.SetColor(this._player.hairColor);
1199	      this._colorPickers[4].SetColor(this._player.eyeColor);
1200	      this._colorPickers[5].SetColor(this._player.skinColor);
1201	      this._colorPickers[6].SetColor(this._player.shirtColor);
1202	      this._colorPickers[7].SetColor(this._player.underShirtColor);
1203	      this._colorPickers[8].SetColor(this._player.pantsColor);
1204	      this._colorPickers[9].SetColor(this._player.shoeColor);
1205	    }
1206	
1207	    public override void Draw(SpriteBatch spriteBatch)
1208	    {
1209	      base.Draw(spriteBatch);
1210	      string text = (string) null;
1211	      if (this._copyHexButton.IsMouseHovering)
1212	        text = Language.GetTextValue("UI.CopyColorToClipboard");
1213	      if (this._pasteHexButton.IsMouseHovering)
1214	        text = Language.GetTextValue("UI.PasteColorFromClipboard");
1215	      if (this._randomColorButton.IsMouseHovering)
1216	        text = Language.GetTextValue("UI.RandomizeColor");
1217	      if (this._copyTemplateButton.IsMouseHovering)
1218	        text = Language.GetTextValue("UI.CopyPlayerToClipboard");
1219	      if (this._pasteTemplateButton.IsMouseHovering)
1220	        text = Language.GetTextValue("UI.PastePlayerFromClipboard");
1221	      if (this._randomizePlayerButton.IsMouseHovering)
1222	        text = Language.GetTextValue("UI.RandomizePlayer");
1223	      if (text != null)
1224	      {
1225	        float x = FontAssets.MouseText.Value.MeasureString(text).X;
1226	        Vector2 vector2 = new Vector2((float) Main.mouseX, (float) Main.mouseY) + new Vector2(16f);
1227	        if ((double) vector2.Y > (double) (Main.screenHeight - 30))
1228	          vector2.Y = (float) (Main.screenHeight - 30);
1229	        if ((double) vector2.X > (double) Main.screenWidth - (double) x)
1230	          vector2.X = (float) (Main.screenWidth - 460);
1231	        Utils.DrawBorderStringFourWay(spriteBatch, FontAssets.MouseText.Value, text, vector2.X, vector2.Y, new Color((int) Main.mouseTextColor, (int) Main.mouseTextColor, (int) Main.mouseTextColor, (int) Main.mouseTextColor), Color.Black, Vector2.Zero, 1f);
1232	      }
1233	      this.SetupGamepadPoints(spriteBatch);
1234	    }
1235	
1236	    private void SetupGamepadPoints(SpriteBatch spriteBatch)
1237	    {
1238	      UILinkPointNavigator.Shortcuts.BackButtonCommand = 1;
1239	      int num1 = 3000;
1240	      int num2 = num1 + 20;
1241	      int ID1 = num1;
1242	      List<SnapPoint> snapPoints = this.GetSnapPoints();
1243	      SnapPoint snapPoint1 = snapPoints.First<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Back"));
1244	      SnapPoint snapPoint2 = snapPoints.First<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Create"));
1245	      UILinkPoint point1 = UILinkPointNavigator.Points[ID1];
1246	      point1.Unlink();
1247	      UILinkPointNavigator.SetPosition(ID1, snapPoint1.Position);
1248	      int ID2 = ID1 + 1;
1249	      UILinkPoint point2 = UILinkPointNavigator.Points[ID2];
1250	      point2.Unlink();
1251	      UILinkPointNavigator.SetPosition(ID2, snapPoint2.Position);
1252	      int ID3 = ID2 + 1;
1253	      point1.Right = point2.ID;
1254	      point2.Left = point1.ID;
1255	      this._foundPoints.Clear();
1256	      this._foundPoints.Add(point1.ID);
1257	      this._foundPoints.Add(point2.ID);
1258	      List<SnapPoint> list1 = snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Top")).ToList<SnapPoint>();
1259	      list1.Sort(new Comparison<SnapPoint>(this.SortPoints));
1260	      for (int index = 0; index < list1.Count; ++index)
1261	      {
1262	        UILinkPoint point3 = UILinkPointNavigator.Points[ID3];
1263	        point3.Unlink();
1264	        UILinkPointNavigator.SetPosition(ID3, list1[index].Position);
1265	        point3.Left = ID3 - 1;
1266	        point3.Right = ID3 + 1;
1267	        point3.Down = num2;
1268	        if (index == 0)
1269	          point3.Left = -3;
1270	        if (index == list1.Count - 1)
1271	          point3.Right = -4;
1272	        if (this._selectedPicker == UICharacterCreation.CategoryId.HairStyle || this._selectedPicker == UICharacterCreation.CategoryId.Clothing)
1273	          point3.Down = num2 + index;
1274	        this._foundPoints.Add(ID3);
1275	        ++ID3;
1276	      }
1277	      List<SnapPoint> list2 = snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Middle")).ToList<SnapPoint>();
1278	      list2.Sort(new Comparison<SnapPoint>(this.SortPoints));
1279	      int ptid1 = num2;
1280	      switch (this._selectedPicker)
1281	      {
1282	        case UICharacterCreation.CategoryId.CharInfo:
1283	          for (int index = 0; index < list2.Count; ++index)
1284	          {
1285	            UILinkPoint andSet = this.GetAndSet(ptid1, list2[index]);
1286	            andSet.Up = andSet.ID - 1;
1287	            andSet.Down = andSet.ID + 1;
1288	            if (index == 0)
1289	              andSet.Up = num1 + 2;
1290	            if (index == list2.Count - 1)
1291	            {
1292	              andSet.Down = point1.ID;
1293	              point1.Up = andSet.ID;
1294	              point2.Up = andSet.ID;
1295	            }
1296	            this._foundPoints.Add(ptid1);
1297	            ++ptid1;
1298	          }
1299	          break;
1300	        case UICharacterCreation.CategoryId.Clothing:
1301	          List<SnapPoint> list3 = snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Low")).ToList<SnapPoint>();
1302	          list3.Sort(new Comparison<SnapPoint>(this.SortPoints));
1303	          int num3 = -2;
1304	          int num4 = -2;
1305	          int ptid2 = num2 + 20;
1306	          for (int index = 0; index < list3.Count; ++index)
1307	          {
1308	            UILinkPoint andSet = this.GetAndSet(ptid2, list3[index]);
1309	            andSet.Up = num2 + index + 2;
1310	            andSet.Down = point1.ID;
1311	            if (index >= 3)
1312	            {
1313	              ++andSet.Up;
1314	              andSet.Down = point2.ID;
1315	            }
1316	            andSet.Left = andSet.ID - 1;
1317	            andSet.Right = andSet.ID + 1;
1318	            if (index == 0)
1319	            {
1320	              num3 = andSet.ID;
1321	              andSet.Left = andSet.ID + 4;
1322	              point1.Up = andSet.ID;
1323	            }
1324	            if (index == list3.Count - 1)
1325	            {
1326	              num4 = andSet.ID;
1327	              andSet.Right = andSet.ID - 4;
1328	              point2.Up = andSet.ID;
1329	            }
1330	            this._foundPoints.Add(ptid2);
1331	            ++ptid2;
1332	          }
1333	          int ptid3 = num2;
1334	          for (int index = 0; index < list2.Count; ++index)
1335	          {
1336	            UILinkPoint andSet = this.GetAndSet(ptid3, list2[index]);
1337	            andSet.Up = num1 + 2 + index;
1338	            andSet.Left = andSet.ID - 1;
1339	            andSet.Right = andSet.ID + 1;
1340	            if (index == 0)
1341	              andSet.Left = andSet.ID + 9;
1342	            if (index == list2.Count - 1)
1343	              andSet.Right = andSet.ID - 9;
1344	            andSet.Down = num3;
1345	            if (index >= 5)
1346	              andSet.Down = num4;
1347	            this._foundPoints.Add(ptid3);
1348	            ++ptid3;
1349	          }
1350	          break;
1351	        case UICharacterCreation.CategoryId.HairStyle:
1352	          if (list2.Count != 0)
1353	          {
1354	            this._helper.CullPointsOutOfElementArea(spriteBatch, list2, this._hairstylesContainer);
1355	            SnapPoint snapPoint3 = list2[list2.Count - 1];
1356	            int num5 = snapPoint3.Id / 10;
1357	            int num6 = snapPoint3.Id % 10;
1358	            int count = Main.Hairstyles.AvailableHairstyles.Count;
1359	            for (int index = 0; index < list2.Count; ++index)
1360	            {
1361	              SnapPoint snap = list2[index];
1362	              UILinkPoint andSet = this.GetAndSet(ptid1, snap);
1363	              andSet.Left = andSet.ID - 1;
1364	              if (snap.Id == 0)
1365	                andSet.Left = -3;
1366	              andSet.Right = andSet.ID + 1;
1367	              if (snap.Id == count - 1)
1368	                andSet.Right = -4;
1369	              andSet.Up = andSet.ID - 10;
1370	              if (index < 10)
1371	                andSet.Up = num1 + 2 + index;
1372	              andSet.Down = andSet.ID + 10;
1373	              if (snap.Id + 10 > snapPoint3.Id)
1374	                andSet.Down = snap.Id % 10 >= 5 ? point2.ID : point1.ID;
1375	              if (index == list2.Count - 1)
1376	              {
1377	                point1.Up = andSet.ID;
1378	                point2.Up = andSet.ID;
1379	              }
1380	              this._foundPoints.Add(ptid1);
1381	              ++ptid1;
1382	            }
1383	            break;
1384	          }
1385	          break;
1386	        default:
1387	          List<SnapPoint> list4 = snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Low")).ToList<SnapPoint>();
1388	          list4.Sort(new Comparison<SnapPoint>(this.SortPoints));
1389	          int ptid4 = num2 + 20;
1390	          for (int index = 0; index < list4.Count; ++index)
1391	          {
1392	            UILinkPoint andSet = this.GetAndSet(ptid4, list4[index]);
1393	            andSet.Up = num2 + 2;
1394	            andSet.Down = point1.ID;
1395	            andSet.Left = andSet.ID - 1;
1396	            andSet.Right = andSet.ID + 1;
1397	            if (index == 0)
1398	            {
1399	              andSet.Left = andSet.ID + 2;
1400	              point1.Up = andSet.ID;
1401	            }
1402	            if (index == list4.Count - 1)
1403	            {
1404	              andSet.Right = andSet.ID - 2;
1405	              point2.Up = andSet.ID;
1406	            }
1407	            this._foundPoints.Add(ptid4);
1408	            ++ptid4;
1409	          }
1410	          int ptid5 = num2;
1411	          for (int index = 0; index < list2.Count; ++index)
1412	          {
1413	            UILinkPoint andSet = this.GetAndSet(ptid5, list2[index]);
1414	            andSet.Up = andSet.ID - 1;
1415	            andSet.Down = andSet.ID + 1;
1416	            if (index == 0)
1417	              andSet.Up = num1 + 2 + 5;
1418	            if (index == list2.Count - 1)
1419	              andSet.Down = num2 + 20 + 2;
1420	            this._foundPoints.Add(ptid5);
1421	            ++ptid5;
1422	          }
1423	          break;
1424	      }
1425	      if (!PlayerInput.UsingGamepadUI || this._foundPoints.Contains(UILinkPointNavigator.CurrentPoint))
1426	        return;
1427	      this.MoveToVisuallyClosestPoint();
1428	    }
1429	
1430	    private void MoveToVisuallyClosestPoint()
1431	    {
1432	      Dictionary<int, UILinkPoint> points = UILinkPointNavigator.Points;
1433	      Vector2 mouseScreen = Main.MouseScreen;
1434	      UILinkPoint uiLinkPoint1 = (UILinkPoint) null;
1435	      foreach (int foundPoint in this._foundPoints)
1436	      {
1437	        UILinkPoint uiLinkPoint2;
1438	        if (!points.TryGetValue(foundPoint, out uiLinkPoint2))
1439	          return;
1440	        if (uiLinkPoint1 == null || (double) Vector2.Distance(mouseScreen, uiLinkPoint1.Position) > (double) Vector2.Distance(mouseScreen, uiLinkPoint2.Position))
1441	          uiLinkPoint1 = uiLinkPoint2;
1442	      }
1443	      if (uiLinkPoint1 == null)
1444	        return;
1445	      UILinkPointNavigator.ChangePoint(uiLinkPoint1.ID);
1446	    }
1447	
1448	    public void TryMovingCategory(int direction)
1449	    {
1450	      int num = (int) (this._selectedPicker + direction) % 10;
1451	      if (num < 0)
1452	        num += 10;
1453	      this.SelectColorPicker((UICharacterCreation.CategoryId) num);
1454	    }
1455	
1456	    private UILinkPoint GetAndSet(int ptid, SnapPoint snap)
1457	    {
1458	      UILinkPoint point = UILinkPointNavigator.Points[ptid];
1459	      point.Unlink();
1460	      UILinkPointNavigator.SetPosition(point.ID, snap.Position);
1461	      return point;
1462	    }
1463	
1464	    private bool PointWithName(SnapPoint a, string comp)
1465	    {
1466	      return a.Name == comp;
1467	    }
1468	
1469	    private int SortPoints(SnapPoint a, SnapPoint b)
1470	    {
1471	      return a.Id.CompareTo(b.Id);
1472	    }
1473	
1474	    private static Color ScaledHslToRgb(Vector3 hsl)
1475	    {
1476	      return UICharacterCreation.ScaledHslToRgb(hsl.X, hsl.Y, hsl.Z);
1477	    }
1478	
1479	    private static Color ScaledHslToRgb(float hue, float saturation, float luminosity)
1480	    {
1481	      return Main.hslToRgb(hue, saturation, (float) ((double) luminosity * 0.850000023841858 + 0.150000005960464));
1482	    }
1483	
1484	    private static Vector3 RgbToScaledHsl(Color color)
1485	    {
1486	      Vector3 hsl = Main.rgbToHsl(color);
1487	      hsl.Z = (float) (((double) hsl.Z - 0.150000005960464) / 0.850000023841858);
1488	      return Vector3.Clamp(hsl, Vector3.Zero, Vector3.One);
1489	    }
1490	
1491	    private enum CategoryId
1492	    {
1493	      CharInfo,
1494	      Clothing,
1495	      HairStyle,
1496	      HairColor,
1497	      Eye,
1498	      Skin,
1499	      Shirt,
1500	      Undershirt,
1501	      Pants,
1502	      Shoes,
1503	      Count,
1504	    }
1505	
1506	    private enum HSLSliderId
1507	    {
1508	      Hue,
1509	      Saturation,
1510	      Luminance,
1511	    }
1512	  }
1513	}
1514	

```


---

## 🤖 Assistant · 2026-08-09T11:48:45.527Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read the new version UICharacterCreation.cs (2386 lines).
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:48:45.530Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterCreation.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:45.737Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using System.Globalization;
4	using System.Linq;
5	using Microsoft.Xna.Framework;
6	using Microsoft.Xna.Framework.Graphics;
7	using Newtonsoft.Json;
8	using ReLogic.Content;
9	using ReLogic.OS;
10	using Terraria.Audio;
11	using Terraria.GameContent.Creative;
12	using Terraria.GameContent.UI.Elements;
13	using Terraria.GameInput;
14	using Terraria.ID;
15	using Terraria.IO;
16	using Terraria.Initializers;
17	using Terraria.Localization;
18	using Terraria.UI;
19	using Terraria.UI.Gamepad;
20	
21	namespace Terraria.GameContent.UI.States;
22	
23	public class UICharacterCreation : UIState, IHaveBackButtonCommand
24	{
25		private enum CategoryId
26		{
27			CharInfo,
28			Clothing,
29			HairStyle,
30			HairColor,
31			Eye,
32			Skin,
33			Shirt,
34			Undershirt,
35			Pants,
36			Shoes,
37			Count
38		}
39	
40		private enum HSLSliderId
41		{
42			Hue,
43			Saturation,
44			Luminance
45		}
46	
47		private struct ArmorAssignments
48		{
49			public int HeadItem;
50	
51			public int BodyItem;
52	
53			public int LegItem;
54	
55			public int Accessory1Item;
56		}
57	
58		private int[] _validClothStyles = new int[10] { 0, 2, 1, 3, 8, 9, 7, 5, 6, 4 };
59	
60		private Dictionary<int, int> _defaultHairstylesForClothStyle = new Dictionary<int, int>
61		{
62			{ 0, 0 },
63			{ 2, 1 },
64			{ 1, 12 },
65			{ 3, 2 },
66			{ 8, 28 },
67			{ 9, 68 },
68			{ 7, 18 },
69			{ 5, 22 },
70			{ 6, 81 },
71			{ 4, 5 }
72		};
73	
74		private int[] _validVoiceStyles = new int[3] { 1, 2, 3 };
75	
76		private readonly Player _player;
77	
78		private UIColoredImageButton[] _colorPickers;
79	
80		private CategoryId _selectedPicker;
81	
82		private Vector3 _currentColorHSL;
83	
84		private UIColoredImageButton _clothingStylesCategoryButton;
85	
86		private UIColoredImageButton _hairStylesCategoryButton;
87	
88		private UIColoredImageButton _charInfoCategoryButton;
89	
90		private UIElement _topContainer;
91	
92		private UIElement _middleContainer;
93	
94		private UIElement _hslContainer;
95	
96		private UIElement _hairstylesContainer;
97	
98		private UIElement _clothStylesContainer;
99	
100		private UIElement _infoContainer;
101	
102		private UIText _hslHexText;
103	
104		private UIText _difficultyDescriptionText;
105	
106		private UIElement _copyHexButton;
107	
108		private UIElement _pasteHexButton;
109	
110		private UIElement _randomColorButton;
111	
112		private UIElement _copyTemplateButton;
113	
114		private UIElement _pasteTemplateButton;
115	
116		private UIElement _randomizePlayerButton;
117	
118		private UIElement _pitchSlider;
119	
120		private UIElement _voiceNext;
121	
122		private UIElement _voicePrevious;
123	
124		private UIElement _voicePlay;
125	
126		private float _pitchAmount;
127	
128		private UIElement[] _previewArmorButton = new UIElement[0];
129	
130		private UICharacterNameButton _charName;
131	
132		private UIText _helpGlyphLeft;
133	
134		private UIText _helpGlyphRight;
135	
136		private bool _oldMaleForVoiceAutoSwitch = true;
137	
138		private int? _lastSelectedHairstyle;
139	
140		private UIImageFramed[] _characterPreviewLayers = new UIImageFramed[7];
141	
142		public const int MAX_NAME_LENGTH = 20;
143	
144		private bool _playedVoicePreviewThisFrame;
145	
146		private ArmorAssignments _maleArmor;
147	
148		private ArmorAssignments _femaleArmor;
149	
150		private GameTipsDisplay _tips;
151	
152		public static UIState BackupConfirmationState;
153	
154		private static bool dirty;
155	
156		private string initialState;
157	
158		private bool _pitchChanged;
159	
160		private int _pitchChangedCooldown;
161	
162		private UIGamepadHelper _helper;
163	
164		private List<int> _foundPoints = new List<int>();
165	
166		public UICharacterCreation(Player player)
167		{
168			_player = player;
169			_player.difficulty = 0;
170			_tips = new GameTipsDisplay(new CharacterCreationTipsProvider());
171			BuildPage();
172			initialState = GetPlayerTemplateValues();
173			dirty = false;
174		}
175	
176		public override void Update(GameTime gameTime)
177		{
178			_playedVoicePreviewThisFrame = false;
179			base.Update(gameTime);
180		}
181	
182		private void BuildPage()
183		{
184			RemoveAllChildren();
185			int num = 4;
186			UIElement uIElement = new UIElement
187			{
188				Width = StyleDimension.FromPixels(500f),
189				Height = StyleDimension.FromPixels(380 + num),
190				Top = StyleDimension.FromPixels(220f),
191				HAlign = 0.5f,
192				VAlign = 0f
193			};
194			uIElement.SetPadding(0f);
195			Append(uIElement);
196			UIPanel uIPanel = new UIPanel
197			{
198				Width = StyleDimension.FromPercent(1f),
199				Height = StyleDimension.FromPixels(uIElement.Height.Pixels - 150f - (float)num),
200				Top = StyleDimension.FromPixels(50f),
201				BackgroundColor = new Color(33, 43, 79) * 0.8f
202			};
203			uIPanel.SetPadding(0f);
204			uIElement.Append(uIPanel);
205			MakeBackAndCreatebuttons(uIElement);
206			MakeCharPreview(uIPanel);
207			UIElement uIElement2 = new UIElement
208			{
209				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
210				Height = StyleDimension.FromPixelsAndPercent(50f, 0f)
211			};
212			uIElement2.SetPadding(0f);
213			uIElement2.PaddingTop = 4f;
214			uIElement2.PaddingBottom = 0f;
215			uIPanel.Append(uIElement2);
216			UIElement uIElement3 = new UIElement
217			{
218				Top = StyleDimension.FromPixelsAndPercent(uIElement2.Height.Pixels + 6f, 0f),
219				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
220				Height = StyleDimension.FromPixelsAndPercent(uIPanel.Height.Pixels - 70f, 0f)
221			};
222			uIElement3.SetPadding(0f);
223			uIElement3.PaddingTop = 3f;
224			uIElement3.PaddingBottom = 0f;
225			uIPanel.Append(uIElement3);
226			_topContainer = uIElement2;
227			_middleContainer = uIElement3;
228			MakeInfoMenu(uIElement3);
229			MakeHSLMenu(uIElement3);
230			MakeHairstylesMenu(uIElement3);
231			MakeClothStylesMenu(uIElement3);
232			MakeCategoriesBar(uIElement2);
233			Click_CharInfo(null, null);
234		}
235	
236		private void MakeCharPreview(UIPanel container)
237		{
238			float num = 70f;
239			for (float num2 = 0f; num2 < 1f; num2 += 1f)
240			{
241				UICharacter uICharacter = new UICharacter(_player, animated: true, hasBackPanel: false, 1.5f)
242				{
243					Width = StyleDimension.FromPixels(80f),
244					Height = StyleDimension.FromPixelsAndPercent(80f, 0f),
245					Top = StyleDimension.FromPixelsAndPercent(0f - num, 0f),
246					VAlign = 0f,
247					HAlign = 0.5f
248				};
249				uICharacter.PrepareAction = PreparePreview_Main;
250				container.Append(uICharacter);
251			}
252		}
253	
254		private void MakeHairstylesMenu(UIElement middleInnerPanel)
255		{
256			Main.Hairstyles.UpdateUnlocks();
257			UIElement uIElement = new UIElement
258			{
259				Width = StyleDimension.FromPixelsAndPercent(-10f, 1f),
260				Height = StyleDimension.FromPixelsAndPercent(0f, 1f),
261				HAlign = 0.5f,
262				VAlign = 0.5f,
263				Top = StyleDimension.FromPixels(6f)
264			};
265			middleInnerPanel.Append(uIElement);
266			uIElement.SetPadding(0f);
267			UIList uIList = new UIList
268			{
269				Width = StyleDimension.FromPixelsAndPercent(-18f, 1f),
270				Height = StyleDimension.FromPixelsAndPercent(-6f, 1f)
271			};
272			uIList.SetPadding(4f);
273			uIElement.Append(uIList);
274			UIScrollbar uIScrollbar = new UIScrollbar
275			{
276				HAlign = 1f,
277				Height = StyleDimension.FromPixelsAndPercent(-30f, 1f),
278				Top = StyleDimension.FromPixels(10f)
279			};
280			uIScrollbar.SetView(100f, 1000f);
281			uIList.SetScrollbar(uIScrollbar);
282			uIElement.Append(uIScrollbar);
283			int count = Main.Hairstyles.AvailableHairstyles.Count;
284			UIElement uIElement2 = new UIElement
285			{
286				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
287				Height = StyleDimension.FromPixelsAndPercent(48 * (count / 10 + ((count % 10 != 0) ? 1 : 0)), 0f)
288			};
289			uIList.Add(uIElement2);
290			uIElement2.SetPadding(0f);
291			for (int i = 0; i < count; i++)
292			{
293				UIHairStyleButton uIHairStyleButton = new UIHairStyleButton(_player, Main.Hairstyles.AvailableHairstyles[i])
294				{
295					Left = StyleDimension.FromPixels((float)(i % 10) * 46f + 6f),
296					Top = StyleDimension.FromPixels((float)(i / 10) * 48f + 1f)
297				};
298				uIHairStyleButton.SetSnapPoint("Middle", i);
299				uIHairStyleButton.SkipRenderingContent(i);
300				uIHairStyleButton.OnLeftMouseDown += RecordThatHairWasSelected;
301				uIElement2.Append(uIHairStyleButton);
302			}
303			_hairstylesContainer = uIElement;
304		}
305	
306		private void RecordThatHairWasSelected(UIMouseEvent evt, UIElement listeningElement)
307		{
308			_lastSelectedHairstyle = _player.hair;
309		}
310	
311		private void MakeClothStylesMenu(UIElement middleInnerPanel)
312		{
313			UIElement uIElement = new UIElement
314			{
315				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
316				Height = StyleDimension.FromPixelsAndPercent(0f, 1f),
317				HAlign = 0.5f,
318				VAlign = 0.5f
319			};
320			middleInnerPanel.Append(uIElement);
321			uIElement.SetPadding(0f);
322			int num = 0;
323			for (int i = 0; i < _validClothStyles.Length; i++)
324			{
325				int num2 = 19;
326				num2 = ((i < _validClothStyles.Length / 2) ? (num2 - 8) : (num2 + 10));
327				UIClothStyleButton uIClothStyleButton = new UIClothStyleButton(_player, _validClothStyles[i], PreparePreview_ClothStyle)
328				{
329					Left = StyleDimension.FromPixels((float)i * 46f + (float)num2),
330					Top = StyleDimension.FromPixels(num)
331				};
332				uIClothStyleButton.OnLeftMouseDown += Click_CharClothStyle;
333				uIClothStyleButton.SetSnapPoint("Middle", i);
334				uIElement.Append(uIClothStyleButton);
335			}
336			int num3 = 15;
337			int num4 = 60;
338			UIElement uIElement2 = new UIElement
339			{
340				Width = StyleDimension.FromPixels(170f),
341				Height = StyleDimension.FromPixels(50f),
342				HAlign = 0f,
343				Left = new StyleDimension((float)num4 - 34f, 0.5f),
344				VAlign = 1f,
345				Top = StyleDimension.FromPixels(-num3 - 7)
346			};
347			uIElement.Append(uIElement2);
348			UIColoredImageButton uIColoredImageButton = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/Item_" + (short)271, (AssetRequestMode)1), isSmall: true)
349			{
350				VAlign = 0.5f,
351				HAlign = 0f,
352				Left = StyleDimension.FromPixelsAndPercent(0f, 0f)
353			};
354			uIColoredImageButton.SetColor(_player.hairColor);
355			uIColoredImageButton.OnLeftMouseDown += EquipArmorNone;
356			uIElement2.Append(uIColoredImageButton);
357			UIColoredImageButton uIColoredImageButton2 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/Item_" + (short)5660, (AssetRequestMode)1), isSmall: true)
358			{
359				VAlign = 0.5f,
360				HAlign = 0.5f
361			};
362			uIColoredImageButton2.OnLeftMouseDown += EquipArmorHallowed;
363			uIElement2.Append(uIColoredImageButton2);
364			UIColoredImageButton uIColoredImageButton3 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/Item_" + (short)91, (AssetRequestMode)1), isSmall: true)
365			{
366				VAlign = 0.5f,
367				HAlign = 0.25f
368			};
369			uIColoredImageButton3.OnLeftMouseDown += EquipArmorSilver;
370			uIElement2.Append(uIColoredImageButton3);
371			UIColoredImageButton uIColoredImageButton4 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/Item_" + (short)239, (AssetRequestMode)1), isSmall: true)
372			{
373				VAlign = 0.5f,
374				HAlign = 0.75f
375			};
376			uIColoredImageButton4.OnLeftMouseDown += EquipArmorFormal;
377			uIElement2.Append(uIColoredImageButton4);
378			UIColoredImageButton uIColoredImageButton5 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/Item_" + (short)237, (AssetRequestMode)1), isSmall: true)
379			{
380				VAlign = 0.5f,
381				HAlign = 1f
382			};
383			uIColoredImageButton5.OnLeftMouseDown += EquipArmorSwimming;
384			uIElement2.Append(uIColoredImageButton5);
385			_previewArmorButton = new UIElement[5];
386			_previewArmorButton[0] = uIColoredImageButton;
387			_previewArmorButton[1] = uIColoredImageButton2;
388			_previewArmorButton[2] = uIColoredImageButton3;
389			_previewArmorButton[3] = uIColoredImageButton4;
390			_previewArmorButton[4] = uIColoredImageButton5;
391			_previewArmorButton[0].SetSnapPoint("Preview", 0);
392			_previewArmorButton[2].SetSnapPoint("Preview", 1);
393			_previewArmorButton[1].SetSnapPoint("Preview", 2);
394			_previewArmorButton[3].SetSnapPoint("Preview", 3);
395			_previewArmorButton[4].SetSnapPoint("Preview", 4);
396			UIElement uIElement3 = new UIElement
397			{
398				Width = StyleDimension.FromPixels(100f),
399				Height = StyleDimension.FromPixels(50f),
400				HAlign = 0f,
401				Left = new StyleDimension(num4, 0.5f),
402				VAlign = 1f,
403				Top = StyleDimension.FromPixels(-num3 + 38 - 9)
404			};
405			uIElement.Append(uIElement3);
406			UIColoredImageButton uIColoredImageButton6 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Copy", (AssetRequestMode)1), isSmall: true)
407			{
408				VAlign = 0.5f,
409				HAlign = 0f,
410				Left = StyleDimension.FromPixelsAndPercent(0f, 0f)
411			};
412			uIColoredImageButton6.OnLeftMouseDown += Click_CopyPlayerTemplate;
413			uIElement3.Append(uIColoredImageButton6);
414			_copyTemplateButton = uIColoredImageButton6;
415			UIColoredImageButton uIColoredImageButton7 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Paste", (AssetRequestMode)1), isSmall: true)
416			{
417				VAlign = 0.5f,
418				HAlign = 0.5f
419			};
420			uIColoredImageButton7.OnLeftMouseDown += Click_PastePlayerTemplate;
421			uIElement3.Append(uIColoredImageButton7);
422			_pasteTemplateButton = uIColoredImageButton7;
423			UIColoredImageButton uIColoredImageButton8 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Randomize", (AssetRequestMode)1), isSmall: true)
424			{
425				VAlign = 0.5f,
426				HAlign = 1f
427			};
428			uIColoredImageButton8.OnLeftMouseDown += Click_RandomizePlayer;
429			uIElement3.Append(uIColoredImageButton8);
430			_randomizePlayerButton = uIColoredImageButton8;
431			UIElement uIElement4 = new UIElement
432			{
433				Width = StyleDimension.FromPixels(90f),
434				Height = StyleDimension.FromPixels(50f),
435				HAlign = 1f,
436				Left = new StyleDimension(-num4, -0.5f),
437				VAlign = 1f,
438				Top = StyleDimension.FromPixels(-num3)
439			};
440			uIElement.Append(uIElement4);
441			UIHorizontalSeparator element = new UIHorizontalSeparator
442			{
443				Width = StyleDimension.FromPixelsAndPercent(-38f, 1f),
444				HAlign = 0.5f,
445				VAlign = 1f,
446				Top = StyleDimension.FromPixelsAndPercent(-52 - num3, 0f),
447				Left = new StyleDimension(-3f, 0f),
448				Color = Color.Lerp(Color.White, new Color(63, 65, 151, 255), 0.85f) * 0.9f
449			};
450			uIElement.Append(element);
451			Asset<Texture2D> obj = Main.Assets.Request<Texture2D>("Images/UI/TexturePackButtons", (AssetRequestMode)1);
452			Asset<Texture2D> val = Main.Assets.Request<Texture2D>("Images/UI/TexturePackButtonsOutline", (AssetRequestMode)1);
453			UIImageButton uIImageButton = new UIImageButton(obj, obj.Frame(2, 2, 0, 1))
454			{
455				VAlign = 0.5f,
456				HAlign = 0f,
457				Left = StyleDimension.FromPixelsAndPercent(0f, 0f),
458				BorderColor = Main.OurFavoriteColor
459			};
460			uIImageButton.SetVisibility(1f, 1f);
461			uIImageButton.SetHoverImage(val, val.Frame(2, 2, 0, 1));
462			uIImageButton.OnLeftMouseDown += Click_VoiceCycleBack;
463			uIElement4.Append(uIImageButton);
464			UIImageButton uIImageButton2 = new UIImageButton(obj, obj.Frame(2, 2, 1, 1))
465			{
466				VAlign = 0.5f,
467				HAlign = 1f,
468				Left = StyleDimension.FromPixelsAndPercent(0f, 0f),
469				BorderColor = Main.OurFavoriteColor
470			};
471			uIImageButton2.SetVisibility(1f, 1f);
472			uIImageButton2.SetHoverImage(val, val.Frame(2, 2, 1, 1));
473			uIImageButton2.OnLeftMouseDown += Click_VoiceCycleForward;
474			uIElement4.Append(uIImageButton2);
475			UIColoredImageButton uIColoredImageButton9 = new UIColoredImageButton(null)
476			{
477				VAlign = 0.5f,
478				HAlign = 0.5f,
479				Left = StyleDimension.FromPixelsAndPercent(0f, 0f),
480				Width = StyleDimension.FromPixels(52f),
481				Height = StyleDimension.FromPixels(52f)
482			};
483			UIImage uIImage = new UIImage(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Voice", (AssetRequestMode)1))
484			{
485				VAlign = 0.5f,
486				HAlign = 0.5f,
487				IgnoresMouseInteraction = true,
488				Color = Main.OurFavoriteColor
489			};
490			uIImage.OnUpdate += voiceIcon_OnUpdate;
491			uIColoredImageButton9.Append(uIImage);
492			UIText uIText = new UIText("", 0.85f)
493			{
494				VAlign = 1f,
495				HAlign = 1f,
496				TextOriginX = 0.5f,
497				TextOriginY = 1f,
498				Top = StyleDimension.FromPixels(-6f),
499				Left = StyleDimension.FromPixels(-12f),
500				ShadowColor = Color.Black * 0.3f
501			};
502			uIText.OnUpdate += voiceNumber_OnUpdate;
503			uIColoredImageButton9.Append(uIText);
504			uIColoredImageButton9.OnLeftMouseDown += Click_VoicePlay;
505			uIElement4.Append(uIColoredImageButton9);
506			UIColoredSlider uIColoredSlider = new UIColoredSlider(LocalizedText.Empty, GetPitchSlider, SetPitchSlider_Keyboard, SetPitchSlider_GamePad, GetVoicePitchColorAt, Color.Transparent)
507			{
508				VAlign = 1f,
509				HAlign = 0.5f,
510				Width = StyleDimension.FromPixelsAndPercent(187f, 0f),
511				Top = StyleDimension.FromPixels(-10f),
512				Left = StyleDimension.FromPixels(55f)
513			};
514			uIColoredSlider.OnLeftMouseDown += Click_VoicePitch;
515			uIColoredSlider.OnUpdate += PitchSliderUpdate;
516			uIColoredSlider.SetSnapPoint("pitch", 0, null, new Vector2(-93f, 16f));
517			uIElement4.Append(uIColoredSlider);
518			_pitchSlider = uIColoredSlider;
519			uIImageButton.SetSnapPoint("Low", 1);
520			uIColoredImageButton9.SetSnapPoint("Low", 2);
521			uIImageButton2.SetSnapPoint("Low", 3);
522			_voicePrevious = uIImageButton;
523			_voiceNext = uIImageButton2;
524			_voicePlay = uIColoredImageButton9;
525			uIColoredImageButton6.SetSnapPoint("Low", 4);
526			uIColoredImageButton7.SetSnapPoint("Low", 5);
527			uIColoredImageButton8.SetSnapPoint("Low", 6);
528			_clothStylesContainer = uIElement;
529		}
530	
531		private void EquipArmorNone(UIMouseEvent evt, UIElement listeningElement)
532		{
533			SoundEngine.PlaySound(12);
534			_femaleArmor = (_maleArmor = default(ArmorAssignments));
535		}
536	
537		private void EquipArmorGold(UIMouseEvent evt, UIElement listeningElement)
538		{
539			SoundEngine.PlaySound(12);
540			_femaleArmor = (_maleArmor = new ArmorAssignments
541			{
542				HeadItem = 92,
543				BodyItem = 83,
544				LegItem = 79
545			});
546		}
547	
548		private void EquipArmorSilver(UIMouseEvent evt, UIElement listeningElement)
549		{
550			SoundEngine.PlaySound(12);
551			_femaleArmor = (_maleArmor = new ArmorAssignments
552			{
553				HeadItem = 91,
554				BodyItem = 82,
555				LegItem = 78
556			});
557		}
558	
559		private void EquipArmorFuneral(UIMouseEvent evt, UIElement listeningElement)
560		{
561			SoundEngine.PlaySound(12);
562			_femaleArmor = (_maleArmor = new ArmorAssignments
563			{
564				HeadItem = 4704,
565				BodyItem = 4705,
566				LegItem = 4706
567			});
568		}
569	
570		private void EquipArmorHallowed(UIMouseEvent evt, UIElement listeningElement)
571		{
572			SoundEngine.PlaySound(12);
573			_femaleArmor = (_maleArmor = new ArmorAssignments
574			{
575				HeadItem = 5660,
576				BodyItem = 551,
577				LegItem = 552
578			});
579		}
580	
581		private void EquipArmorFormal(UIMouseEvent evt, UIElement listeningElement)
582		{
583			SoundEngine.PlaySound(12);
584			_maleArmor = new ArmorAssignments
585			{
586				HeadItem = 239,
587				BodyItem = 240,
588				LegItem = 241
589			};
590			_femaleArmor = new ArmorAssignments
591			{
592				HeadItem = 3478,
593				BodyItem = 3479,
594				LegItem = 0
595			};
596		}
597	
598		private void EquipArmorSwimming(UIMouseEvent evt, UIElement listeningElement)
599		{
600			SoundEngine.PlaySound(12);
601			_maleArmor = new ArmorAssignments
602			{
603				HeadItem = 237,
604				BodyItem = 3785,
605				LegItem = 5649
606			};
607			_femaleArmor = new ArmorAssignments
608			{
609				HeadItem = 237,
610				BodyItem = 5646,
611				LegItem = 5647,
612				Accessory1Item = 208
613			};
614		}
615	
616		private void PreparePreview_Main()
617		{
618			_player.direction = 1;
619			TryAutoAssigningHair();
620			UpdatePreviewItems();
621		}
622	
623		private void PreparePreview_ClothStyle()
624		{
625			_player.direction = (_player.Male ? 1 : (-1));
626			TryAutoAssigningHair();
627			UpdatePreviewItems();
628		}
629	
630		private void TryAutoAssigningHair()
631		{
632			if (!_lastSelectedHairstyle.HasValue && _defaultHairstylesForClothStyle.TryGetValue(_player.skinVariant, out var value))
633			{
634				_player.hair = value;
635			}
636		}
637	
638		private void UpdatePreviewItems()
639		{
640			ArmorAssignments armorAssignments = _femaleArmor;
641			if (_player.Male)
642			{
643				armorAssignments = _maleArmor;
644			}
645			_player.armor[0].SetDefaults(armorAssignments.HeadItem);
646			_player.armor[1].SetDefaults(armorAssignments.BodyItem);
647			_player.armor[2].SetDefaults(armorAssignments.LegItem);
648		}
649	
650		private void PitchSliderUpdate(UIElement affectedElement)
651		{
652			if (_pitchChanged && --_pitchChangedCooldown <= 0)
653			{
654				_pitchChanged = false;
655				PlayVoicePreview();
656			}
657		}
658	
659		private void PitchChanged()
660		{
661			_pitchChanged = true;
662			_pitchChangedCooldown = 3;
663		}
664	
665		private void SetPitchSlider_GamePad()
666		{
667			if (PlayerInput.UsingGamepad)
668			{
669				float pitchAmount = _pitchAmount;
670				float num = UILinksInitializer.HandleSliderHorizontalInput(Utils.Remap(_pitchAmount, -1f, 1f, 0f, 1f), 0f, 1f, PlayerInput.CurrentProfile.InterfaceDeadzoneX, 0.35f);
671				_pitchAmount = Utils.Remap(num, 0f, 1f, -1f, 1f);
672				num = RemapPitchSliderKnob(num);
673				_player.voicePitchOffset = Utils.Remap(num, 0f, 1f, -1f, 1f);
674				if (pitchAmount != _pitchAmount)
675				{
676					PitchChanged();
677				}
678			}
679		}
680	
681		private float RemapPitchSliderKnob(float pitchSliderValue)
682		{
683			int num = 20;
684			return (float)Math.Round(pitchSliderValue * (float)num) / (float)num;
685		}
686	
687		private void SetPitchSlider_Keyboard(float amount)
688		{
689			amount = RemapPitchSliderKnob(amount);
690			float voicePitchOffset = _player.voicePitchOffset;
691			_pitchAmount = (_player.voicePitchOffset = Utils.Remap(amount, 0f, 1f, -1f, 1f));
692			_pitchChangedCooldown = 3;
693			if (voicePitchOffset != _player.voicePitchOffset)
694			{
695				PitchChanged();
696			}
697		}
698	
699		private float GetPitchSlider()
700		{
701			return Utils.Remap(RemapPitchSliderKnob(_pitchAmount), -1f, 1f, 0f, 1f);
702		}
703	
704		private Color GetVoicePitchColorAt(float x)
705		{
706			float fromValue = (x * 4f + 0.5f) % 1f;
707			float num = Utils.Remap(fromValue, 0f, 0.5f, 0f, 1f) * Utils.Remap(fromValue, 0.5f, 1f, 1f, 0f);
708			float amount = num * num * num * num * num;
709			return Color.Lerp(new Color(90, 90, 120), Color.White, amount);
710		}
711	
712		private void voiceNumber_OnUpdate(UIElement affectedElement)
713		{
714			int num = 0;
715			int[] variantOrder = PlayerVoiceID.VariantOrder;
716			for (int i = 0; i < variantOrder.Length; i++)
717			{
718				if (variantOrder[i] == _player.voiceVariant)
719				{
720					num = i;
721					break;
722				}
723			}
724			(affectedElement as UIText).SetText((num + 1).ToString());
725		}
726	
727		private void voiceIcon_OnUpdate(UIElement affectedElement)
728		{
729			(affectedElement as UIImage).Color = PlayerVoiceID.Sets.Colors[_player.voiceVariant];
730		}
731	
732		private void MakeCategoriesBar(UIElement categoryContainer)
733		{
734			float xPositionStart = -240f;
735			float xPositionPerId = 48f;
736			_colorPickers = new UIColoredImageButton[10];
737			categoryContainer.Append(CreateColorPicker(CategoryId.HairColor, "Images/UI/CharCreation/ColorHair", xPositionStart, xPositionPerId));
738			categoryContainer.Append(CreateColorPicker(CategoryId.Eye, "Images/UI/CharCreation/ColorEye", xPositionStart, xPositionPerId));
739			categoryContainer.Append(CreateColorPicker(CategoryId.Skin, "Images/UI/CharCreation/ColorSkin", xPositionStart, xPositionPerId));
740			categoryContainer.Append(CreateColorPicker(CategoryId.Shirt, "Images/UI/CharCreation/ColorShirt", xPositionStart, xPositionPerId));
741			categoryContainer.Append(CreateColorPicker(CategoryId.Undershirt, "Images/UI/CharCreation/ColorUndershirt", xPositionStart, xPositionPerId));
742			categoryContainer.Append(CreateColorPicker(CategoryId.Pants, "Images/UI/CharCreation/ColorPants", xPositionStart, xPositionPerId));
743			categoryContainer.Append(CreateColorPicker(CategoryId.Shoes, "Images/UI/CharCreation/ColorShoes", xPositionStart, xPositionPerId));
744			_colorPickers[4].SetMiddleTexture(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/ColorEyeBack", (AssetRequestMode)1));
745			_clothingStylesCategoryButton = CreatePickerWithoutClick(CategoryId.Clothing, "Images/UI/CharCreation/ClothStyleMale", xPositionStart, xPositionPerId);
746			_clothingStylesCategoryButton.OnLeftMouseDown += Click_ClothStyles;
747			_clothingStylesCategoryButton.SetSnapPoint("Top", 1);
748			categoryContainer.Append(_clothingStylesCategoryButton);
749			Asset<Texture2D> val = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/ColorCharacter", (AssetRequestMode)1);
750			_clothingStylesCategoryButton.SetColor(Color.Transparent);
751			for (int i = 0; i < _characterPreviewLayers.Length; i++)
752			{
753				UIImageFramed uIImageFramed = new UIImageFramed(val, val.Frame(1, 7, 0, i))
754				{
755					HAlign = 0.5f,
756					VAlign = 0.5f
757				};
758				_characterPreviewLayers[i] = uIImageFramed;
759				_clothingStylesCategoryButton.Append(uIImageFramed);
760				_clothingStylesCategoryButton.OnUpdate += _clothingStylesCategoryButton_OnUpdate;
761			}
762			_hairStylesCategoryButton = CreatePickerWithoutClick(CategoryId.HairStyle, "Images/UI/CharCreation/HairStyle_Hair", xPositionStart, xPositionPerId);
763			_hairStylesCategoryButton.OnLeftMouseDown += Click_HairStyles;
764			_hairStylesCategoryButton.SetMiddleTexture(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/HairStyle_Arrow", (AssetRequestMode)1));
765			_hairStylesCategoryButton.SetSnapPoint("Top", 2);
766			categoryContainer.Append(_hairStylesCategoryButton);
767			_charInfoCategoryButton = CreatePickerWithoutClick(CategoryId.CharInfo, "Images/UI/CharCreation/CharInfo", xPositionStart, xPositionPerId);
768			_charInfoCategoryButton.OnLeftMouseDown += Click_CharInfo;
769			_charInfoCategoryButton.SetSnapPoint("Top", 0);
770			categoryContainer.Append(_charInfoCategoryButton);
771			UpdateColorPickers();
772			UIHorizontalSeparator element = new UIHorizontalSeparator
773			{
774				Width = StyleDimension.FromPixelsAndPercent(-25f, 1f),
775				Top = StyleDimension.FromPixels(6f),
776				Left = new StyleDimension(-2.5f, 0f),
777				VAlign = 1f,
778				HAlign = 0.5f,
779				Color = Color.Lerp(Color.White, new Color(63, 65, 151, 255), 0.85f) * 0.9f
780			};
781			categoryContainer.Append(element);
782			int num = 21;
783			UIText uIText = new UIText(PlayerInput.GenerateInputTag_ForCurrentGamemode(tagForGameplay: false, "HotbarMinus"))
784			{
785				Left = new StyleDimension(-num, 0f),
786				VAlign = 0.5f,
787				Top = new StyleDimension(-4f, 0f)
788			};
789			categoryContainer.Append(uIText);
790			UIText uIText2 = new UIText(PlayerInput.GenerateInputTag_ForCurrentGamemode(tagForGameplay: false, "HotbarMinus"))
791			{
792				HAlign = 1f,
793				Left = new StyleDimension(12 + num, 0f),
794				VAlign = 0.5f,
795				Top = new StyleDimension(-4f, 0f)
796			};
797			categoryContainer.Append(uIText2);
798			_helpGlyphLeft = uIText;
799			_helpGlyphRight = uIText2;
800			categoryContainer.OnUpdate += UpdateHelpGlyphs;
801		}
802	
803		private void _clothingStylesCategoryButton_OnUpdate(UIElement affectedElement)
804		{
805			_characterPreviewLayers[0].Color = _player.hairColor;
806			_characterPreviewLayers[1].Color = _player.eyeColor;
807			_characterPreviewLayers[2].Color = _player.skinColor;
808			_characterPreviewLayers[3].Color = _player.shirtColor;
809			_characterPreviewLayers[4].Color = _player.underShirtColor;
810			_characterPreviewLayers[5].Color = _player.pantsColor;
811			_characterPreviewLayers[6].Color = _player.shoeColor;
812		}
813	
814		private void UpdateHelpGlyphs(UIElement element)
815		{
816			string text = "";
817			string text2 = "";
818			if (PlayerInput.UsingGamepad)
819			{
820				text = PlayerInput.GenerateInputTag_ForCurrentGamemode(tagForGameplay: false, "HotbarMinus");
821				text2 = PlayerInput.GenerateInputTag_ForCurrentGamemode(tagForGameplay: false, "HotbarPlus");
822			}
823			_helpGlyphLeft.SetText(text);
824			_helpGlyphRight.SetText(text2);
825		}
826	
827		private UIColoredImageButton CreateColorPicker(CategoryId id, string texturePath, float xPositionStart, float xPositionPerId)
828		{
829			UIColoredImageButton uIColoredImageButton = new UIColoredImageButton(Main.Assets.Request<Texture2D>(texturePath, (AssetRequestMode)1));
830			_colorPickers[(int)id] = uIColoredImageButton;
831			uIColoredImageButton.VAlign = 0f;
832			uIColoredImageButton.HAlign = 0f;
833			uIColoredImageButton.Left.Set(xPositionStart + (float)id * xPositionPerId, 0.5f);
834			uIColoredImageButton.OnLeftMouseDown += Click_ColorPicker;
835			uIColoredImageButton.SetSnapPoint("Top", (int)id);
836			return uIColoredImageButton;
837		}
838	
839		private UIColoredImageButton CreatePickerWithoutClick(CategoryId id, string texturePath, float xPositionStart, float xPositionPerId)
840		{
841			UIColoredImageButton uIColoredImageButton = new UIColoredImageButton(Main.Assets.Request<Texture2D>(texturePath, (AssetRequestMode)1));
842			uIColoredImageButton.VAlign = 0f;
843			uIColoredImageButton.HAlign = 0f;
844			uIColoredImageButton.Left.Set(xPositionStart + (float)id * xPositionPerId, 0.5f);
845			return uIColoredImageButton;
846		}
847	
848		private void MakeInfoMenu(UIElement parentContainer)
849		{
850			UIElement uIElement = new UIElement
851			{
852				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
853				Height = StyleDimension.FromPixelsAndPercent(0f, 1f),
854				HAlign = 0.5f,
855				VAlign = 0f
856			};
857			uIElement.SetPadding(10f);
858			uIElement.PaddingBottom = 0f;
859			uIElement.PaddingTop = 0f;
860			parentContainer.Append(uIElement);
861			UICharacterNameButton uICharacterNameButton = new UICharacterNameButton(Language.GetText("UI.WorldCreationName"), Language.GetText("UI.PlayerEmptyName"));
862			uICharacterNameButton.Width = StyleDimension.FromPixelsAndPercent(0f, 1f);
863			uICharacterNameButton.HAlign = 0.5f;
864			uIElement.Append(uICharacterNameButton);
865			_charName = uICharacterNameButton;
866			uICharacterNameButton.OnLeftMouseDown += Click_Naming;
867			uICharacterNameButton.SetSnapPoint("Middle", 0);
868			float num = 4f;
869			float num2 = 0f;
870			float num3 = 0.4f;
871			UIElement uIElement2 = new UIElement
872			{
873				HAlign = 0f,
874				VAlign = 1f,
875				Width = StyleDimension.FromPixelsAndPercent(0f - num, num3),
876				Height = StyleDimension.FromPixelsAndPercent(-50f, 1f)
877			};
878			uIElement2.SetPadding(0f);
879			uIElement.Append(uIElement2);
880			UISlicedImage uISlicedImage = new UISlicedImage(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode)1))
881			{
882				HAlign = 1f,
883				VAlign = 1f,
884				Width = StyleDimension.FromPixelsAndPercent((0f - num) * 2f, 1f - num3),
885				Left = StyleDimension.FromPixels(0f - num),
886				Height = StyleDimension.FromPixelsAndPercent(uIElement2.Height.Pixels, uIElement2.Height.Precent)
887			};
888			uISlicedImage.SetSliceDepths(10);
889			uISlicedImage.Color = Color.LightGray * 0.7f;
890			uIElement.Append(uISlicedImage);
891			float num4 = 4f;
892			UIDifficultyButton uIDifficultyButton = new UIDifficultyButton(_player, Lang.menu[26], Lang.menu[31], 0, Color.Cyan)
893			{
894				HAlign = 0f,
895				VAlign = 1f / (num4 - 1f),
896				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
897				Height = StyleDimension.FromPixelsAndPercent(0f - num2, 1f / num4)
898			};
899			UIDifficultyButton uIDifficultyButton2 = new UIDifficultyButton(_player, Lang.menu[25], Lang.menu[30], 1, Main.mcColor)
900			{
901				HAlign = 0f,
902				VAlign = 2f / (num4 - 1f),
903				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
904				Height = StyleDimension.FromPixelsAndPercent(0f - num2, 1f / num4)
905			};
906			UIDifficultyButton uIDifficultyButton3 = new UIDifficultyButton(_player, Lang.menu[24], Lang.menu[29], 2, Main.hcColor)
907			{
908				HAlign = 0f,
909				VAlign = 1f,
910				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
911				Height = StyleDimension.FromPixelsAndPercent(0f - num2, 1f / num4)
912			};
913			UIDifficultyButton uIDifficultyButton4 = new UIDifficultyButton(_player, Language.GetText("UI.Creative"), Language.GetText("UI.CreativeDescriptionPlayer"), 3, Main.creativeModeColor)
914			{
915				HAlign = 0f,
916				VAlign = 0f,
917				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
918				Height = StyleDimension.FromPixelsAndPercent(0f - num2, 1f / num4)
919			};
920			UIText uIText = new UIText(Lang.menu[26])
921			{
922				HAlign = 0f,
923				VAlign = 0.5f,
924				Width = StyleDimension.FromPixelsAndPercent(0f, 1f),
925				Height = StyleDimension.FromPixelsAndPercent(0f, 1f),
926				Top = StyleDimension.FromPixelsAndPercent(15f, 0f),
927				IsWrapped = true
928			};
929			uIText.PaddingLeft = 20f;
930			uIText.PaddingRight = 20f;
931			uISlicedImage.Append(uIText);
932			uIElement2.Append(uIDifficultyButton4);
933			uIElement2.Append(uIDifficultyButton);
934			uIElement2.Append(uIDifficultyButton2);
935			uIElement2.Append(uIDifficultyButton3);
936			_infoContainer = uIElement;
937			_difficultyDescriptionText = uIText;
938			uIDifficultyButton4.OnLeftMouseDown += UpdateDifficultyDescription;
939			uIDifficultyButton.OnLeftMouseDown += UpdateDifficultyDescription;
940			uIDifficultyButton2.OnLeftMouseDown += UpdateDifficultyDescription;
941			uIDifficultyButton3.OnLeftMouseDown += UpdateDifficultyDescription;
942			UpdateDifficultyDescription(null, null);
943			uIDifficultyButton4.SetSnapPoint("Middle", 1);
944			uIDifficultyButton.SetSnapPoint("Middle", 2);
945			uIDifficultyButton2.SetSnapPoint("Middle", 3);
946			uIDifficultyButton3.SetSnapPoint("Middle", 4);
947		}
948	
949		private void UpdateDifficultyDescription(UIMouseEvent evt, UIElement listeningElement)
950		{
951			LocalizedText text = Lang.menu[31];
952			switch (_player.difficulty)
953			{
954			case 0:
955				text = Lang.menu[31];
956				break;
957			case 1:
958				text = Lang.menu[30];
959				break;
960			case 2:
961				text = Lang.menu[29];
962				break;
963			case 3:
964				text = Language.GetText("UI.CreativeDescriptionPlayer");
965				break;
966			}
967			_difficultyDescriptionText.SetText(text);
968		}
969	
970		private void MakeHSLMenu(UIElement parentContainer)
971		{
972			UIElement uIElement = new UIElement
973			{
974				Width = StyleDimension.FromPixelsAndPercent(220f, 0f),
975				Height = StyleDimension.FromPixelsAndPercent(158f, 0f),
976				HAlign = 0.5f,
977				VAlign = 0f
978			};
979			uIElement.SetPadding(0f);
980			parentContainer.Append(uIElement);
981			UIElement uIElement2 = new UIPanel
982			{
983				Width = StyleDimension.FromPixelsAndPercent(220f, 0f),
984				Height = StyleDimension.FromPixelsAndPercent(104f, 0f),
985				HAlign = 0.5f,
986				VAlign = 0f,
987				Top = StyleDimension.FromPixelsAndPercent(10f, 0f)
988			};
989			uIElement2.SetPadding(0f);
990			uIElement2.PaddingTop = 3f;
991			uIElement.Append(uIElement2);
992			uIElement2.Append(CreateHSLSlider(HSLSliderId.Hue));
993			uIElement2.Append(CreateHSLSlider(HSLSliderId.Saturation));
994			uIElement2.Append(CreateHSLSlider(HSLSliderId.Luminance));
995			UIPanel uIPanel = new UIPanel
996			{
997				VAlign = 1f,
998				HAlign = 1f,
999				Width = StyleDimension.FromPixelsAndPercent(100f, 0f),
1000				Height = StyleDimension.FromPixelsAndPercent(32f, 0f)
1001			};
1002			UIText uIText = new UIText("FFFFFF")
1003			{
1004				VAlign = 0.5f,
1005				HAlign = 0.5f
1006			};
1007			uIPanel.Append(uIText);
1008			uIElement.Append(uIPanel);
1009			UIColoredImageButton uIColoredImageButton = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Copy", (AssetRequestMode)1), isSmall: true)
1010			{
1011				VAlign = 1f,
1012				HAlign = 0f,
1013				Left = StyleDimension.FromPixelsAndPercent(0f, 0f)
1014			};
1015			uIColoredImageButton.OnLeftMouseDown += Click_CopyHex;
1016			uIElement.Append(uIColoredImageButton);
1017			_copyHexButton = uIColoredImageButton;
1018			UIColoredImageButton uIColoredImageButton2 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Paste", (AssetRequestMode)1), isSmall: true)
1019			{
1020				VAlign = 1f,
1021				HAlign = 0f,
1022				Left = StyleDimension.FromPixelsAndPercent(40f, 0f)
1023			};
1024			uIColoredImageButton2.OnLeftMouseDown += Click_PasteHex;
1025			uIElement.Append(uIColoredImageButton2);
1026			_pasteHexButton = uIColoredImageButton2;
1027			UIColoredImageButton uIColoredImageButton3 = new UIColoredImageButton(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/Randomize", (AssetRequestMode)1), isSmall: true)
1028			{
1029				VAlign = 1f,
1030				HAlign = 0f,
1031				Left = StyleDimension.FromPixelsAndPercent(80f, 0f)
1032			};
1033			uIColoredImageButton3.OnLeftMouseDown += Click_RandomizeSingleColor;
1034			uIElement.Append(uIColoredImageButton3);
1035			_randomColorButton = uIColoredImageButton3;
1036			_hslContainer = uIElement;
1037			_hslHexText = uIText;
1038			uIColoredImageButton.SetSnapPoint("Low", 0);
1039			uIColoredImageButton2.SetSnapPoint("Low", 1);
1040			uIColoredImageButton3.SetSnapPoint("Low", 2);
1041		}
1042	
1043		private void Click_VoicePitch(UIMouseEvent evt, UIElement listeningElement)
1044		{
1045			SoundEngine.PlaySound(12);
1046		}
1047	
1048		private UIColoredSlider CreateHSLSlider(HSLSliderId id)
1049		{
1050			UIColoredSlider uIColoredSlider = CreateHSLSliderButtonBase(id);
1051			uIColoredSlider.VAlign = 0f;
1052			uIColoredSlider.HAlign = 0f;
1053			uIColoredSlider.Width = StyleDimension.FromPixelsAndPercent(-10f, 1f);
1054			uIColoredSlider.Top.Set(30 * (int)id, 0f);
1055			uIColoredSlider.OnLeftMouseDown += Click_ColorPicker;
1056			uIColoredSlider.SetSnapPoint("Middle", (int)id, null, new Vector2(0f, 20f));
1057			return uIColoredSlider;
1058		}
1059	
1060		private UIColoredSlider CreateHSLSliderButtonBase(HSLSliderId id)
1061		{
1062			return id switch
1063			{
1064				HSLSliderId.Saturation => new UIColoredSlider(LocalizedText.Empty, () => GetHSLSliderPosition(HSLSliderId.Saturation), delegate(float x)
1065				{
1066					UpdateHSLValue(HSLSliderId.Saturation, x);
1067				}, UpdateHSL_S, (float x) => GetHSLSliderColorAt(HSLSliderId.Saturation, x), Color.Transparent), 
1068				HSLSliderId.Luminance => new UIColoredSlider(LocalizedText.Empty, () => GetHSLSliderPosition(HSLSliderId.Luminance), delegate(float x)
1069				{
1070					UpdateHSLValue(HSLSliderId.Luminance, x);
1071				}, UpdateHSL_L, (float x) => GetHSLSliderColorAt(HSLSliderId.Luminance, x), Color.Transparent), 
1072				_ => new UIColoredSlider(LocalizedText.Empty, () => GetHSLSliderPosition(HSLSliderId.Hue), delegate(float x)
1073				{
1074					UpdateHSLValue(HSLSliderId.Hue, x);
1075				}, UpdateHSL_H, (float x) => GetHSLSliderColorAt(HSLSliderId.Hue, x), Color.Transparent), 
1076			};
1077		}
1078	
1079		private void UpdateHSL_H()
1080		{
1081			float value = UILinksInitializer.HandleSliderHorizontalInput(_currentColorHSL.X, 0f, 1f, PlayerInput.CurrentProfile.InterfaceDeadzoneX, 0.35f);
1082			UpdateHSLValue(HSLSliderId.Hue, value);
1083		}
1084	
1085		private void UpdateHSL_S()
1086		{
1087			float value = UILinksInitializer.HandleSliderHorizontalInput(_currentColorHSL.Y, 0f, 1f, PlayerInput.CurrentProfile.InterfaceDeadzoneX, 0.35f);
1088			UpdateHSLValue(HSLSliderId.Saturation, value);
1089		}
1090	
1091		private void UpdateHSL_L()
1092		{
1093			float value = UILinksInitializer.HandleSliderHorizontalInput(_currentColorHSL.Z, 0f, 1f, PlayerInput.CurrentProfile.InterfaceDeadzoneX, 0.35f);
1094			UpdateHSLValue(HSLSliderId.Luminance, value);
1095		}
1096	
1097		private float GetHSLSliderPosition(HSLSliderId id)
1098		{
1099			return id switch
1100			{
1101				HSLSliderId.Hue => _currentColorHSL.X, 
1102				HSLSliderId.Saturation => _currentColorHSL.Y, 
1103				HSLSliderId.Luminance => _currentColorHSL.Z, 
1104				_ => 1f, 
1105			};
1106		}
1107	
1108		private void UpdateHSLValue(HSLSliderId id, float value)
1109		{
1110			switch (id)
1111			{
1112			case HSLSliderId.Hue:
1113				_currentColorHSL.X = value;
1114				break;
1115			case HSLSliderId.Saturation:
1116				_currentColorHSL.Y = value;
1117				break;
1118			case HSLSliderId.Luminance:
1119				_currentColorHSL.Z = value;
1120				break;
1121			}
1122			Color color = ScaledHslToRgb(_currentColorHSL.X, _currentColorHSL.Y, _currentColorHSL.Z);
1123			ApplyPendingColor(color);
1124			_colorPickers[(int)_selectedPicker]?.SetColor(color);
1125			if (_selectedPicker == CategoryId.HairColor)
1126			{
1127				_hairStylesCategoryButton.SetColor(color);
1128			}
1129			UpdateHexText(color);
1130		}
1131	
1132		private Color GetHSLSliderColorAt(HSLSliderId id, float pointAt)
1133		{
1134			return id switch
1135			{
1136				HSLSliderId.Hue => ScaledHslToRgb(pointAt, 1f, 0.5f), 
1137				HSLSliderId.Saturation => ScaledHslToRgb(_currentColorHSL.X, pointAt, _currentColorHSL.Z), 
1138				HSLSliderId.Luminance => ScaledHslToRgb(_currentColorHSL.X, _currentColorHSL.Y, pointAt), 
1139				_ => Color.White, 
1140			};
1141		}
1142	
1143		private void ApplyPendingColor(Color pendingColor)
1144		{
1145			switch (_selectedPicker)
1146			{
1147			case CategoryId.HairColor:
1148				_player.hairColor = pendingColor;
1149				break;
1150			case CategoryId.Eye:
1151				_player.eyeColor = pendingColor;
1152				break;
1153			case CategoryId.Skin:
1154				_player.skinColor = pendingColor;
1155				break;
1156			case CategoryId.Shirt:
1157				_player.shirtColor = pendingColor;
1158				break;
1159			case CategoryId.Undershirt:
1160				_player.underShirtColor = pendingColor;
1161				break;
1162			case CategoryId.Pants:
1163				_player.pantsColor = pendingColor;
1164				break;
1165			case CategoryId.Shoes:
1166				_player.shoeColor = pendingColor;
1167				break;
1168			}
1169		}
1170	
1171		private void UpdateHexText(Color pendingColor)
1172		{
1173			_hslHexText.SetText(GetHexText(pendingColor));
1174		}
1175	
1176		private static string GetHexText(Color pendingColor)
1177		{
1178			return "#" + pendingColor.Hex3().ToUpper();
1179		}
1180	
1181		private void MakeBackAndCreatebuttons(UIElement outerContainer)
1182		{
1183			UITextPanel<LocalizedText> uITextPanel = new UITextPanel<LocalizedText>(Language.GetText("UI.Back"), 0.7f, large: true)
1184			{
1185				Width = StyleDimension.FromPixelsAndPercent(-10f, 0.5f),
1186				Height = StyleDimension.FromPixels(50f),
1187				VAlign = 1f,
1188				HAlign = 0f,
1189				Top = StyleDimension.FromPixels(-45f)
1190			};
1191			uITextPanel.OnMouseOver += FadedMouseOver;
1192			uITextPanel.OnMouseOut += FadedMouseOut;
1193			uITextPanel.OnLeftMouseDown += Click_GoBack;
1194			uITextPanel.SetSnapPoint("Back", 0);
1195			outerContainer.Append(uITextPanel);
1196			UITextPanel<LocalizedText> uITextPanel2 = new UITextPanel<LocalizedText>(Language.GetText("UI.Create"), 0.7f, large: true)
1197			{
1198				Width = StyleDimension.FromPixelsAndPercent(-10f, 0.5f),
1199				Height = StyleDimension.FromPixels(50f),
1200				VAlign = 1f,
1201				HAlign = 1f,
1202				Top = StyleDimension.FromPixels(-45f)
1203			};
1204			uITextPanel2.OnMouseOver += FadedMouseOver;
1205			uITextPanel2.OnMouseOut += FadedMouseOut;
1206			uITextPanel2.OnLeftMouseDown += Click_NamingAndCreating;
1207			uITextPanel2.SetSnapPoint("Create", 0);
1208			outerContainer.Append(uITextPanel2);
1209		}
1210	
1211		private void Click_GoBack(UIMouseEvent evt, UIElement listeningElement)
1212		{
1213			GoBack();
1214		}
1215	
1216		private static void GoBack()
1217		{
1218			SoundEngine.PlaySound(11);
1219			if (dirty)
1220			{
1221				BackupConfirmationState = Main.MenuUI.CurrentState;
1222				Main.menuMode = 40;
1223			}
1224			else
1225			{
1226				Main.OpenCharacterSelectUI();
1227			}
1228		}
1229	
1230		private void FadedMouseOver(UIMouseEvent evt, UIElement listeningElement)
1231		{
1232			SoundEngine.PlaySound(12);
1233			((UIPanel)evt.Target).BackgroundColor = new Color(73, 94, 171);
1234			((UIPanel)evt.Target).BorderColor = Colors.FancyUIFatButtonMouseOver;
1235		}
1236	
1237		private void FadedMouseOut(UIMouseEvent evt, UIElement listeningElement)
1238		{
1239			((UIPanel)evt.Target).BackgroundColor = new Color(63, 82, 151) * 0.8f;
1240			((UIPanel)evt.Target).BorderColor = Color.Black;
1241		}
1242	
1243		private void Click_ColorPicker(UIMouseEvent evt, UIElement listeningElement)
1244		{
1245			SoundEngine.PlaySound(12);
1246			for (int i = 0; i < _colorPickers.Length; i++)
1247			{
1248				if (_colorPickers[i] == evt.Target)
1249				{
1250					SelectColorPicker((CategoryId)i);
1251					break;
1252				}
1253			}
1254		}
1255	
1256		private void Click_ClothStyles(UIMouseEvent evt, UIElement listeningElement)
1257		{
1258			SoundEngine.PlaySound(12);
1259			UnselectAllCategories();
1260			_selectedPicker = CategoryId.Clothing;
1261			_middleContainer.Append(_clothStylesContainer);
1262			_clothingStylesCategoryButton.SetSelected(selected: true);
1263		}
1264	
1265		private void Click_HairStyles(UIMouseEvent evt, UIElement listeningElement)
1266		{
1267			SoundEngine.PlaySound(12);
1268			UnselectAllCategories();
1269			_selectedPicker = CategoryId.HairStyle;
1270			_middleContainer.Append(_hairstylesContainer);
1271			_hairStylesCategoryButton.SetSelected(selected: true);
1272		}
1273	
1274		private void Click_CharInfo(UIMouseEvent evt, UIElement listeningElement)
1275		{
1276			SoundEngine.PlaySound(12);
1277			UnselectAllCategories();
1278			_selectedPicker = CategoryId.CharInfo;
1279			_middleContainer.Append(_infoContainer);
1280			_charInfoCategoryButton.SetSelected(selected: true);
1281		}
1282	
1283		private void Click_CharClothStyle(UIMouseEvent evt, UIElement listeningElement)
1284		{
1285			if (_maleArmor.HeadItem != 0 || _maleArmor.BodyItem != 0 || _maleArmor.LegItem != 0)
1286			{
1287				EquipArmorNone(evt, listeningElement);
1288				return;
1289			}
1290			if (listeningElement is UIClothStyleButton { ClothStyleId: var clothStyleId })
1291			{
1292				_player.skinVariant = clothStyleId;
1293			}
1294			SoundEngine.PlaySound(12);
1295			_clothingStylesCategoryButton.SetImageWithoutSettingSize(Main.Assets.Request<Texture2D>("Images/UI/CharCreation/" + (_player.Male ? "ClothStyleMale" : "ClothStyleFemale"), (AssetRequestMode)1));
1296			UpdateSelectedGender();
1297		}
1298	
1299		private void TryChangingVoice()
1300		{
1301			if (_player.Male && _player.voiceVariant == 2)
1302			{
1303				_player.voiceVariant = 1;
1304			}
1305			if (!_player.Male && _player.voiceVariant == 1)
1306			{
1307				_player.voiceVariant = 2;
1308			}
1309		}
1310	
1311		private void UpdateSelectedGender()
1312		{
1313			if (_oldMaleForVoiceAutoSwitch == _player.Male)
1314			{
1315				PlayVoicePreview();
1316				return;
1317			}
1318			switch (_player.voiceVariant)
1319			{
1320			case 1:
1321				if (_oldMaleForVoiceAutoSwitch)
1322				{
1323					_player.voiceVariant = 2;
1324				}
1325				break;
1326			case 2:
1327				if (!_oldMaleForVoiceAutoSwitch)
1328				{
1329					_player.voiceVariant = 1;
1330				}
1331				break;
1332			}
1333			_oldMaleForVoiceAutoSwitch = _player.Male;
1334			PlayVoicePreview();
1335		}
1336	
1337		private void Click_CopyHex(UIMouseEvent evt, UIElement listeningElement)
1338		{
1339			SoundEngine.PlaySound(12);
1340			Platform.Get<IClipboard>().Value = _hslHexText.Text;
1341		}
1342	
1343		private void Click_PasteHex(UIMouseEvent evt, UIElement listeningElement)
1344		{
1345			SoundEngine.PlaySound(12);
1346			string value = Platform.Get<IClipboard>().Value;
1347			if (GetHexColor(value, out var hsl))
1348			{
1349				ApplyPendingColor(ScaledHslToRgb(hsl.X, hsl.Y, hsl.Z));
1350				_currentColorHSL = hsl;
1351				UpdateHexText(ScaledHslToRgb(hsl.X, hsl.Y, hsl.Z));
1352				UpdateColorPickers();
1353			}
1354		}
1355	
1356		private string GetPlayerTemplateValues()
1357		{
1358			//IL_013f: Unknown result type (might be due to invalid IL or missing references)
1359			//IL_0144: Unknown result type (might be due to invalid IL or missing references)
1360			//IL_014b: Unknown result type (might be due to invalid IL or missing references)
1361			//IL_0152: Unknown result type (might be due to invalid IL or missing references)
1362			//IL_015e: Expected O, but got Unknown
1363			string text = JsonConvert.SerializeObject((object)new Dictionary<string, object>
1364			{
1365				{ "version", 1 },
1366				{ "hairStyle", _player.hair },
1367				{ "clothingStyle", _player.skinVariant },
1368				{ "voiceStyle", _player.voiceVariant },
1369				{ "voicePitch", _player.voicePitchOffset },
1370				{
1371					"hairColor",
1372					GetHexText(_player.hairColor)
1373				},
1374				{
1375					"eyeColor",
1376					GetHexText(_player.eyeColor)
1377				},
1378				{
1379					"skinColor",
1380					GetHexText(_player.skinColor)
1381				},
1382				{
1383					"shirtColor",
1384					GetHexText(_player.shirtColor)
1385				},
1386				{
1387					"underShirtColor",
1388					GetHexText(_player.underShirtColor)
1389				},
1390				{
1391					"pantsColor",
1392					GetHexText(_player.pantsColor)
1393				},
1394				{
1395					"shoeColor",
1396					GetHexText(_player.shoeColor)
1397				}
1398			}, new JsonSerializerSettings
1399			{
1400				TypeNameHandling = (TypeNameHandling)4,
1401				MetadataPropertyHandling = (MetadataPropertyHandling)1,
1402				Formatting = (Formatting)1
1403			});
1404			PlayerInput.PrettyPrintProfiles(ref text);
1405			return text;
1406		}
1407	
1408		private void Click_CopyPlayerTemplate(UIMouseEvent evt, UIElement listeningElement)
1409		{
1410			SoundEngine.PlaySound(12);
1411			Platform.Get<IClipboard>().Value = GetPlayerTemplateValues();
1412		}
1413	
1414		private void Click_PastePlayerTemplate(UIMouseEvent evt, UIElement listeningElement)
1415		{
1416			SoundEngine.PlaySound(12);
1417			try
1418			{
1419				string value = Platform.Get<IClipboard>().Value;
1420				int num = value.IndexOf("{");
1421				if (num == -1)
1422				{
1423					return;
1424				}
1425				value = value.Substring(num);
1426				int num2 = value.LastIndexOf("}");
1427				if (num2 == -1)
1428				{
1429					return;
1430				}
1431				value = value.Substring(0, num2 + 1);
1432				Dictionary<string, object> dictionary = JsonConvert.DeserializeObject<Dictionary<string, object>>(value);
1433				if (dictionary == null)
1434				{
1435					return;
1436				}
1437				Dictionary<string, object> dictionary2 = new Dictionary<string, object>();
1438				foreach (KeyValuePair<string, object> item in dictionary)
1439				{
1440					dictionary2[item.Key.ToLower()] = item.Value;
1441				}
1442				if (dictionary2.TryGetValue("version", out var value2))
1443				{
1444					_ = (long)value2;
1445				}
1446				if (dictionary2.TryGetValue("hairstyle", out value2))
1447				{
1448					int num3 = (int)(long)value2;
1449					if (Main.Hairstyles.AvailableHairstyles.Contains(num3))
1450					{
1451						_player.hair = num3;
1452						_lastSelectedHairstyle = num3;
1453					}
1454				}
1455				if (dictionary2.TryGetValue("clothingstyle", out value2))
1456				{
1457					int num4 = (int)(long)value2;
1458					if (_validClothStyles.Contains(num4))
1459					{
1460						_player.skinVariant = num4;
1461					}
1462				}
1463				if (dictionary2.TryGetValue("voicestyle", out value2))
1464				{
1465					int num5 = (int)(long)value2;
1466					if (_validVoiceStyles.Contains(num5))
1467					{
1468						_player.voiceVariant = num5;
1469					}
1470				}
1471				if (dictionary2.TryGetValue("voicepitch", out value2))
1472				{
1473					float num6 = (float)(double)value2;
1474					_player.voicePitchOffset = num6;
1475					_pitchAmount = num6;
1476				}
1477				if (dictionary2.TryGetValue("haircolor", out value2) && GetHexColor((string)value2, out var hsl))
1478				{
1479					_player.hairColor = ScaledHslToRgb(hsl);
1480				}
1481				if (dictionary2.TryGetValue("eyecolor", out value2) && GetHexColor((string)value2, out hsl))
1482				{
1483					_player.eyeColor = ScaledHslToRgb(hsl);
1484				}
1485				if (dictionary2.TryGetValue("skincolor", out value2) && GetHexColor((string)value2, out hsl))
1486				{
1487					_player.skinColor = ScaledHslToRgb(hsl);
1488				}
1489				if (dictionary2.TryGetValue("shirtcolor", out value2) && GetHexColor((string)value2, out hsl))
1490				{
1491					_player.shirtColor = ScaledHslToRgb(hsl);
1492				}
1493				if (dictionary2.TryGetValue("undershirtcolor", out value2) && GetHexColor((string)value2, out hsl))
1494				{
1495					_player.underShirtColor = ScaledHslToRgb(hsl);
1496				}
1497				if (dictionary2.TryGetValue("pantscolor", out value2) && GetHexColor((string)value2, out hsl))
1498				{
1499					_player.pantsColor = ScaledHslToRgb(hsl);
1500				}
1501				if (dictionary2.TryGetValue("shoecolor", out value2) && GetHexColor((string)value2, out hsl))
1502				{
1503					_player.shoeColor = ScaledHslToRgb(hsl);
1504				}
1505				Click_CharClothStyle(null, null);
1506				UpdateColorPickers();
1507			}
1508			catch
1509			{
1510			}
1511		}
1512	
1513		private void Click_VoicePlay(UIMouseEvent evt, UIElement listeningElement)
1514		{
1515			PlayVoicePreview();
1516		}
1517	
1518		private void PlayVoicePreview()
1519		{
1520			if (!_playedVoicePreviewThisFrame)
1521			{
1522				_playedVoicePreviewThisFrame = true;
1523				Vector2 position = _player.position;
1524				_player.position = new Vector2(-1f, -1f);
1525				_player.PlayHurtSound();
1526				_player.position = position;
1527			}
1528		}
1529	
1530		private void Click_VoiceCycleBack(UIMouseEvent evt, UIElement listeningElement)
1531		{
1532			Main.CycleVoiceStyle(_player, -1);
1533			PlayVoicePreview();
1534		}
1535	
1536		private void Click_VoiceCycleForward(UIMouseEvent evt, UIElement listeningElement)
1537		{
1538			Main.CycleVoiceStyle(_player, 1);
1539			PlayVoicePreview();
1540		}
1541	
1542		private void Update_VoiceIconColor()
1543		{
1544		}
1545	
1546		private void Click_RandomizePlayer(UIMouseEvent evt, UIElement listeningElement)
1547		{
1548			SoundEngine.PlaySound(12);
1549			Player player = _player;
1550			int index = Main.rand.Next(Main.Hairstyles.AvailableHairstyles.Count);
1551			player.hair = Main.Hairstyles.AvailableHairstyles[index];
1552			_lastSelectedHairstyle = player.hair;
1553			player.eyeColor = ScaledHslToRgb(GetRandomColorVector());
1554			while (player.eyeColor.R + player.eyeColor.G + player.eyeColor.B > 300)
1555			{
1556				player.eyeColor = ScaledHslToRgb(GetRandomColorVector());
1557			}
1558			float num = (float)Main.rand.Next(60, 120) * 0.01f;
1559			if (num > 1f)
1560			{
1561				num = 1f;
1562			}
1563			player.skinColor.R = (byte)((float)Main.rand.Next(240, 255) * num);
1564			player.skinColor.G = (byte)((float)Main.rand.Next(110, 140) * num);
1565			player.skinColor.B = (byte)((float)Main.rand.Next(75, 110) * num);
1566			player.hairColor = ScaledHslToRgb(GetRandomColorVector());
1567			player.shirtColor = ScaledHslToRgb(GetRandomColorVector());
1568			player.underShirtColor = ScaledHslToRgb(GetRandomColorVector());
1569			player.pantsColor = ScaledHslToRgb(GetRandomColorVector());
1570			player.shoeColor = ScaledHslToRgb(GetRandomColorVector());
1571			player.skinVariant = _validClothStyles[Main.rand.Next(_validClothStyles.Length)];
1572			player.voiceVariant = (player.Male ? 1 : 2);
1573			if (Main.rand.Next(2) == 0)
1574			{
1575				player.voiceVariant = 3;
1576			}
1577			switch (player.hair + 1)
1578			{
1579			case 5:
1580			case 6:
1581			case 7:
1582			case 10:
1583			case 12:
1584			case 19:
1585			case 22:
1586			case 23:
1587			case 26:
1588			case 27:
1589			case 30:
1590			case 33:
1591			case 34:
1592			case 35:
1593			case 37:
1594			case 38:
1595			case 39:
1596			case 40:
1597			case 41:
1598			case 44:
1599			case 45:
1600			case 46:
1601			case 47:
1602			case 48:
1603			case 49:
1604			case 51:
1605			case 56:
1606			case 65:
1607			case 66:
1608			case 67:
1609			case 68:
1610			case 69:
1611			case 70:
1612			case 71:
1613			case 72:
1614			case 73:
1615			case 74:
1616			case 79:
1617			case 80:
1618			case 81:
1619			case 82:
1620			case 84:
1621			case 85:
1622			case 86:
1623			case 87:
1624			case 88:
1625			case 90:
1626			case 91:
1627			case 92:
1628			case 93:
1629			case 95:
1630			case 96:
1631			case 98:
1632			case 100:
1633			case 102:
1634			case 104:
1635			case 107:
1636			case 108:
1637			case 113:
1638			case 124:
1639			case 126:
1640			case 133:
1641			case 134:
1642			case 135:
1643			case 144:
1644			case 146:
1645			case 147:
1646			case 163:
1647			case 165:
1648				player.Male = false;
1649				break;
1650			default:
1651				player.Male = true;
1652				break;
1653			}
1654			_femaleArmor = (_maleArmor = default(ArmorAssignments));
1655			Click_CharClothStyle(null, null);
1656			UpdateSelectedGender();
1657			UpdateColorPickers();
1658		}
1659	
1660		private void Click_Naming(UIMouseEvent evt, UIElement listeningElement)
1661		{
1662			SoundEngine.PlaySound(10);
1663			_player.name = "";
1664			Main.clrInput();
1665			UIVirtualKeyboard state = new UIVirtualKeyboard(Lang.menu[45].Value, "", OnFinishedNaming, OnCanceledNaming, 0, allowEmpty: true);
1666			Main.MenuUI.SetState(state);
1667		}
1668	
1669		private void Click_NamingAndCreating(UIMouseEvent evt, UIElement listeningElement)
1670		{
1671			SoundEngine.PlaySound(10);
1672			if (string.IsNullOrEmpty(_player.name))
1673			{
1674				_player.name = "";
1675				Main.clrInput();
1676				UIVirtualKeyboard state = new UIVirtualKeyboard(Lang.menu[45].Value, "", OnFinishedNamingAndCreating, OnCanceledNaming);
1677				Main.MenuUI.SetState(state);
1678			}
1679			else
1680			{
1681				FinishCreatingCharacter();
1682			}
1683		}
1684	
1685		private void OnFinishedNaming(string name)
1686		{
1687			_player.name = name.Trim();
1688			Main.MenuUI.SetState(this);
1689			_charName.SetContents(_player.name);
1690		}
1691	
1692		private void OnCanceledNaming()
1693		{
1694			Main.MenuUI.SetState(this);
1695		}
1696	
1697		private void OnFinishedNamingAndCreating(string name)
1698		{
1699			_player.name = name.Trim();
1700			Main.MenuUI.SetState(this);
1701			_charName.SetContents(_player.name);
1702			FinishCreatingCharacter();
1703		}
1704	
1705		private void FinishCreatingCharacter()
1706		{
1707			TryAutoAssigningHair();
1708			SetupPlayerStatsAndInventoryBasedOnDifficulty();
1709			PlayerFileData.CreateAndSave(_player);
1710			Main.LoadPlayers();
1711			Main.menuMode = 1;
1712		}
1713	
1714		private void SetupPlayerStatsAndInventoryBasedOnDifficulty()
1715		{
1716			_femaleArmor = (_maleArmor = default(ArmorAssignments));
1717			UpdatePreviewItems();
1718			int num = 0;
1719			byte difficulty = _player.difficulty;
1720			if (difficulty == 3)
1721			{
1722				_player.statLife = (_player.statLifeMax = 100);
1723				_player.statMana = (_player.statManaMax = 20);
1724				_player.inventory[num].SetDefaults(6);
1725				_player.inventory[num++].Prefix(-1);
1726				_player.inventory[num].SetDefaults(1);
1727				_player.inventory[num++].Prefix(-1);
1728				_player.inventory[num].SetDefaults(10);
1729				_player.inventory[num++].Prefix(-1);
1730				_player.inventory[num].SetDefaults(7);
1731				_player.inventory[num++].Prefix(-1);
1732				_player.inventory[num].SetDefaults(4281);
1733				_player.inventory[num++].Prefix(-1);
1734				_player.inventory[num].SetDefaults(8);
1735				_player.inventory[num++].stack = 100;
1736				_player.inventory[num].SetDefaults(965);
1737				_player.inventory[num++].stack = 100;
1738				_player.inventory[num++].SetDefaults(50);
1739				_player.inventory[num++].SetDefaults(84);
1740				_player.armor[3].SetDefaults(4978);
1741				_player.armor[3].Prefix(-1);
1742				string text = _player.name.ToLower();
1743				if (text == "wolf pet" || text == "wolfpet")
1744				{
1745					_player.miscEquips[3].SetDefaults(5130);
1746				}
1747				_player.AddBuff(216, 3600);
1748			}
1749			else
1750			{
1751				_player.inventory[num].SetDefaults(3507);
1752				_player.inventory[num++].Prefix(-1);
1753				_player.inventory[num].SetDefaults(3509);
1754				_player.inventory[num++].Prefix(-1);
1755				_player.inventory[num].SetDefaults(3506);
1756				_player.inventory[num++].Prefix(-1);
1757			}
1758			if (Main.runningCollectorsEdition)
1759			{
1760				_player.inventory[num++].SetDefaults(603);
1761			}
1762			_player.savedPerPlayerFieldsThatArentInThePlayerClass = new Player.SavedPlayerDataWithAnnoyingRules();
1763			CreativePowerManager.Instance.ResetDataForNewPlayer(_player);
1764		}
1765	
1766		private bool GetHexColor(string hexString, out Vector3 hsl)
1767		{
1768			if (hexString.StartsWith("#"))
1769			{
1770				hexString = hexString.Substring(1);
1771			}
1772			if (hexString.Length <= 6 && uint.TryParse(hexString, NumberStyles.HexNumber, CultureInfo.CurrentCulture, out var result))
1773			{
1774				uint b = result & 0xFF;
1775				uint g = (result >> 8) & 0xFF;
1776				uint r = (result >> 16) & 0xFF;
1777				hsl = RgbToScaledHsl(new Color((int)r, (int)g, (int)b));
1778				return true;
1779			}
1780			hsl = Vector3.Zero;
1781			return false;
1782		}
1783	
1784		private void Click_RandomizeSingleColor(UIMouseEvent evt, UIElement listeningElement)
1785		{
1786			SoundEngine.PlaySound(12);
1787			Vector3 randomColorVector = GetRandomColorVector();
1788			ApplyPendingColor(ScaledHslToRgb(randomColorVector.X, randomColorVector.Y, randomColorVector.Z));
1789			_currentColorHSL = randomColorVector;
1790			UpdateHexText(ScaledHslToRgb(randomColorVector.X, randomColorVector.Y, randomColorVector.Z));
1791			UpdateColorPickers();
1792		}
1793	
1794		private static Vector3 GetRandomColorVector()
1795		{
1796			return new Vector3(Main.rand.NextFloat(), Main.rand.NextFloat(), Main.rand.NextFloat());
1797		}
1798	
1799		private void UnselectAllCategories()
1800		{
1801			UIColoredImageButton[] colorPickers = _colorPickers;
1802			for (int i = 0; i < colorPickers.Length; i++)
1803			{
1804				colorPickers[i]?.SetSelected(selected: false);
1805			}
1806			_clothingStylesCategoryButton.SetSelected(selected: false);
1807			_hairStylesCategoryButton.SetSelected(selected: false);
1808			_charInfoCategoryButton.SetSelected(selected: false);
1809			_hslContainer.Remove();
1810			_hairstylesContainer.Remove();
1811			_clothStylesContainer.Remove();
1812			_infoContainer.Remove();
1813		}
1814	
1815		private void SelectColorPicker(CategoryId selection)
1816		{
1817			_selectedPicker = selection;
1818			switch (selection)
1819			{
1820			case CategoryId.CharInfo:
1821				Click_CharInfo(null, null);
1822				return;
1823			case CategoryId.Clothing:
1824				Click_ClothStyles(null, null);
1825				return;
1826			case CategoryId.HairStyle:
1827				Click_HairStyles(null, null);
1828				return;
1829			}
1830			UnselectAllCategories();
1831			_middleContainer.Append(_hslContainer);
1832			for (int i = 0; i < _colorPickers.Length; i++)
1833			{
1834				if (_colorPickers[i] != null)
1835				{
1836					_colorPickers[i].SetSelected(i == (int)selection);
1837				}
1838			}
1839			Vector3 currentColorHSL = Vector3.One;
1840			switch (_selectedPicker)
1841			{
1842			case CategoryId.HairColor:
1843				currentColorHSL = RgbToScaledHsl(_player.hairColor);
1844				break;
1845			case CategoryId.Eye:
1846				currentColorHSL = RgbToScaledHsl(_player.eyeColor);
1847				break;
1848			case CategoryId.Skin:
1849				currentColorHSL = RgbToScaledHsl(_player.skinColor);
1850				break;
1851			case CategoryId.Shirt:
1852				currentColorHSL = RgbToScaledHsl(_player.shirtColor);
1853				break;
1854			case CategoryId.Undershirt:
1855				currentColorHSL = RgbToScaledHsl(_player.underShirtColor);
1856				break;
1857			case CategoryId.Pants:
1858				currentColorHSL = RgbToScaledHsl(_player.pantsColor);
1859				break;
1860			case CategoryId.Shoes:
1861				currentColorHSL = RgbToScaledHsl(_player.shoeColor);
1862				break;
1863			}
1864			_currentColorHSL = currentColorHSL;
1865			UpdateHexText(ScaledHslToRgb(currentColorHSL.X, currentColorHSL.Y, currentColorHSL.Z));
1866		}
1867	
1868		private void UpdateColorPickers()
1869		{
1870			_ = _selectedPicker;
1871			_colorPickers[3].SetColor(_player.hairColor);
1872			_hairStylesCategoryButton.SetColor(_player.hairColor);
1873			_colorPickers[4].SetColor(_player.eyeColor);
1874			_colorPickers[5].SetColor(_player.skinColor);
1875			_colorPickers[6].SetColor(_player.shirtColor);
1876			_colorPickers[7].SetColor(_player.underShirtColor);
1877			_colorPickers[8].SetColor(_player.pantsColor);
1878			_colorPickers[9].SetColor(_player.shoeColor);
1879		}
1880	
1881		public override void Draw(SpriteBatch spriteBatch)
1882		{
1883			base.Draw(spriteBatch);
1884			string text = null;
1885			if (_copyHexButton.IsMouseHovering)
1886			{
1887				text = Language.GetTextValue("UI.CopyColorToClipboard");
1888			}
1889			if (_pasteHexButton.IsMouseHovering)
1890			{
1891				text = Language.GetTextValue("UI.PasteColorFromClipboard");
1892			}
1893			if (_randomColorButton.IsMouseHovering)
1894			{
1895				text = Language.GetTextValue("UI.RandomizeColor");
1896			}
1897			if (_copyTemplateButton.IsMouseHovering)
1898			{
1899				text = Language.GetTextValue("UI.CopyPlayerToClipboard");
1900			}
1901			if (_pasteTemplateButton.IsMouseHovering)
1902			{
1903				text = Language.GetTextValue("UI.PastePlayerFromClipboard");
1904			}
1905			if (_randomizePlayerButton.IsMouseHovering)
1906			{
1907				text = Language.GetTextValue("UI.RandomizePlayer");
1908			}
1909			if (_previewArmorButton[0].IsMouseHovering)
1910			{
1911				text = Language.GetTextValue("UI.PreviewArmorNone");
1912			}
1913			if (_previewArmorButton[1].IsMouseHovering)
1914			{
1915				text = Language.GetTextValue("UI.PreviewArmorHallowed");
1916			}
1917			if (_previewArmorButton[2].IsMouseHovering)
1918			{
1919				text = Language.GetTextValue("UI.PreviewArmorSilver");
1920			}
1921			if (_previewArmorButton[3].IsMouseHovering)
1922			{
1923				text = Language.GetTextValue("UI.PreviewArmorFormal");
1924			}
1925			if (_previewArmorButton[4].IsMouseHovering)
1926			{
1927				text = Language.GetTextValue("UI.PreviewArmorSwimming");
1928			}
1929			if (UISliderBase.CurrentAimedSlider == _pitchSlider)
1930			{
1931				text = Language.GetTextValue("UI.PlayerCreateVoicePitch");
1932			}
1933			if (_voicePrevious.IsMouseHovering)
1934			{
1935				text = Language.GetTextValue("UI.PlayerCreateVoicePrev");
1936			}
1937			if (_voiceNext.IsMouseHovering)
1938			{
1939				text = Language.GetTextValue("UI.PlayerCreateVoiceNext");
1940			}
1941			if (_voicePlay.IsMouseHovering)
1942			{
1943				text = Language.GetTextValue("UI.PlayerCreateVoicePlay");
1944			}
1945			if (_charInfoCategoryButton.IsMouseHovering)
1946			{
1947				text = Language.GetTextValue("UI.PlayerCreateCategoryInfo");
1948			}
1949			if (_clothingStylesCategoryButton.IsMouseHovering)
1950			{
1951				text = Language.GetTextValue("UI.PlayerCreateCategoryBodyStyle");
1952			}
1953			if (_hairStylesCategoryButton.IsMouseHovering)
1954			{
1955				text = Language.GetTextValue("UI.PlayerCreateCategoryHairStyle");
1956			}
1957			if (_colorPickers[3].IsMouseHovering)
1958			{
1959				text = Language.GetTextValue("UI.PlayerCreateCategoryHairColor");
1960			}
1961			if (_colorPickers[4].IsMouseHovering)
1962			{
1963				text = Language.GetTextValue("UI.PlayerCreateCategoryEyeColor");
1964			}
1965			if (_colorPickers[5].IsMouseHovering)
1966			{
1967				text = Language.GetTextValue("UI.PlayerCreateCategorySkinColor");
1968			}
1969			if (_colorPickers[6].IsMouseHovering)
1970			{
1971				text = Language.GetTextValue("UI.PlayerCreateCategoryShirtColor");
1972			}
1973			if (_colorPickers[7].IsMouseHovering)
1974			{
1975				text = Language.GetTextValue("UI.PlayerCreateCategoryUndershirtColor");
1976			}
1977			if (_colorPickers[8].IsMouseHovering)
1978			{
1979				text = Language.GetTextValue("UI.PlayerCreateCategoryPantsColor");
1980			}
1981			if (_colorPickers[9].IsMouseHovering)
1982			{
1983				text = Language.GetTextValue("UI.PlayerCreateCategoryShoesColor");
1984			}
1985			if (text != null)
1986			{
1987				float x = FontAssets.MouseText.Value.MeasureString(text).X;
1988				Vector2 vector = new Vector2(Main.mouseX, Main.mouseY) + new Vector2(16f);
1989				if (vector.Y > (float)(Main.screenHeight - 30))
1990				{
1991					vector.Y = Main.screenHeight - 30;
1992				}
1993				if (vector.X > (float)Main.screenWidth - x)
1994				{
1995					vector.X = Main.screenWidth - 460;
1996				}
1997				Utils.DrawBorderStringFourWay(spriteBatch, FontAssets.MouseText.Value, text, vector.X, vector.Y, new Color(Main.mouseTextColor, Main.mouseTextColor, Main.mouseTextColor, Main.mouseTextColor), Color.Black, Vector2.Zero);
1998			}
1999			SetupGamepadPoints(spriteBatch);
2000			_tips.Update();
2001			int num = Main.screenHeight - 560;
2002			if (num < 0)
2003			{
2004				num = 0;
2005			}
2006			int num2 = 150;
2007			if (num < 300)
2008			{
2009				num2 = num / 2;
2010			}
2011			if (num > 30)
2012			{
2013				_tips.TipOffsetY = -num2;
2014				_tips.Draw();
2015			}
2016			if (!dirty)
2017			{
2018				if (!string.IsNullOrEmpty(_player.name))
2019				{
2020					dirty = true;
2021				}
2022				if (GetPlayerTemplateValues() != initialState)
2023				{
2024					dirty = true;
2025				}
2026			}
2027		}
2028	
2029		private void SetupGamepadPoints(SpriteBatch spriteBatch)
2030		{
2031			UILinkPointNavigator.Shortcuts.BackButtonCommand = 7;
2032			int num = 3000;
2033			int num2 = num + 20;
2034			int num3 = num;
2035			List<SnapPoint> snapPoints = GetSnapPoints();
2036			SnapPoint snapPoint = snapPoints.First((SnapPoint a) => a.Name == "Back");
2037			SnapPoint snapPoint2 = snapPoints.First((SnapPoint a) => a.Name == "Create");
2038			UILinkPoint uILinkPoint = UILinkPointNavigator.Points[num3];
2039			uILinkPoint.Unlink();
2040			UILinkPointNavigator.SetPosition(num3, snapPoint.Position);
2041			num3++;
2042			UILinkPoint uILinkPoint2 = UILinkPointNavigator.Points[num3];
2043			uILinkPoint2.Unlink();
2044			UILinkPointNavigator.SetPosition(num3, snapPoint2.Position);
2045			num3++;
2046			uILinkPoint.Right = uILinkPoint2.ID;
2047			uILinkPoint2.Left = uILinkPoint.ID;
2048			_foundPoints.Clear();
2049			_foundPoints.Add(uILinkPoint.ID);
2050			_foundPoints.Add(uILinkPoint2.ID);
2051			List<SnapPoint> list = snapPoints.Where((SnapPoint a) => a.Name == "Top").ToList();
2052			list.Sort(SortPoints);
2053			for (int num4 = 0; num4 < list.Count; num4++)
2054			{
2055				UILinkPoint uILinkPoint3 = UILinkPointNavigator.Points[num3];
2056				uILinkPoint3.Unlink();
2057				UILinkPointNavigator.SetPosition(num3, list[num4].Position);
2058				uILinkPoint3.Left = num3 - 1;
2059				uILinkPoint3.Right = num3 + 1;
2060				uILinkPoint3.Down = num2;
2061				if (num4 == 0)
2062				{
2063					uILinkPoint3.Left = -3;
2064				}
2065				if (num4 == list.Count - 1)
2066				{
2067					uILinkPoint3.Right = -4;
2068				}
2069				if (_selectedPicker == CategoryId.HairStyle || _selectedPicker == CategoryId.Clothing)
2070				{
2071					uILinkPoint3.Down = num2 + num4;
2072				}
2073				_foundPoints.Add(num3);
2074				num3++;
2075			}
2076			List<SnapPoint> list2 = snapPoints.Where((SnapPoint a) => a.Name == "Middle").ToList();
2077			list2.Sort(SortPoints);
2078			num3 = num2;
2079			switch (_selectedPicker)
2080			{
2081			case CategoryId.CharInfo:
2082			{
2083				for (int num13 = 0; num13 < list2.Count; num13++)
2084				{
2085					UILinkPoint andSet7 = GetAndSet(num3, list2[num13]);
2086					andSet7.Up = andSet7.ID - 1;
2087					andSet7.Down = andSet7.ID + 1;
2088					if (num13 == 0)
2089					{
2090						andSet7.Up = num + 2;
2091					}
2092					if (num13 == list2.Count - 1)
2093					{
2094						andSet7.Down = uILinkPoint.ID;
2095						uILinkPoint.Up = andSet7.ID;
2096						uILinkPoint2.Up = andSet7.ID;
2097					}
2098					_foundPoints.Add(num3);
2099					num3++;
2100				}
2101				break;
2102			}
2103			case CategoryId.HairStyle:
2104			{
2105				if (list2.Count == 0)
2106				{
2107					break;
2108				}
2109				_helper.CullPointsOutOfElementArea(spriteBatch, list2, _hairstylesContainer);
2110				SnapPoint snapPoint3 = list2[list2.Count - 1];
2111				_ = snapPoint3.Id / 10;
2112				_ = snapPoint3.Id % 10;
2113				int count = Main.Hairstyles.AvailableHairstyles.Count;
2114				for (int num12 = 0; num12 < list2.Count; num12++)
2115				{
2116					SnapPoint snapPoint4 = list2[num12];
2117					UILinkPoint andSet6 = GetAndSet(num3, snapPoint4);
2118					andSet6.Left = andSet6.ID - 1;
2119					if (snapPoint4.Id == 0)
2120					{
2121						andSet6.Left = -3;
2122					}
2123					andSet6.Right = andSet6.ID + 1;
2124					if (snapPoint4.Id == count - 1)
2125					{
2126						andSet6.Right = -4;
2127					}
2128					andSet6.Up = andSet6.ID - 10;
2129					if (num12 < 10)
2130					{
2131						andSet6.Up = num + 2 + num12;
2132					}
2133					andSet6.Down = andSet6.ID + 10;
2134					if (snapPoint4.Id + 10 > snapPoint3.Id)
2135					{
2136						if (snapPoint4.Id % 10 < 5)
2137						{
2138							andSet6.Down = uILinkPoint.ID;
2139						}
2140						else
2141						{
2142							andSet6.Down = uILinkPoint2.ID;
2143						}
2144					}
2145					if (num12 == list2.Count - 1)
2146					{
2147						uILinkPoint.Up = andSet6.ID;
2148						uILinkPoint2.Up = andSet6.ID;
2149					}
2150					_foundPoints.Add(num3);
2151					num3++;
2152				}
2153				break;
2154			}
2155			default:
2156			{
2157				List<SnapPoint> list5 = snapPoints.Where((SnapPoint a) => a.Name == "Low").ToList();
2158				list5.Sort(SortPoints);
2159				num3 = num2 + 20;
2160				for (int num10 = 0; num10 < list5.Count; num10++)
2161				{
2162					UILinkPoint andSet4 = GetAndSet(num3, list5[num10]);
2163					andSet4.Up = num2 + 2;
2164					andSet4.Down = uILinkPoint.ID;
2165					andSet4.Left = andSet4.ID - 1;
2166					andSet4.Right = andSet4.ID + 1;
2167					if (num10 == 0)
2168					{
2169						andSet4.Left = andSet4.ID + 2;
2170						uILinkPoint.Up = andSet4.ID;
2171					}
2172					if (num10 == list5.Count - 1)
2173					{
2174						andSet4.Right = andSet4.ID - 2;
2175						uILinkPoint2.Up = andSet4.ID;
2176					}
2177					_foundPoints.Add(num3);
2178					num3++;
2179				}
2180				num3 = num2;
2181				for (int num11 = 0; num11 < list2.Count; num11++)
2182				{
2183					UILinkPoint andSet5 = GetAndSet(num3, list2[num11]);
2184					andSet5.Up = andSet5.ID - 1;
2185					andSet5.Down = andSet5.ID + 1;
2186					if (num11 == 0)
2187					{
2188						andSet5.Up = num + 2 + 5;
2189					}
2190					if (num11 == list2.Count - 1)
2191					{
2192						andSet5.Down = num2 + 20 + 2;
2193					}
2194					_foundPoints.Add(num3);
2195					num3++;
2196				}
2197				break;
2198			}
2199			case CategoryId.Clothing:
2200			{
2201				List<SnapPoint> list3 = snapPoints.Where((SnapPoint a) => a.Name == "Preview").ToList();
2202				list3.Sort(SortPoints);
2203				List<SnapPoint> list4 = snapPoints.Where((SnapPoint a) => a.Name == "Low").ToList();
2204				list4.Sort(SortPoints);
2205				int down = -2;
2206				SnapPoint point = null;
2207				UILinkPoint uILinkPoint4 = null;
2208				if (_pitchSlider.GetSnapPoint(out point))
2209				{
2210					uILinkPoint4 = GetAndSet(num2 + 40, point);
2211					_foundPoints.Add(uILinkPoint4.ID);
2212				}
2213				uILinkPoint4.Down = uILinkPoint.ID;
2214				int num5 = num2 + 20;
2215				num3 = num2 + 20;
2216				int num6 = num3 + list4.Count;
2217				UILinkPoint uILinkPoint5 = null;
2218				for (int num7 = 0; num7 < list4.Count; num7++)
2219				{
2220					UILinkPoint andSet = GetAndSet(num3, list4[num7]);
2221					andSet.Up = num2 + num7 + 2;
2222					andSet.Down = uILinkPoint4.ID;
2223					if (num7 >= 3)
2224					{
2225						andSet.Up = num6 + (num7 - 3) + 1;
2226						andSet.Down = uILinkPoint2.ID;
2227					}
2228					andSet.Left = andSet.ID - 1;
2229					andSet.Right = andSet.ID + 1;
2230					if (num7 == 0)
2231					{
2232						down = andSet.ID;
2233						andSet.Left = andSet.ID + 5;
2234						uILinkPoint.Up = andSet.ID;
2235					}
2236					if (num7 == list4.Count - 1)
2237					{
2238						_ = andSet.ID;
2239						andSet.Right = andSet.ID - 5;
2240						uILinkPoint2.Up = andSet.ID;
2241					}
2242					if (num7 == 1)
2243					{
2244						uILinkPoint5 = andSet;
2245					}
2246					_foundPoints.Add(num3);
2247					num3++;
2248				}
2249				for (int num8 = 0; num8 < list3.Count; num8++)
2250				{
2251					UILinkPoint andSet2 = GetAndSet(num3, list3[num8]);
2252					andSet2.Up = num2 + num8 + 5;
2253					andSet2.Down = num5 + ((int)MathHelper.Clamp(num8, 1f, 4f) - 1) + 3;
2254					andSet2.Left = andSet2.ID - 1;
2255					andSet2.Right = andSet2.ID + 1;
2256					if (num8 == 0)
2257					{
2258						andSet2.Left = num5 + 2;
2259					}
2260					if (num8 == list3.Count - 1)
2261					{
2262						andSet2.Right = num5;
2263					}
2264					_foundPoints.Add(num3);
2265					num3++;
2266				}
2267				if (list4.Count > 1)
2268				{
2269					uILinkPoint4.Up = uILinkPoint5.ID;
2270				}
2271				uILinkPoint.Up = uILinkPoint4.ID;
2272				num3 = num2;
2273				for (int num9 = 0; num9 < list2.Count; num9++)
2274				{
2275					UILinkPoint andSet3 = GetAndSet(num3, list2[num9]);
2276					andSet3.Up = num + 2 + num9;
2277					andSet3.Left = andSet3.ID - 1;
2278					andSet3.Right = andSet3.ID + 1;
2279					if (num9 == 0)
2280					{
2281						andSet3.Left = andSet3.ID + 9;
2282					}
2283					if (num9 == list2.Count - 1)
2284					{
2285						andSet3.Right = andSet3.ID - 9;
2286					}
2287					andSet3.Down = down;
2288					if (num9 >= 5)
2289					{
2290						andSet3.Down = num6 + num9 - 5;
2291					}
2292					_foundPoints.Add(num3);
2293					num3++;
2294				}
2295				break;
2296			}
2297			}
2298			if (PlayerInput.UsingGamepadUI && !_foundPoints.Contains(UILinkPointNavigator.CurrentPoint))
2299			{
2300				MoveToVisuallyClosestPoint();
2301			}
2302		}
2303	
2304		private void MoveToVisuallyClosestPoint()
2305		{
2306			Dictionary<int, UILinkPoint> points = UILinkPointNavigator.Points;
2307			Vector2 mouseScreen = Main.MouseScreen;
2308			UILinkPoint uILinkPoint = null;
2309			foreach (int foundPoint in _foundPoints)
2310			{
2311				if (!points.TryGetValue(foundPoint, out var value))
2312				{
2313					return;
2314				}
2315				if (uILinkPoint == null || Vector2.Distance(mouseScreen, uILinkPoint.Position) > Vector2.Distance(mouseScreen, value.Position))
2316				{
2317					uILinkPoint = value;
2318				}
2319			}
2320			if (uILinkPoint != null)
2321			{
2322				UILinkPointNavigator.ChangePoint(uILinkPoint.ID);
2323			}
2324		}
2325	
2326		public void TryMovingCategory(int direction)
2327		{
2328			int num = (int)(_selectedPicker + direction) % 10;
2329			if (num < 0)
2330			{
2331				num += 10;
2332			}
2333			SelectColorPicker((CategoryId)num);
2334		}
2335	
2336		private UILinkPoint GetAndSet(int ptid, SnapPoint snap)
2337		{
2338			UILinkPoint uILinkPoint = UILinkPointNavigator.Points[ptid];
2339			uILinkPoint.Unlink();
2340			UILinkPointNavigator.SetPosition(uILinkPoint.ID, snap.Position);
2341			return uILinkPoint;
2342		}
2343	
2344		private bool PointWithName(SnapPoint a, string comp)
2345		{
2346			return a.Name == comp;
2347		}
2348	
2349		private int SortPoints(SnapPoint a, SnapPoint b)
2350		{
2351			return a.Id.CompareTo(b.Id);
2352		}
2353	
2354		private static Color ScaledHslToRgb(Vector3 hsl)
2355		{
2356			return ScaledHslToRgb(hsl.X, hsl.Y, hsl.Z);
2357		}
2358	
2359		private static Color ScaledHslToRgb(float hue, float saturation, float luminosity)
2360		{
2361			return Main.hslToRgb(hue, saturation, luminosity * 0.85f + 0.15f);
2362		}
2363	
2364		private static Vector3 RgbToScaledHsl(Color color)
2365		{
2366			Vector3 value = Main.rgbToHsl(color);
2367			value.Z = (value.Z - 0.15f) / 0.85f;
2368			return Vector3.Clamp(value, Vector3.Zero, Vector3.One);
2369		}
2370	
2371		public void HandleBackButtonUsage()
2372		{
2373			if (_selectedPicker != CategoryId.CharInfo)
2374			{
2375				SoundEngine.PlaySound(12);
2376				UnselectAllCategories();
2377				_selectedPicker = CategoryId.CharInfo;
2378				_middleContainer.Append(_infoContainer);
2379				_charInfoCategoryButton.SetSelected(selected: true);
2380			}
2381			else
2382			{
2383				GoBack();
2384			}
2385		}
2386	}
2387	

```


---

## 🤖 Assistant · 2026-08-09T11:48:57.312Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. Big findings for UICharacterCreation:

- `_validClothStyles` old: {0,2,1,3,8,4,6,5,7,9} (lines 31-43) → new: {0,2,1,3,8,9,7,5,6,4} (line 58). Changed order!
- New `_defaultHairstylesForClothStyle` dict (lines 60-72): {0:0, 2:1, 1:12, 3:2, 8:28, 9:68, 7:18, 5:22, 6:81, 4:5}.
- New `_validVoiceStyles` {1,2,3} line 74; voice UI (voice prev/next/play, pitch slider) lines 441-527; voice preview via PlayHurtSound lines 1513-1540.
- Default difficulty: old `= 3` (creative) line 76 → new `= 0` (softcore/journey?) line 169. Actually 0 = softcore "Classic". Big behavioral change: default difficulty changed from Creative(3) to Classic(0).
- CategoryId enum same structure (10 items).
- Cloth styles menu: old had gender male/female buttons below cloth styles; new removed gender buttons and replaced with armor preview buttons (5: none/hallowed/silver/formal/swimming) + copy/paste/randomize + voice cycle. Gender selection now presumably by clicking cloth style (male variants vs female). Note Click_CharGenderMale/Female removed. New Click_CharClothStyle sets skinVariant from the button, and skinVariant itself determines Male? Actually in 1.4.4, skinVariant includes gender — variants: 0-4 male? Actually new cloth style list {0,2,1,3,8,9,7,5,6,4} — first five are male styles (0,2,1,3,8) and next five female (9,7,5,6,4)? In old, {0,2,1,3,8,4,6,5,7,9}: male 0-4? Hmm. Player.skinVariant in 1.4.4: 0=StarterMale... Let me check Player.cs for skinVariant and Male determination.

- Randomize logic: new adds eyeColor initial assignment before while loop (old didn't assign initially, just looped on existing color — same effect but new assigns random first then loops), plus voiceVariant randomization (line 1572-1576), much larger female-hairstyle case list (lines 1577-1653), and resets armor (line 1654).
- Hair auto-assign: new TryAutoAssigningHair + _lastSelectedHairstyle + SkipRenderingContent(i) (first frame skip to avoid rendering all heads same frame?).
- Preview direction: PreparePreview_Main sets direction=1; cloth style sets direction by gender.
- Armor preview: male/female ArmorAssignments, UpdatePreviewItems sets armor[0..2].
- Back button: dirty check / backup confirmation (GoBack, menuMode 40).
- GameTipsDisplay.
- LeftMouseDown naming changed (OnLeftMouseDown vs OnMouseDown) — minor API.
- Character preview: PrepareAction = PreparePreview_Main.
- UICharacterNameButton now takes 2 args.
- UIColoredImageButton constructor: old had (texture, isSmall) bool second param; new has (texture) and optional named `isSmall`. Fine.

Now read Player.cs defaults in both, and PlayerDrawLayers. Let me grep Player.cs for hairColor defaults.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:48:58.946Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"hairColor = new Color\\|skinColor = new Color\\|eyeColor = new Color\\|shirtColor = new Color\\|underShirtColor = new Color\\|pantsColor = new Color\\|shoeColor = new Color\\|skinVariant = \\|hair = \\|Male = \\|voiceVariant = \\|voicePitchOffset = \" ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs | head -30; echo \"===NEW===\"; grep -n \"hairColor = new Color\\|skinColor = new Color\\|eyeColor = new Color\\|shirtColor = new Color\\|underShirtColor = new Color\\|pantsColor = new Color\\|shoeColor = new Color\\|skinVariant = \\|hair = \\|Male = \\|voiceVariant = \\|voicePitchOffset = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | head -30",
 "description": "Compare Player default appearance fields"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:48:59.010Z

**📎 ToolResult**

```
199:    public Color hairColor = new Color(215, 90, 55);
200:    public Color skinColor = new Color((int) byte.MaxValue, 125, 90);
201:    public Color eyeColor = new Color(105, 90, 75);
202:    public Color shirtColor = new Color(175, 165, 140);
203:    public Color underShirtColor = new Color(160, 180, 215);
204:    public Color pantsColor = new Color((int) byte.MaxValue, 230, 175);
205:    public Color shoeColor = new Color(160, 105, 60);
1172:          this.skinVariant = PlayerVariantID.Sets.AltGenderReference[this.skinVariant];
1178:          this.skinVariant = PlayerVariantID.Sets.AltGenderReference[this.skinVariant];
10770:      int hair = this.hair;
28169:                this.Male = !this.Male;
34908:      this.skinVariant = other.skinVariant;
34914:      this.hair = other.hair;
35400:              player1.hair = binaryReader.ReadInt32();
35421:                player1.Male = player1.hair != 5 && player1.hair != 6 && (player1.hair != 9 && player1.hair != 11);
35423:                player1.Male = binaryReader.ReadBoolean();
35425:                player1.skinVariant = (int) binaryReader.ReadByte();
35427:                player1.skinVariant = 9;
35834:      newPlayer.skinVariant = (int) MathHelper.Clamp((float) newPlayer.skinVariant, 0.0f, 11f);
===NEW===
2420:	public Color hairColor = new Color(215, 90, 55);
2422:	public Color skinColor = new Color(255, 125, 90);
2424:	public Color eyeColor = new Color(105, 90, 75);
2426:	public Color shirtColor = new Color(175, 165, 140);
2428:	public Color underShirtColor = new Color(160, 180, 215);
2430:	public Color pantsColor = new Color(255, 230, 175);
2432:	public Color shoeColor = new Color(160, 105, 60);
3255:					skinVariant = PlayerVariantID.Sets.AltGenderReference[skinVariant];
3260:				skinVariant = PlayerVariantID.Sets.AltGenderReference[skinVariant];
35342:			Male = Male,
35355:			Male = Male,
35368:			Male = Male,
42526:						Male = !Male;
42530:							voiceVariant = 2;
42533:							voiceVariant = 1;
53478:		skinVariant = other.skinVariant;
53484:		hair = other.hair;
54209:		newPlayer.hair = fileIO.ReadInt32();
54212:			newPlayer.hair = 0;
54251:				newPlayer.Male = false;
54255:				newPlayer.Male = true;
54260:			newPlayer.Male = fileIO.ReadBoolean();
54264:			newPlayer.skinVariant = fileIO.ReadByte();
54268:			newPlayer.skinVariant = 9;
54775:			newPlayer.voiceVariant = fileIO.ReadByte();
54779:			newPlayer.skinVariant = (int)MathHelper.Clamp(newPlayer.skinVariant, 0f, PlayerVariantID.Count - 1);
54780:			newPlayer.voiceVariant = (newPlayer.Male ? 1 : 2);
54781:			newPlayer.voicePitchOffset = 0f;
54785:			newPlayer.voicePitchOffset = fileIO.ReadSingle();
54789:			newPlayer.voicePitchOffset = 0f;

```


---

## 🤖 Assistant · 2026-08-09T11:49:00.235Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"TotalHairStyles\\|HairCount\\|numHairstyles\\| hairstyle\\|GetHair\\|hair >= \\|hair < \\|hair > \" ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | head -20; echo \"===hairTex arrays===\"; grep -n \"hairTexture\\|hairIdx\\|PlayerHair\\|HairIDs\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | head",
 "description": "Find hairstyle count constants in Player.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:00.284Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:4335:	public Vector2 GetHairDrawOffset(int hairID, bool hatHair)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:16645:	public void GetHairSettings(out bool fullHair, out bool hatHair, out bool hideHair, out bool backHairDraw, out bool drawsBackHairWithoutHeadgear)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:54210:		if (newPlayer.hair >= 228)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:54933:	public Color GetHairColor(bool useLighting = true)
~/Project/GLM/SandboxWorld/Terarria1405/Player.cs:10660:    public void GetHairSettings(
~/Project/GLM/SandboxWorld/Terarria1405/Player.cs:10771:      backHairDraw = hair > 50 && (hair < 56 || hair > 63) && ((hair < 74 || hair > 77) && (hair < 88 || hair > 89)) && (hair != 94 && hair != 100 && (hair != 104 && hair != 112)) && hair < 116;
~/Project/GLM/SandboxWorld/Terarria1405/Player.cs:35868:    public Color GetHairColor(bool useLighting = true)
===hairTex arrays===

```


---

## 🤖 Assistant · 2026-08-09T11:49:03.643Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Player default colors unchanged (same RGB values). Voice fields new: voiceVariant, voicePitchOffset.

Hair count: old Player.cs check for hair >= 228? Let me check old line around 35400 and new 54209-54212: newPlayer.hair >= 228 → hair = 0. Old likely same. Let me check old line ~35397.

Also check PlayerVariantID.Count (new) vs old clamp 0-11. Old: `MathHelper.Clamp(newPlayer.skinVariant, 0.0f, 11f)` line 35834. New: clamp to PlayerVariantID.Count - 1. Need PlayerVariantID values.

Let me check PlayerVariantID.cs in both.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:49:04.390Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1405 ~/Project/GLM/SandboxWorld/Terarria1456 -iname \"*VariantID*\" -o -iname \"*VoiceID*\" -o -iname \"*Hairstyles*\" -o -iname \"*PlayerHair*\" | sort; echo \"===old hair clamp===\"; grep -n \"hair >= 2\\|hair > 2\\|228\\|236\\|247\" ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs | head",
 "description": "Find variant/voice/hairstyle ID files and hair count"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:04.434Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/ID/PlayerVariantID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerVariantID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerVoiceID.cs
===old hair clamp===
4048:          this.QuickSpawnItem(3228, 1);
6931:            if (this.ownedProjectileCounts[236] > 0)
6934:              Projectile.NewProjectile(this.position.X + (float) (this.width / 2), this.position.Y + (float) (this.height / 2), 0.0f, 0.0f, 236, 0, 0.0f, this.whoAmI, 0.0f, 0.0f);
7873:          if (this.armor[slot].type == 111 || this.armor[slot].type == 228 || (this.armor[slot].type == 229 || this.armor[slot].type == 230) || (this.armor[slot].type == 960 || this.armor[slot].type == 961 || this.armor[slot].type == 962))
7875:          if (this.armor[slot].type == 228 || this.armor[slot].type == 960)
7877:          if (this.armor[slot].type == 228 || this.armor[slot].type == 229 || (this.armor[slot].type == 230 || this.armor[slot].type == 960) || (this.armor[slot].type == 961 || this.armor[slot].type == 962))
7941:          if (this.armor[slot].type >= 2367 && this.armor[slot].type <= 2369)
8279:          if (this.armor[slot].type == 2361)
8284:          if (this.armor[slot].type == 2362)
8289:          if (this.armor[slot].type == 2363)

```


---

## 🤖 Assistant · 2026-08-09T11:49:06.097Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/ID/PlayerVariantID.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:49:06.099Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerVariantID.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:49:06.101Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/PlayerVoiceID.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:06.107Z

**📎 ToolResult**

```
1	using Microsoft.Xna.Framework;
2	
3	namespace Terraria.ID;
4	
5	public class PlayerVoiceID
6	{
7		public static class Sets
8		{
9			public static SetFactory Factory = new SetFactory(4);
10	
11			public static Color[] Colors = Factory.CreateCustomSet(Color.White, 1, Color.CornflowerBlue, 2, Color.HotPink, 3, Color.LimeGreen);
12		}
13	
14		public static int[] VariantOrder = new int[3] { 1, 2, 3 };
15	
16		public const int None = 0;
17	
18		public const int Male = 1;
19	
20		public const int Female = 2;
21	
22		public const int Other = 3;
23	
24		public const int Count = 4;
25	}
26	

```


---

## 👤 User(sidechain) · 2026-08-09T11:49:06.108Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.ID.PlayerVariantID
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	namespace Terraria.ID
8	{
9	  public static class PlayerVariantID
10	  {
11	    public static SetFactory Factory = new SetFactory(12);
12	    public const int MaleStarter = 0;
13	    public const int MaleSticker = 1;
14	    public const int MaleGangster = 2;
15	    public const int MaleCoat = 3;
16	    public const int FemaleStarter = 4;
17	    public const int FemaleSticker = 5;
18	    public const int FemaleGangster = 6;
19	    public const int FemaleCoat = 7;
20	    public const int MaleDress = 8;
21	    public const int FemaleDress = 9;
22	    public const int MaleDisplayDoll = 10;
23	    public const int FemaleDisplayDoll = 11;
24	    public const int Count = 12;
25	
26	    public class Sets
27	    {
28	      public static bool[] Male = PlayerVariantID.Factory.CreateBoolSet(0, 1, 2, 3, 8, 10);
29	      public static int[] AltGenderReference = PlayerVariantID.Factory.CreateIntSet(0, 0, 4, 4, 0, 1, 5, 5, 1, 2, 6, 6, 2, 3, 7, 7, 3, 8, 9, 9, 8, 10, 11, 11, 10);
30	      public static int[] VariantOrderMale = new int[6]
31	      {
32	        0,
33	        1,
34	        2,
35	        3,
36	        8,
37	        10
38	      };
39	      public static int[] VariantOrderFemale = new int[6]
40	      {
41	        4,
42	        5,
43	        6,
44	        7,
45	        9,
46	        11
47	      };
48	    }
49	  }
50	}
51	

```


---

## 👤 User(sidechain) · 2026-08-09T11:49:06.108Z

**📎 ToolResult**

```
1	namespace Terraria.ID;
2	
3	public static class PlayerVariantID
4	{
5		public class Sets
6		{
7			public static SetFactory Factory = new SetFactory(Count);
8	
9			public static bool[] Male = Factory.CreateBoolSet(0, 1, 2, 3, 8, 10);
10	
11			public static int[] AltGenderReference = Factory.CreateIntSet(0, 0, 4, 4, 0, 1, 5, 5, 1, 2, 6, 6, 2, 3, 7, 7, 3, 8, 9, 9, 8, 10, 11, 11, 10);
12	
13			public static int[] VariantOrderMale = new int[6] { 0, 1, 2, 3, 8, 10 };
14	
15			public static int[] VariantOrderFemale = new int[6] { 4, 5, 6, 7, 9, 11 };
16		}
17	
18		public const int MaleStarter = 0;
19	
20		public const int MaleSticker = 1;
21	
22		public const int MaleGangster = 2;
23	
24		public const int MaleCoat = 3;
25	
26		public const int FemaleStarter = 4;
27	
28		public const int FemaleSticker = 5;
29	
30		public const int FemaleGangster = 6;
31	
32		public const int FemaleCoat = 7;
33	
34		public const int MaleDress = 8;
35	
36		public const int FemaleDress = 9;
37	
38		public const int MaleDisplayDoll = 10;
39	
40		public const int FemaleDisplayDoll = 11;
41	
42		public static readonly int Count = 12;
43	}
44	

```


---

## 🤖 Assistant · 2026-08-09T11:49:08.294Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
PlayerVariantID unchanged (Count=12, variants 0-11, same Sets). PlayerVoiceID new.

Now hairstyles count. Main.Hairstyles — check for the hairstyles asset/count. Search Main.cs for Hairstyles and "228" or hairstyles count in both.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:49:12.227Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"AvailableHairstyles\" ~/Project/GLM/SandboxWorld/Terarria1405/Main.cs | head -5; grep -n \"class Hairstyle\\|AvailableHairstyles\\|TotalCount\\|_hairstyles\" ~/Project/GLM/SandboxWorld/Terarria1405/Main.cs | head -20; echo \"===NEW===\"; grep -n \"class Hairstyle\\|AvailableHairstyles\\|TotalCount\\|_hairstyles\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -20",
 "description": "Locate hairstyle list initialization in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:12.275Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:31261:        int count = Main.Hairstyles.AvailableHairstyles.Count;
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:31566:          int availableHairstyle = Main.Hairstyles.AvailableHairstyles[Main.hairStart + index2];
31261:        int count = Main.Hairstyles.AvailableHairstyles.Count;
31566:          int availableHairstyle = Main.Hairstyles.AvailableHairstyles[Main.hairStart + index2];
===NEW===
43137:		int count = Hairstyles.AvailableHairstyles.Count;
43528:			int num34 = Hairstyles.AvailableHairstyles[hairStart + m];

```


---

## 🤖 Assistant · 2026-08-09T11:49:14.653Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Hairstyles\" ~/Project/GLM/SandboxWorld/Terarria1405/*.cs ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/**/*.cs 2>/dev/null | grep -iv \"availablehairstyles\\[\\|availablehairstyles.count\" | head -10; echo \"---\"; grep -rln \"class HairstylesInfo\\|HairstylesInfo\\|SetAvailableHair\" ~/Project/GLM/SandboxWorld/Terarria1405 | head",
 "description": "Find Hairstyles info class in old version"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:14.729Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:556:    public static HairstyleUnlocksHelper Hairstyles = new HairstyleUnlocksHelper();
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:1851:    public const int numberOfHairstyles = 162;
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:31260:        Main.Hairstyles.UpdateUnlocks();
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs:13:    public List<int> AvailableHairstyles = new List<int>();
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs:44:      List<int> availableHairstyles = this.AvailableHairstyles;
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs:45:      availableHairstyles.Clear();
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs:49:          availableHairstyles.Add(index);
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs:50:        availableHairstyles.Add(136);
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs:51:        availableHairstyles.Add(137);
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs:52:        availableHairstyles.Add(138);
---

```


---

## 🤖 Assistant · 2026-08-09T11:49:16.646Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/HairstyleUnlocksHelper.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:16.652Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.HairstyleUnlocksHelper
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using System.Collections.Generic;
8	
9	namespace Terraria.GameContent
10	{
11	  public class HairstyleUnlocksHelper
12	  {
13	    public List<int> AvailableHairstyles = new List<int>();
14	    private bool _defeatedMartians;
15	    private bool _defeatedMoonlord;
16	    private bool _isAtStylist;
17	    private bool _isAtCharacterCreation;
18	
19	    public void UpdateUnlocks()
20	    {
21	      if (!this.ListWarrantsRemake())
22	        return;
23	      this.RebuildList();
24	    }
25	
26	    private bool ListWarrantsRemake()
27	    {
28	      bool flag1 = NPC.downedMartians && !Main.gameMenu;
29	      bool flag2 = NPC.downedMoonlord && !Main.gameMenu;
30	      bool flag3 = Main.hairWindow && !Main.gameMenu;
31	      bool gameMenu = Main.gameMenu;
32	      bool flag4 = false;
33	      if (this._defeatedMartians != flag1 || this._defeatedMoonlord != flag2 || (this._isAtStylist != flag3 || this._isAtCharacterCreation != gameMenu))
34	        flag4 = true;
35	      this._defeatedMartians = flag1;
36	      this._defeatedMoonlord = flag2;
37	      this._isAtStylist = flag3;
38	      this._isAtCharacterCreation = gameMenu;
39	      return flag4;
40	    }
41	
42	    private void RebuildList()
43	    {
44	      List<int> availableHairstyles = this.AvailableHairstyles;
45	      availableHairstyles.Clear();
46	      if (this._isAtCharacterCreation || this._isAtStylist)
47	      {
48	        for (int index = 0; index < 51; ++index)
49	          availableHairstyles.Add(index);
50	        availableHairstyles.Add(136);
51	        availableHairstyles.Add(137);
52	        availableHairstyles.Add(138);
53	        availableHairstyles.Add(139);
54	        availableHairstyles.Add(140);
55	        availableHairstyles.Add(141);
56	        availableHairstyles.Add(142);
57	        availableHairstyles.Add(143);
58	        availableHairstyles.Add(144);
59	        availableHairstyles.Add(147);
60	        availableHairstyles.Add(148);
61	        availableHairstyles.Add(149);
62	        availableHairstyles.Add(150);
63	        availableHairstyles.Add(151);
64	        availableHairstyles.Add(154);
65	        availableHairstyles.Add(155);
66	        availableHairstyles.Add(157);
67	        availableHairstyles.Add(158);
68	        availableHairstyles.Add(161);
69	      }
70	      if (!this._isAtStylist)
71	        return;
72	      for (int index = 51; index < 123; ++index)
73	        availableHairstyles.Add(index);
74	      availableHairstyles.Add(134);
75	      availableHairstyles.Add(135);
76	      availableHairstyles.Add(145);
77	      availableHairstyles.Add(146);
78	      availableHairstyles.Add(152);
79	      availableHairstyles.Add(153);
80	      availableHairstyles.Add(156);
81	      availableHairstyles.Add(159);
82	      availableHairstyles.Add(160);
83	      if (this._defeatedMartians)
84	        availableHairstyles.AddRange((IEnumerable<int>) new int[10]
85	        {
86	          132,
87	          131,
88	          130,
89	          129,
90	          128,
91	          (int) sbyte.MaxValue,
92	          126,
93	          125,
94	          124,
95	          123
96	        });
97	      if (!this._defeatedMartians || !this._defeatedMoonlord)
98	        return;
99	      availableHairstyles.Add(133);
100	    }
101	  }
102	}
103	

```


---

## 🤖 Assistant · 2026-08-09T11:49:16.752Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1456 -iname \"*HairstyleUnlocks*\"; echo \"---\"; grep -n \"numberOfHairstyles\\|hairCount\\|HairCount\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head",
 "description": "Find new hairstyle unlocks helper and count"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:16.796Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/HairstyleUnlocksHelper.cs
---
1393:	public const int numberOfHairstyles = 228;

```


---

## 🤖 Assistant · 2026-08-09T11:49:18.463Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/HairstyleUnlocksHelper.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:18.470Z

**📎 ToolResult**

```
1	using System.Collections.Generic;
2	
3	namespace Terraria.GameContent;
4	
5	public class HairstyleUnlocksHelper
6	{
7		public List<int> AvailableHairstyles = new List<int>();
8	
9		private bool _defeatedMartians;
10	
11		private bool _defeatedMoonlord;
12	
13		private bool _defeatedPlantera;
14	
15		private bool _isAtStylist;
16	
17		private bool _isAtCharacterCreation;
18	
19		public void UpdateUnlocks()
20		{
21			if (ListWarrantsRemake())
22			{
23				RebuildList();
24			}
25		}
26	
27		private bool ListWarrantsRemake()
28		{
29			bool flag = NPC.downedMartians && !Main.gameMenu;
30			bool flag2 = NPC.downedMoonlord && !Main.gameMenu;
31			bool flag3 = NPC.downedPlantBoss && !Main.gameMenu;
32			bool flag4 = Main.hairWindow && !Main.gameMenu;
33			bool gameMenu = Main.gameMenu;
34			bool result = false;
35			if (_defeatedMartians != flag || _defeatedMoonlord != flag2 || _defeatedPlantera != flag3 || _isAtStylist != flag4 || _isAtCharacterCreation != gameMenu)
36			{
37				result = true;
38			}
39			_defeatedMartians = flag;
40			_defeatedMoonlord = flag2;
41			_defeatedPlantera = flag3;
42			_isAtStylist = flag4;
43			_isAtCharacterCreation = gameMenu;
44			return result;
45		}
46	
47		private void RebuildList()
48		{
49			List<int> availableHairstyles = AvailableHairstyles;
50			availableHairstyles.Clear();
51			if (_isAtCharacterCreation || _isAtStylist)
52			{
53				for (int i = 0; i < 51; i++)
54				{
55					availableHairstyles.Add(i);
56				}
57				availableHairstyles.Add(136);
58				availableHairstyles.Add(137);
59				availableHairstyles.Add(138);
60				availableHairstyles.Add(139);
61				availableHairstyles.Add(140);
62				availableHairstyles.Add(141);
63				availableHairstyles.Add(142);
64				availableHairstyles.Add(143);
65				availableHairstyles.Add(144);
66				availableHairstyles.Add(147);
67				availableHairstyles.Add(148);
68				availableHairstyles.Add(149);
69				availableHairstyles.Add(150);
70				availableHairstyles.Add(151);
71				availableHairstyles.Add(154);
72				availableHairstyles.Add(155);
73				availableHairstyles.Add(157);
74				availableHairstyles.Add(158);
75				availableHairstyles.Add(161);
76				for (int j = 51; j < 123; j++)
77				{
78					availableHairstyles.Add(j);
79				}
80				availableHairstyles.Add(134);
81				availableHairstyles.Add(135);
82				availableHairstyles.Add(146);
83				availableHairstyles.Add(152);
84				availableHairstyles.Add(153);
85				availableHairstyles.Add(156);
86				availableHairstyles.Add(159);
87				availableHairstyles.Add(165);
88				availableHairstyles.Add(160);
89				for (int k = 166; k < 228; k++)
90				{
91					availableHairstyles.Add(k);
92				}
93			}
94			if (_isAtStylist)
95			{
96				if (_defeatedPlantera)
97				{
98					availableHairstyles.Add(162);
99					availableHairstyles.Add(164);
100					availableHairstyles.Add(163);
101					availableHairstyles.Add(145);
102				}
103				if (_defeatedMartians)
104				{
105					availableHairstyles.AddRange(new int[10] { 132, 131, 130, 129, 128, 127, 126, 125, 124, 123 });
106				}
107				if (_defeatedMartians && _defeatedMoonlord)
108				{
109					availableHairstyles.Add(133);
110				}
111			}
112		}
113	}
114	

```


---

## 🤖 Assistant · 2026-08-09T11:49:24.484Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Big change: at character creation, available hairstyles in old = 0-50 + list (51 base + 19 = 70 total: 51 + 19 = 70 styles). New = 0-50 + extras + 51-122 + extras + 166-227 → much more (all 228 minus a few locked). Let me count: old char creation: 51 + 19 = 70. New: 51 + 19 + 72 + 9 + 62 = let's count: 0-50 (51), then 9 additions (136-144 = 9), 147-151 (5), 154,155 (2), 157,158 (2), 161 (1) → 19. Then 51-122 (72). Then 134,135,146,152,153,156,165,160 (8). Then 166-227 (62). Total = 51+19+72+8+62 = 212. So 212 hairstyles available at creation in 1.4.5.6 vs 70 in 1.4.0.5.

Total hair count: old Main.numberOfHairstyles = 162? Wait, old Main.cs line 1851 says `public const int numberOfHairstyles = 162;`. But Player.cs old check for hair >= 228? I didn't find it. Let me verify: user says old hairstyles 228. Actually old load code: `player1.hair = binaryReader.ReadInt32();` then check? Let me look at old Player.cs near 35400 and new near 54209.

Also total hairstyles: old 162? Hmm, but user said old 228. Let me check both. Old Main.cs numberOfHairstyles=162 at line 1851. Let me grep new.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:49:25.114Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"numberOfHairstyles\" ~/Project/GLM/SandboxWorld/Terarria1405/Main.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head; echo \"===old load hair===\"; sed -n '35395,35430p' ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs; echo \"===new load hair===\"; sed -n '54200,54220p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs",
 "description": "Compare total hairstyle count and hair load clamp"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:25.160Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:1851:    public const int numberOfHairstyles = 162;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:1393:	public const int numberOfHairstyles = 228;
===old load hair===
              }
              if (num1 >= 138)
                playerFileData.SetPlayTime(new TimeSpan(binaryReader.ReadInt64()));
              else
                playerFileData.SetPlayTime(TimeSpan.Zero);
              player1.hair = binaryReader.ReadInt32();
              if (num1 >= 82)
                player1.hairDye = binaryReader.ReadByte();
              if (num1 >= 124)
              {
                BitsByte bitsByte = (BitsByte) binaryReader.ReadByte();
                for (int index = 0; index < 8; ++index)
                  player1.hideVisibleAccessory[index] = bitsByte[index];
                bitsByte = (BitsByte) binaryReader.ReadByte();
                for (int index = 0; index < 2; ++index)
                  player1.hideVisibleAccessory[index + 8] = bitsByte[index];
              }
              else if (num1 >= 83)
              {
                BitsByte bitsByte = (BitsByte) binaryReader.ReadByte();
                for (int index = 0; index < 8; ++index)
                  player1.hideVisibleAccessory[index] = bitsByte[index];
              }
              if (num1 >= 119)
                player1.hideMisc = (BitsByte) binaryReader.ReadByte();
              if (num1 <= 17)
                player1.Male = player1.hair != 5 && player1.hair != 6 && (player1.hair != 9 && player1.hair != 11);
              else if (num1 < 107)
                player1.Male = binaryReader.ReadBoolean();
              else
                player1.skinVariant = (int) binaryReader.ReadByte();
              if (num1 < 161 && player1.skinVariant == 7)
                player1.skinVariant = 9;
              player1.statLife = binaryReader.ReadInt32();
              player1.statLifeMax = binaryReader.ReadInt32();
              if (player1.statLifeMax > 500)
===new load hair===
		}
		if (release >= 138)
		{
			data.SetPlayTime(new TimeSpan(fileIO.ReadInt64()));
		}
		else
		{
			data.SetPlayTime(TimeSpan.Zero);
		}
		newPlayer.hair = fileIO.ReadInt32();
		if (newPlayer.hair >= 228)
		{
			newPlayer.hair = 0;
		}
		if (release >= 82)
		{
			newPlayer.hairDye = fileIO.ReadByte();
		}
		if (release >= 283)
		{
			newPlayer.team = fileIO.ReadByte();

```


---

## 🤖 Assistant · 2026-08-09T11:49:27.670Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Total hairstyles: old 162, new 228. At char creation available: old 70, new 212.

Now PlayerDrawLayers.cs. This is the big one (2771 old, 4421 new). Focus on Players texture channel mapping (skin/shirt/undershirt/pants/shoes/eye/white), plus how skinVariant maps to texture rows. Let me grep for "Players" texture and the channel usage in both.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:49:28.219Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\\\"Players\\\"\\|Players\\\", \\|TextureAssets.Players\\|GetHairSettings\\|skinVariant\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | head -60",
 "description": "Find Players texture channel usage in old PlayerDrawLayers"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:28.245Z

**📎 ToolResult**

```
818:          drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 3].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorBodySkin, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0)
829:          PlayerDrawLayers.DrawSittingLegs(ref drawinfo, TextureAssets.Players[drawinfo.skinVar, 10].Value, drawinfo.colorLegs, 0, false);
833:          drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 10].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.legFrame), drawinfo.colorLegs, drawinfo.drawPlayer.legRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
897:        drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 3].Value, position, new Rectangle?(drawinfo.compTorsoFrame), drawinfo.colorBodySkin, bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
906:          PlayerDrawLayers.DrawSittingLegs(ref drawinfo, TextureAssets.Players[drawinfo.skinVar, 10].Value, drawinfo.colorLegs, drawinfo.skinDyePacked, false);
910:          drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 10].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.legFrame), drawinfo.colorLegs, drawinfo.drawPlayer.legRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
949:            drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 7].Value, position1, new Rectangle?(drawinfo.compBackArmFrame), drawinfo.colorBodySkin, rotation, origin1, 1f, drawinfo.playerEffect, 0);
957:            drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 5].Value, position1, new Rectangle?(drawinfo.compBackArmFrame), drawinfo.colorBodySkin, rotation, origin1, 1f, drawinfo.playerEffect, 0);
990:            drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 7].Value, position1, new Rectangle?(drawinfo.compBackArmFrame), drawinfo.colorBodySkin, rotation, origin1, 1f, drawinfo.playerEffect, 0);
998:            drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 5].Value, position1, new Rectangle?(drawinfo.compBackArmFrame), drawinfo.colorBodySkin, rotation, origin1, 1f, drawinfo.playerEffect, 0);
1006:          drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 8].Value, position1, new Rectangle?(drawinfo.compBackArmFrame), drawinfo.colorUnderShirt, rotation, origin1, 1f, drawinfo.playerEffect, 0));
1007:          drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 13].Value, position1, new Rectangle?(drawinfo.compBackArmFrame), drawinfo.colorShirt, rotation, origin1, 1f, drawinfo.playerEffect, 0));
1046:          PlayerDrawLayers.DrawSittingLegs(ref drawinfo, TextureAssets.Players[drawinfo.skinVar, 11].Value, drawinfo.colorPants, 0, false);
1047:          PlayerDrawLayers.DrawSittingLegs(ref drawinfo, TextureAssets.Players[drawinfo.skinVar, 12].Value, drawinfo.colorShoes, 0, false);
1106:        DrawData drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 11].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.legFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.legFrame.Height + 4.0)) + drawinfo.drawPlayer.legPosition + drawinfo.legVect, new Rectangle?(drawinfo.drawPlayer.legFrame), drawinfo.colorPants, drawinfo.drawPlayer.legRotation, drawinfo.legVect, 1f, drawinfo.playerEffect, 0);
1108:        drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 12].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.legFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.legFrame.Height + 4.0)) + drawinfo.drawPlayer.legPosition + drawinfo.legVect, new Rectangle?(drawinfo.drawPlayer.legFrame), drawinfo.colorShoes, drawinfo.drawPlayer.legRotation, drawinfo.legVect, 1f, drawinfo.playerEffect, 0);
1199:        PlayerDrawLayers.DrawSittingLegs(ref drawinfo, TextureAssets.Players[drawinfo.skinVar, 14].Value, drawinfo.colorShirt, 0, false);
1203:        DrawData drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 14].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.legFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.legFrame.Height + 4.0)) + drawinfo.drawPlayer.legPosition + drawinfo.legVect, new Rectangle?(drawinfo.drawPlayer.legFrame), drawinfo.colorShirt, drawinfo.drawPlayer.legRotation, drawinfo.legVect, 1f, drawinfo.playerEffect, 0);
1306:        DrawData drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 5].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorBodySkin, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0)
1318:          DrawData drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 4].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorUnderShirt, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
1320:          drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 6].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorShirt, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
1325:          DrawData drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 4].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorUnderShirt, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
1327:          drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 6].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorShirt, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
1330:        DrawData drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 5].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorBodySkin, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0)
1366:        drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 4].Value, position, new Rectangle?(drawinfo.compBackShoulderFrame), drawinfo.colorUnderShirt, bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0));
1367:        drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 6].Value, position, new Rectangle?(drawinfo.compBackShoulderFrame), drawinfo.colorShirt, bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0));
1368:        drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 4].Value, position, new Rectangle?(drawinfo.compTorsoFrame), drawinfo.colorUnderShirt, bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0));
1369:        drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 6].Value, position, new Rectangle?(drawinfo.compTorsoFrame), drawinfo.colorShirt, bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0));
1684:      DrawData drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 0].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
1688:      drawData2 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 1].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorEyeWhites, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
1690:      drawData2 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 2].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorEyes, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
1692:      Asset<Texture2D> player = TextureAssets.Players[drawinfo.skinVar, 15];
2256:            drawData2 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 7].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorBodySkin, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
2261:          drawData2 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 9].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorBodySkin, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
2293:        DrawData drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 7].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorBodySkin, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0)
2298:        drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 8].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorUnderShirt, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
2300:        drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 13].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.bodyPosition + new Vector2((float) (drawinfo.drawPlayer.bodyFrame.Width / 2), (float) (drawinfo.drawPlayer.bodyFrame.Height / 2)), new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorShirt, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect, 0);
2339:                drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 7].Value, position1, new Rectangle?(drawinfo.compFrontArmFrame), drawinfo.colorBodySkin, rotation, origin, 1f, drawinfo.playerEffect, 0);
2347:                drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 9].Value, position1, new Rectangle?(drawinfo.compFrontArmFrame), drawinfo.colorBodySkin, rotation, origin, 1f, drawinfo.playerEffect, 0);
2381:              drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 7].Value, position2, new Rectangle?(drawinfo.compFrontShoulderFrame), drawinfo.colorBodySkin, bodyRotation, origin, 1f, drawinfo.playerEffect, 0);
2386:            drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 8].Value, position2, new Rectangle?(drawinfo.compFrontShoulderFrame), drawinfo.colorUnderShirt, bodyRotation, origin, 1f, drawinfo.playerEffect, 0));
2387:            drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 13].Value, position2, new Rectangle?(drawinfo.compFrontShoulderFrame), drawinfo.colorShirt, bodyRotation, origin, 1f, drawinfo.playerEffect, 0));
2388:            drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 6].Value, position2, new Rectangle?(drawinfo.compFrontShoulderFrame), drawinfo.colorShirt, bodyRotation, origin, 1f, drawinfo.playerEffect, 0));
2395:              drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 7].Value, position1, new Rectangle?(drawinfo.compFrontArmFrame), drawinfo.colorBodySkin, rotation, origin, 1f, drawinfo.playerEffect, 0);
2400:            drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 8].Value, position1, new Rectangle?(drawinfo.compFrontArmFrame), drawinfo.colorUnderShirt, rotation, origin, 1f, drawinfo.playerEffect, 0));
2401:            drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 13].Value, position1, new Rectangle?(drawinfo.compFrontArmFrame), drawinfo.colorShirt, rotation, origin, 1f, drawinfo.playerEffect, 0));
2402:            drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.Players[drawinfo.skinVar, 6].Value, position1, new Rectangle?(drawinfo.compFrontArmFrame), drawinfo.colorShirt, rotation, origin, 1f, drawinfo.playerEffect, 0));

```


---

## 🤖 Assistant · 2026-08-09T11:49:30.390Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now new PlayerDrawLayers channel mapping. Grep the same in new.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:49:31.503Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Players\\[drawinfo.skinVar\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs | sed -E 's/^([0-9]+):.*(Players\\[drawinfo.skinVar, [0-9]+\\]).*/\\1 \\2/' | sort -t, -k2 -n | uniq -c -f1 | sort -rn | head -40; echo \"===distinct channels===\"; grep -o \"Players\\[drawinfo.skinVar, [0-9]*\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs | sort -u -t, -k2 -V; echo \"===OLD distinct channels===\"; grep -o \"Players\\[drawinfo.skinVar, [0-9]*\\]\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | sort -u -t, -k2 -V",
 "description": "List distinct Players texture channels used in both versions"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:49:47.962Z

**📎 ToolResult**

```
   7 1331 Players[drawinfo.skinVar, 7]
   6 1970 Players[drawinfo.skinVar, 6]
   4 1968 Players[drawinfo.skinVar, 4]
   4 1403 Players[drawinfo.skinVar, 13]
   4 1401 Players[drawinfo.skinVar, 8]
   4 1338 Players[drawinfo.skinVar, 5]
   4 1197 Players[drawinfo.skinVar, 10]
   2 3630 Players[drawinfo.skinVar, 9]
   2 1783 Players[drawinfo.skinVar, 14]
   2 1501 Players[drawinfo.skinVar, 12]
   2 1500 Players[drawinfo.skinVar, 11]
   2 1187 Players[drawinfo.skinVar, 3]
   1 2642 Players[drawinfo.skinVar, 15]
   1 2621 Players[drawinfo.skinVar, 2]
   1 2619 Players[drawinfo.skinVar, 1]
   1 2615 Players[drawinfo.skinVar, 0]
===distinct channels===
Players[drawinfo.skinVar, 0]
Players[drawinfo.skinVar, 1]
Players[drawinfo.skinVar, 2]
Players[drawinfo.skinVar, 3]
Players[drawinfo.skinVar, 4]
Players[drawinfo.skinVar, 5]
Players[drawinfo.skinVar, 6]
Players[drawinfo.skinVar, 7]
Players[drawinfo.skinVar, 8]
Players[drawinfo.skinVar, 9]
Players[drawinfo.skinVar, 10]
Players[drawinfo.skinVar, 11]
Players[drawinfo.skinVar, 12]
Players[drawinfo.skinVar, 13]
Players[drawinfo.skinVar, 14]
Players[drawinfo.skinVar, 15]
===OLD distinct channels===
Players[drawinfo.skinVar, 0]
Players[drawinfo.skinVar, 1]
Players[drawinfo.skinVar, 2]
Players[drawinfo.skinVar, 3]
Players[drawinfo.skinVar, 4]
Players[drawinfo.skinVar, 5]
Players[drawinfo.skinVar, 6]
Players[drawinfo.skinVar, 7]
Players[drawinfo.skinVar, 8]
Players[drawinfo.skinVar, 9]
Players[drawinfo.skinVar, 10]
Players[drawinfo.skinVar, 11]
Players[drawinfo.skinVar, 12]
Players[drawinfo.skinVar, 13]
Players[drawinfo.skinVar, 14]
Players[drawinfo.skinVar, 15]

```


---

## 🤖 Assistant · 2026-08-09T11:49:51.037Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Same channel set. Now verify the color mapping per channel in new version — check key lines: head 0, eye whites 1, eyes 2, torso skin 3, undershirt 4, arm skin 5, shirt 6, arm skin 7, undershirt 8, skin 9, legs 10, pants 11, shoes 12, shirt 13, shirt 14. Let me grep with color names in new version.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:49:51.876Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -o \"Players\\[drawinfo.skinVar, [0-9]*\\].\\{0,120\\}\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs | sed -E 's/(Players\\[drawinfo.skinVar, [0-9]+\\]).*(drawinfo.color[A-Za-z]+).*/\\1 -> \\2/' | sort -u -t, -k2 -V",
 "description": "Map channel index to color in new PlayerDrawLayers"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:07.101Z

**📎 ToolResult**

```
Players[drawinfo.skinVar, 0].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 1].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 2].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 3] -> drawinfo.colorBodySkin
Players[drawinfo.skinVar, 3].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 4] -> drawinfo.colorUnderShirt
Players[drawinfo.skinVar, 4].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 5] -> drawinfo.colorBodySkin
Players[drawinfo.skinVar, 5].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 6] -> drawinfo.colorShirt
Players[drawinfo.skinVar, 6].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 7] -> drawinfo.colorBodySkin
Players[drawinfo.skinVar, 7].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 8] -> drawinfo.colorUnderShirt
Players[drawinfo.skinVar, 8].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 9] -> drawinfo.colorBodySkin
Players[drawinfo.skinVar, 9].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 10] -> drawinfo.colorLegs
Players[drawinfo.skinVar, 10].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 11] -> drawinfo.colorPants
Players[drawinfo.skinVar, 11].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.legFrame.Width / 2) 
Players[drawinfo.skinVar, 12] -> drawinfo.colorShoes
Players[drawinfo.skinVar, 12].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.legFrame.Width / 2) 
Players[drawinfo.skinVar, 13] -> drawinfo.colorShirt
Players[drawinfo.skinVar, 13].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2)
Players[drawinfo.skinVar, 14] -> drawinfo.colorShirt
Players[drawinfo.skinVar, 14].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.legFrame.Width / 2) 
Players[drawinfo.skinVar, 15];

```


---

## 🤖 Assistant · 2026-08-09T11:50:11.832Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Channel → color mapping is identical between versions. Good — 通道映射无变化 (0 head, 1 eyeWhites, 2 eyes, 3/5/7/9 bodySkin, 10 legs, 4/8 undershirt, 6/13/14 shirt, 11 pants, 12 shoes, 15 onFemale=... hair/hat hair).

But there may be draw-order changes. Let me check the draw layer order/registration and new layers in PlayerDrawLayers new (e.g., new draw layers added between 1.4.0.5 and 1.4.5.6). Also PlayerDrawSet/skinVar computation and "Male" hair offset etc.

Let me quickly look at struct registrations (AddLayer / layer lists) in both, and also check DrawPlayer_Head changes. Given time constraints, I'll compare layer build lists.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:13.375Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"new PlayerDrawLayer\\|PlayerDrawLayer(\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | wc -l; grep -n \"new PlayerDrawLayer\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs | wc -l; echo \"===old layers===\"; grep -n \"\\\"[A-Za-z]*\\\"\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | grep \"new PlayerDrawLayer\" -A0 | head -0; grep -o 'new PlayerDrawLayer(\"[^\"]*\"' ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | sort -u; echo \"===new layers===\"; grep -o 'new PlayerDrawLayer(\"[^\"]*\"' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs | sort -u",
 "description": "Compare registered draw layer names"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:13.428Z

**📎 ToolResult**

```
       0
       0
===old layers===
head: illegal line count -- 0
===new layers===

```


---

## 🤖 Assistant · 2026-08-09T11:50:15.595Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"static.*PlayerDrawLayer \\|readonly PlayerDrawLayer\\|PlayerDrawLayer [A-Z]\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | head -20; echo \"===\"; grep -rn \"SortedList\\|AddLayer\\|layerList\\|_layerList\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | head -10",
 "description": "Find draw layer registration in old file"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:15.627Z

**📎 ToolResult**

```
===

```


---

## 🤖 Assistant · 2026-08-09T11:50:21.878Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Layer registration likely in PlayerDrawLayers via "PlayerLayer" legacy or in "Terraria.DataStructures.PlayerDrawLayers" with static methods, and the actual layer list in Terraria.Initializers or in Player class `drawOrder`? In 1.4, draw layers are registered in `PlayerDrawLayers` via a static constructor with `new LegacyPlayerLayer`? Actually there's `Terraria.GameContent.Drawing.PlayerDrawingSettings`? The layer list building is in "Terraria.ModLoader"? No — vanilla: `PlayerDrawLayers` has methods `BuildPlayerDrawOrder`? Let me search for "SortMethod" or in PlayerLoader. Actually the layer registration is in Terraria.Initializers/ or in PlayerDrawLayers.cs partial? Let me search for where DrawPlayer is invoked and layer list built: `Main.PlayerRenderer` uses `PlayerDrawLayers` with a list `PlayerDrawLayer.LegacyLayerOrder`? Hmm.

Given the focus of the task (appearance rendering mapping + counts), full layer-list diff is beyond scope. The key rendering questions from the user: channel mapping (unchanged), skinVariant count (unchanged 12), hairstyle count (162 → 228, and creation-available 70 → 212), and UI sizes/animation formula (unchanged).

Let me still check DrawPlayer_Head and hair rendering changes (hair texture frames), since UIHairStyleButton draws head. Also check "DrawPlayerHead" signature change. And check how `skinVar` is computed in PlayerDrawSet (maybe new: skinVar assignment via Male). Let me grep skinVar assignment in both.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:23.616Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"skinVar = \\|skinVar= \" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs; echo \"===head draw===\"; grep -n \"DrawPlayer_Head\\|DrawPlayerHead\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs ~/Project/GLM/SandboxWorld/Terarria1405/Initializers/*.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Initializers/*.cs 2>/dev/null | head; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"PlayerDrawSet.cs\" -o -name \"PlayerRenderer.cs\"; find ~/Project/GLM/SandboxWorld/Terarria1405 -name \"PlayerDrawSet.cs\" -o -name \"PlayerRenderer.cs\"",
 "description": "Locate skinVar computation and head rendering"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:23.657Z

**📎 ToolResult**

```
===head draw===
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs:2359:							int num19 = DrawPlayer_Head_GetTVScreen(drawinfo.drawPlayer);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs:2514:	public static int DrawPlayer_Head_GetTVScreen(Player plr)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawSet.cs
~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawSet.cs

```


---

## 🤖 Assistant · 2026-08-09T11:50:25.869Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"skinVar\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawSet.cs | head; echo \"===NEW===\"; grep -n \"skinVar\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawSet.cs | head; echo \"=== DrawPlayerHead renderer ===\"; find ~/Project/GLM/SandboxWorld/Terarria1405 -name \"*.cs\" -path \"*Drawing*\" | head; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"*.cs\" -path \"*Drawing*\" | head -20",
 "description": "Compare skinVar in PlayerDrawSet and renderer files"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:25.913Z

**📎 ToolResult**

```
31:    public int skinVar;
212:      this.skinVar = this.drawPlayer.skinVariant;
===NEW===
35:	public int skinVar;
368:		skinVar = drawPlayer.skinVariant;
=== DrawPlayerHead renderer ===
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/WindGrid.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/TileDrawing.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/ParticleOrchestraType.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/WallDrawing.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/ParticleOrchestrator.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/Drawing/ParticleOrchestraSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/NextNatureRenderer.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/WindGrid.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/DrawBlackHelper.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/EmptyHorizonRenderer.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/BackgroundGradientDrawer.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/OriginalNatureRenderer.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/INatureRenderer.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/NextHorizonRenderer.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/GetBackgroundDrawWeightMethod.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/ParticleOrchestraType.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/WallDrawing.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/LensFlareElement.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/IHorizonRenderer.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/BackgroundArrayGetterMethod.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/SideFlags.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/ParticleOrchestrator.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/ParticleOrchestraSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawingBase.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/HorizonHelper.cs

```


---

## 🤖 Assistant · 2026-08-09T11:50:27.581Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
skinVar unchanged. Now UICharacterSelect and UICharacterListItem. Read both pairs.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:27.583Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.States/UICharacterSelect.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:50:27.586Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/States/UICharacterSelect.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:27.602Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.UI.States.UICharacterSelect
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using System;
10	using System.Collections.Generic;
11	using System.Linq;
12	using Terraria.Audio;
13	using Terraria.GameContent.UI.Elements;
14	using Terraria.GameInput;
15	using Terraria.ID;
16	using Terraria.IO;
17	using Terraria.Localization;
18	using Terraria.UI;
19	using Terraria.UI.Gamepad;
20	
21	namespace Terraria.GameContent.UI.States
22	{
23	  public class UICharacterSelect : UIState
24	  {
25	    private List<Tuple<string, bool>> favoritesCache = new List<Tuple<string, bool>>();
26	    private UIList _playerList;
27	    private UITextPanel<LocalizedText> _backPanel;
28	    private UITextPanel<LocalizedText> _newPanel;
29	    private UIPanel _containerPanel;
30	    private UIScrollbar _scrollbar;
31	    private bool _isScrollbarAttached;
32	    private bool skipDraw;
33	
34	    public override void OnInitialize()
35	    {
36	      UIElement element = new UIElement();
37	      element.Width.Set(0.0f, 0.8f);
38	      element.MaxWidth.Set(650f, 0.0f);
39	      element.Top.Set(220f, 0.0f);
40	      element.Height.Set(-220f, 1f);
41	      element.HAlign = 0.5f;
42	      UIPanel uiPanel = new UIPanel();
43	      uiPanel.Width.Set(0.0f, 1f);
44	      uiPanel.Height.Set(-110f, 1f);
45	      uiPanel.BackgroundColor = new Color(33, 43, 79) * 0.8f;
46	      this._containerPanel = uiPanel;
47	      element.Append((UIElement) uiPanel);
48	      this._playerList = new UIList();
49	      this._playerList.Width.Set(0.0f, 1f);
50	      this._playerList.Height.Set(0.0f, 1f);
51	      this._playerList.ListPadding = 5f;
52	      uiPanel.Append((UIElement) this._playerList);
53	      this._scrollbar = new UIScrollbar();
54	      this._scrollbar.SetView(100f, 1000f);
55	      this._scrollbar.Height.Set(0.0f, 1f);
56	      this._scrollbar.HAlign = 1f;
57	      this._playerList.SetScrollbar(this._scrollbar);
58	      UITextPanel<LocalizedText> uiTextPanel1 = new UITextPanel<LocalizedText>(Language.GetText("UI.SelectPlayer"), 0.8f, true);
59	      uiTextPanel1.HAlign = 0.5f;
60	      uiTextPanel1.Top.Set(-40f, 0.0f);
61	      uiTextPanel1.SetPadding(15f);
62	      uiTextPanel1.BackgroundColor = new Color(73, 94, 171);
63	      element.Append((UIElement) uiTextPanel1);
64	      UITextPanel<LocalizedText> uiTextPanel2 = new UITextPanel<LocalizedText>(Language.GetText("UI.Back"), 0.7f, true);
65	      uiTextPanel2.Width.Set(-10f, 0.5f);
66	      uiTextPanel2.Height.Set(50f, 0.0f);
67	      uiTextPanel2.VAlign = 1f;
68	      uiTextPanel2.Top.Set(-45f, 0.0f);
69	      uiTextPanel2.OnMouseOver += new UIElement.MouseEvent(this.FadedMouseOver);
70	      uiTextPanel2.OnMouseOut += new UIElement.MouseEvent(this.FadedMouseOut);
71	      uiTextPanel2.OnClick += new UIElement.MouseEvent(this.GoBackClick);
72	      uiTextPanel2.SetSnapPoint("Back", 0, new Vector2?(), new Vector2?());
73	      element.Append((UIElement) uiTextPanel2);
74	      this._backPanel = uiTextPanel2;
75	      UITextPanel<LocalizedText> uiTextPanel3 = new UITextPanel<LocalizedText>(Language.GetText("UI.New"), 0.7f, true);
76	      uiTextPanel3.CopyStyle((UIElement) uiTextPanel2);
77	      uiTextPanel3.HAlign = 1f;
78	      uiTextPanel3.OnMouseOver += new UIElement.MouseEvent(this.FadedMouseOver);
79	      uiTextPanel3.OnMouseOut += new UIElement.MouseEvent(this.FadedMouseOut);
80	      uiTextPanel3.OnClick += new UIElement.MouseEvent(this.NewCharacterClick);
81	      element.Append((UIElement) uiTextPanel3);
82	      uiTextPanel2.SetSnapPoint("New", 0, new Vector2?(), new Vector2?());
83	      this._newPanel = uiTextPanel3;
84	      this.Append(element);
85	    }
86	
87	    public override void Recalculate()
88	    {
89	      if (this._scrollbar != null)
90	      {
91	        if (this._isScrollbarAttached && !this._scrollbar.CanScroll)
92	        {
93	          this._containerPanel.RemoveChild((UIElement) this._scrollbar);
94	          this._isScrollbarAttached = false;
95	          this._playerList.Width.Set(0.0f, 1f);
96	        }
97	        else if (!this._isScrollbarAttached && this._scrollbar.CanScroll)
98	        {
99	          this._containerPanel.Append((UIElement) this._scrollbar);
100	          this._isScrollbarAttached = true;
101	          this._playerList.Width.Set(-25f, 1f);
102	        }
103	      }
104	      base.Recalculate();
105	    }
106	
107	    private void NewCharacterClick(UIMouseEvent evt, UIElement listeningElement)
108	    {
109	      SoundEngine.PlaySound(10, -1, -1, 1, 1f, 0.0f);
110	      Main.PendingPlayer = new Player();
111	      Main.MenuUI.SetState((UIState) new UICharacterCreation(Main.PendingPlayer));
112	      Main.menuMode = 888;
113	    }
114	
115	    private void GoBackClick(UIMouseEvent evt, UIElement listeningElement)
116	    {
117	      SoundEngine.PlaySound(11, -1, -1, 1, 1f, 0.0f);
118	      Main.menuMode = 0;
119	    }
120	
121	    private void FadedMouseOver(UIMouseEvent evt, UIElement listeningElement)
122	    {
123	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
124	      ((UIPanel) evt.Target).BackgroundColor = new Color(73, 94, 171);
125	      ((UIPanel) evt.Target).BorderColor = Colors.FancyUIFatButtonMouseOver;
126	    }
127	
128	    private void FadedMouseOut(UIMouseEvent evt, UIElement listeningElement)
129	    {
130	      ((UIPanel) evt.Target).BackgroundColor = new Color(63, 82, 151) * 0.7f;
131	      ((UIPanel) evt.Target).BorderColor = Color.Black;
132	    }
133	
134	    public override void OnActivate()
135	    {
136	      Main.LoadPlayers();
137	      Main.ActivePlayerFileData = new PlayerFileData();
138	      this.UpdatePlayersList();
139	      if (!PlayerInput.UsingGamepadUI)
140	        return;
141	      UILinkPointNavigator.ChangePoint(3000 + (this._playerList.Count == 0 ? 1 : 2));
142	    }
143	
144	    private void UpdatePlayersList()
145	    {
146	      this._playerList.Clear();
147	      List<PlayerFileData> playerFileDataList = new List<PlayerFileData>((IEnumerable<PlayerFileData>) Main.PlayerList);
148	      playerFileDataList.Sort((Comparison<PlayerFileData>) ((x, y) =>
149	      {
150	        if (x.IsFavorite && !y.IsFavorite)
151	          return -1;
152	        if (!x.IsFavorite && y.IsFavorite)
153	          return 1;
154	        return x.Name.CompareTo(y.Name) != 0 ? x.Name.CompareTo(y.Name) : x.GetFileName(true).CompareTo(y.GetFileName(true));
155	      }));
156	      int num = 0;
157	      foreach (PlayerFileData data in playerFileDataList)
158	        this._playerList.Add((UIElement) new UICharacterListItem(data, num++));
159	    }
160	
161	    public override void Draw(SpriteBatch spriteBatch)
162	    {
163	      if (this.skipDraw)
164	      {
165	        this.skipDraw = false;
166	      }
167	      else
168	      {
169	        if (this.UpdateFavoritesCache())
170	        {
171	          this.skipDraw = true;
172	          Main.MenuUI.Draw(spriteBatch, new GameTime());
173	        }
174	        base.Draw(spriteBatch);
175	        this.SetupGamepadPoints(spriteBatch);
176	      }
177	    }
178	
179	    private bool UpdateFavoritesCache()
180	    {
181	      List<PlayerFileData> playerFileDataList = new List<PlayerFileData>((IEnumerable<PlayerFileData>) Main.PlayerList);
182	      playerFileDataList.Sort((Comparison<PlayerFileData>) ((x, y) =>
183	      {
184	        if (x.IsFavorite && !y.IsFavorite)
185	          return -1;
186	        if (!x.IsFavorite && y.IsFavorite)
187	          return 1;
188	        return x.Name.CompareTo(y.Name) != 0 ? x.Name.CompareTo(y.Name) : x.GetFileName(true).CompareTo(y.GetFileName(true));
189	      }));
190	      bool flag = false;
191	      if (!flag && playerFileDataList.Count != this.favoritesCache.Count)
192	        flag = true;
193	      if (!flag)
194	      {
195	        for (int index = 0; index < this.favoritesCache.Count; ++index)
196	        {
197	          Tuple<string, bool> tuple = this.favoritesCache[index];
198	          if (!(playerFileDataList[index].Name == tuple.Item1) || playerFileDataList[index].IsFavorite != tuple.Item2)
199	          {
200	            flag = true;
201	            break;
202	          }
203	        }
204	      }
205	      if (flag)
206	      {
207	        this.favoritesCache.Clear();
208	        foreach (PlayerFileData playerFileData in playerFileDataList)
209	          this.favoritesCache.Add(Tuple.Create<string, bool>(playerFileData.Name, playerFileData.IsFavorite));
210	        this.UpdatePlayersList();
211	      }
212	      return flag;
213	    }
214	
215	    private void SetupGamepadPoints(SpriteBatch spriteBatch)
216	    {
217	      UILinkPointNavigator.Shortcuts.BackButtonCommand = 1;
218	      int ID1 = 3000;
219	      UILinkPointNavigator.SetPosition(ID1, this._backPanel.GetInnerDimensions().ToRectangle().Center.ToVector2());
220	      UILinkPointNavigator.SetPosition(ID1 + 1, this._newPanel.GetInnerDimensions().ToRectangle().Center.ToVector2());
221	      int index1 = ID1;
222	      UILinkPoint point1 = UILinkPointNavigator.Points[index1];
223	      point1.Unlink();
224	      point1.Right = index1 + 1;
225	      int index2 = ID1 + 1;
226	      UILinkPoint point2 = UILinkPointNavigator.Points[index2];
227	      point2.Unlink();
228	      point2.Left = index2 - 1;
229	      float num = 1f / Main.UIScale;
230	      Rectangle clippingRectangle = this._containerPanel.GetClippingRectangle(spriteBatch);
231	      Vector2 minimum = clippingRectangle.TopLeft() * num;
232	      Vector2 maximum = clippingRectangle.BottomRight() * num;
233	      List<SnapPoint> snapPoints = this.GetSnapPoints();
234	      for (int index3 = 0; index3 < snapPoints.Count; ++index3)
235	      {
236	        if (!snapPoints[index3].Position.Between(minimum, maximum))
237	        {
238	          snapPoints.Remove(snapPoints[index3]);
239	          --index3;
240	        }
241	      }
242	      SnapPoint[,] snapPointArray = new SnapPoint[this._playerList.Count, 4];
243	      foreach (SnapPoint snapPoint in snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Play")))
244	        snapPointArray[snapPoint.Id, 0] = snapPoint;
245	      foreach (SnapPoint snapPoint in snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Favorite")))
246	        snapPointArray[snapPoint.Id, 1] = snapPoint;
247	      foreach (SnapPoint snapPoint in snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Cloud")))
248	        snapPointArray[snapPoint.Id, 2] = snapPoint;
249	      foreach (SnapPoint snapPoint in snapPoints.Where<SnapPoint>((Func<SnapPoint, bool>) (a => a.Name == "Delete")))
250	        snapPointArray[snapPoint.Id, 3] = snapPoint;
251	      int ID2 = ID1 + 2;
252	      int[] numArray = new int[this._playerList.Count];
253	      for (int index3 = 0; index3 < numArray.Length; ++index3)
254	        numArray[index3] = -1;
255	      for (int index3 = 0; index3 < 4; ++index3)
256	      {
257	        int index4 = -1;
258	        for (int index5 = 0; index5 < snapPointArray.GetLength(0); ++index5)
259	        {
260	          if (snapPointArray[index5, index3] != null)
261	          {
262	            UILinkPoint point3 = UILinkPointNavigator.Points[ID2];
263	            point3.Unlink();
264	            UILinkPointNavigator.SetPosition(ID2, snapPointArray[index5, index3].Position);
265	            if (index4 != -1)
266	            {
267	              point3.Up = index4;
268	              UILinkPointNavigator.Points[index4].Down = ID2;
269	            }
270	            if (numArray[index5] != -1)
271	            {
272	              point3.Left = numArray[index5];
273	              UILinkPointNavigator.Points[numArray[index5]].Right = ID2;
274	            }
275	            point3.Down = ID1;
276	            if (index3 == 0)
277	              UILinkPointNavigator.Points[ID1].Up = UILinkPointNavigator.Points[ID1 + 1].Up = ID2;
278	            index4 = ID2;
279	            numArray[index5] = ID2;
280	            UILinkPointNavigator.Shortcuts.FANCYUI_HIGHEST_INDEX = ID2;
281	            ++ID2;
282	          }
283	        }
284	      }
285	      if (!PlayerInput.UsingGamepadUI || this._playerList.Count != 0 || UILinkPointNavigator.CurrentPoint <= 3001)
286	        return;
287	      UILinkPointNavigator.ChangePoint(3001);
288	    }
289	  }
290	}
291	

```


---

## 👤 User(sidechain) · 2026-08-09T11:50:27.603Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using System.Linq;
4	using Microsoft.Xna.Framework;
5	using Microsoft.Xna.Framework.Graphics;
6	using Terraria.Audio;
7	using Terraria.GameContent.UI.Elements;
8	using Terraria.GameInput;
9	using Terraria.ID;
10	using Terraria.IO;
11	using Terraria.Localization;
12	using Terraria.UI;
13	using Terraria.UI.Gamepad;
14	
15	namespace Terraria.GameContent.UI.States;
16	
17	public class UICharacterSelect : UIState
18	{
19		private UIList _playerList;
20	
21		private UITextPanel<LocalizedText> _backPanel;
22	
23		private UITextPanel<LocalizedText> _newPanel;
24	
25		private UIPanel _containerPanel;
26	
27		private UIScrollbar _scrollbar;
28	
29		private bool _isScrollbarAttached;
30	
31		private List<Tuple<string, bool>> favoritesCache = new List<Tuple<string, bool>>();
32	
33		private bool skipDraw;
34	
35		public override void OnInitialize()
36		{
37			UIElement uIElement = new UIElement();
38			uIElement.Width.Set(0f, 0.8f);
39			uIElement.MaxWidth.Set(650f, 0f);
40			uIElement.Top.Set(220f, 0f);
41			uIElement.Height.Set(-220f, 1f);
42			uIElement.HAlign = 0.5f;
43			UIPanel uIPanel = new UIPanel();
44			uIPanel.Width.Set(0f, 1f);
45			uIPanel.Height.Set(-110f, 1f);
46			uIPanel.BackgroundColor = new Color(33, 43, 79) * 0.8f;
47			_containerPanel = uIPanel;
48			uIElement.Append(uIPanel);
49			_playerList = new UIList();
50			_playerList.Width.Set(0f, 1f);
51			_playerList.Height.Set(0f, 1f);
52			_playerList.ListPadding = 5f;
53			uIPanel.Append(_playerList);
54			_scrollbar = new UIScrollbar();
55			_scrollbar.SetView(100f, 1000f);
56			_scrollbar.Height.Set(0f, 1f);
57			_scrollbar.HAlign = 1f;
58			_playerList.SetScrollbar(_scrollbar);
59			UITextPanel<LocalizedText> uITextPanel = new UITextPanel<LocalizedText>(Language.GetText("UI.SelectPlayer"), 0.8f, large: true);
60			uITextPanel.HAlign = 0.5f;
61			uITextPanel.Top.Set(-40f, 0f);
62			uITextPanel.SetPadding(15f);
63			uITextPanel.BackgroundColor = new Color(73, 94, 171);
64			uIElement.Append(uITextPanel);
65			UITextPanel<LocalizedText> uITextPanel2 = new UITextPanel<LocalizedText>(Language.GetText("UI.Back"), 0.7f, large: true);
66			uITextPanel2.Width.Set(-10f, 0.5f);
67			uITextPanel2.Height.Set(50f, 0f);
68			uITextPanel2.VAlign = 1f;
69			uITextPanel2.Top.Set(-45f, 0f);
70			uITextPanel2.OnMouseOver += FadedMouseOver;
71			uITextPanel2.OnMouseOut += FadedMouseOut;
72			uITextPanel2.OnLeftClick += GoBackClick;
73			uITextPanel2.SetSnapPoint("Back", 0);
74			uIElement.Append(uITextPanel2);
75			_backPanel = uITextPanel2;
76			UITextPanel<LocalizedText> uITextPanel3 = new UITextPanel<LocalizedText>(Language.GetText("UI.New"), 0.7f, large: true);
77			uITextPanel3.CopyStyle(uITextPanel2);
78			uITextPanel3.HAlign = 1f;
79			uITextPanel3.OnMouseOver += FadedMouseOver;
80			uITextPanel3.OnMouseOut += FadedMouseOut;
81			uITextPanel3.OnLeftClick += NewCharacterClick;
82			uIElement.Append(uITextPanel3);
83			uITextPanel2.SetSnapPoint("New", 0);
84			_newPanel = uITextPanel3;
85			Append(uIElement);
86		}
87	
88		public override void Recalculate()
89		{
90			if (_scrollbar != null)
91			{
92				if (_isScrollbarAttached && !_scrollbar.CanScroll)
93				{
94					_containerPanel.RemoveChild(_scrollbar);
95					_isScrollbarAttached = false;
96					_playerList.Width.Set(0f, 1f);
97				}
98				else if (!_isScrollbarAttached && _scrollbar.CanScroll)
99				{
100					_containerPanel.Append(_scrollbar);
101					_isScrollbarAttached = true;
102					_playerList.Width.Set(-25f, 1f);
103				}
104			}
105			base.Recalculate();
106		}
107	
108		private void NewCharacterClick(UIMouseEvent evt, UIElement listeningElement)
109		{
110			SoundEngine.PlaySound(10);
111			Main.PendingPlayer = new Player();
112			Main.menuMode = 888;
113			Main.MenuUI.SetState(new UICharacterCreation(Main.PendingPlayer));
114		}
115	
116		private void GoBackClick(UIMouseEvent evt, UIElement listeningElement)
117		{
118			SoundEngine.PlaySound(11);
119			Main.menuMode = 0;
120		}
121	
122		private void FadedMouseOver(UIMouseEvent evt, UIElement listeningElement)
123		{
124			SoundEngine.PlaySound(12);
125			((UIPanel)evt.Target).BackgroundColor = new Color(73, 94, 171);
126			((UIPanel)evt.Target).BorderColor = Colors.FancyUIFatButtonMouseOver;
127		}
128	
129		private void FadedMouseOut(UIMouseEvent evt, UIElement listeningElement)
130		{
131			((UIPanel)evt.Target).BackgroundColor = new Color(63, 82, 151) * 0.7f;
132			((UIPanel)evt.Target).BorderColor = Color.Black;
133		}
134	
135		public override void OnActivate()
136		{
137			Main.LoadPlayers();
138			Main.ActivePlayerFileData = new PlayerFileData();
139			UpdatePlayersList();
140			if (PlayerInput.UsingGamepadUI)
141			{
142				UILinkPointNavigator.ChangePoint(3000 + ((_playerList.Count == 0) ? 1 : 2));
143			}
144		}
145	
146		private void UpdatePlayersList()
147		{
148			_playerList.Clear();
149			IOrderedEnumerable<PlayerFileData> orderedEnumerable = from x in Main.PlayerList
150				orderby x.IsFavorite descending, x.LastPlayed descending, x.Name, x.GetFileName()
151				select x;
152			int num = 0;
153			foreach (PlayerFileData item in orderedEnumerable)
154			{
155				_playerList.Add(new UICharacterListItem(item, num++));
156			}
157		}
158	
159		public override void Draw(SpriteBatch spriteBatch)
160		{
161			if (skipDraw)
162			{
163				skipDraw = false;
164				return;
165			}
166			if (UpdateFavoritesCache())
167			{
168				skipDraw = true;
169				Main.MenuUI.Draw(spriteBatch, new GameTime());
170			}
171			base.Draw(spriteBatch);
172			SetupGamepadPoints(spriteBatch);
173		}
174	
175		private bool UpdateFavoritesCache()
176		{
177			List<PlayerFileData> list = new List<PlayerFileData>(Main.PlayerList);
178			list.Sort(delegate(PlayerFileData x, PlayerFileData y)
179			{
180				if (x.IsFavorite && !y.IsFavorite)
181				{
182					return -1;
183				}
184				if (!x.IsFavorite && y.IsFavorite)
185				{
186					return 1;
187				}
188				return (x.Name.CompareTo(y.Name) != 0) ? x.Name.CompareTo(y.Name) : x.GetFileName().CompareTo(y.GetFileName());
189			});
190			bool flag = false;
191			if (!flag && list.Count != favoritesCache.Count)
192			{
193				flag = true;
194			}
195			if (!flag)
196			{
197				for (int num = 0; num < favoritesCache.Count; num++)
198				{
199					Tuple<string, bool> tuple = favoritesCache[num];
200					if (!(list[num].Name == tuple.Item1) || list[num].IsFavorite != tuple.Item2)
201					{
202						flag = true;
203						break;
204					}
205				}
206			}
207			if (flag)
208			{
209				favoritesCache.Clear();
210				foreach (PlayerFileData item in list)
211				{
212					favoritesCache.Add(Tuple.Create(item.Name, item.IsFavorite));
213				}
214				UpdatePlayersList();
215			}
216			return flag;
217		}
218	
219		private void SetupGamepadPoints(SpriteBatch spriteBatch)
220		{
221			UILinkPointNavigator.Shortcuts.BackButtonCommand = 1;
222			int num = 3000;
223			UILinkPointNavigator.SetPosition(num, _backPanel.GetInnerDimensions().ToRectangle().Center.ToVector2());
224			UILinkPointNavigator.SetPosition(num + 1, _newPanel.GetInnerDimensions().ToRectangle().Center.ToVector2());
225			int num2 = num;
226			UILinkPoint uILinkPoint = UILinkPointNavigator.Points[num2];
227			uILinkPoint.Unlink();
228			uILinkPoint.Right = num2 + 1;
229			num2 = num + 1;
230			uILinkPoint = UILinkPointNavigator.Points[num2];
231			uILinkPoint.Unlink();
232			uILinkPoint.Left = num2 - 1;
233			float num3 = 1f / Main.UIScale;
234			Rectangle clippingRectangle = _containerPanel.GetClippingRectangle(spriteBatch);
235			Vector2 minimum = clippingRectangle.TopLeft() * num3;
236			Vector2 maximum = clippingRectangle.BottomRight() * num3;
237			List<SnapPoint> snapPoints = GetSnapPoints();
238			for (int i = 0; i < snapPoints.Count; i++)
239			{
240				if (!snapPoints[i].Position.Between(minimum, maximum))
241				{
242					snapPoints.Remove(snapPoints[i]);
243					i--;
244				}
245			}
246			int num4 = 5;
247			SnapPoint[,] array = new SnapPoint[_playerList.Count, num4];
248			foreach (SnapPoint item in snapPoints.Where((SnapPoint a) => a.Name == "Play"))
249			{
250				array[item.Id, 0] = item;
251			}
252			foreach (SnapPoint item2 in snapPoints.Where((SnapPoint a) => a.Name == "Favorite"))
253			{
254				array[item2.Id, 1] = item2;
255			}
256			foreach (SnapPoint item3 in snapPoints.Where((SnapPoint a) => a.Name == "Cloud"))
257			{
258				array[item3.Id, 2] = item3;
259			}
260			foreach (SnapPoint item4 in snapPoints.Where((SnapPoint a) => a.Name == "Rename"))
261			{
262				array[item4.Id, 3] = item4;
263			}
264			foreach (SnapPoint item5 in snapPoints.Where((SnapPoint a) => a.Name == "Delete"))
265			{
266				array[item5.Id, 4] = item5;
267			}
268			num2 = num + 2;
269			int[] array2 = new int[_playerList.Count];
270			for (int num5 = 0; num5 < array2.Length; num5++)
271			{
272				array2[num5] = -1;
273			}
274			for (int num6 = 0; num6 < num4; num6++)
275			{
276				int num7 = -1;
277				for (int num8 = 0; num8 < array.GetLength(0); num8++)
278				{
279					if (array[num8, num6] != null)
280					{
281						uILinkPoint = UILinkPointNavigator.Points[num2];
282						uILinkPoint.Unlink();
283						UILinkPointNavigator.SetPosition(num2, array[num8, num6].Position);
284						if (num7 != -1)
285						{
286							uILinkPoint.Up = num7;
287							UILinkPointNavigator.Points[num7].Down = num2;
288						}
289						if (array2[num8] != -1)
290						{
291							uILinkPoint.Left = array2[num8];
292							UILinkPointNavigator.Points[array2[num8]].Right = num2;
293						}
294						uILinkPoint.Down = num;
295						if (num6 == 0)
296						{
297							UILinkPointNavigator.Points[num].Up = (UILinkPointNavigator.Points[num + 1].Up = num2);
298						}
299						num7 = num2;
300						array2[num8] = num2;
301						UILinkPointNavigator.Shortcuts.FANCYUI_HIGHEST_INDEX = num2;
302						num2++;
303					}
304				}
305			}
306			if (PlayerInput.UsingGamepadUI && _playerList.Count == 0 && UILinkPointNavigator.CurrentPoint > 3001)
307			{
308				UILinkPointNavigator.ChangePoint(3001);
309			}
310		}
311	}
312	

```


---

## 🤖 Assistant · 2026-08-09T11:50:33.942Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
UICharacterSelect changes:
- Sort order: old favorite-then-name; new adds LastPlayed descending (order by IsFavorite desc, LastPlayed desc, Name, FileName) at lines 149-151.
- New gamepad snap point column "Rename" added (5 columns vs 4) — reflects UICharacterListItem new rename button.
- Event name OnClick → OnLeftClick.

Now UICharacterListItem both.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:34.214Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UICharacterListItem.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:50:34.218Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UICharacterListItem.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:34.232Z

**📎 ToolResult**

```
1	using System;
2	using Microsoft.Xna.Framework;
3	using Microsoft.Xna.Framework.Graphics;
4	using ReLogic.Content;
5	using Terraria.Audio;
6	using Terraria.GameContent.UI.States;
7	using Terraria.ID;
8	using Terraria.IO;
9	using Terraria.Localization;
10	using Terraria.Social;
11	using Terraria.UI;
12	
13	namespace Terraria.GameContent.UI.Elements;
14	
15	public class UICharacterListItem : UIPanel
16	{
17		private PlayerFileData _data;
18	
19		private Asset<Texture2D> _dividerTexture;
20	
21		private Asset<Texture2D> _innerPanelTexture;
22	
23		private UICharacter _playerPanel;
24	
25		private UIText _buttonLabel;
26	
27		private UIText _deleteButtonLabel;
28	
29		private Asset<Texture2D> _buttonCloudActiveTexture;
30	
31		private Asset<Texture2D> _buttonCloudInactiveTexture;
32	
33		private Asset<Texture2D> _buttonFavoriteActiveTexture;
34	
35		private Asset<Texture2D> _buttonFavoriteInactiveTexture;
36	
37		private Asset<Texture2D> _buttonPlayTexture;
38	
39		private Asset<Texture2D> _buttonRenameTexture;
40	
41		private Asset<Texture2D> _buttonDeleteTexture;
42	
43		private UIImageButton _deleteButton;
44	
45		private int _orderInList;
46	
47		public bool IsFavorite => _data.IsFavorite;
48	
49		public UICharacterListItem(PlayerFileData data, int orderInList)
50		{
51			BorderColor = new Color(89, 116, 213) * 0.7f;
52			_dividerTexture = Main.Assets.Request<Texture2D>("Images/UI/Divider", (AssetRequestMode)1);
53			_innerPanelTexture = Main.Assets.Request<Texture2D>("Images/UI/InnerPanelBackground", (AssetRequestMode)1);
54			_buttonCloudActiveTexture = Main.Assets.Request<Texture2D>("Images/UI/ButtonCloudActive", (AssetRequestMode)1);
55			_buttonCloudInactiveTexture = Main.Assets.Request<Texture2D>("Images/UI/ButtonCloudInactive", (AssetRequestMode)1);
56			_buttonFavoriteActiveTexture = Main.Assets.Request<Texture2D>("Images/UI/ButtonFavoriteActive", (AssetRequestMode)1);
57			_buttonFavoriteInactiveTexture = Main.Assets.Request<Texture2D>("Images/UI/ButtonFavoriteInactive", (AssetRequestMode)1);
58			_buttonPlayTexture = Main.Assets.Request<Texture2D>("Images/UI/ButtonPlay", (AssetRequestMode)1);
59			_buttonRenameTexture = Main.Assets.Request<Texture2D>("Images/UI/ButtonRename", (AssetRequestMode)1);
60			_buttonDeleteTexture = Main.Assets.Request<Texture2D>("Images/UI/ButtonDelete", (AssetRequestMode)1);
61			Height.Set(96f, 0f);
62			Width.Set(0f, 1f);
63			SetPadding(6f);
64			_data = data;
65			_orderInList = orderInList;
66			_playerPanel = new UICharacter(data.Player, animated: false, hasBackPanel: true, 1f, useAClone: true);
67			_playerPanel.Left.Set(4f, 0f);
68			_playerPanel.OnLeftDoubleClick += PlayGame;
69			base.OnLeftDoubleClick += PlayGame;
70			Append(_playerPanel);
71			float num = 4f;
72			UIImageButton uIImageButton = new UIImageButton(_buttonPlayTexture);
73			uIImageButton.VAlign = 1f;
74			uIImageButton.Left.Set(num, 0f);
75			uIImageButton.OnLeftClick += PlayGame;
76			uIImageButton.OnMouseOver += PlayMouseOver;
77			uIImageButton.OnMouseOut += ButtonMouseOut;
78			Append(uIImageButton);
79			num += 24f;
80			UIImageButton uIImageButton2 = new UIImageButton(_data.IsFavorite ? _buttonFavoriteActiveTexture : _buttonFavoriteInactiveTexture);
81			uIImageButton2.VAlign = 1f;
82			uIImageButton2.Left.Set(num, 0f);
83			uIImageButton2.OnLeftClick += FavoriteButtonClick;
84			uIImageButton2.OnMouseOver += FavoriteMouseOver;
85			uIImageButton2.OnMouseOut += ButtonMouseOut;
86			uIImageButton2.SetVisibility(1f, _data.IsFavorite ? 0.8f : 0.4f);
87			Append(uIImageButton2);
88			num += 24f;
89			if (SocialAPI.Cloud != null)
90			{
91				UIImageButton uIImageButton3 = new UIImageButton(_data.IsCloudSave ? _buttonCloudActiveTexture : _buttonCloudInactiveTexture);
92				uIImageButton3.VAlign = 1f;
93				uIImageButton3.Left.Set(num, 0f);
94				uIImageButton3.OnLeftClick += CloudButtonClick;
95				uIImageButton3.OnMouseOver += CloudMouseOver;
96				uIImageButton3.OnMouseOut += ButtonMouseOut;
97				Append(uIImageButton3);
98				uIImageButton3.SetSnapPoint("Cloud", orderInList);
99				num += 24f;
100			}
101			UIImageButton uIImageButton4 = new UIImageButton(_buttonRenameTexture);
102			uIImageButton4.VAlign = 1f;
103			uIImageButton4.Left.Set(num, 0f);
104			uIImageButton4.OnLeftClick += RenameButtonClick;
105			uIImageButton4.OnMouseOver += RenameMouseOver;
106			uIImageButton4.OnMouseOut += ButtonMouseOut;
107			Append(uIImageButton4);
108			num += 24f;
109			UIImageButton uIImageButton5 = new UIImageButton(_buttonDeleteTexture)
110			{
111				VAlign = 1f,
112				HAlign = 1f
113			};
114			if (!_data.IsFavorite)
115			{
116				uIImageButton5.OnLeftClick += DeleteButtonClick;
117			}
118			uIImageButton5.OnMouseOver += DeleteMouseOver;
119			uIImageButton5.OnMouseOut += DeleteMouseOut;
120			_deleteButton = uIImageButton5;
121			Append(uIImageButton5);
122			num += 4f;
123			_buttonLabel = new UIText("");
124			_buttonLabel.VAlign = 1f;
125			_buttonLabel.Left.Set(num, 0f);
126			_buttonLabel.Top.Set(-3f, 0f);
127			Append(_buttonLabel);
128			_deleteButtonLabel = new UIText("");
129			_deleteButtonLabel.VAlign = 1f;
130			_deleteButtonLabel.HAlign = 1f;
131			_deleteButtonLabel.Left.Set(-30f, 0f);
132			_deleteButtonLabel.Top.Set(-3f, 0f);
133			Append(_deleteButtonLabel);
134			uIImageButton.SetSnapPoint("Play", orderInList);
135			uIImageButton2.SetSnapPoint("Favorite", orderInList);
136			uIImageButton4.SetSnapPoint("Rename", orderInList);
137			uIImageButton5.SetSnapPoint("Delete", orderInList);
138		}
139	
140		private void RenameMouseOver(UIMouseEvent evt, UIElement listeningElement)
141		{
142			_buttonLabel.SetText(Language.GetTextValue("UI.Rename"));
143		}
144	
145		private void FavoriteMouseOver(UIMouseEvent evt, UIElement listeningElement)
146		{
147			if (_data.IsFavorite)
148			{
149				_buttonLabel.SetText(Language.GetTextValue("UI.Unfavorite"));
150			}
151			else
152			{
153				_buttonLabel.SetText(Language.GetTextValue("UI.Favorite"));
154			}
155		}
156	
157		private void CloudMouseOver(UIMouseEvent evt, UIElement listeningElement)
158		{
159			if (_data.IsCloudSave)
160			{
161				_buttonLabel.SetText(Language.GetTextValue("UI.MoveOffCloud"));
162			}
163			else
164			{
165				_buttonLabel.SetText(Language.GetTextValue("UI.MoveToCloud"));
166			}
167		}
168	
169		private void PlayMouseOver(UIMouseEvent evt, UIElement listeningElement)
170		{
171			_buttonLabel.SetText(Language.GetTextValue("UI.Play"));
172		}
173	
174		private void DeleteMouseOver(UIMouseEvent evt, UIElement listeningElement)
175		{
176			if (_data.IsFavorite)
177			{
178				_deleteButtonLabel.SetText(Language.GetTextValue("UI.CannotDeleteFavorited"));
179			}
180			else
181			{
182				_deleteButtonLabel.SetText(Language.GetTextValue("UI.Delete"));
183			}
184		}
185	
186		private void DeleteMouseOut(UIMouseEvent evt, UIElement listeningElement)
187		{
188			_deleteButtonLabel.SetText("");
189		}
190	
191		private void ButtonMouseOut(UIMouseEvent evt, UIElement listeningElement)
192		{
193			_buttonLabel.SetText("");
194		}
195	
196		private void RenameButtonClick(UIMouseEvent evt, UIElement listeningElement)
197		{
198			SoundEngine.PlaySound(10);
199			Main.clrInput();
200			UIVirtualKeyboard state = new UIVirtualKeyboard(Lang.menu[45].Value, _data.Name, OnFinishedSettingName, GoBackHere, 0, allowEmpty: true);
201			Main.MenuUI.SetState(state);
202			if (base.Parent.Parent is UIList uIList)
203			{
204				uIList.UpdateOrder();
205			}
206		}
207	
208		private void OnFinishedSettingName(string name)
209		{
210			string newName = name.Trim();
211			Main.menuMode = 10;
212			_data.Rename(newName);
213			Main.OpenCharacterSelectUI();
214		}
215	
216		private void GoBackHere()
217		{
218			Main.OpenCharacterSelectUI();
219		}
220	
221		private void CloudButtonClick(UIMouseEvent evt, UIElement listeningElement)
222		{
223			if (_data.IsCloudSave)
224			{
225				_data.MoveToLocal();
226			}
227			else
228			{
229				_data.MoveToCloud();
230			}
231			((UIImageButton)evt.Target).SetImage(_data.IsCloudSave ? _buttonCloudActiveTexture : _buttonCloudInactiveTexture);
232			if (_data.IsCloudSave)
233			{
234				_buttonLabel.SetText(Language.GetTextValue("UI.MoveOffCloud"));
235			}
236			else
237			{
238				_buttonLabel.SetText(Language.GetTextValue("UI.MoveToCloud"));
239			}
240		}
241	
242		private void DeleteButtonClick(UIMouseEvent evt, UIElement listeningElement)
243		{
244			for (int i = 0; i < Main.PlayerList.Count; i++)
245			{
246				if (Main.PlayerList[i] == _data)
247				{
248					SoundEngine.PlaySound(10);
249					Main.selectedPlayer = i;
250					Main.menuMode = 5;
251					break;
252				}
253			}
254		}
255	
256		private void PlayGame(UIMouseEvent evt, UIElement listeningElement)
257		{
258			if (listeningElement == evt.Target && _data.Player.loadStatus == StatusID.Ok)
259			{
260				Main.SelectPlayer(_data);
261			}
262		}
263	
264		private void FavoriteButtonClick(UIMouseEvent evt, UIElement listeningElement)
265		{
266			_data.ToggleFavorite();
267			((UIImageButton)evt.Target).SetImage(_data.IsFavorite ? _buttonFavoriteActiveTexture : _buttonFavoriteInactiveTexture);
268			((UIImageButton)evt.Target).SetVisibility(1f, _data.IsFavorite ? 0.8f : 0.4f);
269			if (_data.IsFavorite)
270			{
271				_buttonLabel.SetText(Language.GetTextValue("UI.Unfavorite"));
272				_deleteButton.OnLeftClick -= DeleteButtonClick;
273			}
274			else
275			{
276				_buttonLabel.SetText(Language.GetTextValue("UI.Favorite"));
277				_deleteButton.OnLeftClick += DeleteButtonClick;
278			}
279			if (base.Parent.Parent is UIList uIList)
280			{
281				uIList.UpdateOrder();
282			}
283		}
284	
285		public override int CompareTo(object obj)
286		{
287			if (obj is UICharacterListItem uICharacterListItem)
288			{
289				return _orderInList.CompareTo(uICharacterListItem._orderInList);
290			}
291			return base.CompareTo(obj);
292		}
293	
294		public override void MouseOver(UIMouseEvent evt)
295		{
296			base.MouseOver(evt);
297			BackgroundColor = new Color(73, 94, 171);
298			BorderColor = new Color(89, 116, 213);
299			_playerPanel.SetAnimated(animated: true);
300		}
301	
302		public override void MouseOut(UIMouseEvent evt)
303		{
304			base.MouseOut(evt);
305			BackgroundColor = new Color(63, 82, 151) * 0.7f;
306			BorderColor = new Color(89, 116, 213) * 0.7f;
307			_playerPanel.SetAnimated(animated: false);
308		}
309	
310		private void DrawPanel(SpriteBatch spriteBatch, Vector2 position, float width)
311		{
312			spriteBatch.Draw(_innerPanelTexture.Value, position, new Rectangle(0, 0, 8, _innerPanelTexture.Height()), Color.White);
313			spriteBatch.Draw(_innerPanelTexture.Value, new Vector2(position.X + 8f, position.Y), new Rectangle(8, 0, 8, _innerPanelTexture.Height()), Color.White, 0f, Vector2.Zero, new Vector2((width - 16f) / 8f, 1f), SpriteEffects.None, 0f);
314			spriteBatch.Draw(_innerPanelTexture.Value, new Vector2(position.X + width - 8f, position.Y), new Rectangle(16, 0, 8, _innerPanelTexture.Height()), Color.White);
315		}
316	
317		protected override void DrawSelf(SpriteBatch spriteBatch)
318		{
319			base.DrawSelf(spriteBatch);
320			CalculatedStyle innerDimensions = GetInnerDimensions();
321			CalculatedStyle dimensions = _playerPanel.GetDimensions();
322			float num = dimensions.X + dimensions.Width;
323			Color color = Color.White;
324			string text = _data.Name;
325			if (_data.Player.loadStatus != StatusID.Ok)
326			{
327				color = Color.Gray;
328				string name = StatusID.Search.GetName(_data.Player.loadStatus);
329				text = "(" + name + ") " + text;
330			}
331			Utils.DrawBorderString(spriteBatch, text, new Vector2(num + 6f, dimensions.Y - 2f), color);
332			spriteBatch.Draw(_dividerTexture.Value, new Vector2(num, innerDimensions.Y + 21f), null, Color.White, 0f, Vector2.Zero, new Vector2((GetDimensions().X + GetDimensions().Width - num) / 8f, 1f), SpriteEffects.None, 0f);
333			Vector2 vector = new Vector2(num + 6f, innerDimensions.Y + 29f);
334			float num2 = 200f;
335			Vector2 vector2 = vector;
336			DrawPanel(spriteBatch, vector2, num2);
337			spriteBatch.Draw(TextureAssets.Heart.Value, vector2 + new Vector2(5f, 2f), Color.White);
338			vector2.X += 10f + (float)TextureAssets.Heart.Width();
339			Utils.DrawBorderString(spriteBatch, _data.Player.statLifeMax + Language.GetTextValue("GameUI.PlayerLifeMax"), vector2 + new Vector2(0f, 3f), Color.White);
340			vector2.X += 65f;
341			spriteBatch.Draw(TextureAssets.Mana.Value, vector2 + new Vector2(5f, 2f), Color.White);
342			vector2.X += 10f + (float)TextureAssets.Mana.Width();
343			Utils.DrawBorderString(spriteBatch, _data.Player.statManaMax + Language.GetTextValue("GameUI.PlayerManaMax"), vector2 + new Vector2(0f, 3f), Color.White);
344			vector.X += num2 + 5f;
345			Vector2 vector3 = vector;
346			float num3 = 140f;
347			if (GameCulture.FromCultureName(GameCulture.CultureName.Russian).IsActive)
348			{
349				num3 = 180f;
350			}
351			DrawPanel(spriteBatch, vector3, num3);
352			string text2 = "";
353			Color color2 = Color.White;
354			switch (_data.Player.difficulty)
355			{
356			case 0:
357				text2 = Language.GetTextValue("UI.Softcore");
358				break;
359			case 1:
360				text2 = Language.GetTextValue("UI.Mediumcore");
361				color2 = Main.mcColor;
362				break;
363			case 2:
364				text2 = Language.GetTextValue("UI.Hardcore");
365				color2 = Main.hcColor;
366				break;
367			case 3:
368				text2 = Language.GetTextValue("UI.Creative");
369				color2 = Main.creativeModeColor;
370				break;
371			}
372			vector3 += new Vector2(num3 * 0.5f - FontAssets.MouseText.Value.MeasureString(text2).X * 0.5f, 3f);
373			Utils.DrawBorderString(spriteBatch, text2, vector3, color2);
374			vector.X += num3 + 5f;
375			Vector2 vector4 = vector;
376			float num4 = innerDimensions.X + innerDimensions.Width - vector4.X;
377			DrawPanel(spriteBatch, vector4, num4);
378			TimeSpan playTime = _data.GetPlayTime();
379			int num5 = playTime.Days * 24 + playTime.Hours;
380			string text3 = ((num5 < 10) ? "0" : "") + num5 + playTime.ToString("\\:mm\\:ss");
381			vector4 += new Vector2(num4 * 0.5f - FontAssets.MouseText.Value.MeasureString(text3).X * 0.5f, 3f);
382			Utils.DrawBorderString(spriteBatch, text3, vector4, Color.White);
383		}
384	}
385	

```


---

## 👤 User(sidechain) · 2026-08-09T11:50:34.233Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.UI.Elements.UICharacterListItem
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using ReLogic.Content;
10	using System;
11	using Terraria.Audio;
12	using Terraria.IO;
13	using Terraria.Localization;
14	using Terraria.Social;
15	using Terraria.UI;
16	
17	namespace Terraria.GameContent.UI.Elements
18	{
19	  public class UICharacterListItem : UIPanel
20	  {
21	    private PlayerFileData _data;
22	    private Asset<Texture2D> _dividerTexture;
23	    private Asset<Texture2D> _innerPanelTexture;
24	    private UICharacter _playerPanel;
25	    private UIText _buttonLabel;
26	    private UIText _deleteButtonLabel;
27	    private Asset<Texture2D> _buttonCloudActiveTexture;
28	    private Asset<Texture2D> _buttonCloudInactiveTexture;
29	    private Asset<Texture2D> _buttonFavoriteActiveTexture;
30	    private Asset<Texture2D> _buttonFavoriteInactiveTexture;
31	    private Asset<Texture2D> _buttonPlayTexture;
32	    private Asset<Texture2D> _buttonDeleteTexture;
33	    private UIImageButton _deleteButton;
34	
35	    public bool IsFavorite
36	    {
37	      get
38	      {
39	        return this._data.IsFavorite;
40	      }
41	    }
42	
43	    public UICharacterListItem(PlayerFileData data, int snapPointIndex)
44	    {
45	      this.BorderColor = new Color(89, 116, 213) * 0.7f;
46	      this._dividerTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/Divider", (AssetRequestMode) 1);
47	      this._innerPanelTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/InnerPanelBackground", (AssetRequestMode) 1);
48	      this._buttonCloudActiveTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/ButtonCloudActive", (AssetRequestMode) 1);
49	      this._buttonCloudInactiveTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/ButtonCloudInactive", (AssetRequestMode) 1);
50	      this._buttonFavoriteActiveTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/ButtonFavoriteActive", (AssetRequestMode) 1);
51	      this._buttonFavoriteInactiveTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/ButtonFavoriteInactive", (AssetRequestMode) 1);
52	      this._buttonPlayTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/ButtonPlay", (AssetRequestMode) 1);
53	      this._buttonDeleteTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/ButtonDelete", (AssetRequestMode) 1);
54	      this.Height.Set(96f, 0.0f);
55	      this.Width.Set(0.0f, 1f);
56	      this.SetPadding(6f);
57	      this._data = data;
58	      this._playerPanel = new UICharacter(data.Player, false, true, 1f);
59	      this._playerPanel.Left.Set(4f, 0.0f);
60	      this._playerPanel.OnDoubleClick += new UIElement.MouseEvent(this.PlayGame);
61	      this.OnDoubleClick += new UIElement.MouseEvent(this.PlayGame);
62	      this.Append((UIElement) this._playerPanel);
63	      UIImageButton uiImageButton1 = new UIImageButton(this._buttonPlayTexture);
64	      uiImageButton1.VAlign = 1f;
65	      uiImageButton1.Left.Set(4f, 0.0f);
66	      uiImageButton1.OnClick += new UIElement.MouseEvent(this.PlayGame);
67	      uiImageButton1.OnMouseOver += new UIElement.MouseEvent(this.PlayMouseOver);
68	      uiImageButton1.OnMouseOut += new UIElement.MouseEvent(this.ButtonMouseOut);
69	      this.Append((UIElement) uiImageButton1);
70	      UIImageButton uiImageButton2 = new UIImageButton(this._data.IsFavorite ? this._buttonFavoriteActiveTexture : this._buttonFavoriteInactiveTexture);
71	      uiImageButton2.VAlign = 1f;
72	      uiImageButton2.Left.Set(28f, 0.0f);
73	      uiImageButton2.OnClick += new UIElement.MouseEvent(this.FavoriteButtonClick);
74	      uiImageButton2.OnMouseOver += new UIElement.MouseEvent(this.FavoriteMouseOver);
75	      uiImageButton2.OnMouseOut += new UIElement.MouseEvent(this.ButtonMouseOut);
76	      uiImageButton2.SetVisibility(1f, this._data.IsFavorite ? 0.8f : 0.4f);
77	      this.Append((UIElement) uiImageButton2);
78	      if (SocialAPI.Cloud != null)
79	      {
80	        UIImageButton uiImageButton3 = new UIImageButton(this._data.IsCloudSave ? this._buttonCloudActiveTexture : this._buttonCloudInactiveTexture);
81	        uiImageButton3.VAlign = 1f;
82	        uiImageButton3.Left.Set(52f, 0.0f);
83	        uiImageButton3.OnClick += new UIElement.MouseEvent(this.CloudButtonClick);
84	        uiImageButton3.OnMouseOver += new UIElement.MouseEvent(this.CloudMouseOver);
85	        uiImageButton3.OnMouseOut += new UIElement.MouseEvent(this.ButtonMouseOut);
86	        this.Append((UIElement) uiImageButton3);
87	        uiImageButton3.SetSnapPoint("Cloud", snapPointIndex, new Vector2?(), new Vector2?());
88	      }
89	      UIImageButton uiImageButton4 = new UIImageButton(this._buttonDeleteTexture);
90	      uiImageButton4.VAlign = 1f;
91	      uiImageButton4.HAlign = 1f;
92	      if (!this._data.IsFavorite)
93	        uiImageButton4.OnClick += new UIElement.MouseEvent(this.DeleteButtonClick);
94	      uiImageButton4.OnMouseOver += new UIElement.MouseEvent(this.DeleteMouseOver);
95	      uiImageButton4.OnMouseOut += new UIElement.MouseEvent(this.DeleteMouseOut);
96	      this._deleteButton = uiImageButton4;
97	      this.Append((UIElement) uiImageButton4);
98	      this._buttonLabel = new UIText("", 1f, false);
99	      this._buttonLabel.VAlign = 1f;
100	      this._buttonLabel.Left.Set(80f, 0.0f);
101	      this._buttonLabel.Top.Set(-3f, 0.0f);
102	      this.Append((UIElement) this._buttonLabel);
103	      this._deleteButtonLabel = new UIText("", 1f, false);
104	      this._deleteButtonLabel.VAlign = 1f;
105	      this._deleteButtonLabel.HAlign = 1f;
106	      this._deleteButtonLabel.Left.Set(-30f, 0.0f);
107	      this._deleteButtonLabel.Top.Set(-3f, 0.0f);
108	      this.Append((UIElement) this._deleteButtonLabel);
109	      uiImageButton1.SetSnapPoint("Play", snapPointIndex, new Vector2?(), new Vector2?());
110	      uiImageButton2.SetSnapPoint("Favorite", snapPointIndex, new Vector2?(), new Vector2?());
111	      uiImageButton4.SetSnapPoint("Delete", snapPointIndex, new Vector2?(), new Vector2?());
112	    }
113	
114	    private void FavoriteMouseOver(UIMouseEvent evt, UIElement listeningElement)
115	    {
116	      if (this._data.IsFavorite)
117	        this._buttonLabel.SetText(Language.GetTextValue("UI.Unfavorite"));
118	      else
119	        this._buttonLabel.SetText(Language.GetTextValue("UI.Favorite"));
120	    }
121	
122	    private void CloudMouseOver(UIMouseEvent evt, UIElement listeningElement)
123	    {
124	      if (this._data.IsCloudSave)
125	        this._buttonLabel.SetText(Language.GetTextValue("UI.MoveOffCloud"));
126	      else
127	        this._buttonLabel.SetText(Language.GetTextValue("UI.MoveToCloud"));
128	    }
129	
130	    private void PlayMouseOver(UIMouseEvent evt, UIElement listeningElement)
131	    {
132	      this._buttonLabel.SetText(Language.GetTextValue("UI.Play"));
133	    }
134	
135	    private void DeleteMouseOver(UIMouseEvent evt, UIElement listeningElement)
136	    {
137	      if (this._data.IsFavorite)
138	        this._deleteButtonLabel.SetText(Language.GetTextValue("UI.CannotDeleteFavorited"));
139	      else
140	        this._deleteButtonLabel.SetText(Language.GetTextValue("UI.Delete"));
141	    }
142	
143	    private void DeleteMouseOut(UIMouseEvent evt, UIElement listeningElement)
144	    {
145	      this._deleteButtonLabel.SetText("");
146	    }
147	
148	    private void ButtonMouseOut(UIMouseEvent evt, UIElement listeningElement)
149	    {
150	      this._buttonLabel.SetText("");
151	    }
152	
153	    private void CloudButtonClick(UIMouseEvent evt, UIElement listeningElement)
154	    {
155	      if (this._data.IsCloudSave)
156	        this._data.MoveToLocal();
157	      else
158	        this._data.MoveToCloud();
159	      ((UIImageButton) evt.Target).SetImage(this._data.IsCloudSave ? this._buttonCloudActiveTexture : this._buttonCloudInactiveTexture);
160	      if (this._data.IsCloudSave)
161	        this._buttonLabel.SetText(Language.GetTextValue("UI.MoveOffCloud"));
162	      else
163	        this._buttonLabel.SetText(Language.GetTextValue("UI.MoveToCloud"));
164	    }
165	
166	    private void DeleteButtonClick(UIMouseEvent evt, UIElement listeningElement)
167	    {
168	      for (int index = 0; index < Main.PlayerList.Count; ++index)
169	      {
170	        if (Main.PlayerList[index] == this._data)
171	        {
172	          SoundEngine.PlaySound(10, -1, -1, 1, 1f, 0.0f);
173	          Main.selectedPlayer = index;
174	          Main.menuMode = 5;
175	          break;
176	        }
177	      }
178	    }
179	
180	    private void PlayGame(UIMouseEvent evt, UIElement listeningElement)
181	    {
182	      if (listeningElement != evt.Target || this._data.Player.loadStatus != 0)
183	        return;
184	      Main.SelectPlayer(this._data);
185	    }
186	
187	    private void FavoriteButtonClick(UIMouseEvent evt, UIElement listeningElement)
188	    {
189	      this._data.ToggleFavorite();
190	      ((UIImageButton) evt.Target).SetImage(this._data.IsFavorite ? this._buttonFavoriteActiveTexture : this._buttonFavoriteInactiveTexture);
191	      ((UIImageButton) evt.Target).SetVisibility(1f, this._data.IsFavorite ? 0.8f : 0.4f);
192	      if (this._data.IsFavorite)
193	      {
194	        this._buttonLabel.SetText(Language.GetTextValue("UI.Unfavorite"));
195	        this._deleteButton.OnClick -= new UIElement.MouseEvent(this.DeleteButtonClick);
196	      }
197	      else
198	      {
199	        this._buttonLabel.SetText(Language.GetTextValue("UI.Favorite"));
200	        this._deleteButton.OnClick += new UIElement.MouseEvent(this.DeleteButtonClick);
201	      }
202	      if (!(this.Parent.Parent is UIList parent))
203	        return;
204	      parent.UpdateOrder();
205	    }
206	
207	    public override int CompareTo(object obj)
208	    {
209	      if (!(obj is UICharacterListItem characterListItem))
210	        return base.CompareTo(obj);
211	      if (this.IsFavorite && !characterListItem.IsFavorite)
212	        return -1;
213	      if (!this.IsFavorite && characterListItem.IsFavorite)
214	        return 1;
215	      return this._data.Name.CompareTo(characterListItem._data.Name) != 0 ? this._data.Name.CompareTo(characterListItem._data.Name) : this._data.GetFileName(true).CompareTo(characterListItem._data.GetFileName(true));
216	    }
217	
218	    public override void MouseOver(UIMouseEvent evt)
219	    {
220	      base.MouseOver(evt);
221	      this.BackgroundColor = new Color(73, 94, 171);
222	      this.BorderColor = new Color(89, 116, 213);
223	      this._playerPanel.SetAnimated(true);
224	    }
225	
226	    public override void MouseOut(UIMouseEvent evt)
227	    {
228	      base.MouseOut(evt);
229	      this.BackgroundColor = new Color(63, 82, 151) * 0.7f;
230	      this.BorderColor = new Color(89, 116, 213) * 0.7f;
231	      this._playerPanel.SetAnimated(false);
232	    }
233	
234	    private void DrawPanel(SpriteBatch spriteBatch, Vector2 position, float width)
235	    {
236	      spriteBatch.Draw(this._innerPanelTexture.Value, position, new Rectangle?(new Rectangle(0, 0, 8, this._innerPanelTexture.Height())), Color.White);
237	      spriteBatch.Draw(this._innerPanelTexture.Value, new Vector2(position.X + 8f, position.Y), new Rectangle?(new Rectangle(8, 0, 8, this._innerPanelTexture.Height())), Color.White, 0.0f, Vector2.Zero, new Vector2((float) (((double) width - 16.0) / 8.0), 1f), SpriteEffects.None, 0.0f);
238	      spriteBatch.Draw(this._innerPanelTexture.Value, new Vector2((float) ((double) position.X + (double) width - 8.0), position.Y), new Rectangle?(new Rectangle(16, 0, 8, this._innerPanelTexture.Height())), Color.White);
239	    }
240	
241	    protected override void DrawSelf(SpriteBatch spriteBatch)
242	    {
243	      base.DrawSelf(spriteBatch);
244	      CalculatedStyle innerDimensions = this.GetInnerDimensions();
245	      CalculatedStyle dimensions = this._playerPanel.GetDimensions();
246	      float x = dimensions.X + dimensions.Width;
247	      Utils.DrawBorderString(spriteBatch, this._data.Name, new Vector2(x + 6f, dimensions.Y - 2f), Color.White, 1f, 0.0f, 0.0f, -1);
248	      spriteBatch.Draw(this._dividerTexture.Value, new Vector2(x, innerDimensions.Y + 21f), new Rectangle?(), Color.White, 0.0f, Vector2.Zero, new Vector2((float) (((double) this.GetDimensions().X + (double) this.GetDimensions().Width - (double) x) / 8.0), 1f), SpriteEffects.None, 0.0f);
249	      Vector2 vector2 = new Vector2(x + 6f, innerDimensions.Y + 29f);
250	      float width1 = 200f;
251	      Vector2 position1 = vector2;
252	      this.DrawPanel(spriteBatch, position1, width1);
253	      spriteBatch.Draw(TextureAssets.Heart.Value, position1 + new Vector2(5f, 2f), Color.White);
254	      position1.X += 10f + (float) TextureAssets.Heart.Width();
255	      Utils.DrawBorderString(spriteBatch, this._data.Player.statLifeMax.ToString() + Language.GetTextValue("GameUI.PlayerLifeMax"), position1 + new Vector2(0.0f, 3f), Color.White, 1f, 0.0f, 0.0f, -1);
256	      position1.X += 65f;
257	      spriteBatch.Draw(TextureAssets.Mana.Value, position1 + new Vector2(5f, 2f), Color.White);
258	      position1.X += 10f + (float) TextureAssets.Mana.Width();
259	      Utils.DrawBorderString(spriteBatch, this._data.Player.statManaMax.ToString() + Language.GetTextValue("GameUI.PlayerManaMax"), position1 + new Vector2(0.0f, 3f), Color.White, 1f, 0.0f, 0.0f, -1);
260	      vector2.X += width1 + 5f;
261	      Vector2 position2 = vector2;
262	      float width2 = 140f;
263	      if (GameCulture.FromCultureName(GameCulture.CultureName.Russian).IsActive)
264	        width2 = 180f;
265	      this.DrawPanel(spriteBatch, position2, width2);
266	      string text1 = "";
267	      Color color = Color.White;
268	      switch (this._data.Player.difficulty)
269	      {
270	        case 0:
271	          text1 = Language.GetTextValue("UI.Softcore");
272	          break;
273	        case 1:
274	          text1 = Language.GetTextValue("UI.Mediumcore");
275	          color = Main.mcColor;
276	          break;
277	        case 2:
278	          text1 = Language.GetTextValue("UI.Hardcore");
279	          color = Main.hcColor;
280	          break;
281	        case 3:
282	          text1 = Language.GetTextValue("UI.Creative");
283	          color = Main.creativeModeColor;
284	          break;
285	      }
286	      Vector2 pos1 = position2 + new Vector2((float) ((double) width2 * 0.5 - (double) FontAssets.MouseText.Value.MeasureString(text1).X * 0.5), 3f);
287	      Utils.DrawBorderString(spriteBatch, text1, pos1, color, 1f, 0.0f, 0.0f, -1);
288	      vector2.X += width2 + 5f;
289	      Vector2 position3 = vector2;
290	      float width3 = innerDimensions.X + innerDimensions.Width - position3.X;
291	      this.DrawPanel(spriteBatch, position3, width3);
292	      TimeSpan playTime = this._data.GetPlayTime();
293	      int num = playTime.Days * 24 + playTime.Hours;
294	      string text2 = (num < 10 ? (object) "0" : (object) "").ToString() + (object) num + playTime.ToString("\\:mm\\:ss");
295	      Vector2 pos2 = position3 + new Vector2((float) ((double) width3 * 0.5 - (double) FontAssets.MouseText.Value.MeasureString(text2).X * 0.5), 3f);
296	      Utils.DrawBorderString(spriteBatch, text2, pos2, Color.White, 1f, 0.0f, 0.0f, -1);
297	    }
298	  }
299	}
300	

```


---

## 🤖 Assistant · 2026-08-09T11:50:38.398Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
UICharacterListItem changes:
- New Rename button (ButtonRename texture), positions computed via running `num` offset (buttonLabel at num+4 instead of fixed 80).
- `_playerPanel` created with `useAClone: true` (serialized clone so animations don't mutate original).
- CompareTo uses _orderInList instead of favorite/name.
- DrawSelf: name prefixed with loadStatus name + gray if loadStatus != Ok.
- Snap points: Rename added.

Now a few more checks:
1. UIDifficultyButton differences (layout/colors). Quick diff.
2. DrawPlayerHead signature / hair rendering in new (PlayerDrawLayers head method) — check head draw hair handling changes (e.g. hairDye, hatHair). The user asked mainly about channel mapping; verified unchanged.
3. Check `Player.Male` determination from skinVariant in new? In new UICharacterCreation there's no explicit gender button; Click_CharClothStyle sets skinVariant and presumably Player.skinVariant setter updates Male? Check Player.cs skinVariant property.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:39.784Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"skinVariant\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | sed -n '1,15p'; echo \"===setter new===\"; grep -n \"int skinVariant\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs; grep -n -A6 \"public int skinVariant\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | head -20; echo \"===old===\"; grep -n \"int skinVariant\" ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs; grep -n -A6 \"public int skinVariant\" ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs | head -20",
 "description": "Compare skinVariant property definition"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:39.825Z

**📎 ToolResult**

```
1232:	public int skinVariant;
3247:			return PlayerVariantID.Sets.Male[skinVariant];
3255:					skinVariant = PlayerVariantID.Sets.AltGenderReference[skinVariant];
3260:				skinVariant = PlayerVariantID.Sets.AltGenderReference[skinVariant];
53478:		skinVariant = other.skinVariant;
53823:		fileIO.Write((byte)newPlayer.skinVariant);
54264:			newPlayer.skinVariant = fileIO.ReadByte();
54266:		if (release < 161 && newPlayer.skinVariant == 7)
54268:			newPlayer.skinVariant = 9;
54779:			newPlayer.skinVariant = (int)MathHelper.Clamp(newPlayer.skinVariant, 0f, PlayerVariantID.Count - 1);
54877:		newPlayer.skinVariant = (int)MathHelper.Clamp(newPlayer.skinVariant, 0f, PlayerVariantID.Count - 1);
===setter new===
1232:	public int skinVariant;
1232:	public int skinVariant;
1233-
1234-	public int voiceVariant;
1235-
1236-	public float voicePitchOffset;
1237-
1238-	public bool ghost;
===old===
418:    public int skinVariant;
418:    public int skinVariant;
419-    public bool ghost;
420-    public int ghostFrame;
421-    public int ghostFrameCounter;
422-    public int miscTimer;
423-    public bool pvpDeath;
424-    public bool boneArmor;

```


---

## 🤖 Assistant · 2026-08-09T11:50:41.843Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
skinVariant is a plain field in both; Male is auto-derived: `return PlayerVariantID.Sets.Male[skinVariant];` (new line 3247 — Male property getter). Old? Check old Male getter.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:42.042Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -B4 -A8 \"public bool Male\" ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs | head -40; echo \"===NEW===\"; sed -n '3240,3270p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs",
 "description": "Compare Male property getters"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:42.077Z

**📎 ToolResult**

```
1156-        return (float) this.miscCounter / 300f;
1157-      }
1158-    }
1159-
1160:    public bool Male
1161-    {
1162-      get
1163-      {
1164-        return PlayerVariantID.Sets.Male[this.skinVariant];
1165-      }
1166-      set
1167-      {
1168-        if (value)
===NEW===

	public float miscCounterNormalized => (float)miscCounter / 300f;

	public bool Male
	{
		get
		{
			return PlayerVariantID.Sets.Male[skinVariant];
		}
		set
		{
			if (value)
			{
				if (!Male)
				{
					skinVariant = PlayerVariantID.Sets.AltGenderReference[skinVariant];
				}
			}
			else if (Male)
			{
				skinVariant = PlayerVariantID.Sets.AltGenderReference[skinVariant];
			}
		}
	}

	public bool ZoneDungeon
	{
		get
		{
			return zone1[0];
		}

```


---

## 🤖 Assistant · 2026-08-09T11:50:43.973Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Same Male logic. Now check UIDifficultyButton diff quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:44.360Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIDifficultyButton.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIDifficultyButton.cs; grep -n \"Width\\|Height\\|Left\\|Top\\|FillPercent\\|Slider\\|ContainsPoint\\|corruption\\|crimson\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIDifficultyButton.cs | head -25",
 "description": "Compare UIDifficultyButton files"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:44.402Z

**📎 ToolResult**

```
      94 ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIDifficultyButton.cs
     100 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIDifficultyButton.cs
     194 total
32:		Width = StyleDimension.FromPixels(44f);
33:		Height = StyleDimension.FromPixels(110f);
42:			Width = StyleDimension.FromPixelsAndPercent(-10f, 1f),
43:			Top = StyleDimension.FromPixels(5f)
64:		if (dimensions.Height < 30f)
71:		Utils.DrawSplicedPanel(spriteBatch, _BasePanelTexture.Value, (int)dimensions.X, (int)dimensions.Y, (int)dimensions.Width, (int)dimensions.Height, num2, num2, num3, num3, Color.Lerp(Color.Black, _color, 0.8f) * 0.5f);
74:			Utils.DrawSplicedPanel(spriteBatch, _BasePanelTexture.Value, (int)dimensions.X + num, (int)dimensions.Y + num - 2, (int)dimensions.Width - num * 2, (int)dimensions.Height - num * 2, num2, num2, num3, num3, Color.Lerp(_color, Color.White, 0.7f) * 0.5f);
78:			Utils.DrawSplicedPanel(spriteBatch, _hoveredBorderTexture.Value, (int)dimensions.X, (int)dimensions.Y, (int)dimensions.Width, (int)dimensions.Height, num2, num2, num3, num3, Color.White);
82:	public override void LeftMouseDown(UIMouseEvent evt)
86:		base.LeftMouseDown(evt);

```


---

## 🤖 Assistant · 2026-08-09T11:50:45.970Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.UI.Elements/UIDifficultyButton.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:50:45.972Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/GameContent/UI/Elements/UIDifficultyButton.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:45.977Z

**📎 ToolResult**

```
1	using Microsoft.Xna.Framework;
2	using Microsoft.Xna.Framework.Graphics;
3	using ReLogic.Content;
4	using Terraria.Audio;
5	using Terraria.Localization;
6	using Terraria.UI;
7	
8	namespace Terraria.GameContent.UI.Elements;
9	
10	public class UIDifficultyButton : UIElement
11	{
12		private readonly Player _player;
13	
14		private readonly Asset<Texture2D> _BasePanelTexture;
15	
16		private readonly Asset<Texture2D> _selectedBorderTexture;
17	
18		private readonly Asset<Texture2D> _hoveredBorderTexture;
19	
20		private readonly byte _difficulty;
21	
22		private readonly Color _color;
23	
24		private bool _hovered;
25	
26		private bool _soundedHover;
27	
28		public UIDifficultyButton(Player player, LocalizedText title, LocalizedText description, byte difficulty, Color color)
29		{
30			_player = player;
31			_difficulty = difficulty;
32			Width = StyleDimension.FromPixels(44f);
33			Height = StyleDimension.FromPixels(110f);
34			_BasePanelTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/PanelGrayscale", (AssetRequestMode)1);
35			_selectedBorderTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode)1);
36			_hoveredBorderTexture = Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelBorder", (AssetRequestMode)1);
37			_color = color;
38			UIText element = new UIText(title, 0.9f)
39			{
40				HAlign = 0.5f,
41				VAlign = 0f,
42				Width = StyleDimension.FromPixelsAndPercent(-10f, 1f),
43				Top = StyleDimension.FromPixels(5f)
44			};
45			Append(element);
46		}
47	
48		protected override void DrawSelf(SpriteBatch spriteBatch)
49		{
50			if (_hovered)
51			{
52				if (!_soundedHover)
53				{
54					SoundEngine.PlaySound(12);
55				}
56				_soundedHover = true;
57			}
58			else
59			{
60				_soundedHover = false;
61			}
62			CalculatedStyle dimensions = GetDimensions();
63			int num = 7;
64			if (dimensions.Height < 30f)
65			{
66				num = 5;
67			}
68			int num2 = 10;
69			int num3 = 10;
70			bool num4 = _difficulty == _player.difficulty;
71			Utils.DrawSplicedPanel(spriteBatch, _BasePanelTexture.Value, (int)dimensions.X, (int)dimensions.Y, (int)dimensions.Width, (int)dimensions.Height, num2, num2, num3, num3, Color.Lerp(Color.Black, _color, 0.8f) * 0.5f);
72			if (num4)
73			{
74				Utils.DrawSplicedPanel(spriteBatch, _BasePanelTexture.Value, (int)dimensions.X + num, (int)dimensions.Y + num - 2, (int)dimensions.Width - num * 2, (int)dimensions.Height - num * 2, num2, num2, num3, num3, Color.Lerp(_color, Color.White, 0.7f) * 0.5f);
75			}
76			if (_hovered)
77			{
78				Utils.DrawSplicedPanel(spriteBatch, _hoveredBorderTexture.Value, (int)dimensions.X, (int)dimensions.Y, (int)dimensions.Width, (int)dimensions.Height, num2, num2, num3, num3, Color.White);
79			}
80		}
81	
82		public override void LeftMouseDown(UIMouseEvent evt)
83		{
84			_player.difficulty = _difficulty;
85			SoundEngine.PlaySound(12);
86			base.LeftMouseDown(evt);
87		}
88	
89		public override void MouseOver(UIMouseEvent evt)
90		{
91			base.MouseOver(evt);
92			_hovered = true;
93		}
94	
95		public override void MouseOut(UIMouseEvent evt)
96		{
97			base.MouseOut(evt);
98			_hovered = false;
99		}
100	}
101	

```


---

## 👤 User(sidechain) · 2026-08-09T11:50:45.978Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.GameContent.UI.Elements.UIDifficultyButton
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using ReLogic.Content;
10	using Terraria.Audio;
11	using Terraria.Localization;
12	using Terraria.UI;
13	
14	namespace Terraria.GameContent.UI.Elements
15	{
16	  public class UIDifficultyButton : UIElement
17	  {
18	    private readonly Player _player;
19	    private readonly Asset<Texture2D> _BasePanelTexture;
20	    private readonly Asset<Texture2D> _selectedBorderTexture;
21	    private readonly Asset<Texture2D> _hoveredBorderTexture;
22	    private readonly byte _difficulty;
23	    private readonly Color _color;
24	    private bool _hovered;
25	    private bool _soundedHover;
26	
27	    public UIDifficultyButton(
28	      Player player,
29	      LocalizedText title,
30	      LocalizedText description,
31	      byte difficulty,
32	      Color color)
33	    {
34	      this._player = player;
35	      this._difficulty = difficulty;
36	      this.Width = StyleDimension.FromPixels(44f);
37	      this.Height = StyleDimension.FromPixels(110f);
38	      this._BasePanelTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/PanelGrayscale", (AssetRequestMode) 1);
39	      this._selectedBorderTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelHighlight", (AssetRequestMode) 1);
40	      this._hoveredBorderTexture = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/UI/CharCreation/CategoryPanelBorder", (AssetRequestMode) 1);
41	      this._color = color;
42	      UIText uiText = new UIText(title, 0.9f, false);
43	      uiText.HAlign = 0.5f;
44	      uiText.VAlign = 0.0f;
45	      uiText.Width = StyleDimension.FromPixelsAndPercent(-10f, 1f);
46	      uiText.Top = StyleDimension.FromPixels(5f);
47	      this.Append((UIElement) uiText);
48	    }
49	
50	    protected override void DrawSelf(SpriteBatch spriteBatch)
51	    {
52	      if (this._hovered)
53	      {
54	        if (!this._soundedHover)
55	          SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
56	        this._soundedHover = true;
57	      }
58	      else
59	        this._soundedHover = false;
60	      CalculatedStyle dimensions = this.GetDimensions();
61	      int num1 = 7;
62	      if ((double) dimensions.Height < 30.0)
63	        num1 = 5;
64	      int num2 = 10;
65	      int num3 = 10;
66	      int num4 = (int) this._difficulty == (int) this._player.difficulty ? 1 : 0;
67	      Utils.DrawSplicedPanel(spriteBatch, this._BasePanelTexture.Value, (int) dimensions.X, (int) dimensions.Y, (int) dimensions.Width, (int) dimensions.Height, num2, num2, num3, num3, Color.Lerp(Color.Black, this._color, 0.8f) * 0.5f);
68	      if (num4 != 0)
69	        Utils.DrawSplicedPanel(spriteBatch, this._BasePanelTexture.Value, (int) dimensions.X + num1, (int) dimensions.Y + num1 - 2, (int) dimensions.Width - num1 * 2, (int) dimensions.Height - num1 * 2, num2, num2, num3, num3, Color.Lerp(this._color, Color.White, 0.7f) * 0.5f);
70	      if (!this._hovered)
71	        return;
72	      Utils.DrawSplicedPanel(spriteBatch, this._hoveredBorderTexture.Value, (int) dimensions.X, (int) dimensions.Y, (int) dimensions.Width, (int) dimensions.Height, num2, num2, num3, num3, Color.White);
73	    }
74	
75	    public override void MouseDown(UIMouseEvent evt)
76	    {
77	      this._player.difficulty = this._difficulty;
78	      SoundEngine.PlaySound(12, -1, -1, 1, 1f, 0.0f);
79	      base.MouseDown(evt);
80	    }
81	
82	    public override void MouseOver(UIMouseEvent evt)
83	    {
84	      base.MouseOver(evt);
85	      this._hovered = true;
86	    }
87	
88	    public override void MouseOut(UIMouseEvent evt)
89	    {
90	      base.MouseOut(evt);
91	      this._hovered = false;
92	    }
93	  }
94	}
95	

```


---

## 🤖 Assistant · 2026-08-09T11:50:49.724Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
UIDifficultyButton: identical behavior (only MouseDown → LeftMouseDown rename).

Now check head/hair drawing differences in PlayerDrawLayers: DrawPlayer_21_Head (hair drawing) - old uses TextureAssets.PlayerHair[drawinfo.hair]; check for changes like hairDyeIndex, new hats/hat hair. Also check "GetHairDrawOffset" (new method in Player.cs — old had?). Old: GetHairSettings at 10660; check if old had GetHairDrawOffset.

Also confirm hair texture count: TextureAssets.PlayerHair array size — check AssetRequestHelpers/TextureAssets: "Images/Player/Hair" 162 vs 228.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:49.918Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"PlayerHair\" ~/Project/GLM/SandboxWorld/Terarria1405/Graphics/TextureAssets.cs 2>/dev/null | head; find ~/Project/GLM/SandboxWorld/Terarria1405 -name \"TextureAssets.cs\"; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"TextureAssets.cs\"",
 "description": "Locate TextureAssets hair array declaration"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:49.959Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1405/GameContent/TextureAssets.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/TextureAssets.cs

```


---

## 🤖 Assistant · 2026-08-09T11:50:52.392Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"PlayerHair\\|Players\" ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/TextureAssets.cs; echo \"===NEW===\"; grep -n \"PlayerHair\\|Players\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/TextureAssets.cs; echo \"===load counts===\"; grep -rn \"\\\"Images/Player/Hair\\\"\\|Images/Player/Hair\\|PlayerHair = \\|Players = \" ~/Project/GLM/SandboxWorld/Terarria1405/*.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/*.cs 2>/dev/null | head",
 "description": "Compare PlayerHair texture array sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:52.431Z

**📎 ToolResult**

```
91:    public static Asset<Texture2D>[] PlayerHair = new Asset<Texture2D>[162];
92:    public static Asset<Texture2D>[] PlayerHairAlt = new Asset<Texture2D>[162];
284:    public static Asset<Texture2D>[,] Players;
===NEW===
582:	public static Asset<Texture2D>[,] Players;
584:	public static Asset<Texture2D>[] PlayerHair = new Asset<Texture2D>[228];
586:	public static Asset<Texture2D>[] PlayerHairAlt = new Asset<Texture2D>[228];
===load counts===
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:2935:        this.statsAreScaledForThisManyPlayers = 0;
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:12488:        int numPlayers = !activePlayersCount.HasValue ? NPC.GetActivePlayerCount() : activePlayersCount.Value;
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:12489:        this.statsAreScaledForThisManyPlayers = numPlayers;
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:12520:      int numPlayers = !activePlayersCount.HasValue ? NPC.GetActivePlayerCount() : activePlayersCount.Value;
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs:12521:      this.statsAreScaledForThisManyPlayers = numPlayers;
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:381:    public static int maxNetPlayers = (int) byte.MaxValue;
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:1418:    public static ParticleRenderer ParticleSystem_World_OverPlayers = new ParticleRenderer();
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:1419:    public static ParticleRenderer ParticleSystem_World_BehindPlayers = new ParticleRenderer();
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:1510:    public List<int> DrawCacheNPCsOverPlayers = new List<int>(200);
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs:1517:    public List<int> DrawCacheProjsOverPlayers = new List<int>(1000);

```


---

## 🤖 Assistant · 2026-08-09T11:50:54.826Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: PlayerHair 162 → 228.

Check Players[,] texture array dimensions load in TextureAssets (both) — probably both load 12 variants x 16 sheets ("Images/Players_"+variant). Let me check the loading loop.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:50:55.769Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -A6 \"Players = new\" ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/TextureAssets.cs; echo \"===NEW===\"; grep -n -A6 \"Players = new\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/TextureAssets.cs; echo \"===load loop old===\"; grep -n -B2 -A8 \"Players\\[\" ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/TextureAssets.cs | head -30; echo \"===load loop new===\"; grep -n -B2 -A8 \"Players\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/TextureAssets.cs | head -30",
 "description": "Compare Players texture sheet loading"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:55.812Z

**📎 ToolResult**

```
===NEW===
===load loop old===
===load loop new===

```


---

## 🤖 Assistant · 2026-08-09T11:50:57.690Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Players\" ~/Project/GLM/SandboxWorld/Terarria1405/GameContent/TextureAssets.cs | head; echo \"---load sites---\"; grep -rn \"TextureAssets.Players = \\|TextureAssets.Players=\" ~/Project/GLM/SandboxWorld/Terarria1405 ~/Project/GLM/SandboxWorld/Terarria1456 2>/dev/null | head",
 "description": "Find where Players texture array is populated"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:57.768Z

**📎 ToolResult**

```
284:    public static Asset<Texture2D>[,] Players;
---load sites---
~/Project/GLM/SandboxWorld/Terarria1405/Initializers/PlayerDataInitializer.cs:17:      TextureAssets.Players = new Asset<Texture2D>[12, 16];
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Initializers/PlayerDataInitializer.cs:12:		TextureAssets.Players = new Asset<Texture2D>[PlayerVariantID.Count, PlayerTextureID.Count];

```


---

## 🤖 Assistant · 2026-08-09T11:50:59.418Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/Initializers/PlayerDataInitializer.cs"
}
```


---

## 🤖 Assistant · 2026-08-09T11:50:59.419Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Initializers/PlayerDataInitializer.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:50:59.424Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.Initializers.PlayerDataInitializer
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework.Graphics;
8	using ReLogic.Content;
9	using Terraria.GameContent;
10	
11	namespace Terraria.Initializers
12	{
13	  public static class PlayerDataInitializer
14	  {
15	    public static void Load()
16	    {
17	      TextureAssets.Players = new Asset<Texture2D>[12, 16];
18	      PlayerDataInitializer.LoadStarterMale();
19	      PlayerDataInitializer.LoadStarterFemale();
20	      PlayerDataInitializer.LoadStickerMale();
21	      PlayerDataInitializer.LoadStickerFemale();
22	      PlayerDataInitializer.LoadGangsterMale();
23	      PlayerDataInitializer.LoadGangsterFemale();
24	      PlayerDataInitializer.LoadCoatMale();
25	      PlayerDataInitializer.LoadDressFemale();
26	      PlayerDataInitializer.LoadDressMale();
27	      PlayerDataInitializer.LoadCoatFemale();
28	      PlayerDataInitializer.LoadDisplayDollMale();
29	      PlayerDataInitializer.LoadDisplayDollFemale();
30	    }
31	
32	    private static void LoadVariant(int ID, int[] pieceIDs)
33	    {
34	      for (int index = 0; index < pieceIDs.Length; ++index)
35	        TextureAssets.Players[ID, pieceIDs[index]] = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/Player_" + (object) ID + "_" + (object) pieceIDs[index], (AssetRequestMode) 2);
36	    }
37	
38	    private static void CopyVariant(int to, int from)
39	    {
40	      for (int index = 0; index < 16; ++index)
41	        TextureAssets.Players[to, index] = TextureAssets.Players[from, index];
42	    }
43	
44	    private static void LoadStarterMale()
45	    {
46	      PlayerDataInitializer.LoadVariant(0, new int[15]
47	      {
48	        0,
49	        1,
50	        2,
51	        3,
52	        4,
53	        5,
54	        6,
55	        7,
56	        8,
57	        9,
58	        10,
59	        11,
60	        12,
61	        13,
62	        15
63	      });
64	      TextureAssets.Players[0, 14] = (Asset<Texture2D>) Asset<Texture2D>.Empty;
65	    }
66	
67	    private static void LoadStickerMale()
68	    {
69	      PlayerDataInitializer.CopyVariant(1, 0);
70	      PlayerDataInitializer.LoadVariant(1, new int[6]
71	      {
72	        4,
73	        6,
74	        8,
75	        11,
76	        12,
77	        13
78	      });
79	    }
80	
81	    private static void LoadGangsterMale()
82	    {
83	      PlayerDataInitializer.CopyVariant(2, 0);
84	      PlayerDataInitializer.LoadVariant(2, new int[6]
85	      {
86	        4,
87	        6,
88	        8,
89	        11,
90	        12,
91	        13
92	      });
93	    }
94	
95	    private static void LoadCoatMale()
96	    {
97	      PlayerDataInitializer.CopyVariant(3, 0);
98	      PlayerDataInitializer.LoadVariant(3, new int[7]
99	      {
100	        4,
101	        6,
102	        8,
103	        11,
104	        12,
105	        13,
106	        14
107	      });
108	    }
109	
110	    private static void LoadDressMale()
111	    {
112	      PlayerDataInitializer.CopyVariant(8, 0);
113	      PlayerDataInitializer.LoadVariant(8, new int[7]
114	      {
115	        4,
116	        6,
117	        8,
118	        11,
119	        12,
120	        13,
121	        14
122	      });
123	    }
124	
125	    private static void LoadStarterFemale()
126	    {
127	      PlayerDataInitializer.CopyVariant(4, 0);
128	      PlayerDataInitializer.LoadVariant(4, new int[11]
129	      {
130	        3,
131	        4,
132	        5,
133	        6,
134	        7,
135	        8,
136	        9,
137	        10,
138	        11,
139	        12,
140	        13
141	      });
142	    }
143	
144	    private static void LoadStickerFemale()
145	    {
146	      PlayerDataInitializer.CopyVariant(5, 4);
147	      PlayerDataInitializer.LoadVariant(5, new int[6]
148	      {
149	        4,
150	        6,
151	        8,
152	        11,
153	        12,
154	        13
155	      });
156	    }
157	
158	    private static void LoadGangsterFemale()
159	    {
160	      PlayerDataInitializer.CopyVariant(6, 4);
161	      PlayerDataInitializer.LoadVariant(6, new int[6]
162	      {
163	        4,
164	        6,
165	        8,
166	        11,
167	        12,
168	        13
169	      });
170	    }
171	
172	    private static void LoadCoatFemale()
173	    {
174	      PlayerDataInitializer.CopyVariant(7, 4);
175	      PlayerDataInitializer.LoadVariant(7, new int[7]
176	      {
177	        4,
178	        6,
179	        8,
180	        11,
181	        12,
182	        13,
183	        14
184	      });
185	    }
186	
187	    private static void LoadDressFemale()
188	    {
189	      PlayerDataInitializer.CopyVariant(9, 4);
190	      PlayerDataInitializer.LoadVariant(9, new int[6]
191	      {
192	        4,
193	        6,
194	        8,
195	        11,
196	        12,
197	        13
198	      });
199	    }
200	
201	    private static void LoadDisplayDollMale()
202	    {
203	      PlayerDataInitializer.CopyVariant(10, 0);
204	      PlayerDataInitializer.LoadVariant(10, new int[7]
205	      {
206	        0,
207	        2,
208	        3,
209	        5,
210	        7,
211	        9,
212	        10
213	      });
214	      Asset<Texture2D> player = TextureAssets.Players[10, 2];
215	      TextureAssets.Players[10, 2] = player;
216	      TextureAssets.Players[10, 1] = player;
217	      TextureAssets.Players[10, 4] = player;
218	      TextureAssets.Players[10, 6] = player;
219	      TextureAssets.Players[10, 11] = player;
220	      TextureAssets.Players[10, 12] = player;
221	      TextureAssets.Players[10, 13] = player;
222	      TextureAssets.Players[10, 8] = player;
223	      TextureAssets.Players[10, 15] = player;
224	    }
225	
226	    private static void LoadDisplayDollFemale()
227	    {
228	      PlayerDataInitializer.CopyVariant(11, 10);
229	      PlayerDataInitializer.LoadVariant(11, new int[5]
230	      {
231	        3,
232	        5,
233	        7,
234	        9,
235	        10
236	      });
237	      Asset<Texture2D> player = TextureAssets.Players[10, 2];
238	      TextureAssets.Players[11, 2] = player;
239	      TextureAssets.Players[11, 1] = player;
240	      TextureAssets.Players[11, 4] = player;
241	      TextureAssets.Players[11, 6] = player;
242	      TextureAssets.Players[11, 11] = player;
243	      TextureAssets.Players[11, 12] = player;
244	      TextureAssets.Players[11, 13] = player;
245	      TextureAssets.Players[11, 8] = player;
246	      TextureAssets.Players[11, 15] = player;
247	    }
248	  }
249	}
250	

```


---

## 👤 User(sidechain) · 2026-08-09T11:50:59.424Z

**📎 ToolResult**

```
1	using Microsoft.Xna.Framework.Graphics;
2	using ReLogic.Content;
3	using Terraria.GameContent;
4	using Terraria.ID;
5	
6	namespace Terraria.Initializers;
7	
8	public static class PlayerDataInitializer
9	{
10		public static void Load()
11		{
12			TextureAssets.Players = new Asset<Texture2D>[PlayerVariantID.Count, PlayerTextureID.Count];
13			LoadStarterMale();
14			LoadStarterFemale();
15			LoadStickerMale();
16			LoadStickerFemale();
17			LoadGangsterMale();
18			LoadGangsterFemale();
19			LoadCoatMale();
20			LoadDressFemale();
21			LoadDressMale();
22			LoadCoatFemale();
23			LoadDisplayDollMale();
24			LoadDisplayDollFemale();
25		}
26	
27		private static void LoadVariant(int ID, int[] pieceIDs)
28		{
29			for (int i = 0; i < pieceIDs.Length; i++)
30			{
31				TextureAssets.Players[ID, pieceIDs[i]] = Main.Assets.Request<Texture2D>("Images/Player_" + ID + "_" + pieceIDs[i], (AssetRequestMode)2);
32			}
33		}
34	
35		private static void CopyVariant(int to, int from)
36		{
37			for (int i = 0; i < PlayerTextureID.Count; i++)
38			{
39				TextureAssets.Players[to, i] = TextureAssets.Players[from, i];
40			}
41		}
42	
43		private static void LoadStarterMale()
44		{
45			LoadVariant(0, new int[15]
46			{
47				0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
48				10, 11, 12, 13, 15
49			});
50			TextureAssets.Players[0, 14] = Asset<Texture2D>.Empty;
51		}
52	
53		private static void LoadStickerMale()
54		{
55			CopyVariant(1, 0);
56			LoadVariant(1, new int[6] { 4, 6, 8, 11, 12, 13 });
57		}
58	
59		private static void LoadGangsterMale()
60		{
61			CopyVariant(2, 0);
62			LoadVariant(2, new int[6] { 4, 6, 8, 11, 12, 13 });
63		}
64	
65		private static void LoadCoatMale()
66		{
67			CopyVariant(3, 0);
68			LoadVariant(3, new int[7] { 4, 6, 8, 11, 12, 13, 14 });
69		}
70	
71		private static void LoadDressMale()
72		{
73			CopyVariant(8, 0);
74			LoadVariant(8, new int[7] { 4, 6, 8, 11, 12, 13, 14 });
75		}
76	
77		private static void LoadStarterFemale()
78		{
79			CopyVariant(4, 0);
80			LoadVariant(4, new int[11]
81			{
82				3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
83				13
84			});
85		}
86	
87		private static void LoadStickerFemale()
88		{
89			CopyVariant(5, 4);
90			LoadVariant(5, new int[6] { 4, 6, 8, 11, 12, 13 });
91		}
92	
93		private static void LoadGangsterFemale()
94		{
95			CopyVariant(6, 4);
96			LoadVariant(6, new int[6] { 4, 6, 8, 11, 12, 13 });
97		}
98	
99		private static void LoadCoatFemale()
100		{
101			CopyVariant(7, 4);
102			LoadVariant(7, new int[7] { 4, 6, 8, 11, 12, 13, 14 });
103		}
104	
105		private static void LoadDressFemale()
106		{
107			CopyVariant(9, 4);
108			LoadVariant(9, new int[6] { 4, 6, 8, 11, 12, 13 });
109		}
110	
111		private static void LoadDisplayDollMale()
112		{
113			CopyVariant(10, 0);
114			LoadVariant(10, new int[7] { 0, 2, 3, 5, 7, 9, 10 });
115			Asset<Texture2D> val = TextureAssets.Players[10, 2];
116			TextureAssets.Players[10, 2] = val;
117			TextureAssets.Players[10, 1] = val;
118			TextureAssets.Players[10, 4] = val;
119			TextureAssets.Players[10, 6] = val;
120			TextureAssets.Players[10, 11] = val;
121			TextureAssets.Players[10, 12] = val;
122			TextureAssets.Players[10, 13] = val;
123			TextureAssets.Players[10, 8] = val;
124			TextureAssets.Players[10, 15] = val;
125		}
126	
127		private static void LoadDisplayDollFemale()
128		{
129			CopyVariant(11, 10);
130			LoadVariant(11, new int[5] { 3, 5, 7, 9, 10 });
131			Asset<Texture2D> val = TextureAssets.Players[10, 2];
132			TextureAssets.Players[11, 2] = val;
133			TextureAssets.Players[11, 1] = val;
134			TextureAssets.Players[11, 4] = val;
135			TextureAssets.Players[11, 6] = val;
136			TextureAssets.Players[11, 11] = val;
137			TextureAssets.Players[11, 12] = val;
138			TextureAssets.Players[11, 13] = val;
139			TextureAssets.Players[11, 8] = val;
140			TextureAssets.Players[11, 15] = val;
141		}
142	}
143	

```


---

## 🤖 Assistant · 2026-08-09T11:51:02.850Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
PlayerDataInitializer identical.

Now check the head/hair drawing in PlayerDrawLayers for behavior changes relevant to rendering (hair texture selection, PlayerHairAlt usage). Quick diff on key functions: DrawPlayer_21_Head in old vs new head section. Let me look at new lines ~2550-2660 and old ~1650-1750.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:51:03.302Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1670,1740p' ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs",
 "description": "Read old head drawing section"
}
```


---

## 🤖 Assistant · 2026-08-09T11:51:03.306Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2600,2700p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs",
 "description": "Read new head drawing section"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:03.324Z

**📎 ToolResult**

```
			float num = 0f;
			if (drawinfo.drawPlayer.face == 5)
			{
				sbyte faceHead = drawinfo.drawPlayer.faceHead;
				if ((uint)(faceHead - 10) <= 3u)
				{
					num = 2 * drawinfo.drawPlayer.direction;
				}
			}
			item = new DrawData(TextureAssets.AccFace[drawinfo.drawPlayer.face].Value, pos + new Vector2((float)(int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)) + num, (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, drawinfo.drawPlayer.bodyFrame, drawinfo.colorArmorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
			item.shader = drawinfo.cFace;
			drawinfo.DrawDataCache.Add(item);
		}
		else if (!drawinfo.drawPlayer.invis && !flag)
		{
			DrawData drawData = new DrawData(TextureAssets.Players[drawinfo.skinVar, 0].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)), (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, drawinfo.drawPlayer.bodyFrame, drawinfo.colorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
			drawData.shader = drawinfo.skinDyePacked;
			DrawData item = drawData;
			drawinfo.DrawDataCache.Add(item);
			item = new DrawData(TextureAssets.Players[drawinfo.skinVar, 1].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)), (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, drawinfo.drawPlayer.bodyFrame, drawinfo.colorEyeWhites, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
			drawinfo.DrawDataCache.Add(item);
			item = new DrawData(TextureAssets.Players[drawinfo.skinVar, 2].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)), (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, drawinfo.drawPlayer.bodyFrame, drawinfo.colorEyes, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
			drawinfo.DrawDataCache.Add(item);
			DrawPlayer_21_Head_TheFace_Eyelid(ref drawinfo);
			if (drawinfo.drawPlayer.yoraiz0rDarkness)
			{
				drawData = new DrawData(TextureAssets.Extra[67].Value, pos + new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)), (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, drawinfo.drawPlayer.bodyFrame, drawinfo.colorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
				drawData.shader = drawinfo.skinDyePacked;
				item = drawData;
				drawinfo.DrawDataCache.Add(item);
			}
			if (drawinfo.drawPlayer.face > 0 && ArmorIDs.Face.Sets.DrawInFaceUnderHairLayer[drawinfo.drawPlayer.face] && (!drawinfo.drawPlayer.mount.Active || drawinfo.drawPlayer.mount.Type != 54 || ArmorIDs.Face.Sets.CanDrawOnVelociraptorMount[drawinfo.drawPlayer.face]))
			{
				item = new DrawData(TextureAssets.AccFace[drawinfo.drawPlayer.face].Value, pos + new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)), (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, drawinfo.drawPlayer.bodyFrame, drawinfo.colorArmorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
				item.shader = drawinfo.cFace;
				drawinfo.DrawDataCache.Add(item);
			}
		}
	}

	private static void DrawPlayer_21_Head_TheFace_Eyelid(ref PlayerDrawSet drawinfo)
	{
		Asset<Texture2D> val = TextureAssets.Players[drawinfo.skinVar, 15];
		if (val.IsLoaded)
		{
			Vector2 pos = Vector2.Zero;
			drawinfo.drawPlayer.ApplyHeadOffsetFromMount(ref pos);
			Vector2 vector = Main.OffsetsPlayerHeadgear[drawinfo.drawPlayer.bodyFrame.Y / drawinfo.drawPlayer.bodyFrame.Height];
			vector.Y -= 2f;
			vector *= (float)(-((drawinfo.playerEffect & SpriteEffects.FlipVertically) != 0).ToDirectionInt());
			Color color = drawinfo.colorHead;
			int shader = drawinfo.skinDyePacked;
			int frameY = drawinfo.drawPlayer.eyeHelper.EyeFrameToShow;
			if (drawinfo.drawPlayer.mount.Active && drawinfo.drawPlayer.mount.Type == 54)
			{
				color = drawinfo.drawPlayer.GetImmuneAlpha(Lighting.GetColorClamped((int)drawinfo.drawPlayer.MountedCenter.X / 16, (int)drawinfo.drawPlayer.MountedCenter.Y / 16, new Color(158, 92, 67)), drawinfo.shadow);
				shader = drawinfo.drawPlayer.cMount;
			}
			if (drawinfo.drawPlayer.mount.Active && drawinfo.mountHandlesHeadDraw && drawinfo.mountDrawsEyelid && drawinfo.drawPlayer.head == 288)
			{
				color = Color.Black;
				frameY = 2;
			}
			Rectangle value = val.Frame(1, 3, 0, frameY);
			DrawData drawData = new DrawData(val.Value, pos + new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)), (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect + vector, value, color, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
			drawData.shader = shader;
			DrawData item = drawData;
			drawinfo.DrawDataCache.Add(item);
		}
	}

	public static void DrawPlayer_21_1_Magiluminescence(ref PlayerDrawSet drawinfo)
	{
		if (drawinfo.shadow == 0f && drawinfo.drawPlayer.neck == 11 && !drawinfo.hideEntirePlayer && !drawinfo.hideEntirePlayerExceptHelmetsAndFaceAccessories)
		{
			Color colorArmorBody = drawinfo.colorArmorBody;
			Color value = new Color(140, 140, 35, 12);
			float amount = (float)(colorArmorBody.R + colorArmorBody.G + colorArmorBody.B) / 3f / 255f;
			value = Color.Lerp(value, Color.Transparent, amount);
			if (!(value == Color.Transparent))
			{
				DrawData item = new DrawData(TextureAssets.GlowMask[310].Value, new Vector2((int)(drawinfo.Position.X - Main.screenPosition.X - (float)(drawinfo.drawPlayer.bodyFrame.Width / 2) + (float)(drawinfo.drawPlayer.width / 2)), (int)(drawinfo.Position.Y - Main.screenPosition.Y + (float)drawinfo.drawPlayer.height - (float)drawinfo.drawPlayer.bodyFrame.Height + 4f)) + drawinfo.drawPlayer.bodyPosition + new Vector2(drawinfo.drawPlayer.bodyFrame.Width / 2, drawinfo.drawPlayer.bodyFrame.Height / 2), drawinfo.drawPlayer.bodyFrame, value, drawinfo.drawPlayer.bodyRotation, drawinfo.bodyVect, 1f, drawinfo.playerEffect);
				item.shader = drawinfo.cNeck;
				drawinfo.DrawDataCache.Add(item);
			}
		}
	}

	public static void DrawPlayer_ChippysHeadband(ref PlayerDrawSet drawinfo)
	{
		Texture2D value = TextureAssets.Extra[279].Value;
		float num = 0.4f;
		float num2 = 0.8f;
		float num3 = 160f;
		int num4 = 0;
		float num5 = 0f;
		Vector2 zero = Vector2.Zero;
		float num6 = 0f;
		float num7 = 0f;
		float num8 = 0f;
		int num9 = 0;

```


---

## 👤 User(sidechain) · 2026-08-09T11:51:03.325Z

**📎 ToolResult**

```
    {
      Vector2 vector2 = Main.OffsetsPlayerHeadgear[drawinfo.drawPlayer.bodyFrame.Y / drawinfo.drawPlayer.bodyFrame.Height] * drawinfo.drawPlayer.Directions;
      Vector2 vec = (drawinfo.Position - Main.screenPosition + helmetOffset + new Vector2((float) (-drawinfo.drawPlayer.bodyFrame.Width / 2 + drawinfo.drawPlayer.width / 2), (float) (drawinfo.drawPlayer.height - drawinfo.drawPlayer.bodyFrame.Height + 4)) + hatOffset * drawinfo.drawPlayer.Directions + vector2).Floor() + (drawinfo.drawPlayer.headPosition + drawinfo.headVect);
      if ((double) drawinfo.drawPlayer.gravDir == -1.0)
        vec.Y += 12f;
      vec = vec.Floor();
      return vec;
    }

    private static void DrawPlayer_21_Head_TheFace(ref PlayerDrawSet drawinfo)
    {
      bool flag = drawinfo.drawPlayer.head == 38 && drawinfo.drawPlayer.head == 135;
      if (drawinfo.drawPlayer.invis || flag)
        return;
      DrawData drawData1 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 0].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
      drawData1.shader = drawinfo.skinDyePacked;
      DrawData drawData2 = drawData1;
      drawinfo.DrawDataCache.Add(drawData2);
      drawData2 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 1].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorEyeWhites, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
      drawinfo.DrawDataCache.Add(drawData2);
      drawData2 = new DrawData(TextureAssets.Players[drawinfo.skinVar, 2].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorEyes, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
      drawinfo.DrawDataCache.Add(drawData2);
      Asset<Texture2D> player = TextureAssets.Players[drawinfo.skinVar, 15];
      if (player.IsLoaded)
      {
        Vector2 vector2 = Main.OffsetsPlayerHeadgear[drawinfo.drawPlayer.bodyFrame.Y / drawinfo.drawPlayer.bodyFrame.Height];
        vector2.Y -= 2f;
        Rectangle rectangle = player.Frame(1, 3, 0, drawinfo.drawPlayer.eyeHelper.EyeFrameToShow, 0, 0);
        drawData1 = new DrawData(player.Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect + vector2, new Rectangle?(rectangle), drawinfo.colorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
        drawData1.shader = drawinfo.skinDyePacked;
        DrawData drawData3 = drawData1;
        drawinfo.DrawDataCache.Add(drawData3);
      }
      if (!drawinfo.drawPlayer.yoraiz0rDarkness)
        return;
      drawData1 = new DrawData(TextureAssets.Extra[67].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
      drawData1.shader = drawinfo.skinDyePacked;
      DrawData drawData4 = drawData1;
      drawinfo.DrawDataCache.Add(drawData4);
    }

    public static void DrawPlayer_22_FaceAcc(ref PlayerDrawSet drawinfo)
    {
      DrawData drawData;
      if (drawinfo.drawPlayer.face > (sbyte) 0 && drawinfo.drawPlayer.face < (sbyte) 16 && drawinfo.drawPlayer.face != (sbyte) 5)
      {
        if (drawinfo.drawPlayer.face == (sbyte) 7)
        {
          drawData = new DrawData(TextureAssets.AccFace[(int) drawinfo.drawPlayer.face].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), new Color(200, 200, 200, 150), drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
          drawData.shader = drawinfo.cFace;
          drawinfo.DrawDataCache.Add(drawData);
        }
        else
        {
          drawData = new DrawData(TextureAssets.AccFace[(int) drawinfo.drawPlayer.face].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorArmorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
          drawData.shader = drawinfo.cFace;
          drawinfo.DrawDataCache.Add(drawData);
        }
      }
      if (!drawinfo.drawUnicornHorn)
        return;
      drawData = new DrawData(TextureAssets.Extra[143].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.drawPlayer.bodyFrame), drawinfo.colorArmorHead, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
      drawData.shader = drawinfo.cUnicornHorn;
      drawinfo.DrawDataCache.Add(drawData);
    }

    public static void DrawTiedBalloons(ref PlayerDrawSet drawinfo)
    {
      if (drawinfo.drawPlayer.mount.Type != 34)
        return;
      Texture2D texture2D = TextureAssets.Extra[141].Value;

```


---

## 🤖 Assistant · 2026-08-09T11:51:05.778Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Face/eyelid rendering structurally the same (0/1/2 channels, eyelid channel 15 with 3 frames) with added mount-specific tweaks — minor.

Now also check hair drawing (DrawPlayer_23? "DrawPlayer_Hair"). Grep hair in both quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:51:06.651Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"PlayerHair\\b\\|PlayerHairAlt\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawLayers.cs | head; echo \"===NEW===\"; grep -n \"PlayerHair\\b\\|PlayerHairAlt\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs | head; echo \"===hatHair old vs new head draw===\"; grep -n \"DrawPlayer_Head\\b\\|GetHairDrawOffset\\|hatHair\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawLayers.cs | head -20",
 "description": "Compare hair texture draw sites"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:06.691Z

**📎 ToolResult**

```
142:          drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.hairFrame), drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0)
147:          drawinfo.DrawDataCache.Add(new DrawData(TextureAssets.PlayerHairAlt[drawinfo.drawPlayer.hair].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.hairFrame), drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0)
1428:          drawData = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.hairFrame), drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
1435:        drawData = new DrawData(TextureAssets.PlayerHairAlt[drawinfo.drawPlayer.hair].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.hairFrame), drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
1443:          drawData = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.hairFrame), drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
1494:          drawData = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.hairFrame), drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
1603:        drawData = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, new Vector2((float) (int) ((double) drawinfo.Position.X - (double) Main.screenPosition.X - (double) (drawinfo.drawPlayer.bodyFrame.Width / 2) + (double) (drawinfo.drawPlayer.width / 2)), (float) (int) ((double) drawinfo.Position.Y - (double) Main.screenPosition.Y + (double) drawinfo.drawPlayer.height - (double) drawinfo.drawPlayer.bodyFrame.Height + 4.0)) + drawinfo.drawPlayer.headPosition + drawinfo.headVect, new Rectangle?(drawinfo.hairFrame), drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect, 0);
===NEW===
206:				DrawData item = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, position, drawinfo.hairBackFrame, drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
212:				DrawData item = new DrawData(TextureAssets.PlayerHairAlt[drawinfo.drawPlayer.hair].Value, position, drawinfo.hairBackFrame, drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
2155:				item = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, position, drawinfo.hairFrontFrame, drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
2162:			item = new DrawData(TextureAssets.PlayerHairAlt[drawinfo.drawPlayer.hair].Value, position, drawinfo.hairFrontFrame, drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
2252:				item = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, position, drawinfo.hairFrontFrame, drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
2422:			item = new DrawData(TextureAssets.PlayerHair[drawinfo.drawPlayer.hair].Value, position, drawinfo.hairFrontFrame, drawinfo.colorHair, drawinfo.drawPlayer.headRotation, drawinfo.headVect, 1f, drawinfo.playerEffect);
===hatHair old vs new head draw===
210:			else if (drawinfo.hatHair)
400:		if (drawinfo.drawPlayer.leinforsHair && (drawinfo.fullHair || drawinfo.hatHair || drawinfo.drawsBackHairWithoutHeadgear || drawinfo.drawPlayer.head == -1 || drawinfo.drawPlayer.head == 0) && drawinfo.drawPlayer.hair != 12 && drawinfo.shadow == 0f && Main.rgbToHsl(drawinfo.colorHead).Z > 0.2f)
402:			if (Main.rand.Next(20) == 0 && !drawinfo.hatHair)
412:			if (Main.rand.Next(40) == 0 && drawinfo.hatHair)
2160:		if (flag4 && drawinfo.hatHair && !drawinfo.drawPlayer.invis)

```


---

## 🤖 Assistant · 2026-08-09T11:51:08.978Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Hair rendering refactored: old used single `hairFrame` (drawinfo.hairFrame), new splits into `hairFrontFrame` and `hairBackFrame` (hair sheets are 2-row? Actually new hair textures have separate front/back frames). Check PlayerDrawSet for hairFrame vs hairFrontFrame/hairBackFrame.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:51:09.389Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"hairFrame\\|hairFrontFrame\\|hairBackFrame\" ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawSet.cs; echo \"===NEW===\"; grep -n \"hairFrame\\|hairFrontFrame\\|hairBackFrame\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawSet.cs",
 "description": "Compare hair frame fields in PlayerDrawSet"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:09.412Z

**📎 ToolResult**

```
94:    public Rectangle hairFrame;
1181:      this.hairFrame = this.drawPlayer.bodyFrame;
1182:      this.hairFrame.Y -= 336;
1183:      if (this.hairFrame.Y < 0)
1184:        this.hairFrame.Y = 0;
1186:        this.hairFrame.Height = 0;
===NEW===
183:	public Rectangle hairFrontFrame;
185:	public Rectangle hairBackFrame;
1743:		hairFrontFrame = bodyFrame;
1744:		hairBackFrame = bodyFrame;
1747:			hairFrontFrame.Height = 0;
1748:			hairBackFrame.Height = 0;
1753:			hairFrontFrame.Height = height;

```


---

## 🤖 Assistant · 2026-08-09T11:51:12.542Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1170,1195p' ~/Project/GLM/SandboxWorld/Terarria1405/DataStructures/PlayerDrawSet.cs; echo \"===NEW===\"; sed -n '1735,1775p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/PlayerDrawSet.cs",
 "description": "Compare hair frame calculation logic"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:12.588Z

**📎 ToolResult**

```
      this.headVect = new Vector2((float) this.drawPlayer.legFrame.Width * 0.5f, (float) this.drawPlayer.legFrame.Height * 0.4f);
      if ((this.drawPlayer.merman || this.drawPlayer.forceMerman) && !this.drawPlayer.hideMerman)
      {
        this.drawPlayer.headRotation = (float) ((double) this.drawPlayer.velocity.Y * (double) this.drawPlayer.direction * 0.100000001490116);
        if ((double) this.drawPlayer.headRotation < -0.3)
          this.drawPlayer.headRotation = -0.3f;
        if ((double) this.drawPlayer.headRotation > 0.3)
          this.drawPlayer.headRotation = 0.3f;
      }
      else if (!this.drawPlayer.dead)
        this.drawPlayer.headRotation = 0.0f;
      this.hairFrame = this.drawPlayer.bodyFrame;
      this.hairFrame.Y -= 336;
      if (this.hairFrame.Y < 0)
        this.hairFrame.Y = 0;
      if (this.hideHair)
        this.hairFrame.Height = 0;
      this.hidesTopSkin = this.drawPlayer.body == 82 || this.drawPlayer.body == 83 || (this.drawPlayer.body == 93 || this.drawPlayer.body == 21) || this.drawPlayer.body == 22;
      this.hidesBottomSkin = this.drawPlayer.body == 93 || this.drawPlayer.legs == 20 || this.drawPlayer.legs == 21;
      this.drawFloatingTube = this.drawPlayer.hasFloatingTube;
      this.drawUnicornHorn = this.drawPlayer.hasUnicornHorn;
      this.drawFrontAccInNeckAccLayer = false;
      if (this.drawPlayer.bodyFrame.Y / this.drawPlayer.bodyFrame.Height == 5)
        this.drawFrontAccInNeckAccLayer = this.drawPlayer.front > (sbyte) 0 && this.drawPlayer.front < (sbyte) 9 && ArmorIDs.Front.Sets.DrawsInNeckLayer[(int) this.drawPlayer.front];
      this.helmetOffset = this.drawPlayer.GetHelmetDrawOffset();
      this.CreateCompositeData();
===NEW===
		}
		Rectangle bodyFrame = drawPlayer.bodyFrame;
		bodyFrame = drawPlayer.bodyFrame;
		bodyFrame.Y -= 336;
		if (bodyFrame.Y < 0)
		{
			bodyFrame.Y = 0;
		}
		hairFrontFrame = bodyFrame;
		hairBackFrame = bodyFrame;
		if (hideHair)
		{
			hairFrontFrame.Height = 0;
			hairBackFrame.Height = 0;
		}
		else if (backHairDraw)
		{
			int height = 26;
			hairFrontFrame.Height = height;
		}
		hidesTopSkin = drawPlayer.body == 82 || drawPlayer.body == 83 || drawPlayer.body == 93 || drawPlayer.body == 21 || drawPlayer.body == 22;
		hidesBottomSkin = drawPlayer.body == 93 || drawPlayer.legs == 20 || drawPlayer.legs == 21 || drawPlayer.legs == 216 || drawPlayer.legs == 214 || drawPlayer.legs == 215;
		drawFloatingTube = drawPlayer.hasFloatingTube && !hideEntirePlayer && !hideEntirePlayerExceptHelmetsAndFaceAccessories;
		drawUnicornHorn = drawPlayer.hasUnicornHorn;
		drawAngelHalo = drawPlayer.hasAngelHalo;
		drawFrontAccInNeckAccLayer = false;
		if (drawPlayer.front > 0 && drawPlayer.front < ArmorIDs.Front.Count)
		{
			if (ArmorIDs.Front.Sets.DrawsInNeckLayerRegardlessOfPlayerFrame[drawPlayer.front])
			{
				drawFrontAccInNeckAccLayer = true;
			}
			else if (drawPlayer.bodyFrame.Y / drawPlayer.bodyFrame.Height == 5 && ArmorIDs.Front.Sets.DrawsInNeckLayer[drawPlayer.front])
			{
				drawFrontAccInNeckAccLayer = true;
			}
		}
		mountHandlesHeadDraw = false;
		mountDrawsEyelid = false;
		if (drawPlayer.mount.Active && drawPlayer.mount.Type == 54)
		{

```


---

## 🤖 Assistant · 2026-08-09T11:51:15.992Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important rendering change: hair drawing split into front/back frames. New hair textures (228) use `hairBackFrame` drawn behind body when `backHairDraw`, and `hairFrontFrame` (clipped height 26 when backHairDraw) drawn in front. Old used single `hairFrame` offset by -336px.

Also Player.GetHairSettings changed: old `backHairDraw = hair > 50 && (hair < 56 || hair > 63)...` (line 10771) — new one likely different. Let me compare.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:51:15.996Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '10660,10700p' ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs; echo \"===OLD cont===\"; sed -n '10755,10790p' ~/Project/GLM/SandboxWorld/Terarria1405/Player.cs",
 "description": "Read old GetHairSettings"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:16.035Z

**📎 ToolResult**

```
    public void GetHairSettings(
      out bool fullHair,
      out bool hatHair,
      out bool hideHair,
      out bool backHairDraw,
      out bool drawsBackHairWithoutHeadgear)
    {
      fullHair = hatHair = hideHair = drawsBackHairWithoutHeadgear = false;
      switch (this.head)
      {
        case 0:
        case 23:
        case 259:
          drawsBackHairWithoutHeadgear = true;
          break;
        case 10:
        case 12:
        case 28:
        case 42:
        case 62:
        case 97:
        case 106:
        case 113:
        case 116:
        case 119:
        case 133:
        case 138:
        case 139:
        case 163:
        case 178:
        case 181:
        case 191:
        case 198:
        case 217:
        case 218:
        case 220:
        case 222:
        case 224:
        case 225:
        case 228:
        case 229:
===OLD cont===
        case 223:
        case 226:
        case 227:
        case 231:
        case 233:
        case 234:
        case 262:
        case 263:
        case 264:
        case 265:
          hatHair = true;
          break;
      }
      if (this.face > (sbyte) -1 && ArmorIDs.Face.Sets.PreventHairDraw[(int) this.face])
        hideHair = true;
      int hair = this.hair;
      backHairDraw = hair > 50 && (hair < 56 || hair > 63) && ((hair < 74 || hair > 77) && (hair < 88 || hair > 89)) && (hair != 94 && hair != 100 && (hair != 104 && hair != 112)) && hair < 116;
      if (hair != 133)
        return;
      backHairDraw = true;
    }

    public void UpdateDead()
    {
      this._portalPhysicsTime = 0;
      this.MountFishronSpecialCounter = 0.0f;
      this.gem = -1;
      this.ownedLargeGems = (BitsByte) (byte) 0;
      this.brainOfConfusionDodgeAnimationCounter = 0;
      this.ResetFloorFlags();
      this.wings = 0;
      this.wingsLogic = 0;
      this.face = this.neck = this.back = this.front = this.handoff = this.handon = this.shoe = this.waist = this.balloon = this.shield = (sbyte) 0;
      this.poisoned = false;
      this.venom = false;
      this.onFire = false;

```


---

## 🤖 Assistant · 2026-08-09T11:51:16.158Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '16645,16700p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs",
 "description": "Read new GetHairSettings"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:16.188Z

**📎 ToolResult**

```
	public void GetHairSettings(out bool fullHair, out bool hatHair, out bool hideHair, out bool backHairDraw, out bool drawsBackHairWithoutHeadgear)
	{
		fullHair = (hatHair = (hideHair = (drawsBackHairWithoutHeadgear = false)));
		switch (head)
		{
		case 0:
		case 259:
			drawsBackHairWithoutHeadgear = true;
			break;
		case 10:
		case 12:
		case 28:
		case 42:
		case 62:
		case 97:
		case 106:
		case 113:
		case 116:
		case 119:
		case 133:
		case 138:
		case 139:
		case 163:
		case 178:
		case 181:
		case 191:
		case 198:
		case 217:
		case 218:
		case 220:
		case 222:
		case 224:
		case 225:
		case 228:
		case 229:
		case 230:
		case 232:
		case 235:
		case 238:
		case 242:
		case 243:
		case 244:
		case 245:
		case 272:
		case 273:
		case 274:
		case 277:
		case 284:
		case 290:
			fullHair = true;
			break;
		case 13:
		case 14:
		case 15:
		case 16:
		case 18:

```


---

## 🤖 Assistant · 2026-08-09T11:51:19.321Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=16700 && NR<=16830' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | grep -n \"backHairDraw\\|GetHairDrawOffset\\|hatHair = true\\|hatHair=true\" ",
 "description": "Find backHairDraw logic in new GetHairSettings"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:23.572Z

**📎 ToolResult**

```
60:			hatHair = true;
72:		backHairDraw = num > 50 && (num < 56 || num > 63) && (num < 74 || num > 77) && (num < 88 || num > 89) && num != 94 && num != 100 && num != 104 && num != 112 && num < 116;
75:			backHairDraw = true;

```


---

## 🤖 Assistant · 2026-08-09T11:51:25.763Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
backHairDraw formula unchanged.

I now have enough for the report. Let me also quickly check the game/src TS files to reference what exists (UICharacterCreationState.ts, PaperDoll.ts, Appearance.ts) so recommendations map onto them. Light check.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:51:26.828Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/vui/states/ 2>/dev/null; wc -l ~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts ~/Project/GLM/SandboxWorld/game/src/player/PaperDoll.ts ~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts 2>/dev/null; echo \"---\"; grep -n \"validCloth\\|CLOTH_STYLE\\|clothStyle\\|228\\|162\\|hairstyle\\|HAIR_COUNT\\|skinVariant\" ~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts ~/Project/GLM/SandboxWorld/game/src/player/PaperDoll.ts ~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts 2>/dev/null | head -30",
 "description": "Check ported TS files for relevant constants"
}
```


---

## 👤 User(sidechain) · 2026-08-09T11:51:26.875Z

**📎 ToolResult**

```
DataState.ts
GenWorldPreview.ts
TitleState.ts
UICharacterCreationState.ts
UICharacterSelectState.ts
UIWorldCreationState.ts
UIWorldLoadState.ts
UIWorldSelectState.ts
VuiDemoState.ts
     412 ~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts
     126 ~/Project/GLM/SandboxWorld/game/src/player/PaperDoll.ts
     130 ~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts
     668 total
---
~/Project/GLM/SandboxWorld/game/src/player/PaperDoll.ts:60:    a.skinVariant, a.hair,
~/Project/GLM/SandboxWorld/game/src/player/PaperDoll.ts:85:    const img = sheetRect(a.skinVariant, ch.sheet);
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:9:  hair: number;              // 1..228 → Player_Hair_N
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:10:  /** 皮肤/衣服组合变体（0 男 1 女 2-9 特殊套装；UICharacterCreation._validClothStyles） */
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:11:  skinVariant: number;
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:33:export const HAIR_COUNT = 228;
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:47:    skinVariant: 0,
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:65:    hair: clampInt(a.hair, 1, HAIR_COUNT, d.hair),
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:66:    skinVariant: clampInt(a.skinVariant, 0, 11, d.skinVariant),
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:79:export const VALID_CLOTH_STYLES = [0, 2, 1, 3, 8, 4, 6, 5, 7, 9];
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:84:  a.hair = 1 + Math.floor(Math.random() * HAIR_COUNT);
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts:85:  a.skinVariant = Math.random() < 0.5 ? 0 : 1;
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:21:  type Appearance, type RGBColor, randomAppearance, HAIR_COUNT,
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:22:  DIFFICULTY_INFO, rgbToHsl, hslToRgb, VALID_CLOTH_STYLES,
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:248:      VALID_CLOTH_STYLES.forEach((styleId, i) => {
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:251:          this.appearance.skinVariant = styleId;
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:296:      for (let i = 1; i <= HAIR_COUNT; i++) {
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:384:    this.char = new UICharacterPreview({ ...getParentAppearance(), skinVariant: styleId }, false, false, 0.7);
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:395:    this.char.setAppearance({ ...this.getParentAppearance(), skinVariant: this.styleId });
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts:403:    if (this.getParentAppearance().skinVariant === this.styleId) {

```


---

## 🤖 Assistant · 2026-08-09T11:51:57.515Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything I need. Now compose the final report: 「角色系统差异清单」 with rows marked 【必须改】【可选增强】【无变化】, with line numbers for both versions.

Key findings summary:

### 1. UICharacterCreation.cs
- _validClothStyles: old {0,2,1,3,8,4,6,5,7,9} (old L31-43) → new {0,2,1,3,8,9,7,5,6,4} (new L58). 【必须改】 — order matters (first 5 = male, last 5 = female).
- New _defaultHairstylesForClothStyle (new L60-72) + TryAutoAssigningHair (L630-636) + _lastSelectedHairstyle (L138, L306-309, L1446-1454, L1552) — auto hair per cloth style until user picks one. 【可选增强】
- Voice system: _validVoiceStyles (L74), voice prev/next/play buttons + pitch slider UI (L441-527), voice preview PlayHurtSound (L1513-1528), cycle via Main.CycleVoiceStyle (L1530-1540), pitch mapping RemapPitchSliderKnob 20 steps (L681-697), gender→voice auto-switch (L1311-1335, _oldMaleForVoiceAutoSwitch L136). Player fields voiceVariant/voicePitchOffset (Player.cs new L1234-1236). PlayerVoiceID (Male=1/Female=2/Other=3, colors). 【可选增强】(若不实现语音) but appearance-wise voiceVariant affects character template copy/paste.
- Default difficulty: old ctor sets _player.difficulty = 3 (creative, old L76); new sets 0 (classic/softcore, new L169). 【必须改】(如果移植默认难度的话)
- CategoryId enum: unchanged (new L25-38). 【无变化】
- HSL panel: ScaledHslToRgb luminosity mapping unchanged (old L1479-1489 / new L2359-2369); hue/sat/lum sliders unchanged; hex text, copy/paste/randomize unchanged. 【无变化】
- ApplyPendingColor mapping, UpdateColorPickers indices [3]=hair [4]=eye [5]=skin [6]=shirt [7]=undershirt [8]=pants [9]=shoes — unchanged. 【无变化】
- Removed gender male/female buttons (old L221-250) → replaced with 5 armor preview presets (new L336-395: none/hallowed/silver/formal/swimming; ArmorAssignments struct L47-56, EquipArmor* L531-614, UpdatePreviewItems L638-648). 【可选增强】
- ClothStyle click: old UIClothStyleButton.MouseDown set skinVariant directly + Click_CharClothStyle only updated icon (old L790-794, old UIClothStyleButton L70-75); new button's LeftMouseDown no longer sets skinVariant; Click_CharClothStyle sets _player.skinVariant from button's ClothStyleId (new L1283-1297). 【必须改】(click semantics)
- Randomize: new adds initial eyeColor random before loop (new L1553-1557), voiceVariant random (L1572-1576), expanded female hairstyle case list 12 → ~70 ids (old L938-957 vs new L1577-1653), armor reset (L1654). 【必须改】(female hair list) / eye color first-assign minor.
- Template copy/paste adds voiceStyle + voicePitch (new L1368-1369, L1463-1476). 【可选增强】
- Back button dirty-tracking + backup confirmation (new L1216-1228, L152-156, L2016-2026) + GameTipsDisplay (L170, L2000-2015). 【可选增强】
- Category button now renders 7-frame layered character preview (ColorCharacter sheet, _characterPreviewLayers L140, L749-761, L803-812) instead of single-colored icon. 【可选增强】
- Hair button: SkipRenderingContent(i) called per button on creation (new L299) so buttons don't all render heads the first frame(s) — spread across frames. 【可选增强】
- SetupGamepadPoints reworked for new "Preview"/"pitch" snap points (new L2199-2296). 【可选增强】

### 2. UICharacter.cs
- 59×58 unchanged (old L27-28 / new L43-44). 【无变化】
- Animation formula (time/0.07%14+6)*56 unchanged (old L57 / new L92-93). 【无变化】
- ResetEffects/PlayerFrame moved from Update() into DrawSelf (old L37-47,62-73 vs new L76-83,104-114); Update no longer mutates player. 【可选增强】
- New: pet preview projectiles (_petProjectiles, PreparePetProjectiles, DrawPets, GetPlayerPosition shifts X -10 when pets) (new L14, 30, 55-74, 114, 122-152). 【可选增强】
- New: PrepareAction hook (new L28, 108-111) — character creation uses it to set direction/auto hair/armor. 【可选增强】
- New: useAClone param → SerializedClone for list previews (new L34-42) — prevents UI animation mutating real player data. 【必须改】(if UI shares player objects) or 可选.
- DrawPlayerHead call in UIHairStyleButton now passes no rotation/scale/color (old L53: DrawPlayerHead(...,1f,1f,new Color()) vs new L74: DrawPlayerHead(...)) — check PlayerRenderer signature change. Probably additive. 【无变化/微调】

### 3. UICharacterSelect.cs
- Sorting now includes LastPlayed descending (new L149-151 vs old L147-155). 【必须改】(if porting select list order)
- Gamepad snap grid 4 → 5 columns (+Rename) (old L242 vs new L246). 【可选增强】
- Otherwise layout identical (650 max width, 220 top, panel -110 height, list padding 5). 【无变化】

### 4. UICharacterListItem.cs
- New Rename button (ButtonRename) with running X offsets: play 4, favorite 28, cloud 52 (if), rename 76, then label at 104/128 (new L71-133) vs old fixed Left 4/28/52 and label at 80 (old L59-102). 【必须改】(layout) 
- UICharacter preview now useAClone:true (new L66). 【必须改/可选】
- CompareTo: order-in-list instead of favorite/name (new L285-292). 【可选增强】
- Name display: prefix load status name, gray when loadStatus != Ok (new L323-331). 【可选增强】
- Rest (panels, heart/mana, difficulty colors, playtime) unchanged. 【无变化】

### 5. Player.cs
- Default colors unchanged (old L199-205 / new L2420-2432): hair 215,90,55; skin 255,125,90; eye 105,90,75; shirt 175,165,140; undershirt 160,180,215; pants 255,230,175; shoe 160,105,60. 【无变化】
- New fields voiceVariant, voicePitchOffset (new L1234-1236). 【可选增强】
- skinVariant clamp: old clamp(0..11) hard-coded (old L35834); new clamp(0..PlayerVariantID.Count-1) (new L54779) — same value 12. PlayerVariantID.Count=12 both. 【无变化】
- Male getter/setter same (old L1160-1178 / new L3245-3265). 【无变化】
- Hair count: Main.numberOfHairstyles 162 → 228 (old Main.cs L1851 / new Main.cs L1393); PlayerHair/PlayerHairAlt arrays 162 → 228 (TextureAssets old L91-92 / new L584-586). Character-creation available hairstyles: old 70 (HairstyleUnlocksHelper old L48-68) → new 212 (new L53-92). 【必须改】(note: current TS uses 1..228 all available — should use AvailableHairstyles list of 212 ids)
- Hair load clamp: new rejects hair >= 228 → 0 (new L54210-54212); old had none. 【可选增强】
- GetHairSettings: backHairDraw formula same; head switch lists expanded (new hats). 【无变化】(core formula)

### 6. PlayerDrawLayers.cs / PlayerDrawSet.cs
- Channel→color mapping unchanged: 0 head(colorHead), 1 eyeWhites, 2 eyes, 3/5/7/9 bodySkin, 4/8 undershirt, 6/13/14 shirt, 10 legs(colorLegs), 11 pants, 12 shoes, 15 eyelid (3 frames). Verified both versions. 【无变化】
- skinVar = drawPlayer.skinVariant unchanged (old PlayerDrawSet L212 / new L368). 【无变化】
- Hair rendering reworked: old single hairFrame (PlayerDrawSet old L94, L1181-1186, Y-=336, hideHair→height 0) drawn in one layer; new split hairFrontFrame/hairBackFrame (new L183, L185, L1743-1756): back frame drawn behind body (new L206-212) and front frame clipped to height 26 when backHairDraw (new L2150-2162). 【必须改】 for accurate 1.4.5.6 hair look.
- TextureAssets.Players [12,16] both (PlayerDataInitializer identical). 【无变化】
- Eyelid (channel 15) drawing extracted to DrawPlayer_21_Head_TheFace_Eyelid with mount flip tweaks; base logic same (old L1692-1705 / new L2647-2685). 【无变化】
- New minor: hidesBottomSkin adds legs 214/215/216; drawFloatingTube gated on hideEntirePlayer (new PlayerDrawSet L1759-1764). 【可选增强】

### 7. UIHairStyleButton / UIClothStyleButton
- Sizes unchanged 44×44 and 44×80 (old hair L29-30/new L30-31; old cloth L31-32 / new L37-38). 【无变化】
- Hair button new: sets _player.head = -1 during preview so headgear doesn't cover hair (new L70-76) 【可选增强】; SkipRenderingContent (new L23-39, L65-69) 【可选增强】.
- Cloth button new: PrepareAction param (new L30-36, L54-58), calls PlayerFrame() in Draw, LeftMouseDown no longer sets skinVariant (old L70-75 vs new L91-94) 【必须改】click flow.
- ClothStyleButton preview UICharacter now created without explicit 1f scale (uses default) — same.
- UIDifficultyButton: behavior identical; only MouseDown→LeftMouseDown rename (old L75-80 / new L82-87). Size 44×110 unchanged. 【无变化】

Also note event API renames OnMouseDown→OnLeftMouseDown, OnClick→OnLeftClick throughout — irrelevant to TS port.

Also Appearance.ts notes: VALID_CLOTH_STYLES old order needs update to [0,2,1,3,8,9,7,5,6,4]; HAIR_COUNT 228 fine but creation list should be the 212; skinVariant clamp 0-11 fine; hair clamped 1..228 vs vanilla 0..227 — off-by-one! In vanilla hair is 0-based; TS uses 1..228. Worth flagging as must-check.

Let me write the final report in Chinese with tables.
```

</details>


---

## 🤖 Assistant · 2026-08-09T11:52:32.409Z · glm-x-preview-260804

```
# 角色系统差异清单（1.4.0.5 → 1.4.5.6）

对比基准（均已逐行核对）：
- 旧版 `~/Project/GLM/SandboxWorld/Terarria1405/`（`GameContent/UI/...`、`DataStructures/`）
- 新版 `~/Project/GLM/SandboxWorld/Terarria1456/`（`Terraria.GameContent.UI.States/`、`Terraria.GameContent.UI.Elements/`、`Terraria.DataStructures/`、`Terraria/Player.cs`）

下表「行号」格式为：旧版行号 → 新版行号。

## 1. UICharacterCreation.cs

| # | 项目 | 差异 | 标记 |
|---|---|---|---|
| 1.1 | `_validClothStyles` | 旧 `[0,2,1,3,8,4,6,5,7,9]`（旧 L31-43）→ 新 `[0,2,1,3,8,9,7,5,6,4]`（新 L58）。**顺序变了**：前 5 个是男装（0,2,1,3,8），后 5 个是女装（9,7,5,6,4）。`Appearance.ts:79` 目前是旧顺序 | 【必须改】 |
| 1.2 | 新增 `_defaultHairstylesForClothStyle` | 新 L60-72：`{0:0, 2:1, 1:12, 3:2, 8:28, 9:68, 7:18, 5:22, 6:81, 4:5}`，配合 `TryAutoAssigningHair()`（新 L630-636）与 `_lastSelectedHairstyle`（新 L138、L306-309）实现"选服装自动配发型，直到用户手动选发型为止" | 【可选增强】 |
| 1.3 | 语音系统（全新） | `_validVoiceStyles=[1,2,3]`（新 L74）；语音切换/播放按钮 + 音高滑条 UI（新 L441-527）；预览用 `PlayHurtSound()`（新 L1513-1528）；`Main.CycleVoiceStyle`（新 L1530-1540）；音高 20 档量化 `RemapPitchSliderKnob`（新 L681-697）；性别切换自动联动语音 `UpdateSelectedGender`（新 L1311-1335，`_oldMaleForVoiceAutoSwitch` L136）。对应 `Player.cs` 新字段 `voiceVariant`/`voicePitchOffset`（新 Player.cs L1234-1236）、`PlayerVoiceID`（Male=1/Female=2/Other=3，带颜色） | 【可选增强】 |
| 1.4 | 默认难度 | 旧构造函数 `_player.difficulty = 3`（创意模式，旧 L76）→ 新 `= 0`（经典/软核，新 L169） | 【必须改】（若移植默认难度） |
| 1.5 | `CategoryId` 枚举 | 完全一致（新 L25-38：CharInfo/Clothing/HairStyle/HairColor/Eye/Skin/Shirt/Undershirt/Pants/Shoes） | 【无变化】 |
| 1.6 | HSL 取色面板 | 亮度映射 `luminosity*0.85+0.15` 及 `RgbToScaledHsl` 完全一致（旧 L1479-1489 → 新 L2359-2369）；H/S/L 三滑条、HEX 文本、复制/粘贴/随机单色逻辑一致（旧 L499-564/1113-1121 → 新 L970-1041/1784-1792） | 【无变化】 |
| 1.7 | 颜色应用映射 | `ApplyPendingColor` 与 `UpdateColorPickers` 索引一致：`[3]=hair [4]=eye [5]=skin [6]=shirt [7]=undershirt [8]=pants [9]=shoes`（旧 L664-690/1194-1205 → 新 L1143-1169/1868-1879） | 【无变化】 |
| 1.8 | 服装页布局 | 旧的"男/女性别按钮 + 分隔线"（旧 L221-250）被删除，改为 **5 个盔甲预览预设**（无/神圣/银/礼服/泳装，新 L336-395；`ArmorAssignments` 结构 L47-56，`EquipArmor*` L531-614，`UpdatePreviewItems` L638-648 写 armor[0..2]）。性别不再由独立按钮控制，而是由 skinVariant 本身决定（`Player.Male` getter 由 `PlayerVariantID.Sets.Male[skinVariant]` 推导，两边相同） | 【可选增强】 |
| 1.9 | 服装点击语义 | 旧：`UIClothStyleButton.MouseDown` 直接写 `skinVariant`（旧按钮 L70-75），`Click_CharClothStyle` 只换图标（旧 L790-794）。新：按钮自身不再写 `skinVariant`（新按钮 L91-94 只调 `base.LeftMouseDown`），改由 `Click_CharClothStyle` 从 `evt` 的 `ClothStyleId` 写入（新 L1283-1297，含盔甲预览激活时的穿透逻辑） | 【必须改】（点击流程） |
| 1.10 | 随机角色 | ① 新版先随机一次 eyeColor 再进 while（新 L1553-1557，旧 L924 只 while）；② 新增 voiceVariant 随机（新 L1572-1576）；③ **女性发型判定表从 12 个 id 扩到约 70 个**（旧 L938-957 → 新 L1577-1653）；④ 随机后重置盔甲预览（新 L1654） | 【必须改】（③）；①④ 【可选增强】 |
| 1.11 | 模板复制/粘贴 | JSON 新增 `voiceStyle`、`voicePitch` 字段（新 L1368-1369、L1463-1476） | 【可选增强】 |
| 1.12 | 返回按钮 | 新增 dirty 检测 + 返回确认（`BackupConfirmationState`、menuMode 40；新 L152-156、L1216-1228、L2016-2026）；新增 `GameTipsDisplay`（新 L170、L2000-2015） | 【可选增强】 |
| 1.13 | 顶部"服装"分类按钮 | 旧是单色图标；新叠加 7 层 `ColorCharacter` 分层图（`_characterPreviewLayers`，新 L140、L749-761，每层对应 hair/eye/skin/shirt/undershirt/pants/shoes 颜色，L803-812） | 【可选增强】 |
| 1.14 | 发型按钮初始化 | 每个发型按钮创建时 `SkipRenderingContent(i)`（新 L299），把头部渲染分摊到多帧，避免首帧卡顿 | 【可选增强】 |
| 1.15 | 手柄导航点 | 因新增 Preview/pitch snap point，Clothing 分支重写（新 L2199-2296） | 【可选增强】 |

## 2. UICharacter.cs

| # | 项目 | 差异 | 标记 |
|---|---|---|---|
| 2.1 | 尺寸 | 59×58 不变（旧 L27-28 → 新 L43-44） | 【无变化】 |
| 2.2 | 动画帧公式 | `(int)(GlobalTimeWrappedHourly / 0.07) % 14 + 6) * 56` 不变（旧 L57 → 新 L92-93） | 【无变化】 |
| 2.3 | 状态更新时机 | 旧 `Update()` 里调 `ResetEffects/ResetVisibleAccessories/UpdateMiscCounter/UpdateDyes/PlayerFrame`（旧 L37-47）；新版全部移入 `DrawSelf()`，`Update()` 只累加 `_animationCounter`（新 L76-83、L104-114） | 【可选增强】 |
| 2.4 | 宠物预览（全新） | `_petProjectiles` + `PreparePetProjectiles` + `DrawPets`（新 L14、L30、L55-74、L114、L132-152）；有宠物时玩家绘制位置 `X -= 10`（新 L122-130） | 【可选增强】 |
| 2.5 | `PrepareAction` 钩子 | 新增（新 L28、L108-111）；角色创建页用它设置 `direction`、自动发型、盔甲预览（UICharacterCreation L616-628） | 【可选增强】 |
| 2.6 | `useAClone` 参数 | 新增（新 L34-42）：列表预览用 `SerializedClone()`，避免 UI 动画污染真实 Player 数据 | 【必须改】（若 UI 与存档共享对象）否则【可选增强】 |

## 3. UICharacterSelect.cs

| # | 项目 | 差异 | 标记 |
|---|---|---|---|
| 3.1 | 布局 | 外层 80%/650px/Top220/高-220、面板背景色、列表 padding 5、滚动条自动挂载逻辑全部一致（旧 L34-105 → 新 L35-106） | 【无变化】 |
| 3.2 | 排序 | 旧：收藏优先 → 名字 → 文件名（旧 L147-155）。新：收藏优先 → **LastPlayed 降序** → 名字 → 文件名（新 L149-151） | 【必须改】（若移植排序） |
| 3.3 | 手柄点阵 | 4 列 → 5 列（新增 "Rename"）（旧 L242-250 → 新 L246-267） | 【可选增强】 |

## 4. UICharacterListItem.cs

| # | 项目 | 差异 | 标记 |
|---|---|---|---|
| 4.1 | 按钮 X 布局 | 旧：Play=4、Favorite=28、Cloud=52、Delete 右对齐、label 固定 80（旧 L59-111）。新：游标 `num` 递增（Play=4、Favorite=28、Cloud=52、**Rename=76**、label=104/128）（新 L71-133） | 【必须改】（新增 Rename 与 label 位置） |
| 4.2 | Rename 功能（全新） | `ButtonRename` 贴图 + `RenameButtonClick`（新 L59、L101-107、L196-214），虚拟键盘改名 | 【可选增强】 |
| 4.3 | 预览角色 | 新版 `useAClone: true`（新 L66） | 【必须改】/【可选增强】（同 2.6） |
| 4.4 | 排序比较 | 旧 `CompareTo` 用收藏/名字（旧 L207-216）→ 新用 `_orderInList`（新 L285-292，`_orderInList` L45、L65） | 【可选增强】 |
| 4.5 | 名字显示 | 加载失败时名字前缀 `(状态名)` 并置灰（新 L323-331） | 【可选增强】 |
| 4.6 | 其余绘制 | 内嵌血/蓝条、难度颜色（Softcore/Mediumcore 白-橙/Hardcore 红/Creative 紫）、游玩时长格式完全一致（旧 L241-297 → 新 L317-383） | 【无变化】 |

## 5. Player.cs 默认外观

| # | 项目 | 差异 | 标记 |
|---|---|---|---|
| 5.1 | 7 个默认颜色 | **完全一致**：hair `215,90,55` / skin `255,125,90` / eye `105,90,75` / shirt `175,165,140` / underShirt `160,180,215` / pants `255,230,175` / shoe `160,105,60`（旧 L199-205 → 新 L2420-2432） | 【无变化】 |
| 5.2 | 新字段 | `voiceVariant`、`voicePitchOffset`（新 L1234-1236） | 【可选增强】 |
| 5.3 | skinVariant 上限 | 旧硬编码 `Clamp(0,11)`（旧 L35834）→ 新 `Clamp(0, PlayerVariantID.Count-1)`（新 L54779）。`PlayerVariantID.Count = 12` 两边相同，0-11 共 12 个变体，`Sets.Male/AltGenderReference/VariantOrder` 全部一致 | 【无变化】 |
| 5.4 | `Male` 属性 | getter/setter 逻辑一致（旧 L1160-1178 → 新 L3245-3265） | 【无变化】 |
| 5.5 | 发型总数 | `Main.numberOfHairstyles` 162 → 228（旧 Main.cs L1851 → 新 Main.cs L1393）；`TextureAssets.PlayerHair/PlayerHairAlt` 数组 162 → 228（旧 TextureAssets L91-92 → 新 L584-586） | 【必须改】 |
| 5.6 | **角色创建可用发型** | 旧 70 个：0-50 + {136..144,147..151,154,155,157,158,161}（旧 HairstyleUnlocksHelper L48-68）。新 **212 个**：0-50 + 上组 + 51-122 + {134,135,146,152,153,156,165,160} + 166-227（新 L53-92）。注意当前 TS 的 `for (i=1..HAIR_COUNT)` 不等价于原版（且原版发型 id 是 **0 基**，TS 用 1..228 存在整体偏移） | 【必须改】 |
| 5.7 | 存档读取保护 | 新版 `hair >= 228 → 0`（新 L54209-54212），旧版无 | 【可选增强】 |
| 5.8 | `GetHairSettings` | `backHairDraw` 公式一字不差（旧 L10771 → 新 16711 附近）；head switch 列表因新头盔扩表 | 【无变化】 |

## 6. PlayerDrawLayers.cs / PlayerDrawSet.cs

| # | 项目 | 差异 | 标记 |
|---|---|---|---|
| 6.1 | `Players[skinVar, n]` 通道→颜色映射 | **完全一致**（两侧逐通道核对）：`0`=头(colorHead)、`1`=眼白(colorEyeWhites)、`2`=瞳(colorEyes)、`3,5,7,9`=皮肤(colorBodySkin)、`4,8`=内衬(colorUnderShirt)、`6,13,14`=上衣(colorShirt)、`10`=腿(colorLegs)、`11`=裤(colorPants)、`12`=鞋(colorShoes)、`15`=眼睑(3 帧动画) | 【无变化】 |
| 6.2 | `skinVar` 来源 | `skinVar = drawPlayer.skinVariant` 不变（旧 PlayerDrawSet L212 → 新 L368） | 【无变化】 |
| 6.3 | **发型绘制拆分** | 旧：单一 `hairFrame`（Y-336，hideHair 时 Height=0），一张图一层（旧 PlayerDrawSet L94、L1181-1186；旧 Layers L142/147/1428/1435）。新：拆成 `hairFrontFrame` + `hairBackFrame`（新 PlayerDrawSet L183/L185、L1743-1756）；**backHairDraw 时后发层画在身体后**（新 Layers L206-212），前发层裁到 26px 高（新 Layers L2150-2162）。1.4.4+ 发型贴图含前/后两套帧 | 【必须改】（要还原长发/后发效果） |
| 6.4 | `Players[,]` 贴图表 | 两版均 `[12,16]`，`PlayerDataInitializer` 逐变体加载清单完全一致（旧 L17-247 → 新 L12-141） | 【无变化】 |
| 6.5 | 眼睑层 | 抽成 `DrawPlayer_21_Head_TheFace_Eyelid`，新增坐骑翻转/着色特判（新 L2647-2685），基础帧逻辑同旧 L1692-1705 | 【无变化】 |
| 6.6 | 其他小改 | `hidesBottomSkin` 增加 legs 214/215/216；`drawFloatingTube` 增加 hideEntirePlayer 判断（新 PlayerDrawSet L1759-1764） | 【可选增强】 |

## 7. UIHairStyleButton / UIClothStyleButton / UIDifficultyButton

| # | 项目 | 差异 | 标记 |
|---|---|---|---|
| 7.1 | 尺寸 | 发型 44×44、服装 44×80、难度 44×110，全部不变（旧 L29-30/31-32/36-37 → 新 L30-31/37-38/32-33） | 【无变化】 |
| 7.2 | 发型按钮：头盔遮挡 | 绘制头部前临时 `_player.head = -1`（新 L70-76），预览不被头盔挡住 | 【可选增强】 |
| 7.3 | 发型按钮：渲染跳帧 | `SkipRenderingContent`/`_framesToSkip`（新 L23-39、L65-69） | 【可选增强】 |
| 7.4 | 服装按钮：点击 | 旧 `MouseDown` 直接写 `skinVariant`（旧 L70-75）→ 新不写，交给父级 `Click_CharClothStyle`（新 L91-94 + UICharacterCreation L1283-1297） | 【必须改】（同 1.9） |
| 7.5 | 服装按钮：`PrepareAction` | 新增参数，`Draw()` 里在换 skinVariant 后调用并 `PlayerFrame()`（新 L30-36、L50-63） | 【可选增强】 |
| 7.6 | UIDifficultyButton | 行为/尺寸/颜色算法一致，仅 `MouseDown`→`LeftMouseDown` 命名变化（旧 L75-80 → 新 L82-87） | 【无变化】 |
| 7.7 | 全局事件重命名 | `OnMouseDown→OnLeftMouseDown`、`OnClick→OnLeftClick`、`OnDoubleClick→OnLeftDoubleClick`（纯 API 改名，不影响行为） | 【无变化】 |

## 对移植的三条最高优先级建议

1. **`Appearance.ts`**：`VALID_CLOTH_STYLES` 改为 `[0,2,1,3,8,9,7,5,6,4]`（含男/女分组语义）；发型 id 改 0 基（0..227），并按新版 `HairstyleUnlocksHelper` 用 212 个白名单而不是全量 228。
2. **`UICharacterCreationState.ts`**：服装点击改为"点击即写 skinVariant（同时决定性别）"，移除独立性别按钮的必要；随机角色的女性发型判定表需按新版 L1577-1653 更新。
3. **`PaperDoll.ts`**：通道→颜色映射表可原样保留（验证为无变化），但发型渲染需从"单层 hairFrame"升级为"前发 + 后发两层"（backHairDraw 时后发画在身体之后、前发裁 26px），否则 1.4.5.6 的 66 个新发型（166-227）会显示错误。
```
