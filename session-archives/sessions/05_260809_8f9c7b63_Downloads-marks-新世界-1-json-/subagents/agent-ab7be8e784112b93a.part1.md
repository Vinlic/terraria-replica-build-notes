# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-10T06:44:40.482Z

```
你在 ~/Project/GLM/SandboxWorld/game 工作。这是泰拉瑞亚 1:1 复刻项目。任务:把石巨人 Boss 族 AI 从反编译源码 1:1 移植到 TypeScript。

【原版源码】~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs(注意目录名拼写是 Terarria1456;1.4.5.6,以此为准):
- aiStyle 45 石巨人本体 245: 分发在 NPC.cs:31269(4 行委托)→ AI_045_Golem() 在 NPC.cs:19447 开始
- aiStyle 46 石巨人头 246: NPC.cs:31273-31495
- aiStyle 47 石巨人拳 247: 分发 NPC.cs:31496 → AI_047_GolemFist() 在 NPC.cs:19171 开始
1:1 移植(经典模式;expert/getGoodWorld 只注释;netcode 跳过)。

【数据缺口】game/public/sprites/vanilla-npcs.json 缺 NPC 248(石巨人左拳)。先看 SetDefaults 源(NPC.cs 里 `type == 248` 或 247 分支)补一条与 247 对称的数据到该 JSON(只允许改这一个文件;字段完全参照现有 247 条目的字段结构:name/aiStyle=47/lifeMax/damage/defense/width/height/frames/Hitsound 等)。

【写到哪里】新建 game/src/entities/bossAI_golem.ts。**严禁修改** Enemy.ts / Game.ts / Renderer.ts / bossAI.ts / bossAI_*.ts / 其它已有文件(主会话统一接线)。从 './bossAI' 导入:spawnPart(game,src,id)、shoot(game,x,y,vx,vy,dmg,projId,life)、seek、accelTo、losClear、addEnemy。参考 game/src/entities/bossAI.ts 的 Prime 头+部件写法(部件锚定头 id 的 find-head 模式、基值缓存)。

【Enemy 字段】x,y,w,h,cx,cy,vx,vy,facing,spin,ai0-ai3(ai0 默认 -1120,首帧 bInit 复位),aiT,bInit,hp/maxHp,dead,onGround,def.damage/def.defense(临时修正自建 WeakMap 基值缓存)。**移动自己积分**;石巨人本体行走+跳跃(落地判定可在自己文件里复制一份 collideGround——bossAI.ts 里那份是 private)。
【GameHooks】game.world.store(isSolid/inBounds/idx),game.world.clock.isDay,game.enemies(),game.spawnParticles,game.playSfx。
【导出】export function golemAI / golemHeadAI / golemFistAI,(e: Enemy, game: GameHooks, player: Player | null)。
【行为要点】本体 245:跳跃追玩家(按 vanilla 跳跃节奏);本体 hp 归零→头 246 起飞进入二阶段(头脱离本体自主战斗;本体死透后头继续);头 246:悬浮-冲撞循环+火焰弹/眼睛激光(vanilla proj,经典伤害);拳 247/248:锚定本体(或头),蓄力冲拳(直线冲出后回位),ai0=侧别。石巨人白天不逃(神庙 Boss)。参考 bossAI_duke_moonlord.ts 里月总 checkDead 模式:本体/头血尽转换在各自 AI 首行处理(hp<=0 → 置态+按需满血续命),不要依赖外部钩子。
【弹幕贴图】Projectile_N.png 已全量在 game/public/sprites/vanilla/。

【探针】新建 game/scripts/_golemprobe.mts,模板照抄 game/scripts/_mechprobe.mts(fake game + 地板 y=150 + 夜晚,全套空 stub)。断言:①245 首帧生成头 246+双拳 247/248 ②本体跳跃位移(onGround 切换) ③本体 hp→0 后头存活进入自主战斗(头的位移/状态变化) ④拳蓄力冲出后回位(记录拳位移峰值>100px 再回归头部附近) ⑤头死→全族自毁。跑 `node_modules/.bin/vite-node scripts/_golemprobe.mts` 全绿(process.exit(bad?1:0))。
最后 `./node_modules/.bin/tsc --noEmit 2>&1 | grep bossAI_golem` 无错。
【汇报】中文:移植内容、简化项(带行号)、248 数据补了什么、探针结果、接线清单(aiStyle→函数、旋转 NPC id、召唤 key)。
```

---

## 📎 Attachment · skill_listing · 2026-08-10T06:44:40.485Z

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

## 🤖 Assistant · 2026-08-10T06:44:43.554Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the relevant source files and existing project structure.

I need to:
1. Read the vanilla source for AI_045_Golem (NPC.cs:19447), aiStyle 46 dispatch (NPC.cs:31273-31495), AI_047_GolemFist (NPC.cs:19171)
2. Look at SetDefaults for NPC 245, 246, 247, 248
3. Check existing bossAI.ts, bossAI_duke_moonlord.ts for patterns
4. Check vanilla-npcs.json for 247 entry to mirror for 248
5. Write bossAI_golem.ts
6. Write _golemprobe.mts
7. Run probe + tsc

Let me start reading files in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:44:43.991Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19447,19620p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_045_Golem source part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:44:44.024Z

**📎 ToolResult**

```
	private void AI_045_Golem()
	{
		golemBoss = whoAmI;
		float num = GetMyBalance();
		if (Main.getGoodWorld)
		{
			num += 2f;
		}
		if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
		{
			num *= 2f;
		}
		if (localAI[0] == 0f)
		{
			localAI[0] = 1f;
			if (Main.netMode != 1)
			{
				NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X - 84, (int)base.Center.Y - 9, 247);
				NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X + 78, (int)base.Center.Y - 9, 248);
				NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X - 3, (int)base.Center.Y - 57, 246);
			}
		}
		if (target >= 0 && Main.player[target].dead)
		{
			TargetClosest();
			if (Main.player[target].dead)
			{
				noTileCollide = true;
			}
		}
		if (alpha > 0)
		{
			alpha -= 10;
			if (alpha < 0)
			{
				alpha = 0;
			}
			ai[1] = 0f;
		}
		bool flag = false;
		bool flag2 = false;
		bool flag3 = false;
		dontTakeDamage = false;
		for (int i = 0; i < Main.maxNPCs; i++)
		{
			NPC nPC = Main.npc[i];
			if (nPC.active)
			{
				switch (nPC.type)
				{
				case 246:
					flag = true;
					break;
				case 247:
					flag2 = true;
					break;
				case 248:
					flag3 = true;
					break;
				}
			}
		}
		dontTakeDamage = flag;
		if (Main.netMode != 1 && Main.getGoodWorld && velocity.Y > 0f)
		{
			for (int j = (int)(position.X / 16f); (float)j < (position.X + (float)width) / 16f; j++)
			{
				for (int k = (int)(position.Y / 16f); (float)k < (position.Y + (float)width) / 16f; k++)
				{
					Tile tile = Main.tile[j, k];
					if (tile != null && tile.active() && TileID.Sets.Torches[tile.type])
					{
						Main.tile[j, k].active(active: false);
						if (Main.netMode == 2)
						{
							NetMessage.SendTileSquare(-1, j, k);
						}
					}
				}
			}
		}
		position += netOffset;
		if (!Main.getGoodWorld)
		{
			if (!flag2)
			{
				int num2 = Dust.NewDust(new Vector2(base.Center.X - 80f * scale, base.Center.Y - 9f), 8, 8, 31, 0f, 0f, 100);
				Main.dust[num2].alpha += Main.rand.Next(100);
				Main.dust[num2].velocity *= 0.2f;
				Main.dust[num2].velocity.Y -= 0.5f + (float)Main.rand.Next(10) * 0.1f;
				Main.dust[num2].fadeIn = 0.5f + (float)Main.rand.Next(10) * 0.1f;
				if (Main.rand.Next(10) == 0)
				{
					num2 = Dust.NewDust(new Vector2(base.Center.X - 80f * scale, base.Center.Y - 9f), 8, 8, 6);
					if (Main.rand.Next(20) != 0)
					{
						Main.dust[num2].noGravity = true;
						Main.dust[num2].scale *= 1f + (float)Main.rand.Next(10) * 0.1f;
						Main.dust[num2].velocity.Y -= 1f;
					}
				}
			}
			if (!flag3)
			{
				int num3 = Dust.NewDust(new Vector2(base.Center.X + 62f * scale, base.Center.Y - 9f), 8, 8, 31, 0f, 0f, 100);
				Main.dust[num3].alpha += Main.rand.Next(100);
				Main.dust[num3].velocity *= 0.2f;
				Main.dust[num3].velocity.Y -= 0.5f + (float)Main.rand.Next(10) * 0.1f;
				Main.dust[num3].fadeIn = 0.5f + (float)Main.rand.Next(10) * 0.1f;
				if (Main.rand.Next(10) == 0)
				{
					num3 = Dust.NewDust(new Vector2(base.Center.X + 62f * scale, base.Center.Y - 9f), 8, 8, 6);
					if (Main.rand.Next(20) != 0)
					{
						Main.dust[num3].noGravity = true;
						Main.dust[num3].scale *= 1f + (float)Main.rand.Next(10) * 0.1f;
						Main.dust[num3].velocity.Y -= 1f;
					}
				}
			}
		}
		position -= netOffset;
		if (noTileCollide && !Main.player[target].dead)
		{
			if (velocity.Y > 0f && base.Bottom.Y > Main.player[target].Top.Y)
			{
				noTileCollide = false;
			}
			else if (Collision.CanHit(position, width, height, Main.player[target].Center, 1, 1) && !Collision.SolidTiles(position, width, height))
			{
				noTileCollide = false;
			}
		}
		if (ai[0] == 0f)
		{
			if (velocity.Y == 0f)
			{
				velocity.X *= 0.8f;
				float num4 = 1f;
				if (ai[1] > 0f)
				{
					if (!flag2)
					{
						num4 += 2f;
					}
					if (!flag3)
					{
						num4 += 2f;
					}
					if (!flag)
					{
						num4 += 2f;
					}
					if (life < lifeMax)
					{
						num4 += 1f;
					}
					if (life < lifeMax / 2)
					{
						num4 += 4f;
					}
					if (life < lifeMax / 3)
					{
						num4 += 8f;
					}
					num4 *= num;
					if (Main.getGoodWorld)
					{
						num4 += 100f;
					}
				}
				ai[1] += num4;
				if (ai[1] >= 300f)
				{

```


---

## 🤖 Assistant · 2026-08-10T06:44:44.494Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19171,19447p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_047_GolemFist source"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:44:44.520Z

**📎 ToolResult**

```
	private void AI_047_GolemFist()
	{
		float num = GetMyBalance();
		if (Main.getGoodWorld)
		{
			num += 3f;
		}
		if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
		{
			num *= 2f;
		}
		if (golemBoss < 0)
		{
			StrikeNPCNoInteraction(9999, 0f, 0);
			return;
		}
		if (alpha > 0)
		{
			alpha -= 10;
			if (alpha < 0)
			{
				alpha = 0;
			}
			ai[1] = 0f;
		}
		Player player = Main.player[target];
		NPC nPC = Main.npc[golemBoss];
		Vector2 vector = nPC.Center + nPC.velocity + new Vector2(0f, -9f * scale);
		vector.X += (float)((type == 247) ? (-84) : 78) * scale;
		Vector2 vector2 = vector - base.Center;
		float num2 = vector2.Length();
		if (ai[0] == 0f)
		{
			noTileCollide = true;
			float num3 = 14f;
			if (life < lifeMax / 2)
			{
				num3 += 3f;
			}
			if (life < lifeMax / 4)
			{
				num3 += 3f;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
			{
				num3 += 8f;
			}
			num3 *= (num + 3f) / 4f;
			if (num3 > 32f)
			{
				num3 = 32f;
			}
			float x = vector2.X;
			float y = vector2.Y;
			float num4 = num2;
			if (num4 < 12f + num3)
			{
				rotation = 0f;
				velocity.X = x;
				velocity.Y = y;
				float num5 = num;
				ai[1] += num5;
				if (life < lifeMax / 2)
				{
					ai[1] += num5;
				}
				if (life < lifeMax / 4)
				{
					ai[1] += num5;
				}
				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
				{
					ai[1] += 10f * num5;
				}
				if (ai[1] >= 60f)
				{
					TargetClosest();
					if ((type == 247 && base.Center.X + 100f > Main.player[target].Center.X) || (type == 248 && base.Center.X - 100f < Main.player[target].Center.X))
					{
						ai[1] = 0f;
						ai[0] = 1f;
					}
					else
					{
						ai[1] = 0f;
					}
				}
			}
			else
			{
				num4 = num3 / num4;
				velocity.X = x * num4;
				velocity.Y = y * num4;
				rotation = (float)Math.Atan2(0f - velocity.Y, 0f - velocity.X);
				if (type == 247)
				{
					rotation = (float)Math.Atan2(velocity.Y, velocity.X);
				}
			}
		}
		else if (ai[0] == 1f)
		{
			ai[1] += 1f;
			base.Center = vector;
			rotation = 0f;
			velocity = Vector2.Zero;
			if (ai[1] <= 15f)
			{
				for (int i = 0; i < 1; i++)
				{
					Vector2 vector3 = Main.rand.NextVector2Circular(80f, 80f);
					Vector2 vector4 = vector3 * -1f * 0.05f;
					Vector2 vector5 = Main.rand.NextVector2Circular(20f, 20f);
					Dust dust = Dust.NewDustPerfect(base.Center + vector4 + vector3 + vector5, 228, vector4);
					dust.fadeIn = 1.5f;
					dust.scale = 0.5f;
					if (Main.getGoodWorld)
					{
						dust.noLight = true;
					}
					dust.noGravity = true;
				}
			}
			if (ai[1] >= 30f)
			{
				noTileCollide = true;
				collideX = false;
				collideY = false;
				ai[0] = 2f;
				ai[1] = 0f;
				float num6 = 12f;
				if (life < lifeMax / 2)
				{
					num6 += 4f;
				}
				if (life < lifeMax / 4)
				{
					num6 += 4f;
				}
				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
				{
					num6 += 10f;
				}
				num6 *= (num + 3f) / 4f;
				if (num6 > 48f)
				{
					num6 = 48f;
				}
				Vector2 vector6 = new Vector2(base.Center.X, base.Center.Y);
				float num7 = Main.player[target].Center.X - vector6.X;
				float num8 = Main.player[target].Center.Y - vector6.Y;
				float num9 = (float)Math.Sqrt(num7 * num7 + num8 * num8);
				num9 = num6 / num9;
				velocity.X = num7 * num9;
				velocity.Y = num8 * num9;
				rotation = (float)Math.Atan2(velocity.Y, velocity.X);
				if (type == 247)
				{
					rotation = (float)Math.Atan2(0f - velocity.Y, 0f - velocity.X);
				}
			}
		}
		else if (ai[0] == 2f)
		{
			if (Main.netMode != 1 && Main.getGoodWorld)
			{
				for (int j = (int)(position.X / 16f) - 1; (float)j < (position.X + (float)width) / 16f + 1f; j++)
				{
					for (int k = (int)(position.Y / 16f) - 1; (float)k < (position.Y + (float)width) / 16f + 1f; k++)
					{
						Tile tile = Main.tile[j, k];
						if (tile != null && tile.active() && TileID.Sets.Torches[tile.type])
						{
							Main.tile[j, k].active(active: false);
							if (Main.netMode == 2)
							{
								NetMessage.SendTileSquare(-1, j, k);
							}
						}
					}
				}
			}
			ai[1] += 1f;
			if (ai[1] == 1f)
			{
				SoundEngine.PlaySound(SoundID.Item14, position);
			}
			if (Main.rand.Next(2) == 0)
			{
				Vector2 vector7 = velocity * 0.5f;
				Vector2 vector8 = Main.rand.NextVector2Circular(20f, 20f);
				Dust.NewDustPerfect(base.Center + vector7 + vector8, 306, vector7, 0, Main.OurFavoriteColor).scale = 2f;
			}
			if (Math.Abs(velocity.X) > Math.Abs(velocity.Y))
			{
				if (velocity.X > 0f && base.Center.X > player.Center.X)
				{
					noTileCollide = false;
				}
				if (velocity.X < 0f && base.Center.X < player.Center.X)
				{
					noTileCollide = false;
				}
			}
			else
			{
				if (velocity.Y > 0f && base.Center.Y > player.Center.Y)
				{
					noTileCollide = false;
				}
				if (velocity.Y < 0f && base.Center.Y < player.Center.Y)
				{
					noTileCollide = false;
				}
			}
			if (num2 > 700f || collideX || collideY)
			{
				noTileCollide = true;
				ai[0] = 0f;
			}
		}
		else
		{
			if (ai[0] != 3f)
			{
				return;
			}
			noTileCollide = true;
			float num10 = 0.4f;
			Vector2 vector9 = new Vector2(base.Center.X, base.Center.Y);
			float num11 = Main.player[target].Center.X - vector9.X;
			float num12 = Main.player[target].Center.Y - vector9.Y;
			float num13 = (float)Math.Sqrt(num11 * num11 + num12 * num12);
			num13 = 12f / num13;
			num11 *= num13;
			num12 *= num13;
			if (velocity.X < num11)
			{
				velocity.X += num10;
				if (velocity.X < 0f && num11 > 0f)
				{
					velocity.X += num10 * 2f;
				}
			}
			else if (velocity.X > num11)
			{
				velocity.X -= num10;
				if (velocity.X > 0f && num11 < 0f)
				{
					velocity.X -= num10 * 2f;
				}
			}
			if (velocity.Y < num12)
			{
				velocity.Y += num10;
				if (velocity.Y < 0f && num12 > 0f)
				{
					velocity.Y += num10 * 2f;
				}
			}
			else if (velocity.Y > num12)
			{
				velocity.Y -= num10;
				if (velocity.Y > 0f && num12 < 0f)
				{
					velocity.Y -= num10 * 2f;
				}
			}
			rotation = (float)Math.Atan2(velocity.Y, velocity.X);
			if (type == 247)
			{
				rotation = (float)Math.Atan2(0f - velocity.Y, 0f - velocity.X);
			}
		}
	}

	private void AI_045_Golem()

```


---

## 🤖 Assistant · 2026-08-10T06:44:47.871Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait — I notice the fist AI references golemBoss (the body NPC index) — but actually AI_047 uses `golemBoss` which is set by the body's AI_045. Interesting: after the head detaches, the fists still anchor to the body. Hmm, in vanilla 1.4, when the body dies, does the head take over? Let me check: the task says "拳 247/248:锚定本体(或头)". In vanilla, when golem body dies... Let me check the head AI (aiStyle 46) to see what it does — and how golemBoss is updated. Let me read the rest of AI_045 and the head dispatch at 31273.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:44:48.261Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19620,19780p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_045_Golem source part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:44:48.291Z

**📎 ToolResult**

```
				{
					ai[1] = -20f;
					frameCounter = 0.0;
				}
				else if (ai[1] == -1f)
				{
					noTileCollide = true;
					TargetClosest();
					velocity.X = 4 * direction;
					if (life < lifeMax)
					{
						velocity.Y = -12.1f * (num + 9f) / 10f;
						if ((double)velocity.Y < -19.1)
						{
							velocity.Y = -19.1f;
						}
					}
					else
					{
						velocity.Y = -12.1f;
					}
					ai[0] = 1f;
					ai[1] = 0f;
				}
			}
		}
		else if (ai[0] == 1f)
		{
			if (velocity.Y == 0f)
			{
				SoundEngine.PlaySound(SoundID.Item14, position);
				ai[0] = 0f;
				for (int l = (int)position.X - 20; l < (int)position.X + width + 40; l += 20)
				{
					for (int m = 0; m < 4; m++)
					{
						int num5 = Dust.NewDust(new Vector2(position.X - 20f, position.Y + (float)height), width + 20, 4, 31, 0f, 0f, 100, default(Color), 1.5f);
						Main.dust[num5].velocity *= 0.2f;
					}
					int num6 = Gore.NewGore(new Vector2(l - 20, position.Y + (float)height - 8f), default(Vector2), Main.rand.Next(61, 64));
					Main.gore[num6].velocity *= 0.4f;
				}
			}
			else
			{
				TargetClosest();
				if (position.X < Main.player[target].position.X && position.X + (float)width > Main.player[target].position.X + (float)Main.player[target].width)
				{
					velocity.X *= 0.9f;
					if (base.Bottom.Y < Main.player[target].position.Y)
					{
						velocity.Y += 0.2f * (num + 1f) / 2f;
					}
				}
				else
				{
					if (direction < 0)
					{
						velocity.X -= 0.2f;
					}
					else if (direction > 0)
					{
						velocity.X += 0.2f;
					}
					float num7 = 3f;
					if (life < lifeMax)
					{
						num7 += 1f;
					}
					if (life < lifeMax / 2)
					{
						num7 += 1f;
					}
					if (life < lifeMax / 4)
					{
						num7 += 1f;
					}
					num7 *= (num + 1f) / 2f;
					if (velocity.X < 0f - num7)
					{
						velocity.X = 0f - num7;
					}
					if (velocity.X > num7)
					{
						velocity.X = num7;
					}
				}
			}
		}
		if (target <= 0 || target == 255 || Main.player[target].dead)
		{
			TargetClosest();
		}
		int num8 = 3000;
		if (Math.Abs(base.Center.X - Main.player[target].Center.X) + Math.Abs(base.Center.Y - Main.player[target].Center.Y) > (float)num8)
		{
			TargetClosest();
			if (Math.Abs(base.Center.X - Main.player[target].Center.X) + Math.Abs(base.Center.Y - Main.player[target].Center.Y) > (float)num8)
			{
				active = false;
			}
		}
	}

	public static bool SpawnMechQueen(int onWhichPlayer)
	{
		if (AnyNPCs(127) || AnyNPCs(134) || AnyNPCs(125) || AnyNPCs(126))
		{
			return false;
		}
		if (!SpecialSeedFeatures.Mechdusa)
		{
			return false;
		}
		if (Main.netMode == 1)
		{
			NetMessage.SendData(61, -1, -1, null, onWhichPlayer, -16f);
		}
		else
		{
			mechQueen = -2;
			SpawnOnPlayer(onWhichPlayer, 127);
			mechQueen = FindFirstNPC(127);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 125, 1);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 126, 1);
			int num = NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 134, 1);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 139, 1, 0f, 0f, num, -1f);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 139, 1, 0f, 0f, num, 1f);
		}
		return true;
	}

	public bool IsCritterThatIsHostileToPlayers()
	{
		if (type >= 0 && NPCID.Sets.CritterThatCanTurnOnPlayers[type])
		{
			return aiStyle == 3;
		}
		return false;
	}

	public void AI()
	{
		//IL_50cf9: Unknown result type (might be due to invalid IL or missing references)
		//IL_50ac3: Unknown result type (might be due to invalid IL or missing references)
		//IL_50ad0: Unknown result type (might be due to invalid IL or missing references)
		//IL_50ad5: Unknown result type (might be due to invalid IL or missing references)
		//IL_4fefc: Unknown result type (might be due to invalid IL or missing references)
		//IL_50d54: Unknown result type (might be due to invalid IL or missing references)
		//IL_50d35: Unknown result type (might be due to invalid IL or missing references)
		//IL_50d3a: Unknown result type (might be due to invalid IL or missing references)
		//IL_50afe: Unknown result type (might be due to invalid IL or missing references)
		//IL_50b3a: Unknown result type (might be due to invalid IL or missing references)
		//IL_50b3f: Unknown result type (might be due to invalid IL or missing references)
		if (aiStyle == 0)
		{
			if (Main.netMode != 1)
			{
				for (int i = 0; i < 255; i++)
				{
					if (Main.player[i].active && Main.player[i].talkNPC == whoAmI)

```


---

## 🤖 Assistant · 2026-08-10T06:44:48.718Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '31269,31500p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read aiStyle dispatch 45/46/47"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:44:48.751Z

**📎 ToolResult**

```
		else if (aiStyle == 45)
		{
			AI_045_Golem();
		}
		else if (aiStyle == 46)
		{
			float num720 = GetMyBalance();
			if (Main.getGoodWorld)
			{
				num720 += 3f;
			}
			if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
			{
				num720 *= 2f;
			}
			noTileCollide = true;
			if (golemBoss < 0)
			{
				StrikeNPCNoInteraction(9999, 0f, 0);
				return;
			}
			float num721 = 100f;
			Vector2 vector83 = new Vector2(base.Center.X, base.Center.Y);
			float num722 = Main.npc[golemBoss].Center.X - vector83.X;
			float num723 = Main.npc[golemBoss].Center.Y - vector83.Y;
			num723 -= 57f * scale;
			num722 -= 3f * scale;
			float num724 = (float)Math.Sqrt(num722 * num722 + num723 * num723);
			if (num724 < num721)
			{
				rotation = 0f;
				velocity.X = num722;
				velocity.Y = num723;
			}
			else
			{
				num724 = num721 / num724;
				velocity.X = num722 * num724;
				velocity.Y = num723 * num724;
				rotation = velocity.X * 0.1f;
			}
			if (alpha > 0)
			{
				alpha -= 10;
				if (alpha < 0)
				{
					alpha = 0;
				}
				this.ai[1] = 30f;
			}
			if (this.ai[0] == 0f)
			{
				this.ai[1] += 1f;
				int num725 = 300;
				if (this.ai[1] < 20f || this.ai[1] > (float)(num725 - 20))
				{
					this.ai[1] += 2f * (num720 - 1f) / 3f;
					localAI[0] = 1f;
				}
				else
				{
					this.ai[1] += 1f * (num720 - 1f) / 2f;
					localAI[0] = 0f;
				}
				if (this.ai[1] >= (float)num725)
				{
					TargetClosest();
					this.ai[1] = 0f;
					Vector2 vector84 = new Vector2(base.Center.X, base.Center.Y + 10f * scale);
					float num726 = 8f;
					float num727 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector84.X;
					float num728 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector84.Y;
					float num729 = (float)Math.Sqrt(num727 * num727 + num728 * num728);
					num729 = num726 / num729;
					num727 *= num729;
					num728 *= num729;
					int num730 = 18;
					int num731 = 258;
					if (Main.netMode != 1)
					{
						int num732 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector84.X, vector84.Y, num727, num728, num731, num730, 0f, Main.myPlayer);
					}
				}
			}
			else if (this.ai[0] == 1f)
			{
				TargetClosest();
				Vector2 vector85 = new Vector2(base.Center.X, base.Center.Y + 10f * scale);
				if (Main.player[target].Center.X < base.Center.X - (float)width)
				{
					localAI[1] = -1f;
					vector85.X -= 40f * scale;
				}
				else if (Main.player[target].Center.X > base.Center.X + (float)width)
				{
					localAI[1] = 1f;
					vector85.X += 40f * scale;
				}
				else
				{
					localAI[1] = 0f;
				}
				float num733 = (num720 + 3f) / 4f;
				this.ai[1] += num733;
				if ((double)life < (double)lifeMax * 0.4)
				{
					this.ai[1] += num733;
				}
				if ((double)life < (double)lifeMax * 0.2)
				{
					this.ai[1] += num733;
				}
				int num734 = 300;
				if (this.ai[1] < 20f || this.ai[1] > (float)(num734 - 20))
				{
					localAI[0] = 1f;
				}
				else
				{
					localAI[0] = 0f;
				}
				if (this.ai[1] >= (float)num734)
				{
					TargetClosest();
					this.ai[1] = 0f;
					float num735 = 8f;
					float num736 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector85.X;
					float num737 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector85.Y;
					float num738 = (float)Math.Sqrt(num736 * num736 + num737 * num737);
					num738 = num735 / num738;
					num736 *= num738;
					num737 *= num738;
					int num739 = 24;
					int num740 = 258;
					if (Main.netMode != 1)
					{
						int num741 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector85.X, vector85.Y, num736, num737, num740, num739, 0f, Main.myPlayer);
					}
				}
				this.ai[2] += num733;
				if (life < lifeMax / 3)
				{
					this.ai[2] += num733;
				}
				if (life < lifeMax / 4)
				{
					this.ai[2] += num733;
				}
				if (life < lifeMax / 5)
				{
					this.ai[2] += num733;
				}
				if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[2] += 4f;
				}
				if (this.ai[2] > (float)(60 + Main.rand.Next(600)))
				{
					this.ai[2] = 0f;
					int num742 = 28;
					int num743 = 259;
					if (localAI[1] == 0f)
					{
						for (int num744 = 0; num744 < 2; num744++)
						{
							vector85 = new Vector2(base.Center.X, base.Center.Y - 22f * scale);
							if (num744 == 0)
							{
								vector85.X -= 18f * scale;
							}
							else
							{
								vector85.X += 18f * scale;
							}
							float num745 = 11f;
							float num746 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector85.X;
							float num747 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector85.Y;
							float num748 = (float)Math.Sqrt(num746 * num746 + num747 * num747);
							num748 = num745 / num748;
							num746 *= num748;
							num747 *= num748;
							vector85.X += num746 * 3f;
							vector85.Y += num747 * 3f;
							if (Main.netMode != 1)
							{
								int num749 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector85.X, vector85.Y, num746, num747, num743, num742, 0f, Main.myPlayer);
								Main.projectile[num749].timeLeft = 300;
							}
						}
					}
					else if (localAI[1] != 0f)
					{
						vector85 = new Vector2(base.Center.X, base.Center.Y - 22f * scale);
						if (localAI[1] == -1f)
						{
							vector85.X -= 30f * scale;
						}
						else if (localAI[1] == 1f)
						{
							vector85.X += 30f * scale;
						}
						float num750 = 12f;
						float num751 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector85.X;
						float num752 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector85.Y;
						float num753 = (float)Math.Sqrt(num751 * num751 + num752 * num752);
						num753 = num750 / num753;
						num751 *= num753;
						num752 *= num753;
						vector85.X += num751 * 3f;
						vector85.Y += num752 * 3f;
						if (Main.netMode != 1)
						{
							int num754 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector85.X, vector85.Y, num751, num752, num743, num742, 0f, Main.myPlayer);
							Main.projectile[num754].timeLeft = 300;
						}
					}
				}
			}
			if (life < lifeMax / 2)
			{
				this.ai[0] = 1f;
			}
			else
			{
				this.ai[0] = 0f;
			}
		}
		else if (aiStyle == 47)
		{
			AI_047_GolemFist();
		}
		else if (aiStyle == 48)

```


---

## 🤖 Assistant · 2026-08-10T06:44:55.115Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to see how the head detaches and becomes independent. The head AI style 46 anchors to golemBoss... In vanilla 1.4, the head flies off when the body dies — that's handled in checkDead / StrikeNPC. Let me search for how the head transforms. Look for "246" in NPC.cs, especially checkDead or a transformation. Search for "type == 246" or NewNPC(..., 246) with some transformation. Actually the transformation is in `Transform...`? In Terraria, GolemHead becomes GolemHeadFree (type 245 is body? no). Let me recall: 245 = Golem (body), 246 = GolemHead, 247 = GolemFistLeft, 248 = GolemFistRight, 249 = GolemHeadFree. Yes! GolemHeadFree is 249. So when the body dies, the head transforms into 249 (GolemHeadFree) which is aiStyle 48. Let me check checkDead for 245/246 and look at aiStyle 48 AI.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:44:55.527Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"249\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -60",
 "description": "Find NPC 249 references"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:44:55.561Z

**📎 ToolResult**

```
12139:		else if (type == 249)
17958:		else if (type == 249)
18340:		else if (type >= 245 && type <= 249)
18616:		if (type >= 245 && type <= 249)
23495:						float num249 = 0.2f;
23500:						num252 = num249 / num252;
34399:						Lighting.AddLight(i3, j3, 0.10124999f * scale, 0.21374999f * scale, 0.225f * scale);
37493:			int num1249 = num1234 * 7;
37494:			if ((double)num1249 > frameCounter)
37498:			if ((double)num1249 < frameCounter)
39918:				Vector2 vector249 = new Vector2(0f, -8f);
39919:				velocity = (velocity * 9f + vector249) / 10f;
68949:				double num249 = frameCounter;
68952:				if (num249 >= (double)(8 * num60))
73646:		case 249:
78621:		case 249:
80806:		if (type >= 245 && type <= 249)
80810:				if (n != whoAmI && Main.npc[n].active && Main.npc[n].type >= 245 && Main.npc[n].type <= 249)
84126:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
84142:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
84166:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
84182:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
84201:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
84217:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
84236:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
84252:					Dust.NewDust(position, width, height, 249, hitDirection, -1f);
85023:					int num249 = Dust.NewDust(position, width, height, 16, 0f, 0f, 0, default(Color), 1.5f);
85024:					Dust dust = Main.dust[num249];
85026:					Main.dust[num249].noGravity = true;
85833:		if (type >= 245 && type <= 249)
85846:					NewNPC(GetSpawnSource_NPCHurt(), (int)base.Center.X, (int)position.Y + height, 249, whoAmI);
85871:				else if (type == 249)
87373:					Gore.NewGore(position, velocity, 249, scale);
95586:					result = Lang.dialog(249);

```


---

## 🤖 Assistant · 2026-08-10T06:44:56.439Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case 245\\|case 246\\|case 247\\|case 248\\|case 249\\|num\\d* == 245\\|== 245\\|== 246\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -40",
 "description": "Find type 245-249 branches"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:44:56.470Z

**📎 ToolResult**

```
12095:		else if (type == 245)
12111:		else if (type == 246)
17943:		else if (type == 245)
17948:		else if (type == 246)
19497:				case 246:
19500:				case 247:
19503:				case 248:
73581:		case 245:
73614:		case 246:
73646:		case 249:
78618:		case 246:
78619:		case 247:
78620:		case 248:
78621:		case 249:
79692:			if (type == 245 && WorldGen.Skyblock.lowTiles)
79778:		else if (type == 245 || type == 262)
80146:		case 245:
81281:		case 245:
85842:			else if (type == 246)
85855:				if (type == 245)
94193:		if (type == 245 && target >= 0 && Main.player[target].position.Y > position.Y + (float)height)

```


---

## 🤖 Assistant · 2026-08-10T06:44:59.539Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key: 85833-85880 is checkDead for 245-249. Let me read that, plus SetDefaults entries at 12095-12150 (SetDefaults), 17943-17970 (?), 18340-18620 (maybe boss flags / townNPC?), 73581-73660 (aiStyle sets?), 78618-78625 (boss checks), 80146, 80806-80820 (active count / AnyNPCs), 81281.

Let me read those chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:45:00.161Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '12090,12160p;17935,17975p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SetDefaults for 245-249"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:00.184Z

**📎 ToolResult**

```
			alpha = 175;
			value = Item.buyPrice(0, 0, 20);
			knockBackResist = 0.3f;
			rarity = 1;
		}
		else if (type == 245)
		{
			width = 140;
			height = 140;
			aiStyle = 45;
			damage = 72;
			defense = 26;
			lifeMax = 15000;
			HitSound = SoundID.NPCHit4;
			DeathSound = SoundID.NPCDeath14;
			knockBackResist = 0f;
			value = Item.buyPrice(0, 15);
			alpha = 255;
			boss = true;
			npcSlots = 5f;
		}
		else if (type == 246)
		{
			noGravity = true;
			width = 70;
			height = 70;
			aiStyle = 46;
			damage = 64;
			defense = 20;
			lifeMax = 25000;
			HitSound = SoundID.NPCHit4;
			DeathSound = null;
			knockBackResist = 0f;
			alpha = 255;
		}
		else if (type == 247 || type == 248)
		{
			noGravity = true;
			width = 40;
			height = 30;
			aiStyle = 47;
			damage = 59;
			defense = 28;
			lifeMax = 10000;
			HitSound = SoundID.NPCHit4;
			DeathSound = SoundID.NPCDeath14;
			alpha = 255;
			knockBackResist = 0f;
		}
		else if (type == 249)
		{
			noGravity = true;
			width = 70;
			height = 70;
			aiStyle = 48;
			damage = 80;
			defense = 32;
			lifeMax = 16000;
			HitSound = SoundID.NPCHit4;
			DeathSound = SoundID.NPCDeath14;
			knockBackResist = 0f;
			dontTakeDamage = true;
		}
		else if (type == 250)
		{
			width = 34;
			height = 26;
			aiStyle = 49;
			damage = 50;
			defense = 24;
			lifeMax = 300;
			damage += 10;
			defense += 14;
			lifeMax *= 3;
		}
		else if (type == 222)
		{
			scale *= 1.2f;
		}
		else if (type == 245)
		{
			canDisplayBuffs = false;
			scale *= 0.5f;
		}
		else if (type == 246)
		{
			canDisplayBuffs = false;
			scale *= 0.5f;
		}
		else if (type == 247 || type == 248)
		{
			canDisplayBuffs = false;
			scale *= 0.5f;
		}
		else if (type == 249)
		{
			scale *= 0.5f;
		}
		else if (type == 262)
		{
			scale *= 1.3f;
		}
		else if (type == 266)
		{
			defense = (int)((double)defense * 1.5);
			damage = (int)((double)damage * 1.2);
			scale *= 1.1f;
		}
		else if (type == 125)
		{
			scale *= 0.8f;
		}

```


---

## 🤖 Assistant · 2026-08-10T06:45:00.685Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '85825,85890p;73575,73680p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read checkDead and aiStyle switch"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:00.715Z

**📎 ToolResult**

```
			}
			if (frame.Y >= num * Main.npcFrameCount[type])
			{
				frame.Y = 0;
			}
			break;
		case 245:
			if (ai[0] == 0f)
			{
				if (ai[1] < -16f)
				{
					frame.Y = 0;
				}
				else if (ai[1] < -12f)
				{
					frame.Y = num;
				}
				else if (ai[1] < -8f)
				{
					frame.Y = num * 2;
				}
				else if (ai[1] < -4f)
				{
					frame.Y = num * 3;
				}
				else if (ai[1] < 0f)
				{
					frame.Y = num * 4;
				}
				else
				{
					frame.Y = 0;
				}
			}
			else if (ai[0] == 1f)
			{
				frame.Y = 1;
			}
			break;
		case 246:
			if (ai[0] == 0f)
			{
				if (localAI[0] == 1f)
				{
					frame.Y = num;
				}
				else
				{
					frame.Y = 0;
				}
			}
			else if (ai[0] == 1f)
			{
				if (localAI[0] == 1f)
				{
					frame.Y = num;
				}
				else
				{
					frame.Y = 0;
				}
				if (localAI[1] == -1f)
				{
					frame.Y += num * 4;
				}
				if (localAI[1] == 1f)
				{
					frame.Y += num * 2;
				}
			}
			break;
		case 249:
			if (localAI[0] == 1f)
			{
				frame.Y = num;
			}
			else
			{
				frame.Y = 0;
			}
			if ((frameCounter += 1.0) >= 16.0)
			{
				frameCounter = 0.0;
			}
			break;
		case 141:
			spriteDirection = direction;
			if (velocity.Y != 0f)
			{
				frame.Y = num * 2;
				break;
			}
			frameCounter += 1.0;
			if (frameCounter >= 8.0)
			{
				frame.Y += num;
				frameCounter = 0.0;
			}
			if (frame.Y > num)
			{
				frame.Y = 0;
			}
			break;
		case 243:
			if (frameCounter < 0.0)
			{
			{
				for (int num356 = 0; num356 < 50; num356++)
				{
					Dust.NewDust(position, width, height, 192, 2 * hitDirection, -2f, 100, new Color(100, 100, 100, 100));
				}
				Gore.NewGore(position, velocity, 440, scale);
			}
		}
		if (type >= 245 && type <= 249)
		{
			if (life > 0)
			{
				for (int num357 = 0; (double)num357 < dmg / (double)lifeMax * 100.0; num357++)
				{
					Dust.NewDust(position, width, height, 148, hitDirection, -1f);
				}
			}
			else if (type == 246)
			{
				if (Main.netMode != 1)
				{
					NewNPC(GetSpawnSource_NPCHurt(), (int)base.Center.X, (int)position.Y + height, 249, whoAmI);
				}
			}
			else
			{
				for (int num358 = 0; num358 < 50; num358++)
				{
					Dust.NewDust(position, width, height, 148, 2 * hitDirection, -2f);
				}
				if (type == 245)
				{
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(position, velocity, 360, scale);
					Gore.NewGore(position, velocity, 361, scale);
					Gore.NewGore(position, velocity, 362, scale);
					Gore.NewGore(position, velocity, 363, scale);
					Gore.NewGore(position, velocity, 364, scale);
					Gore.NewGore(position, velocity, 367, scale);
					Gore.NewGore(position, velocity, 366, scale);
				}
				else if (type == 249)
				{
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(position, velocity, 365, scale);
					Gore.NewGore(position, velocity, 363, scale);
					Gore.NewGore(position, velocity, 362, scale);
				}
				else
				{
					Gore.NewGore(position, velocity, 369, scale);
					Gore.NewGore(position, velocity, 371, scale);
					Gore.NewGore(position, velocity, 370, scale);
				}
			}
		}
		if (type == 288 && life <= 0)
		{

```


---

## 🤖 Assistant · 2026-08-10T06:45:13.700Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So in vanilla:
- 246 (GolemHead, attached) when its life <= 0 → spawns 249 (GolemHeadFree) which has aiStyle 48. 249 is dontTakeDamage=true and its death kills the whole fight. So actually in vanilla, the head 246 IS the main HP pool (25000 life), and killing the head (which is only vulnerable when the fists are dead? no — dontTakeDamage on body is set while head 246 active: `dontTakeDamage = flag` where flag = head 246 active). So: body is invulnerable while head attached; kill fists → then you can damage the head; when head dies, it becomes GolemHeadFree (249) which fights independently with fireballs and is the real target; killing 249 ends the fight (golemBoss set to -1?).

Hmm wait, but the task description says: "本体 hp 归零→头 246 起飞进入二阶段(头脱离本体自主战斗;本体死透后头继续)". So my port's structure: the body's hp zero triggers head 246 free flight. Hmm, but vanilla is head dies → 249. In our project, the "checkDead 模式" from moon lord: handle hp<=0 at AI top. The task explicitly says:

"本体 245:跳跃追玩家;本体 hp 归零→头 246 起飞进入二阶段(头脱离本体自主战斗;本体死透后头继续);头 246:悬浮-冲撞循环+火焰弹/眼睛激光"

So they want the head to enter phase 2 when the body dies. That's a deviation but instructed. Hmm. But also vanilla semantics: dontTakeDamage of body while head attached. The task says body hp→0 triggers head free flight. OK — I'll follow the task instructions: implement the vanilla AI faithfully, but structure death handling as instructed: at the top of each AI, if hp<=0 → set state + refill HP as needed.

Let me think about how to map this cleanly:

Vanilla phase 1: body 245 walks/jumps; head 246 floats above body shooting fireballs (proj 258, eye lasers 258/259 in ai[0]==1 phase... wait proj 259 is "EyeLaser"? Let me check projectile types: 258 = Fireball? 259 = EyeLaser. num743=259 with num742=28 damage, fired from eyes. 258 with damage 18 fired from mouth (ai[0]==0) and 24 from mouth (ai[0]==1).

Vanilla phase 2: 249 (head free) — aiStyle 48. The task says "头 246:悬浮-冲撞循环+火焰弹/眼睛激光" — the free head does hover-charge cycle + fireballs/eye lasers. I should port aiStyle 48 AI too since that's what the detached head does. Let me read aiStyle 48 (right after 47 dispatch at 31500). It's probably AI_048_GolemHead2 or inline. Let me read NPC.cs:31500 onward.

Also I need golemBoss mechanics: static int golemBoss; set by body's AI (golemBoss = whoAmI). Where is it reset to -1? Probably in UpdateNPC or AI dispatch: `if (!Main.npc[golemBoss].active) golemBoss = -1`? Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:45:13.984Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"golemBoss\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Find all golemBoss references"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:14.013Z

**📎 ToolResult**

```
6052:	public static int golemBoss = -1;
19182:		if (golemBoss < 0)
19197:		NPC nPC = Main.npc[golemBoss];
19214:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
19241:				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
19310:				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
19449:		golemBoss = whoAmI;
31285:			if (golemBoss < 0)
31292:			float num722 = Main.npc[golemBoss].Center.X - vector83.X;
31293:			float num723 = Main.npc[golemBoss].Center.Y - vector83.Y;
31521:			if (golemBoss < 0)
31570:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.8)
31574:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.6)
31578:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
31582:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)
31620:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.25)
31624:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.5)
31628:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 2)
31632:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 3)
31636:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 4)
31640:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 5)
31644:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 6)
31649:			if (!Collision.CanHit(Main.npc[golemBoss].Center, 1, 1, Main.player[target].Center, 1, 1))
31675:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.5)
31680:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.4)
31685:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.3)
31690:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
31695:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)

```


---

## 🤖 Assistant · 2026-08-10T06:45:14.420Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '31500,31660p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read aiStyle 48 dispatch"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:14.449Z

**📎 ToolResult**

```
		else if (aiStyle == 48)
		{
			bool flag48 = false;
			float num755 = GetMyBalance();
			if (Main.getGoodWorld)
			{
				num755 += 3f;
			}
			if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
			{
				num755 *= 2f;
			}
			if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
			{
				noTileCollide = true;
				flag48 = true;
			}
			else if (noTileCollide && Collision.SolidTiles(position, width, height))
			{
				noTileCollide = false;
			}
			if (golemBoss < 0)
			{
				StrikeNPCNoInteraction(9999, 0f, 0);
				return;
			}
			TargetClosest();
			float num756 = 7f;
			float num757 = 0.05f;
			Vector2 vector86 = new Vector2(base.Center.X, base.Center.Y);
			float num758 = Main.player[target].Center.X - vector86.X;
			float num759 = Main.player[target].Center.Y - vector86.Y - 300f;
			float num760 = (float)Math.Sqrt(num758 * num758 + num759 * num759);
			num760 = num756 / num760;
			num758 *= num760;
			num759 *= num760;
			if (velocity.X < num758)
			{
				velocity.X += num757;
				if (velocity.X < 0f && num758 > 0f)
				{
					velocity.X += num757;
				}
			}
			else if (velocity.X > num758)
			{
				velocity.X -= num757;
				if (velocity.X > 0f && num758 < 0f)
				{
					velocity.X -= num757;
				}
			}
			if (velocity.Y < num759)
			{
				velocity.Y += num757;
				if (velocity.Y < 0f && num759 > 0f)
				{
					velocity.Y += num757;
				}
			}
			else if (velocity.Y > num759)
			{
				velocity.Y -= num757;
				if (velocity.Y > 0f && num759 < 0f)
				{
					velocity.Y -= num757;
				}
			}
			float num761 = (num755 + 4f) / 5f;
			this.ai[1] += num761;
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.8)
			{
				this.ai[1] += num761;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.6)
			{
				this.ai[1] += num761;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
			{
				this.ai[1] += num761;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)
			{
				this.ai[1] += num761;
			}
			int num762 = 300;
			if (this.ai[1] < 20f || this.ai[1] > (float)(num762 - 20))
			{
				localAI[0] = 1f;
			}
			else
			{
				localAI[0] = 0f;
			}
			if (flag48)
			{
				this.ai[1] = 20f;
			}
			if (this.ai[1] >= (float)num762)
			{
				TargetClosest();
				this.ai[1] = 0f;
				Vector2 vector87 = new Vector2(base.Center.X, base.Center.Y - 10f * scale);
				float num763 = 8f;
				int num764 = 20;
				int num765 = 258;
				float num766 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector87.X;
				float num767 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector87.Y;
				float num768 = (float)Math.Sqrt(num766 * num766 + num767 * num767);
				num768 = num763 / num768;
				num766 *= num768;
				num767 *= num768;
				if (Main.netMode != 1)
				{
					int num769 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector87.X, vector87.Y, num766, num767, num765, num764, 0f, Main.myPlayer);
				}
			}
			float num770 = num755;
			this.ai[2] += num770;
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.25)
			{
				this.ai[2] += num770;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.5)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 2)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 3)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 4)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 5)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 6)
			{
				this.ai[2] += num770;
			}
			bool flag49 = false;
			if (!Collision.CanHit(Main.npc[golemBoss].Center, 1, 1, Main.player[target].Center, 1, 1))
			{
				flag49 = true;
			}
			if (flag49)
			{
				this.ai[2] += num770 * 10f;
			}
			if (this.ai[2] > (float)(100 + Main.rand.Next(4800)))
			{
				this.ai[2] = 0f;
				for (int num771 = 0; num771 < 2; num771++)

```


---

## 🤖 Assistant · 2026-08-10T06:45:16.016Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continue reading aiStyle 48 to the end (up to aiStyle 49 dispatch).
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:45:16.032Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '31660,31790p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read rest of aiStyle 48"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:16.070Z

**📎 ToolResult**

```
				for (int num771 = 0; num771 < 2; num771++)
				{
					Vector2 vector88 = new Vector2(base.Center.X, base.Center.Y - 50f * scale);
					switch (num771)
					{
					case 0:
						vector88.X -= 14f * scale;
						break;
					case 1:
						vector88.X += 14f * scale;
						break;
					}
					float num772 = 11f;
					int num773 = 24;
					int num774 = 259;
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.5)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.4)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.3)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)
					{
						num773++;
						num772 += 0.25f;
					}
					float num775 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f;
					float num776 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f;
					if (flag49)
					{
						num773 = (int)((double)num773 * 1.5);
						num772 *= 2.5f;
						num775 += Main.player[target].velocity.X * Main.rand.NextFloat() * 50f;
						num776 += Main.player[target].velocity.Y * Main.rand.NextFloat() * 50f;
					}
					num775 -= vector88.X;
					num776 -= vector88.Y;
					float num777 = (float)Math.Sqrt(num775 * num775 + num776 * num776);
					num777 = num772 / num777;
					num775 *= num777;
					num776 *= num777;
					vector88.X += num775 * 3f;
					vector88.Y += num776 * 3f;
					if (Main.netMode != 1)
					{
						int num778 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector88.X, vector88.Y, num775, num776, num774, num773, 0f, Main.myPlayer);
						Main.projectile[num778].timeLeft = 300;
					}
				}
			}
			if (!Main.getGoodWorld)
			{
				position += netOffset;
				int num779 = Main.rand.Next(2) * 2 - 1;
				Vector2 vector89 = base.Bottom + new Vector2((float)(num779 * 22) * scale, -22f * scale);
				Dust dust7 = Dust.NewDustPerfect(vector89, 228, (MathF.PI / 2f + -MathF.PI / 2f * (float)num779 + Main.rand.NextFloatDirection() * (MathF.PI / 4f)).ToRotationVector2() * (2f + Main.rand.NextFloat()));
				Dust dust = dust7;
				dust.velocity += velocity;
				dust7.noGravity = true;
				dust7 = Dust.NewDustPerfect(base.Bottom + new Vector2(Main.rand.NextFloatDirection() * 6f * scale, (Main.rand.NextFloat() * -4f - 8f) * scale), 228, Vector2.UnitY * (2f + Main.rand.NextFloat()));
				dust7.fadeIn = 0f;
				dust7.scale = 0.7f + Main.rand.NextFloat() * 0.5f;
				dust7.noGravity = true;
				dust = dust7;
				dust.velocity += velocity;
				position -= netOffset;
			}
		}
		else if (aiStyle == 49)
		{
			noGravity = true;
			TargetClosest();
			float num780 = 4f;
			float num781 = 0.25f;
			Vector2 vector90 = new Vector2(base.Center.X, base.Center.Y);
			float num782 = Main.player[target].Center.X - vector90.X;
			float num783 = Main.player[target].Center.Y - vector90.Y - 200f;
			float num784 = (float)Math.Sqrt(num782 * num782 + num783 * num783);
			if (num784 < 20f)
			{
				num782 = velocity.X;
				num783 = velocity.Y;
			}
			else
			{
				num784 = num780 / num784;
				num782 *= num784;
				num783 *= num784;
			}
			if (velocity.X < num782)
			{
				velocity.X += num781;
				if (velocity.X < 0f && num782 > 0f)
				{
					velocity.X += num781 * 2f;
				}
			}
			else if (velocity.X > num782)
			{
				velocity.X -= num781;
				if (velocity.X > 0f && num782 < 0f)
				{
					velocity.X -= num781 * 2f;
				}
			}
			if (velocity.Y < num783)
			{
				velocity.Y += num781;
				if (velocity.Y < 0f && num783 > 0f)
				{
					velocity.Y += num781 * 2f;
				}
			}
			else if (velocity.Y > num783)
			{
				velocity.Y -= num781;
				if (velocity.Y > 0f && num783 < 0f)

```


---

## 🤖 Assistant · 2026-08-10T06:45:20.737Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have full source. Note aiStyle 48 (head free) doesn't "冲撞" (charge) — it hovers above player and shoots fireballs + eye lasers. The "悬浮-冲撞循环" in the task description is a loose description; I'll port what vanilla does.

Now the project structure. Let me look at bossAI.ts, bossAI_duke_moonlord.ts, an existing bossAI file (maybe bossAI_prime?), Enemy.ts, vanilla-npcs.json entries for 245/246/247, and _mechprobe.mts.

Let me explore the game/src/entities directory.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:45:21.347Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/entities/ ~/Project/GLM/SandboxWorld/game/scripts/ && wc -l ~/Project/GLM/SandboxWorld/game/src/entities/bossAI*.ts ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "List entities and scripts dirs"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:21.375Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/scripts/:
_alphaprobe.mjs
_audit7.mjs
_batprobe.mjs
_biomeaudio.mjs
_biomeprobe.mjs
_bossprobe.mts
_bowprobe.mjs
_buffprobe.mjs
_cactus3.mjs
_casterprobe.mjs
_chan.mjs
_chargerprobe.mjs
_cursor-probe.mjs
_dbgalpha.mjs
_death-probe.mjs
_dgndbg.mjs
_dukemlprobe.mts
_dungeondtrap.mjs
_dungeonprobe.mjs
_eaterai.mjs
_eaterdbg.mjs
_eaterdbg2.mjs
_eaterpix.mjs
_eyeprobe.mjs
_fighterprobe.mjs
_genwatch.mjs
_globaldg.mjs
_greenbrickprobe.mjs
_halfbrickprobe.mjs
_hud-probe.mjs
_lategameprobe.mts
_lavabottom.mjs
_liquidprobe.mjs
_lootprobe.mjs
_mapprobe.mjs
_mechprobe.mts
_minimap-btn-probe.mjs
_musicprobe.mjs
_npcprobe.mjs
_pixanal.mjs
_potprobe.mjs
_qbprobe.mts
_refdg.mjs
_seamdiag.mjs
_settleprobe.mjs
_sfx-lazy-probe.mts
_sign-verify.mjs
_slimetintprobe.mjs
_soakprobe.mjs
_spawndbg.mjs
_spawnmoveprobe.mjs
_spawnposprobe.mjs
_spawnrateprobe.mjs
_spotdbg.mjs
_spritedbg.mjs
_swarmprobe.mjs
_tex-broken.mjs
_townnpc-pix.mjs
_townnpc.mjs
_trapdmg.mjs
_trapfire.mjs
_trapshot-tex.mjs
_waterfallprobe.mjs
_weap-probe.mts
_wofprobe.mts
_wormprobe.mjs
ascii-map.mjs
asset-audit.mjs
boss.mjs
buffs.mjs
build-atlas.mjs
build-l10n.mjs
carve-shape.mjs
char-smoke.mjs
combat.mjs
copy-sfx.mjs
door-test.mjs
e2e-mechboss.mjs
feat-test.mjs
feat-test2.mjs
feat-test3.mjs
feat-test4.mjs
feat-test5.mjs
feat-test6.mjs
feat-test6b.mjs
feat-test7.mjs
feat-test8.mjs
feat-test8b.mjs
feat-test9.mjs
feat-test9b.mjs
feat-test9c.mjs
gen-audit.mjs
gen-determinism.mjs
gen-preview-smoke.mjs
gen-vanilla-test.mjs
import.mjs
interact.mjs
inv-smoke.mjs
jungle-probe.mjs
l10n-merge.d.mts
l10n-merge.mjs
l10n-smoke.mjs
lighting-test.mts
m4.mjs
probe.mjs
region-compare.mjs
roundtrip-test.mjs
runner-test.mjs
save-ascii.mjs
settings-smoke.mjs
smallholes-test.mjs
smoke.mjs
straight-test.mjs
title-smoke.mjs
vanilla-atlas.mjs
vanilla-smoke.mjs
vanilla-ui-whitelist.json
vanilla-whitelist.json
visual-check.mjs
vui-smoke.mjs
wiring-test.mts

~/Project/GLM/SandboxWorld/game/src/entities/:
Arrow.ts
bossAI_duke_moonlord.ts
bossAI_lategame.ts
bossAI_queenbee_plantera.ts
bossAI_wof.ts
bossAI.ts
Critter.ts
Dart.ts
Enemy.ts
Entity.ts
ItemDrop.ts
MagicProj.ts
Minecart.ts
Player.ts
projTargets.ts
Tombstone.ts
TownNPC.ts
types.ts
waterAvoid.ts
WeaponProj.ts
     997 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts
     922 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts
     604 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts
     413 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_wof.ts
     940 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts
    1466 ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
    5342 total

```


---

## 🤖 Assistant · 2026-08-10T06:45:22.464Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('public/sprites/vanilla-npcs.json'))\nprint(type(d))\nitems = d if isinstance(d,list) else d.get('npcs',d)\nprint(len(items))\nfor it in items:\n    if str(it.get('id')) in ('245','246','247','248','127','134'):\n        print(json.dumps(it,ensure_ascii=False,indent=1))\n\"",
 "description": "Inspect vanilla-npcs.json entries 245-248"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:29.963Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 8, in <module>
AttributeError: 'str' object has no attribute 'get'
<class 'dict'>
628

```


---

## 🤖 Assistant · 2026-08-10T06:45:31.396Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The JSON is a dict. Let me look at its structure.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:45:31.405Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'))\nprint(list(d.keys())[:10])\n\" ",
 "description": "Show top-level JSON keys"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:43.092Z

**📎 ToolResult**

```
['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

```


---

## 🤖 Assistant · 2026-08-10T06:45:44.822Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'))\nfor k in ('245','246','247','248','249'):\n    print(k, json.dumps(d.get(k),ensure_ascii=False))\n\"",
 "description": "Print 245-249 entries"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:45:57.244Z

**📎 ToolResult**

```
245 {"id": 245, "name": "Golem", "frames": 7, "lifeMax": 9000, "damage": 72, "defense": 26, "knockBackResist": 0, "aiStyle": 45, "width": 140, "height": 140, "HitSound": "NPCHit4", "DeathSound": "NPCDeath14", "alpha": 255, "npcSlots": 5}
246 {"id": 246, "name": "NPC_246", "frames": 6, "lifeMax": 16000, "damage": 64, "defense": 20, "knockBackResist": 0, "aiStyle": 46, "width": 70, "height": 70, "noGravity": true, "HitSound": "NPCHit4", "alpha": 255}
247 {"id": 247, "name": "NPC_247", "frames": 1, "lifeMax": 7000, "damage": 59, "defense": 28, "aiStyle": 47, "width": 40, "height": 30, "noGravity": true, "HitSound": "NPCHit4", "DeathSound": "NPCDeath14", "alpha": 255}
248 null
249 {"id": 249, "name": "NPC_249", "frames": 2, "lifeMax": 11000, "damage": 80, "defense": 32, "knockBackResist": 0, "aiStyle": 48, "width": 70, "height": 70, "noGravity": true, "HitSound": "NPCHit4", "DeathSound": "NPCDeath14"}

```


---

## 🤖 Assistant · 2026-08-10T06:46:02.935Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The 247 entry lacks knockBackResist — but the SetDefaults has knockBackResist = 0f for 247/248. For 248 I should mirror 247's field structure exactly (the task says "字段完全参照现有 247 条目的字段结构"). But should I add knockBackResist? The task says "只允许改这一个文件;字段完全参照现有 247 条目的字段结构:name/aiStyle=47/lifeMax/damage/defense/width/height/frames/Hitsound 等". I'll mirror 247 exactly but change id to 248. That's safest. Maybe also add "knockBackResist": 0 to both? No — "只允许改这一个文件" means I can only modify vanilla-npcs.json among existing files. I could add knockBackResist:0 to 248 since vanilla has it, but to stay symmetric with 247 I'll mirror exactly (247 has no knockBackResist; presumably the data loader defaults). Actually adding knockBackResist: 0 to 248 makes it more vanilla-accurate and it's the same file. Hmm, but symmetry in field structure matters for the main session wiring. I'll mirror 247 exactly with id=248, and name "NPC_248". Good.

Note vanilla 1.4.5.6 lifeMax for 245 = 15000 but JSON says 9000. JSON data is extracted with expert scaling maybe. Not my concern; mirror.

Now read bossAI.ts to see the helper exports and the Prime pattern.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:46:03.076Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:03.232Z

**📎 ToolResult**

```
1	// Boss AI 1:1 移植(Terarria1456 NPC.cs SetDefaults 指定 aiStyle 的专用核)。
2	// 由 Enemy.fixedUpdate 的 aiStyle 分发调用;弹幕用 MagicProj/投射桶,部件用 fromVanilla。
3	// 各核保留原版状态机主链与特征机制(移速/计时/阶段),专家专属分支注释标明。
4	import type { Enemy } from './Enemy';
5	import type { GameHooks } from './types';
6	import type { Player } from './Player';
7	import { TILE } from '../core/constants';
8	import { MagicProj } from './MagicProj';
9	import { Arrow } from './Arrow';
10	
11	const addProj = (game: GameHooks, p: MagicProj) => {
12	  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(p, 'projectiles');
13	};
14	export const addEnemy = (game: GameHooks, e: Enemy) => {
15	  const em = (game as unknown as { entities?: { nextId?: number; add?: (en: unknown, b: string) => void } }).entities;
16	  if (em?.nextId !== undefined) e.id = em.nextId++;
17	  em?.add?.(e, 'enemies');
18	  return e;
19	};
20	
21	/** AI_011 骷髅王战斗状态机(NPC.cs:21904-22288 完整核;守卫分支已在 skeletronHeadAI)。
22	 *  ai0=初始化(双手 36 生成);ai1: 0=悬浮(800t)→1=旋冲(400t)循环;2=守卫/白天;3=离场。
23	 *  悬浮: Y 拉向玩家上方 250(0.02/±2),X 朝玩家 0.05/±8;旋冲: rotation+=0.3*dir、
24	 *  朝玩家 1.5 倍速、伤害 ×1.3、防御 -10(:22026-22179)。 */
25	export function skeletronBossAI(e: Enemy, game: GameHooks, player: Player | null) {
26	  const isGuardian = e.vanillaId === 68;
27	  // 初始化:生成双手 36(:21914-21931)
28	  if (!e.bInit) {
29	    e.bInit = true;
30	    if (!isGuardian) {
31	      for (const side of [-1, 1]) {
32	        const h = spawnPart(game, e, 36);
33	        if (h) { h.ai0 = side; h.ai1 = e.id; h.ai3 = 150; h.bInit = true; }
34	      }
35	    }
36	  }
37	  // 白天 → ai1=2(守卫/离场语义);玩家死/超 2000px → 3
38	  if (game.world.clock.isDay && !isGuardian && e.ai1 !== 3) e.ai1 = 2;
39	  if (!player || Math.abs(e.cx - player.cx) > 2000 || Math.abs(e.cy - player.cy) > 2000) {
40	    if (!player || Math.abs(e.cx - player.cx) > 2000 || Math.abs(e.cy - player.cy) > 2000) e.ai1 = 3;
41	  }
42	  if (e.ai1 === 2) {
43	    // 守卫恒速直追(伤害 9999 语义)
44	    e.def.damage = isGuardian ? 9999 : e.def.damage;
45	    const dx = player!.cx - e.cx, dy = player!.cy - e.cy;
46	    const d = Math.hypot(dx, dy) || 1;
47	    e.vx = (dx / d) * 8; e.vy = (dy / d) * 8;
48	    e.x += e.vx; e.y += e.vy;
49	    return;
50	  }
51	  if (e.ai1 === 3) { e.y += 4; return; }
52	  if (!player) return;
53	
54	  e.ai2 += 1;
55	  if (e.ai1 === 0) {
56	    // 悬浮段(:22046-22091)
57	    if (e.ai2 >= 800) { e.ai2 = 0; e.ai1 = 1; }
58	    // 回悬浮:恢复冲撞前的伤害/防御基值
59	    const base = baseStats.get(e);
60	    if (base) { e.def.damage = base.dmg; e.def.defense = base.def; }
61	    if (e.y > player.y - 250) {
62	      if (e.vy > 0) e.vy *= 0.98;
63	      e.vy -= 0.02;
64	      if (e.vy > 2) e.vy = 2;
65	    } else {
66	      if (e.vy < 0) e.vy *= 0.98;
67	      e.vy += 0.02;
68	      if (e.vy < -2) e.vy = -2;
69	    }
70	    if (e.cx > player.cx) {
71	      if (e.vx > 0) e.vx *= 0.98;
72	      e.vx -= 0.05;
73	      if (e.vx > 8) e.vx = 8;
74	    } else {
75	      if (e.vx < 0) e.vx *= 0.98;
76	      e.vx += 0.05;
77	      if (e.vx < -8) e.vx = -8;
78	    }
79	  } else if (e.ai1 === 1) {
80	    // 旋冲段(:22115-22179):rot+=0.3*dir,1.5 倍速直冲,伤害 ×1.3,防御 -10。
81	    // 原版在进入冲撞时一次性应用——每 tick 重乘会把伤害放大 1.3^400,故缓存基值按基值设置
82	    if (e.ai2 >= 400) { e.ai2 = 0; e.ai1 = 0; }
83	    let base = baseStats.get(e);
84	    if (!base) { base = baseOf(e); }
85	    e.def.defense = Math.max(0, base.def - 10);
86	    e.def.damage = Math.round(base.dmg * 1.3);
87	    e.spin += (e.facing || 1) * 0.3;
88	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
89	    const d = Math.hypot(dx, dy) || 1;
90	    const spd = 12; // (1.5x 追击速)
91	    e.vx += ((dx / d) * spd - e.vx) * 0.1;
92	    e.vy += ((dy / d) * spd - e.vy) * 0.1;
93	  }
94	  e.facing = e.vx > 0 ? 1 : -1;
95	  e.x += e.vx; e.y += e.vy;
96	}
97	
98	/** Boss 伤害/防御基值缓存(状态机每 tick 从基值派生临时修正,防重复乘膨胀) */
99	const baseStats = new WeakMap<Enemy, { dmg: number; def: number }>();
100	const baseOf = (e: Enemy) => {
101	  let b = baseStats.get(e);
102	  if (!b) { b = { dmg: e.def.damage, def: e.def.defense ?? 0 }; baseStats.set(e, b); }
103	  return b;
104	};
105	
106	let enemyCtor: (typeof import('./Enemy'))['Enemy'] | null = null;
107	/** Enemy 构造注入(Enemy.ts import 时回填,避免循环依赖) */
108	export function bindEnemyCtor(c: (typeof import('./Enemy'))['Enemy']) { enemyCtor = c; }
109	
110	export function spawnPart(game: GameHooks, src: Enemy, id: number): Enemy | null {
111	  if (!enemyCtor) return null;
112	  const p = enemyCtor.fromVanilla(id, src.cx, src.cy);
113	  if (!p) return null;
114	  return addEnemy(game, p);
115	}
116	
117	/** AI_012 骷髅王手(NPC.cs:22289-22400):锚定头(ai1=头 id),头离场 → 自毁;
118	 *  头非悬浮态 → 漂在头两侧(±120×ai0, 头上方 100);悬浮态 → 缓慢环绕(±200, +230)。
119	 *  每 300t(ai3 计)朝玩家挥击冲刺。 */
120	export function skeletronHandAI(e: Enemy, game: GameHooks, player: Player | null) {
121	  const headId = e.ai1;
122	  const enemies = game.enemies() as unknown[];
123	  const head = enemies.find((n) => (n as Enemy).id === headId) as Enemy | undefined;
124	  if (!head || head.vanilla?.aiStyle !== 11 || head.dead) { e.dead = true; return; }
125	  if (head.ai1 === 3) { e.dead = true; return; }
126	  e.facing = -(e.ai0 || 1);
127	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
128	  // 缓慢环绕(头悬浮态);头冲撞态则回到侧位
129	  const ty = head.y - 100;
130	  const tx = head.x + head.w / 2 - e.w / 2 - 120 * (e.ai0 || 1);
131	  if (head.ai1 === 0) {
132	    e.ai3 += 1;
133	    if (e.ai3 >= 300) { e.ai3 = -120; } // 负值=挥击中
134	    if (e.ai3 < 0) {
135	      // 挥击:朝玩家冲刺 8 速
136	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
137	      const d = Math.hypot(dx, dy) || 1;
138	      e.vx += ((dx / d) * 8 - e.vx) * 0.15;
139	      e.vy += ((dy / d) * 8 - e.vy) * 0.15;
140	    } else {
141	      // 环绕位:头右/左 200px、下方 230(原版 num200 系)
142	      const ox = head.x + head.w / 2 - e.w / 2 - 200 * (e.ai0 || 1);
143	      const oy = head.y + 230;
144	      e.vx += ((ox - e.x) * 0.02 - e.vx) * 0.1;
145	      e.vy += ((oy - e.y) * 0.02 - e.vy) * 0.1;
146	    }
147	  } else {
148	    // 头冲撞中:快速回侧位
149	    e.vx += ((tx - e.x) * 0.05 - e.vx) * 0.2;
150	    e.vy += ((ty - e.y) * 0.05 - e.vy) * 0.2;
151	  }
152	  e.x += e.vx; e.y += e.vy;
153	}
154	
155	/** AI_015 史莱姆王(NPC.cs SetDefaults case 50 / AI_015):大跳朝玩家 + 受击攒怒 +
156	 *  落地砸出小史莱姆(30% 概率)。经典模式无传送(专家专属),暂不移植传送。 */
157	export function kingSlimeAI(e: Enemy, game: GameHooks, player: Player | null) {
158	  if (!player) return;
159	  // Enemy.ai0 默认 -1120(史莱姆族约定);原版 AI_015 的 ai[0] 从 0 起步 → 首帧复位
160	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; }
161	  e.ai0 += 1;
162	  if (!e.onGround) {
163	    e.vy += 0.35; // 重力(原版大跳重力)
164	    // 空中水平减速朝玩家
165	    if (e.vx > 0) e.vx -= 0.02; else if (e.vx < 0) e.vx += 0.02;
166	  } else {
167	    // 落地:砸压判定 + 30% 出小史莱姆(原版 SpawnNPC(16) 语义)
168	    if (e.ai0 > 10) {
169	      const dx = player.cx - e.cx;
170	      e.vy = -8 - Math.random() * 3; // 大跳(原版 -8~-11)
171	      e.vx = Math.max(-7, Math.min(7, dx * 0.06));
172	      if (Math.random() < 0.3) {
173	        for (let k = 0; k < 2; k++) {
174	          const s = spawnPart(game, e, 16);
175	          if (s) { s.x += (Math.random() - 0.5) * 60; s.vy = -4; }
176	        }
177	      }
178	      game.spawnParticles(e.cx, e.y + e.h, '#3080FF', 8, 2.2);
179	    }
180	  }
181	  e.x += e.vx;
182	  e.y += e.vy;
183	  // 地形碰撞(实心块)
184	  collideGround(e, game);
185	}
186	
187	/** AI_054 克苏鲁之脑(NPC.cs AI_054 + 267 爬行者环):
188	 *  一阶段(爬行者存活时无敌:dontTakeDamage)脑体悬空不动,爬行者环绕玩家;
189	 *  爬行者全灭 → 二阶段:瞬移冲刺(3 点环绕) + 幻影(简化:冲刺时半透明)。 */
190	export function brainOfCthulhuAI(e: Enemy, game: GameHooks, player: Player | null) {
191	  if (!player) return;
192	  const enemies = game.enemies() as unknown[];
193	  // 初次:补生成爬行者(原版 371-393 只)——必须先于爬行者计数,
194	  // 否则首 tick 爬行者为 0 直接落二阶段,永远不生成
195	  if (!e.bInit) {
196	    e.bInit = true;
197	    for (let k = 0; k < 8; k++) {
198	      const c = spawnPart(game, e, 267);
199	      if (c) {
200	        const ang = (k / 8) * Math.PI * 2;
201	        c.x = player.cx + Math.cos(ang) * 150;
202	        c.y = player.cy + Math.sin(ang) * 150;
203	      }
204	    }
205	  }
206	  const creepers = enemies.filter((n) => (n as Enemy).vanillaId === 267 && !(n as Enemy).dead);
207	  if (creepers.length > 0) {
208	    // 一阶段:无敌 + 悬浮微移(原版 ai[0]=0 悬空不动;爬行者环攻击)
209	    e.iframes = 2;
210	    e.vx *= 0.9; e.vy *= 0.9;
211	    e.x += e.vx; e.y += e.vy;
212	    return;
213	  }
214	  // 二阶段:瞬移冲刺循环(ai0 计 60t 一冲)
215	  e.ai0 += 1;
216	  e.spawnAlpha = 0;
217	  if (e.ai0 % 60 === 0) {
218	    // 瞬移到玩家周围随机点,朝玩家冲刺
219	    const ang = Math.random() * Math.PI * 2;
220	    e.x = player.cx + Math.cos(ang) * 200 - e.w / 2;
221	    e.y = player.cy + Math.sin(ang) * 200 - e.h / 2;
222	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
223	    const d = Math.hypot(dx, dy) || 1;
224	    e.vx = (dx / d) * 9; e.vy = (dy / d) * 9;
225	    game.spawnParticles(e.cx, e.cy, '#A03050', 10, 2);
226	  }
227	  e.x += e.vx; e.y += e.vy;
228	}
229	
230	/** 267 爬行者(NPC.cs AI_055 简化):环绕主人/玩家漂移 + 接触伤害 */
231	export function creeperAI(e: Enemy, game: GameHooks, player: Player | null) {
232	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
233	  e.ai0 += 0.02;
234	  // 环绕玩家(半径 100-160 摆动)
235	  const r = 130 + Math.sin(e.aiT * 0.03) * 30;
236	  const tx = player.cx - e.w / 2 + Math.cos(e.ai0) * r;
237	  const ty = player.cy - e.h / 2 + Math.sin(e.ai0) * r;
238	  e.vx += (tx - e.x) * 0.01;
239	  e.vy += (ty - e.y) * 0.01;
240	  e.vx *= 0.92; e.vy *= 0.92;
241	  e.x += e.vx; e.y += e.vy;
242	  void game;
243	}
244	
245	// ================= 机械三王(NPC.cs AI_030-037,1.4.5.6 行号见各核注释) =================
246	// 经典模式参数 1:1;专家/大师/FTW 分支仅注释保留。
247	
248	/** 原版速度逼近(L26539-26670 雏形):朝目标速度单轴步进,符号翻转时双倍步进 */
249	export function accelTo(v: number, target: number, a: number): number {
250	  if (v < target) { v += a; if (v < 0 && target > 0) v += a; }
251	  else if (v > target) { v -= a; if (v > 0 && target < 0) v -= a; }
252	  return v;
253	}
254	/** 朝 (tx,ty) 以速度 spd/加速度 acc 追赶(vanilla numXXX = spd/dist 归一后 accelTo) */
255	export function seek(e: Enemy, tx: number, ty: number, spd: number, acc: number): void {
256	  const dx = tx - e.cx, dy = ty - e.cy;
257	  const d = Math.hypot(dx, dy) || 1;
258	  e.vx = accelTo(e.vx, (dx / d) * spd, acc);
259	  e.vy = accelTo(e.vy, (dy / d) * spd, acc);
260	}
261	/** 直线视线(原版 Collision.CanHit 近似:8px 采样无实心块) */
262	export function losClear(game: GameHooks, x0: number, y0: number, x1: number, y1: number): boolean {
263	  const st = game.world.store;
264	  const steps = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / 8));
265	  for (let i = 1; i < steps; i++) {
266	    const t = i / steps;
267	    const tx = Math.floor((x0 + (x1 - x0) * t) / TILE), ty = Math.floor((y0 + (y1 - y0) * t) / TILE);
268	    if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) return false;
269	  }
270	  return true;
271	}
272	/** Boss 弹幕:直飞(grav 0)+ 原版 Projectile_N 贴图 */
273	export function shoot(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId: number, life = 300): void {
274	  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
275	    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav: 0, life, pierce: 1 }), 'projectiles');
276	}
277	
278	/** AI_030/031 双子(NPC.cs:26497-27735):雷神之眼 125 / 魔神之眼 126。
279	 *  旋转持续瞄准玩家(0.1/0.15 步进+绕圈处理);白天/玩家死 → 上飞离场;
280	 *  一阶段(血>40%):侧向悬浮(300/400)→4-10 连冲(12/13 速);二阶段变身自旋;
281	 *  三阶段:雷眼 激光 83→100(伤害×1.5 防+10),魔眼 火焰喷射 101(伤害×1.5 防+18)。 */
282	export function twinsAI(e: Enemy, game: GameHooks, player: Player | null, spaz: boolean) {
283	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
284	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
285	  // ---- 旋转瞄准(num427/num471:atan2(dy-59, 自-玩)+π/2,步进 0.1/0.15) ----
286	  let target = Math.atan2(e.y + e.h - 59 - (player.y + player.h / 2), e.cx - player.cx) + Math.PI / 2;
287	  if (target < 0) target += 6.283; else if (target > 6.283) target -= 6.283;
288	  const step = spaz ? 0.15 : 0.1;
289	  let rot = e.spin;
290	  if (rot < target) { rot += (target - rot > Math.PI ? -step : step); }
291	  else if (rot > target) { rot += (rot - target > Math.PI ? step : -step); }
292	  if (Math.abs(rot - target) < step) rot = target;
293	  if (rot < 0) rot += 6.283; else if (rot > 6.283) rot -= 6.283;
294	  e.spin = rot;
295	
296	  // 白天/玩家死:上飞离场(Game.ts 日出剔除发"逃走"提示)
297	  if (game.world.clock.isDay || player.dead) {
298	    e.vy -= 0.04;
299	    e.x += e.vx; e.y += e.vy;
300	    return;
301	  }
302	
303	  // ---- 一阶段(ai0=0) ----
304	  if (e.ai0 === 0) {
305	    if (e.ai1 === 0) {
306	      // 侧向悬浮:雷眼 玩家侧 300/上方 300 速 7/0.1;魔眼 侧 400 速 12/0.4
307	      const spd = spaz ? 12 : 7, acc = spaz ? 0.4 : 0.1;
308	      const side = e.cx < player.x + player.w ? -1 : 1;
309	      const offX = spaz ? 400 : 300, offY = spaz ? 0 : 300;
310	      const tx = player.cx + side * offX, ty = player.cy - offY;
311	      const hoverDist = Math.hypot(tx - e.cx, ty - e.cy);
312	      seek(e, tx, ty, spd, acc);
313	      e.ai2 += 1;
314	      if (e.ai2 >= 600) { e.ai1 = 1; e.ai2 = 0; e.ai3 = 0; }
315	      // 悬浮期弹幕:魔眼 每 60t 诅咒焰 96(25 伤 12 速);雷眼 位于玩家上方且距悬浮点<400 时绿激光 83(20 伤 9 速)
316	      if (spaz) {
317	        e.ai3 += 1;
318	        if (e.ai3 >= 60) {
319	          e.ai3 = 0;
320	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
321	          const d = Math.hypot(dx, dy) || 1;
322	          shoot(game, e.cx + dx / d * 4, e.cy + dy / d * 4,
323	            dx / d * 12 + (Math.random() - 0.5) * 4, dy / d * 12 + (Math.random() - 0.5) * 4, 25, 96);
324	        }
325	      } else if (e.y + e.h < player.y && hoverDist < 400) {
326	        e.ai3 += 1;
327	        if (e.ai3 >= 60) {
328	          e.ai3 = 0;
329	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
330	          const d = Math.hypot(dx, dy) || 1;
331	          shoot(game, e.cx + dx / d * 15, e.cy + dy / d * 15,
332	            dx / d * 9 + (Math.random() - 0.5) * 6.4, dy / d * 9 + (Math.random() - 0.5) * 6.4, 20, 83);
333	        }
334	      }
335	    } else if (e.ai1 === 1) {
336	      // 冲撞:一次性朝玩家定速(雷眼 12/魔眼 13)
337	      e.spin = target;
338	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
339	      const d = Math.hypot(dx, dy) || 1;
340	      const spd = spaz ? 13 : 12;
341	      e.vx = dx / d * spd; e.vy = dy / d * spd;
342	      e.ai1 = 2;
343	    } else if (e.ai1 === 2) {
344	      e.ai2 += 1;
345	      if (e.ai2 >= (spaz ? 8 : 25)) {
346	        e.vx *= 0.96; e.vy *= 0.96;
347	        if (Math.abs(e.vx) < 0.1) e.vx = 0;
348	        if (Math.abs(e.vy) < 0.1) e.vy = 0;
349	      } else {
350	        e.spin = Math.atan2(e.vy, e.vx) - Math.PI / 2;
351	      }
352	      if (e.ai2 >= (spaz ? 42 : 70)) {
353	        e.ai3 += 1; e.ai2 = 0;
354	        e.spin = target;
355	        if (e.ai3 >= (spaz ? 10 : 4)) { e.ai1 = 0; e.ai3 = 0; }
356	        else e.ai1 = 1;
357	      }
358	    }
359	    if (e.hp < e.maxHp * 0.4) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
360	    e.x += e.vx; e.y += e.vy;
361	    return;
362	  }
363	
364	  // ---- 变身(ai0=1 自旋加速 / ai0=2 减速,各 100t;ai2=角速度 0↔0.5) ----
365	  if (e.ai0 === 1 || e.ai0 === 2) {
366	    if (e.ai0 === 1) { e.ai2 += 0.005; if (e.ai2 > 0.5) e.ai2 = 0.5; }
367	    else { e.ai2 -= 0.005; if (e.ai2 < 0) e.ai2 = 0; }
368	    e.spin += e.ai2;
369	    e.ai1 += 1;
370	    if (e.ai1 >= 100) {
371	      e.ai0 += 1; e.ai1 = 0;
372	      if (e.ai0 === 3) e.ai2 = 0;
373	      else {
374	        game.playSfx('roar', 0.7);
375	        game.spawnParticles(e.cx, e.cy, '#FF6040', 20, 2);
376	      }
377	    }
378	    e.vx *= 0.98; e.vy *= 0.98;
379	    if (Math.abs(e.vx) < 0.1) e.vx = 0;
380	    if (Math.abs(e.vy) < 0.1) e.vy = 0;
381	    e.x += e.vx; e.y += e.vy;
382	    return;
383	  }
384	
385	  // ---- 三阶段(ai0=3):伤害×1.5,防御 +(雷眼10/魔眼18) ----
386	  const b = baseOf(e);
387	  e.def.damage = Math.round(b.dmg * 1.5);
388	  e.def.defense = b.def + (spaz ? 18 : 10);
389	  if (e.ai1 === 0) {
390	    // 上方悬浮:雷眼 玩家正上 300(8/0.15,300t→冲);魔眼 侧 180 同高(4/0.1,400t→冲)+ 火焰喷射 101
391	    const spd = spaz ? 4 : 8, acc = spaz ? 0.1 : 0.15;
392	    const offX = spaz ? 180 : 0, offY = spaz ? 0 : 300;
393	    const side = e.cx < player.x + player.w ? -1 : 1;
394	    seek(e, player.cx + side * offX, player.cy - offY, spd, acc);
395	    e.ai2 += 1;
396	    if (e.ai2 >= (spaz ? 400 : 300)) { e.ai1 = 1; e.ai2 = 0; e.ai3 = 0; }
397	    e.spin = Math.atan2(player.cy - e.cy, player.cx - e.cx) - Math.PI / 2;
398	    if (e.aiT % (spaz ? 8 : 180) === 0 && losClear(game, e.cx, e.cy, player.cx, player.cy)) {
399	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
400	      const d = Math.hypot(dx, dy) || 1;
401	      const spdP = spaz ? 6 : 8.5;
402	      const dmgP = spaz ? 30 : 25;
403	      const pid = spaz ? 101 : 100;
404	      const lead = spaz ? 4 : 15;
405	      shoot(game, e.cx + dx / d * lead, e.cy + dy / d * lead,
406	        dx / d * spdP + (Math.random() - 0.5) * 0.8, dy / d * spdP + (Math.random() - 0.5) * 0.8, dmgP, pid);
407	    }
408	  } else if (e.ai1 === 1) {
409	    // 冲撞:雷眼 侧 340 8/0.2 / 180t 循环;魔眼 直冲 14 速(50/80t 减速,连 6)
410	    if (spaz) {
411	      e.spin = target;
412	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
413	      const d = Math.hypot(dx, dy) || 1;
414	      e.vx = dx / d * 14; e.vy = dy / d * 14;
415	      e.ai1 = 2;
416	    } else {
417	      const side = e.cx < player.x + player.w ? -1 : 1;
418	      seek(e, player.cx + side * 340, player.cy, 8, 0.2);
419	      e.spin = Math.atan2(player.cy - e.cy, player.cx - e.cx) - Math.PI / 2;
420	      if (e.aiT % 60 === 0 && losClear(game, e.cx, e.cy, player.cx, player.cy)) {
421	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
422	        const d = Math.hypot(dx, dy) || 1;
423	        shoot(game, e.cx + dx / d * 15, e.cy + dy / d * 15, dx / d * 9, dy / d * 9, 18, 100);
424	      }
425	      e.ai2 += 1;
426	      if (e.ai2 >= 180) { e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
427	    }
428	  } else if (e.ai1 === 2 && spaz) {
429	    // 魔眼冲撞减速段(50t 起阻尼,80t 一循环,6 循环回悬浮)
430	    e.ai2 += 1;
431	    if (e.ai2 >= 50) {
432	      e.vx *= 0.93; e.vy *= 0.93;
433	      if (Math.abs(e.vx) < 0.1) e.vx = 0;
434	      if (Math.abs(e.vy) < 0.1) e.vy = 0;
435	    } else {
436	      e.spin = Math.atan2(e.vy, e.vx) - Math.PI / 2;
437	    }
438	    if (e.ai2 >= 80) {
439	      e.ai3 += 1; e.ai2 = 0;
440	      e.spin = target;
441	      if (e.ai3 >= 6) { e.ai1 = 0; e.ai3 = 0; } else e.ai1 = 1;
442	    }
443	  } else if (e.ai1 === 2) {
444	    // 雷眼冲撞减速段(25t 起阻尼,70t 一循环,4 循环回悬浮)
445	    e.ai2 += 1;
446	    if (e.ai2 >= 25) {
447	      e.vx *= 0.96; e.vy *= 0.96;
448	      if (Math.abs(e.vx) < 0.1) e.vx = 0;
449	      if (Math.abs(e.vy) < 0.1) e.vy = 0;
450	    } else {
451	      e.spin = Math.atan2(e.vy, e.vx) - Math.PI / 2;
452	    }
453	    if (e.ai2 >= 70) {
454	      e.ai3 += 1; e.ai2 = 0;
455	      e.spin = target;
456	      if (e.ai3 >= 4) { e.ai1 = 0; e.ai3 = 0; } else e.ai1 = 1;
457	    }
458	  }
459	  e.x += e.vx; e.y += e.vy;
460	}
461	
462	/** AI_032 机械骷髅王头 127(NPC.cs:27736-28054):初生成 4 部件;
463	 *  ai1: 0=悬浮(Y 带 200-500/X 窗 ±100,600t)→1=旋冲(防伤×2,2 速,400t);
464	 *  2=白天狂暴(伤/防 9999,10+距离/100 速追杀);3=玩家死/远 6000px 离场。 */
465	export function skeletronPrimeAI(e: Enemy, game: GameHooks, player: Player | null) {
466	  // 初始化:生成 128/129/130/131(ai0=侧 ±1, ai1=头 id;130/131 ai3=150 预热)
467	  if (!e.bInit) {
468	    e.bInit = true;
469	    const specs: Array<[number, number]> = [[128, -1], [129, 1], [130, -1], [131, 1]];
470	    for (const [id, side] of specs) {
471	      const p = spawnPart(game, e, id);
472	      if (p) { p.ai0 = side; p.ai1 = e.id; p.ai3 = id === 130 || id === 131 ? 150 : 0; p.bInit = true; }
473	    }
474	  }
475	  // 每 tick 从基值重置(vanilla damage=defDamage/defense=defDefense 置顶)
476	  const b = baseOf(e);
477	  e.def.damage = b.dmg;
478	  e.def.defense = b.def;
479	  // 玩家死亡(=无有效目标):按离场处理(原版 TargetClosest 落空 → ai[1]=3)
480	  if (!player) e.ai1 = 3;
481	  // 玩家死/超 6000px → 离场
482	  if (!player || Math.abs(e.cx - player.cx) > 6000 || Math.abs(e.cy - player.cy) > 6000) e.ai1 = 3;
483	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
484	  // 白天 → 狂暴(原版不逃走,持续 9999 追杀;Game.ts 日出剔除对 127 豁免)
485	  if (game.world.clock.isDay && e.ai1 !== 3 && e.ai1 !== 2) {
486	    e.ai1 = 2;
487	    game.playSfx('roar', 0.8);
488	  }
489	  if (e.ai1 === 0) {
490	    // 悬浮段(:27787-27874):Y 带 [玩家-200, 玩家-500] 0.1/±2;X 窗 ±100 0.1/±8
491	    e.ai2 += 1;
492	    if (e.ai2 >= 600) { e.ai2 = 0; e.ai1 = 1; }
493	    e.spin = e.vx / 15;
494	    if (e.y > player.y - 200) {
495	      if (e.vy > 0) e.vy *= 0.98;
496	      e.vy -= 0.1;
497	      if (e.vy > 2) e.vy = 2;
498	    } else if (e.y < player.y - 500) {
499	      if (e.vy < 0) e.vy *= 0.98;
500	      e.vy += 0.1;
501	      if (e.vy < -2) e.vy = -2;
502	    }
503	    if (e.cx > player.cx + 100) {
504	      if (e.vx > 0) e.vx *= 0.98;
505	      e.vx -= 0.1;
506	      if (e.vx > 8) e.vx = 8;
507	    }
508	    if (e.cx < player.cx - 100) {
509	      if (e.vx < 0) e.vx *= 0.98;
510	      e.vx += 0.1;
511	      if (e.vx < -8) e.vx = -8;
512	    }
513	  } else if (e.ai1 === 1) {
514	    // 旋冲段(:27875-27970):防伤×2,spin+=0.3*dir,经典 2 速直冲,400t 回悬浮
515	    e.def.defense = b.def * 2;
516	    e.def.damage = b.dmg * 2;
517	    e.ai2 += 1;
518	    if (e.ai2 === 2) game.playSfx('roar', 0.6);
519	    if (e.ai2 >= 400) { e.ai2 = 0; e.ai1 = 0; }
520	    e.spin += (e.facing || 1) * 0.3;
521	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
522	    const d = Math.hypot(dx, dy) || 1;
523	    e.vx = dx / d * 2; e.vy = dy / d * 2;
524	  } else if (e.ai1 === 2) {
525	    // 白天狂暴(:27971-28004):伤/防 9999,速 10+dist/100 钳 [8,32]
526	    e.def.damage = 9999;
527	    e.def.defense = 9999;
528	    e.spin += (e.facing || 1) * 0.3;
529	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
530	    const d = Math.hypot(dx, dy) || 1;
531	    let spd = 10 + d / 100;
532	    spd = Math.max(8, Math.min(32, spd));
533	    e.vx = dx / d * spd; e.vy = dy / d * spd;
534	  } else {
535	    // 离场(:28043-28052):下坠离场
536	    e.vy += 0.1;
537	    if (e.vy < 0) e.vy *= 0.95;
538	    e.vx *= 0.95;
539	    if (e.vy > 13) e.vy = 13;
540	  }
541	  e.facing = e.vx > 0 ? 1 : -1;
542	  e.x += e.vx;
543	  e.y += e.vy;
544	}
545	
546	/** AI_033-036 Prime 四部件(NPC.cs:28055-29110):ai1=头 id,ai0=侧 ±1。
547	 *  33=锯 129(上冲俯冲 22 速)/34=激光 130(直冲 20 速,ai3 初始 150 预热)/
548	 *  35=钳 128(悬头侧,激光 102 0 伤)/36=炮 131(玩家上空悬停,激光 100 25 伤)。
549	 *  公共:头失效→自毁;头离场(ai1==3)→自毁;远离锚点 800px→追赶态 99。 */
550	export function primePartAI(e: Enemy, game: GameHooks, player: Player | null) {
551	  const headId = e.ai1;
552	  const head = (game.enemies() as Enemy[]).find((n) => n.id === headId && n.vanilla?.aiStyle === 32);
553	  // 头死亡/失效 → 自毁(原版 ai2+=10 到 50 清除;简化即时)
554	  if (!head || head.dead) { e.dead = true; return; }
555	  const side = e.ai0 || 1;
556	  e.facing = -side;
557	  const ax = head.cx - 200 * side, ay = head.y + 230; // 部件锚点(vanilla num528 系)
558	  const distA = Math.hypot(ax - e.cx, ay - e.cy);
559	  if (e.ai2 !== 99) { if (distA > 800) e.ai2 = 99; }
560	  else if (distA < 400) e.ai2 = 0;
561	  if (head.ai1 === 3) { e.dead = true; return; } // 头离场:部件跟随消散
562	  if (!player) { e.x += e.vx; e.y += e.vy; return; } // 玩家死亡:悬停不动(原版坠落的简化)
563	
564	  const style = e.vanilla?.aiStyle ?? 33;
565	  const hoverBand = (yLow: number, yHigh: number, acc: number, max: number) => {
566	    // Y 带 [head.y+yLow, head.y+yHigh] 内归位(vanilla 双侧 if)
567	    if (e.y > head.y + yLow) {
568	      if (e.vy > 0) e.vy *= 0.96;
569	      e.vy -= acc;
570	      if (e.vy > max) e.vy = max;
571	    } else if (e.y < head.y + yHigh) {
572	      if (e.vy < 0) e.vy *= 0.96;
573	      e.vy += acc;
574	      if (e.vy < -max) e.vy = -max;
575	    }
576	  };
577	  const xWindow = (winHigh: number, winLow: number, acc: number, max: number) => {
578	    // X 窗 [head.cx+winLow, head.cx+winHigh] 内归位(头侧偏移由调用方传正值)
579	    if (e.cx > head.cx + winHigh) {
580	      if (e.vx > 0) e.vx *= 0.96;
581	      e.vx -= acc;
582	      if (e.vx > max) e.vx = max;
583	    } else if (e.cx < head.cx + winLow) {
584	      if (e.vx < 0) e.vx *= 0.96;
585	      e.vx += acc;
586	      if (e.vx < -max) e.vx = -max;
587	    }
588	  };
589	
590	  if (e.ai2 === 99) {
591	    // 追赶态(:28083-28132):直奔头(0.5/±12 X,0.1/±8 Y)
592	    if (e.y > head.y) { if (e.vy > 0) e.vy *= 0.96; e.vy -= 0.1; if (e.vy > 8) e.vy = 8; }
593	    else if (e.y < head.y) { if (e.vy < 0) e.vy *= 0.96; e.vy += 0.1; if (e.vy < -8) e.vy = -8; }
594	    if (e.cx > head.cx) { if (e.vx > 0) e.vx *= 0.96; e.vx -= 0.5; if (e.vx > 12) e.vx = 12; }
595	    if (e.cx < head.cx) { if (e.vx < 0) e.vx *= 0.96; e.vx += 0.5; if (e.vx < -12) e.vx = -12; }
596	    e.x += e.vx; e.y += e.vy;
597	    return;
598	  }
599	
600	  if (style === 33) {
601	    // ---- 锯(NPC 129,:28134-28358) ----
602	    if (e.ai2 === 0 || e.ai2 === 3) {
603	      if (head.ai1 !== 0) {
604	        // 头冲撞中:7 速逼近玩家(0.05 步进/0.97 阻尼)
605	        seekSteer(e, player, 7, 0.05);
606	        e.ai3 += 1;
607	        if (e.ai3 >= 600) { e.ai2 = 0; e.ai3 = 0; }
608	      } else {
609	        e.ai3 += 1;
610	        if (e.ai3 >= 300) { e.ai2 = 1; e.ai3 = 0; }
611	        hoverBand(320, 260, 0.04, 3);
612	        if (e.cx > head.cx) { if (e.vx > 0) e.vx *= 0.96; e.vx -= 0.3; if (e.vx > 12) e.vx = 12; }
613	        if (e.cx < head.cx - 250) { if (e.vx < 0) e.vx *= 0.96; e.vx += 0.3; if (e.vx < -12) e.vx = -12; }
614	      }
615	      e.spin = Math.atan2(ay - e.cy, ax - e.cx) + Math.PI / 2;
616	    } else if (e.ai2 === 1) {
617	      // 升空俯冲:升至头上 200 → 22 速冲玩家
618	      e.spin = Math.atan2(ay - e.cy, ax - e.cx) + Math.PI / 2;
619	      e.vx *= 0.95;
620	      e.vy -= 0.1;
621	      if (e.vy < -8) e.vy = -8;
622	      if (e.y < head.y - 200 && player) {
623	        e.ai2 = 2;
624	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
625	        const d = Math.hypot(dx, dy) || 1;
626	        e.vx = dx / d * 22; e.vy = dy / d * 22;
627	      }
628	    } else if (e.ai2 === 2) {
629	      // 俯冲到玩家下方/开始上移 → 回环绕(3)
630	      if (!player || e.y > player.y || e.vy < 0) e.ai2 = 3;
631	    } else if (e.ai2 === 5 && player) {
632	      if ((e.vx > 0 && e.cx > player.cx) || (e.vx < 0 && e.cx < player.cx)) e.ai2 = 0;
633	    }
634	  } else if (style === 34) {
635	    // ---- 激光(NPC 130,:28439-28638) ----
636	    if (e.ai2 === 0 || e.ai2 === 3) {
637	      if (head.ai1 !== 0) {
638	        // 头冲撞中:12 速突进(慢于 2 直接定速,否则阻尼)
639	        if (player) {
640	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
641	          const d = Math.hypot(dx, dy) || 1;
642	          if (Math.abs(e.vx) + Math.abs(e.vy) < 2) { e.vx = dx / d * 12; e.vy = dy / d * 12; }
643	          else { e.vx *= 0.97; e.vy *= 0.97; }
644	        }
645	        e.ai3 += 1;
646	        if (e.ai3 >= 600) { e.ai2 = 0; e.ai3 = 0; }
647	      } else {
648	        e.ai3 += 1;
649	        if (e.ai3 >= 600) { e.ai2 = 1; e.ai3 = 0; }
650	        hoverBand(300, 230, 0.1, 3);
651	        if (e.cx > head.cx + 250) { if (e.vx > 0) e.vx *= 0.94; e.vx -= 0.3; if (e.vx > 9) e.vx = 9; }
652	        if (e.cx < head.cx) { if (e.vx < 0) e.vx *= 0.94; e.vx += 0.2; if (e.vx < -8) e.vx = -8; }
653	      }
654	      e.spin = Math.atan2(ay - e.cy, ax - e.cx) + Math.PI / 2;
655	    } else if (e.ai2 === 1) {
656	      // 升空直冲:升至头上 280 → 20 速冲玩家(初 ai3=150 → 首冲提前)
657	      const ax2 = head.cx - 280 * side, ay2 = head.y + 230;
658	      e.spin = Math.atan2(ay2 - e.cy, ax2 - e.cx) + Math.PI / 2;
659	      if (e.vy > 0) e.vy *= 0.9;
660	      e.vx = (e.vx * 5 + head.vx) / 6;
661	      e.vx += 0.5;
662	      e.vy -= 0.5;
663	      if (e.vy < -9) e.vy = -9;
664	      if (e.y < head.y - 280 && player) {
665	        e.ai2 = 2;
666	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
667	        const d = Math.hypot(dx, dy) || 1;
668	        e.vx = dx / d * 20; e.vy = dy / d * 20;
669	      }
670	    } else if (e.ai2 === 2) {
671	      if (!player || e.y > player.y || e.vy < 0) {
672	        if (e.ai3 >= 4) { e.ai2 = 3; e.ai3 = 0; }
673	        else { e.ai2 = 1; e.ai3 += 1; }
674	      }
675	    } else if (e.ai2 === 4) {
676	      // 侧向横扫(原版与 5 互切;头冲撞分支偶尔进入)
677	      e.spin = Math.atan2(ay - e.cy, ax - e.cx) + Math.PI / 2;
678	      e.vy = (e.vy * 5 + head.vy) / 6;
679	      e.vx += 0.5;
680	      if (e.vx > 12) e.vx = 12;
681	      if (player && Math.abs(e.cx - head.cx) > 500) {
682	        e.ai2 = 5;
683	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
684	        const d = Math.hypot(dx, dy) || 1;
685	        e.vx = dx / d * 17; e.vy = dy / d * 17;
686	      }
687	    } else if (e.ai2 === 5 && player && e.cx < player.cx - 100) {
688	      if (e.ai3 >= 4) { e.ai2 = 0; e.ai3 = 0; }
689	      else { e.ai2 = 4; e.ai3 += 1; }
690	    }
691	  } else if (style === 35) {
692	    // ---- 钳(NPC 128,:28653-28874) ----
693	    if (e.ai2 === 0) {
694	      if (head.ai1 !== 0) {
695	        hoverBand(-100, -100, 0.07, 6);
696	        xWindow(-120 * side, -120 * side, 0.1, 8);
697	      } else {
698	        e.ai3 += 1;
699	        if (e.ai3 >= 1100) { e.ai2 = 1; e.ai3 = 0; }
700	        hoverBand(-150, -150, 0.04, 3);
701	        xWindow(200, 160, 0.2, 8);
702	      }
703	      e.spin = Math.atan2(ay - e.cy, ax - e.cx) + Math.PI / 2;
704	      // 反向激光 102(原版伤害 0 = 纯视觉威慑)每 140t
705	      if (e.aiT % 140 === 0) {
706	        const dx = -(ax - e.cx), dy = -(ay - e.cy);
707	        const d = Math.hypot(dx, dy) || 1;
708	        shoot(game, e.cx + dx / d * 4, e.cy + dy / d * 4,
709	          dx / d * 12 + (Math.random() - 0.5) * 0.8, dy / d * 12 + (Math.random() - 0.5) * 0.8, 0, 102);
710	      }
711	    } else if (e.ai2 === 1 && player) {
712	      e.ai3 += 1;
713	      if (e.ai3 >= 300) { e.ai2 = 0; e.ai3 = 0; }
714	      // 悬停:头 X / 玩家上方 80(6 速,0.04 X/0.08 Y,0.9 阻尼)
715	      seekSteer2(e, head.cx, player.cy - 80, 6, 0.04, 0.08);
716	      e.spin = Math.atan2(player.cy - e.cy, player.cx - e.cx) - Math.PI / 2;
717	      if (e.aiT % 40 === 0) {
718	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
719	        const d = Math.hypot(dx, dy) || 1;
720	        shoot(game, e.cx + dx / d * 4, e.cy + dy / d * 4,
721	          dx / d * 10 + (Math.random() - 0.5) * 0.8, dy / d * 10 + (Math.random() - 0.5) * 0.8, 0, 102);
722	      }
723	    }
724	  } else if (style === 36) {
725	    // ---- 炮(NPC 131,:28889-29109;初 ai3=150 计入 800 门) ----
726	    if (e.ai2 === 0 || e.ai2 === 3) {
727	      if (head.ai1 !== 0) {
728	        hoverBand(-100, -100, 0.07, 6);
729	        xWindow(-120 * side, -120 * side, 0.1, 8);
730	      } else {
731	        e.ai3 += 1;
732	        if (e.ai3 >= 800) { e.ai2 = 1; e.ai3 = 0; }
733	        hoverBand(-100, -100, 0.1, 3);
734	        xWindow(-180 * side, -180 * side, 0.14, 8);
735	      }
736	      if (player) {
737	        e.spin = Math.atan2(player.cy - e.cy, player.cx - e.cx) - Math.PI / 2;
738	        if (e.aiT % 200 === 0) {
739	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
740	          const d = Math.hypot(dx, dy) || 1;
741	          shoot(game, e.cx + dx / d * 8, e.cy + dy / d * 8,
742	            dx / d * 8 + (Math.random() - 0.5) * 4, dy / d * 8 + (Math.random() - 0.5) * 4, 25, 100);
743	        }
744	      }
745	    } else if (e.ai2 === 1 && player) {
746	      e.ai3 += 1;
747	      if (e.ai3 >= 200) { e.ai2 = 0; e.ai3 = 0; }
748	      // 悬停玩家左侧 350/上方 20(7 速,0.1/0.03,0.9 阻尼)
749	      seekSteer2(e, player.cx - 350, player.cy - 20, 7, 0.1, 0.03);
750	      e.spin = Math.atan2(player.cy - e.cy, player.cx - e.cx) - Math.PI / 2;
751	      if (e.aiT % 80 === 0) {
752	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
753	        const d = Math.hypot(dx, dy) || 1;
754	        shoot(game, e.cx + dx / d * 8, e.cy + dy / d * 8,
755	          dx / d * 10 + (Math.random() - 0.5) * 4, dy / d * 10 + (Math.random() - 0.5) * 4, 25, 100);
756	      }
757	    }
758	  }
759	  e.x += e.vx;
760	  e.y += e.vy;
761	}
762	
763	/** 原版"逼近目标速度"舵(:28161-28192 锯/激光共用):目标 = dir*spd,0.97 阻尼 ±0.05 步进 */
764	export function seekSteer(e: Enemy, target: { cx: number; cy: number }, spd: number, acc: number): void {
765	  const dx = target.cx - e.cx, dy = target.cy - e.cy;
766	  const d = Math.hypot(dx, dy) || 1;
767	  const tx = (dx / d) * spd, ty = (dy / d) * spd;
768	  if (e.vx > tx) { if (e.vx > 0) e.vx *= 0.97; e.vx -= acc; }
769	  if (e.vx < tx) { if (e.vx < 0) e.vx *= 0.97; e.vx += acc; }
770	  if (e.vy > ty) { if (e.vy > 0) e.vy *= 0.97; e.vy -= acc; }
771	  if (e.vy < ty) { if (e.vy < 0) e.vy *= 0.97; e.vy += acc; }
772	}
773	/** 同上但 X/Y 不同步进(钳/炮悬停态,:28817-28848/:29052-29083),0.9 阻尼 */
774	export function seekSteer2(e: Enemy, tx0: number, ty0: number, spd: number, accX: number, accY: number): void {
775	  const dx = tx0 - e.cx, dy = ty0 - e.cy;
776	  const d = Math.hypot(dx, dy) || 1;
777	  const tx = (dx / d) * spd, ty = (dy / d) * spd;
778	  if (e.vx > tx) { if (e.vx > 0) e.vx *= 0.9; e.vx -= accX; }
779	  if (e.vx < tx) { if (e.vx < 0) e.vx *= 0.9; e.vx += accX; }
780	  if (e.vy > ty) { if (e.vy > 0) e.vy *= 0.9; e.vy -= accY; }
781	  if (e.vy < ty) { if (e.vy < 0) e.vy *= 0.9; e.vy += accY; }
782	}
783	
784	/** AI_037 毁灭者 134-136(NPC.cs:50129-50624):头穿地飞行——
785	 *  空中:下坠 0.15/钳 16 并横漂向玩家;地下(实心/液体):全向舵向玩家(0.1/0.15 双档);
786	 *  白天/玩家死:加速下坠,过岩石层整链消散;体节 135 探针随机激光 100。
787	 *  段链 80 段(原版 GetDestroyerSegmentsCount;链距 44px)由头驱动收缩跟随。 */
788	export function destroyerAI(e: Enemy, game: GameHooks, player: Player | null) {
789	  if (!e.bInit) {
790	    e.bInit = true;
791	    // 原版 ai[0]==0 时头生成 80 段链(body 135×79 + tail 136;链距 44*scale)
792	    const segs = enemySpawnChain(e, 80);
793	    for (const s of segs) addEnemy(game, s);
794	  }
795	  const st = game.world.store;
796	  // 接地判定(flag2):AABB 外扩 1-2 格内实心块或液体>64(:50278-50298)
797	  let buried = false;
798	  const tx0 = Math.max(0, Math.floor(e.x / TILE) - 1), tx1 = Math.min(st.w - 1, Math.floor((e.x + e.w) / TILE) + 2);
799	  const ty0 = Math.max(0, Math.floor(e.y / TILE) - 1), ty1 = Math.min(st.h - 1, Math.floor((e.y + e.h) / TILE) + 2);
800	  for (let x = tx0; x <= tx1 && !buried; x++) {
801	    for (let y = ty0; y <= ty1; y++) {
802	      const i = st.idx(x, y);
803	      if ((st.flags[i] && st.isSolid(x, y)) || st.liquid[i] > 64) {
804	        if (e.x + e.w > x * TILE && e.x < x * TILE + 16 && e.y + e.h > y * TILE && e.y < y * TILE + 16) { buried = true; break; }
805	      }
806	    }
807	  }
808	
809	  // 白天/玩家死:下坠离场;过岩石层整链消散(:50337-50356)
810	  const dayFlee = game.world.clock.isDay || !player || player.dead;
811	  if (dayFlee) {
812	    e.vy += 1;
813	    if (e.y > game.world.groundLevel * TILE) e.vy += 1;
814	    e.spin = Math.atan2(e.vy, e.vx) + Math.PI / 2;
815	    e.x += e.vx; e.y += e.vy;
816	    driveChain(e, 44);
817	    if (e.y > game.world.rockLevel * TILE) {
818	      for (let s: Enemy | null = e; s; s = s.wormNext) s.dead = true;
819	    }
820	    return;
821	  }
822	
823	  const spd = 16, acc = 0.1, acc2 = 0.15;
824	  if (!buried) {
825	    // 空中(:50416-50458):下坠 0.15 钳 16;慢速时横漂,满速下坠时向玩家 X 修正
826	    e.vy += 0.15;
827	    if (e.vy > spd) e.vy = spd;
828	    const px = Math.floor(player.cx / TILE) * TILE, py = Math.floor(player.cy / TILE) * TILE;
829	    const sx = Math.floor(e.cx / TILE) * TILE, sy = Math.floor(e.cy / TILE) * TILE;
830	    const dx = px - sx, dy = py - sy;
831	    if (Math.abs(e.vx) + Math.abs(e.vy) < spd * 0.4) {
832	      e.vx += (e.vx < 0 ? -acc * 1.1 : acc * 1.1);
833	    } else if (e.vy === spd) {
834	      if (e.vx < dx) e.vx += acc;
835	      else if (e.vx > dx) e.vx -= acc;
836	    } else if (e.vy > 4) {
837	      e.vx += (e.vx < 0 ? acc * 0.9 : -acc * 0.9);
838	    }
839	    void dy;
840	  } else {
841	    // 地下(:50459-50585):目标速度 = 方向*16,分档加速(同向双轴 0.15→同向单轴 0.10+
842	    // 反轴轻推→主轴 0.11 次轴补速;含防卡死角交叉助推)
843	    const dx = Math.floor(player.cx / TILE) * TILE - Math.floor(e.cx / TILE) * TILE;
844	    const dy = Math.floor(player.cy / TILE) * TILE - Math.floor(e.cy / TILE) * TILE;
845	    const d = Math.hypot(dx, dy) || 1;
846	    const tvx = (dx / d) * spd, tvy = (dy / d) * spd;
847	    const sameX = (e.vx > 0 && tvx > 0) || (e.vx < 0 && tvx < 0);
848	    const sameY = (e.vy > 0 && tvy > 0) || (e.vy < 0 && tvy < 0);
849	    if (sameX && sameY) {
850	      if (e.vx < tvx) e.vx += acc2; else if (e.vx > tvx) e.vx -= acc2;
851	      if (e.vy < tvy) e.vy += acc2; else if (e.vy > tvy) e.vy -= acc2;
852	    }
853	    if (sameX || sameY) {
854	      if (e.vx < tvx) e.vx += acc; else if (e.vx > tvx) e.vx -= acc;
855	      if (e.vy < tvy) e.vy += acc; else if (e.vy > tvy) e.vy -= acc;
856	      if (Math.abs(tvy) < spd * 0.2 && ((e.vx > 0 && tvx < 0) || (e.vx < 0 && tvx > 0))) {
857	        e.vy += (e.vy > 0 ? acc * 2 : -acc * 2);
858	      }
859	      if (Math.abs(tvx) < spd * 0.2 && ((e.vy > 0 && tvy < 0) || (e.vy < 0 && tvy > 0))) {
860	        e.vx += (e.vx > 0 ? acc * 2 : -acc * 2);
861	      }
862	    } else if (Math.abs(dx) > Math.abs(dy)) {
863	      if (e.vx < tvx) e.vx += acc * 1.1; else if (e.vx > tvx) e.vx -= acc * 1.1;
864	      if (Math.abs(e.vx) + Math.abs(e.vy) < spd * 0.5) e.vy += (e.vy > 0 ? acc : -acc);
865	    } else {
866	      if (e.vy < tvy) e.vy += acc * 1.1; else if (e.vy > tvy) e.vy -= acc * 1.1;
867	      if (Math.abs(e.vx) + Math.abs(e.vy) < spd * 0.5) e.vx += (e.vx > 0 ? acc : -acc);
868	    }
869	  }
870	  e.spin = Math.atan2(e.vy, e.vx) + Math.PI / 2;
871	  e.x += e.vx;
872	  e.y += e.vy;
873	  // 段链跟随(linkDist 44 = 44*scale;原版 num24) + 探针弹幕
874	  driveChain(e, 44);
875	  if (!buried) {
876	    for (let s = e.wormNext; s; s = s.wormNext) {
877	      if (s.vanillaId !== 135 || s.dead) continue;
878	      // 原版 135:localAI[0] += Next(4),达 Next(1400,26000) 触发(期望 ~6850t/节);
879	      // 近似为每 tick 2/6850 概率 + 视线检查
880	      if (Math.random() < 2 / 6850 && losClear(game, s.cx, s.cy, player.cx, player.cy)) {
881	        const dx = player.cx - s.cx + (Math.random() - 0.5) * 40;
882	        const dy = player.cy - s.cy + (Math.random() - 0.5) * 40;
883	        const d = Math.hypot(dx, dy) || 1;
884	        shoot(game, s.cx + dx / d * 5, s.cy + dy / d * 5,
885	          dx / d * 8 + (Math.random() - 0.5) * 2, dy / d * 8 + (Math.random() - 0.5) * 2, 22, 100);
886	      }
887	    }
888	  }
889	}
890	
891	/** 生成蠕虫段链(Enemy.spawnWormChain 的外部包装;Destroyer 用 135/136) */
892	export function enemySpawnChain(head: Enemy, count: number): Enemy[] {
893	  const Ctor = enemyCtor;
894	  if (!Ctor) return [];
895	  return Ctor.spawnWormChain(head, count);
896	}
897	/** 头驱动段链收缩跟随(原版 :50374-50414,linkDist 可配) */
898	export function driveChain(head: Enemy, linkDist: number): void {
899	  for (let s = head.wormNext; s; s = s.wormNext) {
900	    const fx = s.wormFollow!;
901	    const dxC = fx.cx - s.cx;
902	    const dyC = fx.cy - s.cy;
903	    const dist = Math.hypot(dxC, dyC);
904	    if (dist > 0.01) {
905	      const shrink = (dist - linkDist) / dist;
906	      s.x += dxC * shrink;
907	      s.y += dyC * shrink;
908	      s.spin = Math.atan2(dyC, dxC) + Math.PI / 2;
909	      s.facing = dxC < 0 ? 1 : -1;
910	    }
911	  }
912	}
913	
914	// ---- 工具 ----
915	
916	function collideGround(e: Enemy, game: GameHooks) {
917	  const st = game.world.store;
918	  const tx = Math.floor(e.cx / TILE);
919	  const ty = Math.floor((e.y + e.h) / TILE);
920	  if (st.inBounds(tx, ty) && st.isSolid(tx, ty) && e.vy >= 0) {
921	    e.y = ty * TILE - e.h;
922	    e.vy = 0;
923	    e.onGround = true;
924	  } else {
925	    e.onGround = false;
926	  }
927	  const ty2 = Math.floor(e.y / TILE);
928	  if (st.inBounds(tx, ty2) && st.isSolid(tx, ty2) && e.vy < 0) {
929	    e.y = (ty2 + 1) * TILE;
930	    e.vy = 0;
931	  }
932	  const tx2 = Math.floor((e.x + e.w) / TILE);
933	  if (st.inBounds(tx2, Math.floor(e.cy / TILE)) && st.isSolid(tx2, Math.floor(e.cy / TILE)) && e.vx > 0) {
934	    e.x = tx2 * TILE - e.w; e.vx = 0;
935	  }
936	  const tx3 = Math.floor(e.x / TILE);
937	  if (st.inBounds(tx3, Math.floor(e.cy / TILE)) && st.isSolid(tx3, Math.floor(e.cy / TILE)) && e.vx < 0) {
938	    e.x = (tx3 + 1) * TILE; e.vx = 0;
939	  }
940	}
941	

```


---

## 🤖 Assistant · 2026-08-10T06:46:09.262Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: baseOf is private (not exported). The task says "临时修正自建 WeakMap 基值缓存" — I'll create my own WeakMap in bossAI_golem.ts.

Now let me read bossAI_duke_moonlord.ts for the checkDead pattern, and the mechprobe script for the probe template.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:46:09.263Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:09.412Z

**📎 ToolResult**

```
1	// Boss AI 1:1 移植(二):猪鲨鱼龙 AI_069(NPC 370)与月亮领主 aiStyle 77/78/79(NPC 398 核心 / 397 手 / 396 头)。
2	// 源码:Terarria1456(1.4.5.6)NPC.cs ——
3	//   猪鲨 AI_069_DukeFishron        :49143-50127
4	//   月总核心 aiStyle 77(398)      :36774-37198
5	//   月总手   aiStyle 78(397)      :37199-37711
6	//   月总头   aiStyle 79(396)      :37712-38128
7	//   攻击时间表 MoonLordAttacksArray :6830-6946 / MoonLordAttacksArray2 :6948-6987
8	//   死亡转换 checkDead             :78841-78867(396/397 血尽→ai0=-2 闭眼残肢+召真眼;398 血尽→ai0=2 死亡演出)
9	// 经典模式主链 1:1;expert/getGoodWorld 分支保留注释;netcode 跳过。
10	// 无敌语义:dontTakeDamage 用 e.iframes=2 每 tick 刷新近似(同 bossAI.ts 克脑一阶段)。
11	import type { Enemy } from './Enemy';
12	import type { GameHooks } from './types';
13	import type { Player } from './Player';
14	import { TILE } from '../core/constants';
15	import { spawnPart, shoot, accelTo } from './bossAI';
16	
17	// ---------------------------------------------------------------------------
18	// 通用工具
19	// ---------------------------------------------------------------------------
20	
21	/** Boss 伤害/防御基值缓存(状态机每 tick 从基值派生临时修正,防重复乘膨胀) */
22	const baseStats = new WeakMap<Enemy, { dmg: number; def: number }>();
23	const baseOf = (e: Enemy) => {
24	  let b = baseStats.get(e);
25	  if (!b) { b = { dmg: e.def.damage, def: e.def.defense ?? 0 }; baseStats.set(e, b); }
26	  return b;
27	};
28	
29	const TAU = Math.PI * 2;
30	const clamp = (v: number, lo: number, hi: number) => (v < lo ? lo : v > hi ? hi : v);
31	const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
32	/** 标量区间平滑(驱动向量 SmoothStep 的 amount 因子) */
33	const smoothAmt = (t: number) => {
34	  t = clamp(t, 0, 1);
35	  return t * t * (3 - 2 * t);
36	};
37	/** 原版 Vector2.SmoothStep(cur, target, amount):Lerp(amount²(3-2amount)) */
38	const vSmoothStep = (cur: number, target: number, amount: number) => lerp(cur, target, smoothAmt(amount));
39	/** 角度插值(原版 float.AngleLerp:取最短方向步进) */
40	const angleLerp = (cur: number, target: number, t: number) => {
41	  let d = target - cur;
42	  while (d > Math.PI) d -= TAU;
43	  while (d < -Math.PI) d += TAU;
44	  return cur + d * t;
45	};
46	
47	/** 原版 SimpleFlyMovement(:78100)+ 速度折半混合(月总 8/0.5+Lerp0.5 的组合写法):
48	 *  先单轴步进逼近目标速度,再与步进前速度做 0.5 Lerp(等效步长减半) */
49	const flyLerp = (e: Enemy, tx: number, ty: number, acc: number) => {
50	  const ox = e.vx, oy = e.vy;
51	  e.vx = accelTo(e.vx, tx, acc);
52	  e.vy = accelTo(e.vy, ty, acc);
53	  e.vx = lerp(ox, e.vx, 0.5);
54	  e.vy = lerp(oy, e.vy, 0.5);
55	};
56	
57	/** 每实例附加槽位(原版 direction/spriteDirection/localAI/frameCounter 等无对应 Enemy 字段) */
58	interface DukeX { dir: number; spr: number }
59	const dukeX = new WeakMap<Enemy, DukeX>();
60	const dukeOf = (e: Enemy): DukeX => {
61	  let x = dukeX.get(e);
62	  if (!x) { x = { dir: 1, spr: 1 }; dukeX.set(e, x); }
63	  return x;
64	};
65	interface HandX { frame: number; l0: number; l1: number }
66	const handX = new WeakMap<Enemy, HandX>();
67	const handOf = (e: Enemy): HandX => {
68	  let x = handX.get(e);
69	  if (!x) { x = { frame: 0, l0: 0, l1: 0 }; handX.set(e, x); }
70	  return x;
71	};
72	interface HeadX { f2: number; f3: number; l0: number; l1: number; l2: number }
73	const headX = new WeakMap<Enemy, HeadX>();
74	const headOf = (e: Enemy): HeadX => {
75	  let x = headX.get(e);
76	  if (!x) { x = { f2: 0, f3: 0, l0: 0, l1: 0, l2: 0 }; headX.set(e, x); }
77	  return x;
78	};
79	
80	/** 实心块内判定(原版 Collision.SolidCollision 的中心点近似) */
81	const inSolid = (game: GameHooks, e: Enemy): boolean => {
82	  const st = game.world.store;
83	  const tx = Math.floor(e.cx / TILE), ty = Math.floor(e.cy / TILE);
84	  return st.inBounds(tx, ty) && st.isSolid(tx, ty);
85	};
86	
87	/** 原版"攻击时间表"推进(NPC.cs :37229-37251 / :37740-37762 / :38243-38264 同构):
88	 *  ai1 全局计时,逐槽累计时长定位当前槽;全部槽走完回绕 ai1=0。
89	 *  注意:只回写 ai1,不写 ai0——手/头由调用方把槽攻击号赋给 ai0(即其状态),
90	 *  核心二阶段 ai0 是相位状态(0/1/2/3),绝不能被攻击号覆盖。 */
91	function attackSlot(e: Enemy, table: ReadonlyArray<readonly [number, number]>): { atk: number; inSlot: number; dur: number } {
92	  let slot = 0, consumed = 0;
93	  while (slot < table.length) {
94	    const dur = table[slot][1];
95	    if (dur + consumed > e.ai1) break;
96	    consumed += dur;
97	    slot++;
98	  }
99	  if (slot === table.length) { slot = 0; e.ai1 = 0; consumed = 0; }
100	  const atk = table[slot][0];
101	  return { atk, inSlot: e.ai1 - consumed, dur: table[slot][1] };
102	}
103	
104	// ---------------------------------------------------------------------------
105	// AI_069 猪鲨鱼龙(NPC 370,NPC.cs:49143-50127)
106	// ---------------------------------------------------------------------------
107	// 状态 ai0:-1 出生(75t) → 一阶段循环 0 悬浮(num3 t)→1 冲撞(num6 t)×5→2 泡泡弹(80t)
108	//   →3 鲨鱼龙卷(90t);血 ≤50% →4 变身(180t) →5 二阶段循环:0→6 冲撞→7 旋转泡泡冲刺(120t)
109	//   →8 鲨鱼龙卷;9(expert 15% 血)二段变身(180t) →10 隐身悬浮→11 冲撞/12 瞬移(30t)/13 旋转冲刺。
110	// 经典参数:悬浮 60t/0.45/7.5、冲撞 30t@16 速、泡泡 80t 每 4t 一发、龙卷 90t(60t 时发射)、变身 180t。
111	
112	const DUKE = {
113	  spawnT: 75,          // num21 :49215
114	  hoverT: 60,          // num3  :49168(经典)
115	  hoverAcc: 0.45,      // num4  :49169
116	  hoverSpd: 7.5,       // num5  :49170
117	  chargeT: 30,         // num6  :49187
118	  chargeSpd: 16,       // num7  :49188
119	  bubbleT: 80,         // num8  :49202
120	  bubbleEvery: 4,      // num9  :49203
121	  bubbleAcc: 0.3,      // num10 :49204
122	  bubbleSpd: 5,        // num11 :49205
123	  nadoT: 90,           // num12 :49206
124	  p1T: 180,            // num13 :49207(一→二阶段变身)
125	  p2T: 180,            // num14 :49208(二段狂暴变身,expert)
126	  teleT: 30,           // num15 :49209(瞬移)
127	  spinT: 120,          // num16 :49210(旋转冲刺)
128	  spinEvery: 4,        // num17 :49211
129	  spinBubbleSpd: 6,    // num18 :49212
130	  spinDashSpd: 20,     // num19 :49213
131	};
132	/** 旋转冲刺角速度 num20 = 2π/(num16/2) = 2π/60(:49214) */
133	const DUKE_SPIN_RATE = TAU / (DUKE.spinT / 2);
134	
135	/** 狂暴判定 flag6(:49238):玩家在太空(y<800)/地下(y>worldSurface*16)/离开两侧海洋带 */
136	function dukeEnraged(game: GameHooks, player: Player): boolean {
137	  const st = game.world.store;
138	  const surface = (game.world.groundLevel || Math.floor(st.h * 0.3)) * TILE;
139	  return player.y < 800 || player.y > surface ||
140	    (player.x > 6400 && player.x < st.w * TILE - 6400);
141	}
142	
143	/** 一阶段悬浮结束的下一招(:49471-49542) */
144	function dukePick1(e: Enemy, enraged: boolean): number {
145	  const a3 = Math.floor(e.ai3);
146	  let next = 0; // 0=无事(原版 switch 无匹配分支,ai2 继续累计)
147	  if (a3 >= 0 && a3 <= 9) next = 1;          // 冲撞
148	  else if (a3 === 10) { e.ai3 = 1; next = 2; } // 泡泡弹
149	  else if (a3 === 11) { e.ai3 = 0; next = 3; } // 鲨鱼龙卷
150	  if (enraged && next === 2) next = 3;       // :49495 狂暴时泡泡弹换龙卷
151	  if (e.hp <= e.maxHp * 0.5) next = 4;       // :49499 半血变身
152	  return next;
153	}
154	/** 二阶段悬浮结束的下一招(:49736-49809) */
155	function dukePick2(e: Enemy, enraged: boolean): number {
156	  const a3 = Math.floor(e.ai3);
157	  let next = 0;
158	  if (a3 >= 0 && a3 <= 5) next = 1;          // 冲撞(6)
159	  else if (a3 === 6) { e.ai3 = 1; next = 2; } // 旋转泡泡冲刺(7)
160	  else if (a3 === 7) { e.ai3 = 0; next = 3; } // 鲨鱼龙卷(8)
161	  // flag2(expert hp≤15%):next=4 → ai0=9(:49756-49759)——经典模式不可达,代码保留见 dukeState9
162	  if (enraged && next === 2) next = 3;       // :49760
163	  return next;
164	}
165	/** 冲撞起手(:49503-49520 / :49764-49781 / :49988-50004 同构):定速直冲+朝向修正 */
166	function dukeCharge(e: Enemy, player: Player, spd: number, toState: number, st: DukeX) {
167	  const dx = player.cx - e.cx, dy = player.cy - e.cy;
168	  const d = Math.hypot(dx, dy) || 1;
169	  e.vx = (dx / d) * spd;
170	  e.vy = (dy / d) * spd;
171	  e.ai0 = toState; e.ai1 = 0; e.ai2 = 0;
172	  e.spin = Math.atan2(e.vy, e.vx);
173	  const s = Math.sign(dx) || st.dir;
174	  st.dir = s;
175	  if (st.spr === 1) e.spin += Math.PI;
176	  st.spr = -s;
177	}
178	/** 悬浮段共用(:49415-49468 / :49680-49733 / :49932-49967 同构):
179	 *  目标点 = 玩家 + (ai1 侧偏, -200);desired = normalize(目标-自身-速度)*spd 后 SimpleFlyMovement */
180	function dukeHover(e: Enemy, player: Player, acc: number, spd: number, sideOff: number, st: DukeX) {
181	  if (e.ai1 === 0) e.ai1 = sideOff * Math.sign(e.cx - player.cx || 1);
182	  const dx = player.cx + e.ai1 - e.cx - e.vx;
183	  const dy = player.cy - 200 - e.cy - e.vy;
184	  const d = Math.hypot(dx, dy) || 1;
185	  e.vx = accelTo(e.vx, (dx / d) * spd, acc);
186	  e.vy = accelTo(e.vy, (dy / d) * spd, acc);
187	  const s = Math.sign(player.cx - e.cx) || st.dir;
188	  if (e.ai2 === 0 && s !== st.dir) e.spin += Math.PI;
189	  st.dir = s;
190	  if (st.spr !== -st.dir) e.spin += Math.PI;
191	  st.spr = -st.dir;
192	}
193	
194	/** AI_069 主入口(经典模式) */
195	export function dukeFishronAI(e: Enemy, game: GameHooks, player: Player | null) {
196	  const st = dukeOf(e);
197	  if (!e.bInit) { e.bInit = true; e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; e.spawnAlpha = 255; } // :49247-49257
198	  const b = baseOf(e);
199	  const enraged = player ? dukeEnraged(game, player) : false;
200	  const flag = e.hp <= e.maxHp * 0.5;                       // flag  :49147 二阶段
201	  const flag3 = e.ai0 > 4;                                  // flag3 :49149(二阶段状态 5-13)
202	  const flag4 = e.ai0 > 9;                                  // flag4 :49150(expert 狂暴段 10-13)
203	  const flag5 = e.ai3 < (flag3 ? 3 : 5) * 2;                // flag5 :49151-49152
204	
205	  // 伤害/防御修正(:49153-49167 + 狂暴 :49239-49245)——每 tick 从基值派生
206	  if (flag4) { e.def.damage = Math.round(b.dmg * 1.1); e.def.defense = 0; }
207	  else if (flag3) { e.def.damage = Math.round(b.dmg * 1.2); e.def.defense = Math.round(b.def * 0.8); }
208	  else { e.def.damage = b.dmg; e.def.defense = b.def; }
209	  if (enraged) { e.def.damage = b.dmg * 2; e.def.defense = b.def * 2; }
210	
211	  // 悬浮/冲撞参数(:49168-49201;expert 档注释)
212	  let hoverT = DUKE.hoverT, hoverAcc = DUKE.hoverAcc, hoverSpd = DUKE.hoverSpd;
213	  if (flag4) { hoverAcc = 0.7; hoverSpd = 12; hoverT = 30; }            // :49171-49176
214	  else if (flag3 && flag5) { hoverAcc = 0.5; hoverSpd = 8; hoverT = 20; } // :49177-49182
215	  else if (flag5 && !flag3 && !flag4) hoverT = 30;                       // :49183-49186
216	  let chargeT = DUKE.chargeT, chargeSpd = DUKE.chargeSpd;
217	  if (flag4) { chargeT = 25; chargeSpd = 27; }                           // :49189-49193(expert 同档)
218	  if (enraged) { hoverT = 10; chargeSpd += 6; }                          // :49239-49245
219	
220	  // 玩家死/远离 5600px(:49218-49237):减速升空离场(原版另 EncourageDespawn(10);
221	  // 本工程 Boss 不参与 despawn 块,故仅保留升空)。原版此处无回血逻辑。
222	  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {
223	    e.vy -= 0.4;
224	    e.ai0 = e.ai0 > 4 ? 5 : 0;
225	    e.ai2 = 0;
226	    e.x += e.vx; e.y += e.vy;
227	    return;
228	  }
229	
230	  // ---- 身体旋转朝向(:49258-49345)----
231	  let target = Math.atan2(player.cy - e.cy, player.cx - e.cx);
232	  if (st.spr === 1) target += Math.PI;
233	  if (target < 0) target += TAU; else if (target > TAU) target -= TAU;
234	  if (e.ai0 === -1 || e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) target = 0; // :49271-49286
235	  let step = 0.04;                                                            // num23 :49287
236	  if (e.ai0 === 1 || e.ai0 === 6 || e.ai0 === 7) step = 0;                    // :49288-49295
237	  if (e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) step = 0.01;                 // :49296-49307
238	  let rot = e.spin;
239	  if (rot < target) rot += (target - rot > Math.PI ? -step : step);
240	  if (rot > target) rot += (rot - target > Math.PI ? step : -step);
241	  if (rot > target - step && rot < target + step) rot = target;
242	  if (rot < 0) rot += TAU; else if (rot > TAU) rot -= TAU;
243	  if (rot > target - step && rot < target + step) rot = target;
244	  e.spin = rot;
245	
246	  // ---- 透明度(:49346-49364 + 各状态内分支;近似为 spawnAlpha 渐变) ----
247	  if (e.ai0 !== -1 && e.ai0 < 9) e.spawnAlpha = inSolid(game, e) ? Math.min(255, e.spawnAlpha + 15) : Math.max(0, e.spawnAlpha - 15);
248	
249	  let invuln = false; // flag7(dontTakeDamage = !flag7,:50126)
250	  switch (e.ai0) {
251	    case -1: { // 出生(:49365-49414)
252	      invuln = true;
253	      e.vx *= 0.98; e.vy *= 0.98;
254	      const s = Math.sign(player.cx - e.cx) || st.dir;
255	      st.dir = s; st.spr = -s;
256	      if (e.ai2 > 20) {
257	        e.vy = -2;
258	        e.spawnAlpha = clamp(e.spawnAlpha - 5 + (inSolid(game, e) ? 15 : 0), 0, 150); // :49375-49391
259	      } else if (e.spawnAlpha < 255) e.spawnAlpha = 255;
260	      if (e.ai2 === DUKE.nadoT - 30) { // :49392 出生尘环
261	        game.spawnParticles(e.cx, e.cy, '#8FD8FF', 18, 2.4, { life: 40 });
262	        game.playSfx('roar', 0.8);
263	      }
264	      e.ai2 += 1;
265	      if (e.ai2 >= DUKE.spawnT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
266	      break;
267	    }
268	    case 0: { // 一阶段悬浮(:49415-49543)
269	      if (player.dead) break;
270	      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
271	      e.ai2 += 1;
272	      if (e.ai2 >= hoverT) {
273	        const next = dukePick1(e, enraged);
274	        if (next === 1) dukeCharge(e, player, chargeSpd, 1, st);
275	        else if (next === 2) { e.ai0 = 2; e.ai1 = 0; e.ai2 = 0; }
276	        else if (next === 3) {
277	          e.ai0 = 3; e.ai1 = 0; e.ai2 = 0;
278	          if (enraged) e.ai2 = DUKE.nadoT - 40; // :49530-49533 狂暴跳过前摇
279	        } else if (next === 4) { e.ai0 = 4; e.ai1 = 0; e.ai2 = 0; }
280	      }
281	      break;
282	    }
283	    case 1: { // 冲撞(:49544-49566)
284	      game.spawnParticles(e.cx + e.w / 2 - Math.cos(e.spin) * e.w * 0.3, e.cy + e.h / 2 - Math.sin(e.spin) * e.h * 0.3, '#8FD8FF', 2, 1.5, { life: 18 });
285	      e.ai2 += 1;
286	      if (e.ai2 >= chargeT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 += 2; }
287	      break;
288	    }
289	    case 2: { // 泡泡弹幕(:49567-49637)
290	      if (player.dead) break;
291	      if (e.ai1 === 0) e.ai1 = 300 * Math.sign(e.cx - player.cx || 1);
292	      const dx = player.cx + e.ai1 - e.cx - e.vx;
293	      const dy = player.cy - 200 - e.cy - e.vy;
294	      const d = Math.hypot(dx, dy) || 1;
295	      e.vx = accelTo(e.vx, (dx / d) * DUKE.bubbleSpd, DUKE.bubbleAcc);
296	      e.vy = accelTo(e.vy, (dy / d) * DUKE.bubbleSpd, DUKE.bubbleAcc);
297	      if (e.ai2 === 0) game.playSfx('roar', 0.5);
298	      if (e.ai2 % DUKE.bubbleEvery === 0) { // :49610-49618 每 4t 吐一颗爆裂泡泡(NPC 371)
299	        const ddx = player.cx - e.cx, ddy = player.cy - e.cy;
300	        const dd = Math.hypot(ddx, ddy) || 1;
301	        const bub = spawnPart(game, e, 371);
302	        if (bub) {
303	          bub.x = e.cx + (ddx / dd) * ((e.w + 20) / 2) - bub.w / 2;
304	          bub.y = e.cy + (ddy / dd) * ((e.w + 20) / 2) + 45 - bub.h / 2;
305	        }
306	      }
307	      const s = Math.sign(player.cx - e.cx) || st.dir;
308	      st.dir = s; st.spr = -s;
309	      e.ai2 += 1;
310	      if (e.ai2 >= DUKE.bubbleT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
311	      break;
312	    }
313	    case 3: dukeSharknado(e, game, player, st, false); break;          // :49638-49660
314	    case 4: { // 一→二阶段变身(:49661-49679)
315	      invuln = true;
316	      e.vx *= 0.98;
317	      e.vy = lerp(e.vy, 0, 0.02);
318	      if (e.ai2 === DUKE.p1T - 60) game.playSfx('roar', 0.9);
319	      e.ai2 += 1;
320	      if (e.ai2 >= DUKE.p1T) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
321	      break;
322	    }
323	    case 5: { // 二阶段悬浮(:49680-49811)
324	      if (player.dead) break;
325	      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
326	      e.ai2 += 1;
327	      if (e.ai2 >= hoverT) {
328	        const next = dukePick2(e, enraged);
329	        if (next === 1) dukeCharge(e, player, chargeSpd, 6, st);
330	        else if (next === 2) { // 旋转泡泡冲刺起手(:49782-49797):20 速直冲
331	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
332	          const d = Math.hypot(dx, dy) || 1;
333	          e.vx = (dx / d) * DUKE.spinDashSpd;
334	          e.vy = (dy / d) * DUKE.spinDashSpd;
335	          e.spin = Math.atan2(e.vy, e.vx);
336	          const s = Math.sign(dx) || st.dir;
337	          st.dir = s;
338	          if (st.spr === 1) e.spin += Math.PI;
339	          st.spr = -s;
340	          e.ai0 = 7; e.ai1 = 0; e.ai2 = 0;
341	        } else if (next === 3) { e.ai0 = 8; e.ai1 = 0; e.ai2 = 0; }
342	        else if (next === 4) { e.ai0 = 9; e.ai1 = 0; e.ai2 = 0; } // expert
343	      }
344	      break;
345	    }
346	    case 6: { // 二阶段冲撞(:49812-49834)
347	      game.spawnParticles(e.cx, e.cy, '#8FD8FF', 2, 1.5, { life: 18 });
348	      e.ai2 += 1;
349	      if (e.ai2 >= chargeT) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; e.ai3 += 2; }
350	      break;
351	    }
352	    case 7: { // 旋转泡泡冲刺(:49835-49864)
353	      if (e.ai2 === 0) game.playSfx('roar', 0.6);
354	      if (e.ai2 % DUKE.spinEvery === 0) { // 每 4t 沿垂直方向甩一颗泡泡
355	        const vlen = Math.hypot(e.vx, e.vy) || 1;
356	        const bub = spawnPart(game, e, 371);
357	        if (bub) {
358	          bub.bInit = true; bub.ai0 = 0; bub.ai1 = 0;          // 预置初速,跳过自初始化
359	          bub.ai3 = (80 + Math.random() * 41) / 100;            // :49751 随机 scale
360	          bub.x = e.cx + (e.vx / vlen) * ((e.w + 20) / 2) - bub.w / 2;
361	          bub.y = e.cy + (e.vy / vlen) * ((e.w + 20) / 2) + 45 - bub.h / 2;
362	          const ang = Math.atan2(e.vy / vlen, e.vx / vlen) + (Math.PI / 2) * st.dir;
363	          bub.vx = Math.cos(ang) * DUKE.spinBubbleSpd;
364	          bub.vy = Math.sin(ang) * DUKE.spinBubbleSpd;
365	        }
366	      }
367	      // 速度/身体同步旋转(-num20*direction,:49854-49855)
368	      {
369	        const r = -DUKE_SPIN_RATE * st.dir;
370	        const cos = Math.cos(r), sin = Math.sin(r);
371	        const nvx = e.vx * cos - e.vy * sin, nvy = e.vx * sin + e.vy * cos;
372	        e.vx = nvx; e.vy = nvy;
373	        e.spin -= DUKE_SPIN_RATE * st.dir;
374	      }
375	      e.ai2 += 1;
376	      if (e.ai2 >= DUKE.spinT) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; }
377	      break;
378	    }
379	    case 8: dukeSharknado(e, game, player, st, true); break;           // :49865-49885
380	    case 9: { // expert 二段狂暴变身(:49886-49931;经典不可达,保留供 expert 接线)
381	      invuln = true;
382	      if (e.ai2 < DUKE.p2T - 90) e.spawnAlpha = clamp(e.spawnAlpha + (inSolid(game, e) ? 15 : -15), 0, 255);
383	      else e.spawnAlpha = Math.min(255, e.spawnAlpha + 4);
384	      e.vx *= 0.98;
385	      e.vy = lerp(e.vy, 0, 0.02);
386	      if (e.ai2 === DUKE.p2T - 60) game.playSfx('roar', 0.9);
387	      e.ai2 += 1;
388	      if (e.ai2 >= DUKE.p2T) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
389	      break;
390	    }
391	    case 10: { // expert 狂暴段悬浮(:49932-50018)
392	      if (player.dead) break;
393	      e.spawnAlpha = Math.min(255, e.spawnAlpha + 25); // 隐身逼近
394	      dukeHover(e, player, hoverAcc, hoverSpd, 360, st);
395	      e.ai2 += 1;
396	      if (e.ai2 >= hoverT) {
397	        const a3 = Math.floor(e.ai3);
398	        const next = (a3 === 0 || a3 === 2 || a3 === 3 || a3 === 5 || a3 === 6 || a3 === 7) ? 1 : 2;
399	        if (next === 1) dukeCharge(e, player, chargeSpd, 11, st);
400	        else { e.ai0 = 12; e.ai1 = 0; e.ai2 = 0; }
401	      }
402	      break;
403	    }
404	    case 11: { // expert 狂暴段冲撞(:50019-50047)
405	      e.spawnAlpha = Math.max(0, e.spawnAlpha - 25);
406	      game.spawnParticles(e.cx, e.cy, '#8FD8FF', 2, 1.5, { life: 18 });
407	      e.ai2 += 1;
408	      if (e.ai2 >= chargeT) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1; }
409	      break;
410	    }
411	    case 12: { // expert 瞬移爆冲(:50048-50107)
412	      invuln = true;
413	      e.spawnAlpha = Math.min(255, e.spawnAlpha + 17);
414	      e.vx *= 0.98;
415	      e.vy = lerp(e.vy, 0, 0.02);
416	      if (e.ai2 === DUKE.teleT / 2) { // :50066-50093 中点瞬移到玩家另一侧
417	        if (e.ai1 === 0) e.ai1 = 300 * Math.sign(e.cx - player.cx || 1);
418	        e.x = player.cx - e.ai1 - e.w / 2;
419	        e.y = player.cy - 200 - e.h / 2;
420	        const s = Math.sign(player.cx - e.cx) || st.dir;
421	        st.dir = s; st.spr = -s;
422	        game.spawnParticles(e.cx, e.cy, '#8FD8FF', 14, 2.4, { life: 30 });
423	        game.playSfx('roar', 0.6);
424	      }
425	      e.ai2 += 1;
426	      if (e.ai2 >= DUKE.teleT) {
427	        e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1;
428	        if (e.ai3 >= 9) e.ai3 = 0;
429	      }
430	      break;
431	    }
432	    case 13: { // expert 狂暴段旋转冲刺(:50108-50125;不吐泡泡)
433	      if (e.ai2 === 0) game.playSfx('roar', 0.6);
434	      {
435	        const r = -DUKE_SPIN_RATE * st.dir;
436	        const cos = Math.cos(r), sin = Math.sin(r);
437	        const nvx = e.vx * cos - e.vy * sin, nvy = e.vx * sin + e.vy * cos;
438	        e.vx = nvx; e.vy = nvy;
439	        e.spin -= DUKE_SPIN_RATE * st.dir;
440	      }
441	      e.ai2 += 1;
442	      if (e.ai2 >= DUKE.spinT) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1; }
443	      break;
444	    }
445	    default: break;
446	  }
447	  if (invuln) e.iframes = 2;
448	  e.facing = st.spr;
449	  e.x += e.vx;
450	  e.y += e.vy;
451	}
452	
453	/** 鲨鱼龙卷(状态 3 :49638-49660 / 状态 8 :49865-49885 共用):
454	 *  减速悬停,ai2==60 时发射龙卷水弹 proj 385(SharknadoBolt,原版伤害 0 的落地生成器)。
455	 *  简化:本工程无 385 落地生成龙卷+鲨鱼龙 372 寻的链,补一发 proj 407 直飞"鲨鱼"弹幕
456	 *  (伤害取 NPC 372 Sharkron 经典接触伤 100)近似龙卷出鲨。 */
457	function dukeSharknado(e: Enemy, game: GameHooks, player: Player, st: DukeX, big: boolean) {
458	  e.vx *= 0.98;
459	  e.vy = lerp(e.vy, 0, 0.02);
460	  if (e.ai2 === DUKE.nadoT - 30) {
461	    game.playSfx('roar', 0.7);
462	    if (big) {
463	      // 状态 8:原地一发(原版 ai0=1 即在自身处展开大龙卷,:49873-49876)
464	      shoot(game, e.cx, e.cy, 0, 2, 0, 385, 300);
465	    } else {
466	      // 状态 3:左右两发斜落(:49646-49651)
467	      shoot(game, e.cx, e.cy, st.dir * 2, 8, 0, 385, 300);
468	      shoot(game, e.cx, e.cy, -st.dir * 2, 8, 0, 385, 300);
469	    }
470	    // 鲨鱼弹幕(原版由龙卷持续生成 372;此为直飞近似)
471	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
472	    const d = Math.hypot(dx, dy) || 1;
473	    for (let k = -1; k <= 1; k++) {
474	      shoot(game, e.cx, e.cy, (dx / d) * 9 + k * 2.5, (dy / d) * 9 + k * 1.2, 100, 407, 300);
475	    }
476	  }
477	  e.ai2 += 1;
478	  if (e.ai2 >= DUKE.nadoT) { e.ai0 = big ? 5 : 0; e.ai1 = 0; e.ai2 = 0; }
479	}
480	
481	/** AI_070 爆裂泡泡(NPC 371,NPC.cs:35122-35195):
482	 *  朝玩家漂移(风偏+微上浮),玩家贴近(外扩 40px)或 150t 后爆炸(体积扩到 100×100,
483	 *  4t 后消散)。原版命中是 justHit→爆炸而非死亡;本工程近似为 hp 受损即转爆炸。
484	 *  简化:ai3 的随机 scale(:35134)无 Enemy 对应字段,仅记录不应用。 */
485	export function dukeBubbleAI(e: Enemy, game: GameHooks, player: Player | null) {
486	  void game;
487	  if (e.ai0 !== 1 && e.hp < e.maxHp) { e.ai0 = 1; e.ai1 = 4; e.hp = e.maxHp; } // justHit→爆
488	  if (!e.bInit && player) { // :35124-35131 初速 = 朝玩家 ±100px 随机偏移 × 11~17.7 速
489	    e.bInit = true;
490	    e.ai0 = 0; e.ai1 = 0;
491	    e.ai3 = (80 + Math.random() * 41) / 100;
492	    const jx = e.cx - player.cx + (Math.random() - 0.5) * 200;
493	    const jy = e.cy - player.cy + (Math.random() - 0.5) * 200;
494	    const d = Math.hypot(jx, jy) || 1;
495	    const spd = (165 + Math.random() * 100) / 15;
496	    e.vx = -(jx / d) * spd;
497	    e.vy = -(jy / d) * spd;
498	    e.alphaFade = false;
499	    e.spawnAlpha = 50; // :35136-35140
500	  }
501	  if (player) {
502	    // :35132-35133 主漂移:v = (v*40 + dir*20)/41
503	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
504	    const d = Math.hypot(dx, dy) || 1;
505	    e.vx = (e.vx * 40 + (dx / d) * 20) / 41;
506	    e.vy = (e.vy * 40 + (dy / d) * 20) / 41;
507	  }
508	  // :35141-35146 风扰+上浮(风取 0)
509	  e.vx = (e.vx * 50 + (Math.random() - 0.5) * 2) / 51;
510	  e.vy = (e.vy * 50 - 0.25 + (Math.random() - 0.5) * 4) / 51;
511	  if (e.vy > 0) e.vy -= 0.04;
512	  if (e.ai0 === 0 && player) { // :35147-35175 玩家贴近 → 爆炸
513	    const pad = 40 + e.w / 2;
514	    if (Math.abs(player.cx - e.cx) < pad + player.w / 2 && Math.abs(player.cy - e.cy) < pad + player.h / 2) {
515	      e.ai0 = 1; e.ai1 = 4;
516	    }
517	  }
518	  if (e.ai0 === 0) {
519	    e.ai1 += 1;
520	    if (e.ai1 >= 150) { e.ai0 = 1; e.ai1 = 4; } // :35167-35175 超时自爆
521	  } else {
522	    // 爆炸:体积扩到 100×100(:35187-35193)并 4t 后消散
523	    if (e.w !== 100) {
524	      e.x = e.cx - 50; e.y = e.cy - 50;
525	      e.w = 100; e.h = 100;
526	      game.spawnParticles(e.cx, e.cy, '#BFE8FF', 8, 2, { life: 20 });
527	    }
528	    e.iframes = 2; // dontTakeDamage
529	    e.ai1 -= 1;
530	    if (e.ai1 <= 0) { e.dead = true; return; }
531	  }
532	  e.x += e.vx;
533	  e.y += e.vy;
534	}
535	
536	// ---------------------------------------------------------------------------
537	// 月亮领主 aiStyle 77 核心(NPC 398,NPC.cs:36774-37198)
538	// ---------------------------------------------------------------------------
539	// ai0:-1 出生演出(60t,生成 2×397 手 + 1×396 头)→ 0 一阶段(双手+头存活期间无敌,随玩家悬停)
540	//   → 1 二阶段(三部件全部闭眼(ai0=-2)后解除无敌,自主追玩家+弹幕循环)
541	//   → 2 死亡演出(600t 后真死,全族消散)/ 3 玩家全灭离场(60t 后全族清除)。
542	//   -2:远距(>2400px)传送归位后的短演出。
543	
544	/** 二阶段弹幕表 = MoonLordAttacksArray2(:6966-6985,10 槽循环)。
545	 *  原版该表驱动 NPC 400 真眼(aiStyle 81,:38243-38264);真眼不在本次范围,
546	 *  攻击主链折叠到核心上执行(投射物 id/伤害取自 78/79/81 的原版发射调用)。 */
547	const ML_CORE_P2: ReadonlyArray<readonly [number, number]> = [
548	  [0, 90], [1, 90], [0, 90], [2, 135], [0, 90], [3, 200], [0, 90], [4, 375], [0, 90], [2, 135],
549	];
550	
551	/** 朝玩家发射一发弹幕的通用出口(伤害/弹 id 全部来自原版 NewProjectile 调用点) */
552	function mlShoot(e: Enemy, game: GameHooks, player: Player, ox: number, oy: number,
553	  spd: number, dmg: number, projId: number) {
554	  const dx = player.cx - (e.cx + ox), dy = player.cy - (e.cy + oy);
555	  const d = Math.hypot(dx, dy) || 1;
556	  shoot(game, e.cx + ox, e.cy + oy, (dx / d) * spd, (dy / d) * spd, dmg, projId, 600);
557	}
558	
559	/** 核心悬停移动(:36854-36865 / :36912-36923 同构):目标 = 玩家 + (0,130),8 速/0.5 步进+半程混合 */
560	function mlCoreHover(e: Enemy, player: Player) {
561	  const dx = player.cx - e.cx;
562	  const dy = player.cy + 130 - e.cy;
563	  if (Math.hypot(dx, dy) > 20) {
564	    const d = Math.hypot(dx - e.vx, dy - e.vy) || 1;
565	    flyLerp(e, ((dx - e.vx) / d) * 8, ((dy - e.vy) / d) * 8, 0.5);
566	  }
567	}
568	
569	export function moonLordCoreAI(e: Enemy, game: GameHooks, player: Player | null) {
570	  if (!e.bInit) { e.bInit = true; e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; } // :36780-36785
571	  // 原版 checkDead(:78859-78867):血尽 → ai0=2 死亡演出,满血续命 600t 后真死
572	  if (e.hp <= 0 && e.ai0 !== 2) { e.ai0 = 2; e.ai1 = 0; e.hp = e.maxHp; e.iframes = 2; }
573	
574	  if (e.ai0 === -2) { // 远距传送归位(:36786-36809)
575	    e.iframes = 2;
576	    e.ai1 += 1;
577	    if (e.ai1 >= 60) { e.ai1 = 0; e.ai0 = 0; }
578	  } else if (e.ai0 === -1) { // 出生演出(:36810-36853)
579	    e.iframes = 2;
580	    e.ai1 += 1;
581	    if (e.ai1 >= 60) {
582	      e.ai1 = 0; e.ai0 = 0; e.ai2 = 0;
583	      // 生成双手 397(核心两侧 ±400)与头 396(上方 400);ai3 = 核心 id(锚定)
584	      for (let i = 0; i < 2; i++) {
585	        const h = spawnPart(game, e, 397);
586	        if (h) {
587	          h.x = e.cx + i * 800 - 400 - h.w / 2;
588	          h.y = e.cy - 100 - h.h / 2;
589	          h.ai0 = 0; h.ai1 = 0; h.ai2 = i; h.ai3 = e.id; h.bInit = true;
590	        }
591	      }
592	      const hd = spawnPart(game, e, 396);
593	      if (hd) {
594	        hd.x = e.cx - hd.w / 2;
595	        hd.y = e.cy - 400 - hd.h / 2;
596	        hd.ai0 = 0; hd.ai1 = 0; hd.ai2 = 0; hd.ai3 = e.id; hd.bInit = true;
597	      }
598	      game.playSfx('roar', 1);
599	    }
600	  } else if (e.ai0 === 0 || e.ai0 === 1) {
601	    // 三部件(锚定本核心)
602	    const parts = (game.enemies() as Enemy[]).filter(
603	      (n) => !n.dead && (n.vanillaId === 396 || n.vanillaId === 397) && n.ai3 === e.id);
604	    if (e.ai0 === 0) {
605	      e.iframes = 2; // dontTakeDamage(:36856)
606	      // 部件缺失 → 核心即毁(:36866-36890 flag84)
607	      if (parts.length < 3) { e.dead = true; return; }
608	      // 三部件全部闭眼残肢(ai0=-2)→ 解除无敌进二阶段(:36891-36909 flag85)
609	      if (parts.every((p) => p.ai0 === -2)) { e.ai0 = 1; e.ai1 = 0; }
610	    }
611	    if (player) mlCoreHover(e, player);
612	    if (e.ai0 === 1 && player) mlCoreBarrage(e, game, player); // 二阶段弹幕(真眼主链折叠)
613	  } else if (e.ai0 === 2) { // 死亡演出(:36925-37064)
614	    e.iframes = 2;
615	    e.vx = lerp(e.vx, 0, 0.02);
616	    e.vy = lerp(e.vy, -0.5, 0.02);
617	    e.ai1 += 1;
618	    // :36954-37022 每 3t 一簇爆炎(60t<ai1<580);:37049 起声效/光效略
619	    if (e.ai1 % 3 === 0 && e.ai1 > 60 && e.ai1 < 580) {
620	      game.spawnParticles(
621	        e.cx + (Math.random() - 0.5) * 400, e.cy + (Math.random() - 0.5) * 400,
622	        '#C04030', 6, 3, { life: 30 });
623	    }
624	    if (e.ai1 >= 600) { // :37053-37063 真死 → 全族由各部件 AI 检测 core.dead 自毁
625	      e.dead = true;
626	      return;
627	    }
628	  } else if (e.ai0 === 3) { // 玩家全灭离场(:37065-37135)
629	    e.iframes = 2;
630	    e.vx = lerp(e.vx, e.facing, 0.02);
631	    e.vy = lerp(e.vy, -0.5, 0.02);
632	    e.ai1 += 1;
633	    if (e.ai1 >= 60) { // :37109-37127 清除全部部件与自身
634	      for (const n of game.enemies() as Enemy[]) {
635	        if (!n.dead && (n.vanillaId === 396 || n.vanillaId === 397 || n.vanillaId === 400) && n.ai3 === e.id) n.dead = true;
636	      }
637	      e.dead = true;
638	      return;
639	    }
640	  }
641	
642	  // 玩家全灭 → 离场(:37136-37161)
643	  if (!player && e.ai0 !== -1 && e.ai0 !== -2 && e.ai0 !== 2 && e.ai0 !== 3) { e.ai0 = 3; e.ai1 = 0; }
644	  // 玩家远距 >2400px → 全族瞬移归位(:37162-37197)
645	  if (player && e.ai0 >= 0 && e.ai0 < 2 && Math.hypot(player.cx - e.cx, player.cy - e.cy) > 2400) {
646	    const dx = player.cx - e.cx;
647	    const dy = player.cy - 150 - e.cy;
648	    e.x += dx; e.y += dy;
649	    for (const n of game.enemies() as Enemy[]) {
650	      if (!n.dead && (n.vanillaId === 396 || n.vanillaId === 397 || n.vanillaId === 400) && n.ai3 === e.id) {
651	        n.x += dx; n.y += dy;
652	      }
653	    }
654	    e.ai0 = -2; e.ai1 = 0;
655	  }
656	  e.x += e.vx;
657	  e.y += e.vy;
658	}
659	
660	/** 核心二阶段弹幕(原版 NPC 400 真眼攻击链,aiStyle 81 :38347-38600;
661	 *  投射物/伤害取原版调用点:462 PhantasmalBolt 35(:38382)、454 PhantasmalSphere 40(:38455)、
662	 *  455 PhantasmalDeathray 75(:37913)、452 PhantasmalEye 30(:37333)) */
663	function mlCoreBarrage(e: Enemy, game: GameHooks, player: Player) {
664	  const { atk, inSlot, dur } = attackSlot(e, ML_CORE_P2);
665	  switch (atk) {
666	    case 1: // 幻影之眼 452×4 扇形(:37326-37334)
667	      if (inSlot === 0) {
668	        for (let k = -1.5; k <= 1.5; k++) {
669	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
670	          const d = Math.hypot(dx, dy) || 1;
671	          const ang = Math.atan2(dy, dx) + k * 0.35;
672	          shoot(game, e.cx, e.cy, Math.cos(ang) * 8, Math.sin(ang) * 8, 30, 452, 600);
673	        }
674	      }
675	      break;
676	    case 2: // 幻影能量球 454:先慢速散出,后段朝玩家加速(原版 30t 后转向寻的,:38447-38456/:38475)
677	      if (inSlot === 0) {
678	        for (let k = 0; k < 3; k++) {
679	          const ang = -Math.PI / 2 + (k - 1) * 0.6;
680	          shoot(game, e.cx, e.cy, Math.cos(ang) * 4, Math.sin(ang) * 4, 40, 454, 600);
681	        }
682	      } else if (inSlot === 60) {
683	        for (let k = -1; k <= 1; k++) mlShoot(e, game, player, 0, 0, 12, 40, 454);
684	      }
685	      break;
686	    case 3: // 三连幻影矢 462(:38378-38383,slot 末 14/7/0 三发)
687	      if (inSlot === dur - 14 || inSlot === dur - 7 || inSlot === dur) {
688	        mlShoot(e, game, player, 0, 0, 8, 35, 462);
689	      }
690	      break;
691	    case 4: // 死亡之光 455(原版为持续扫射激光;直飞弹近似)
692	      if (inSlot === 0 || inSlot === 120 || inSlot === 240) {
693	        mlShoot(e, game, player, 0, 0, 7, 75, 455);
694	      }
695	      break;
696	    default: break; // 0 = 闭眼冷却 90t
697	  }
698	}
699	
700	// ---------------------------------------------------------------------------
701	// 月亮领主 aiStyle 78 手(NPC 397,NPC.cs:37199-37711)
702	// ---------------------------------------------------------------------------
703	// 攻击时间表 MoonLordAttacksArray[0, ai2](:6854-6883):
704	//   ai2=0(左手,side=-1):[闭50, 眼70, 球330, 闭60, 矢90]
705	//   ai2=1(右手,side=+1):[眼70, 闭50, 矢90, 闭60, 球330]
706	// 攻击:0 闭眼悬停(无敌)/ 1 眼球环射 452(30 伤)/ 2 能量球扫射 454(40 伤,末段全数转向玩家)
707	//   / 3 三连幻影矢 462(30 伤,预判 20t)。
708	// 无敌语义:dontTakeDamage = frame>=21(:37215)——只有攻击中(睁眼)可受击。
709	
710	const ML_HAND_ATTACKS: Readonly<Record<number, ReadonlyArray<readonly [number, number]>>> = {
711	  0: [[0, 50], [1, 70], [2, 330], [0, 60], [3, 90]],
712	  1: [[1, 70], [0, 50], [3, 90], [0, 60], [2, 330]],
713	};
714	
715	export function moonLordHandAI(e: Enemy, game: GameHooks, player: Player | null) {
716	  // 锚定核心;核心缺失/死亡 → 自毁(:37202-37207)
717	  const core = (game.enemies() as Enemy[]).find((n) => n.id === e.ai3 && n.vanillaId === 398);
718	  if (!core || core.dead) { e.dead = true; return; }
719	  // 原版 checkDead(:78845-78857):血尽 → ai0=-2 闭眼残肢(满血续命+无敌)+召真眼(此处折叠为核心弹幕)
720	  if (e.hp <= 0 && e.ai0 !== -2) { e.ai0 = -2; e.ai1 = 0; e.hp = e.maxHp; e.iframes = 2; }
721	
722	  const x = handOf(e);
723	  const side = e.ai2 === 0 ? -1 : 1;  // num1231 :37208-37210
724	  e.facing = side;                    // spriteDirection
725	
726	  // 攻击表推进(:37221-37251;ai0=-2 残肢态不参与调度)
727	  let inSlot = 0, dur = 0;
728	  if (e.ai0 !== -2) {
729	    e.ai1 += 1;
730	    const s = attackSlot(e, ML_HAND_ATTACKS[e.ai2 === 0 ? 0 : 1]);
731	    e.ai0 = s.atk; // :37245 原版 ai[0] 即攻击号(亦为手部状态)
732	    inSlot = s.inSlot; dur = s.dur;
733	  }
734	  let frameT = 0; // num1234(帧目标=frameT*7)
735	
736	  if (e.ai0 === -2) { // 闭眼残肢(:37252-37280)
737	    frameT = 0;
738	    e.def.damage = 80; // :37254
739	    if (e.ai1 >= 32) e.ai1 = 0;
740	    handHover(e, core, side);
741	  } else if (e.ai0 === 0) { // 闭眼悬停(:37281-37303)
742	    frameT = 3;
743	    x.l1 = Math.max(0, x.l1 - 0.05);
744	    handHover(e, core, side);
745	  } else if (e.ai0 === 1 && player) { // 眼球环射(:37304-37346)
746	    frameT = 0;
747	    const cyc = 28; // num1240*num1241 = 7*4
748	    if (inSlot >= cyc * 2) {
749	      x.l1 = Math.max(0, x.l1 - 0.07);
750	    } else if (inSlot >= cyc) {
751	      x.l1 = Math.min(0.75, x.l1 + 0.05);
752	      const ang = (TAU * (inSlot % cyc)) / cyc - Math.PI / 2; // :37324
753	      x.l0 = Math.atan2(Math.sin(ang) * 66, Math.cos(ang) * 30);
754	      if (inSlot % 4 === 0) handFireEye(e, game, x, side); // :37326-37334 452(30 伤)
755	    } else {
756	      x.l1 = Math.min(0.75, x.l1 + 0.02);
757	      const ang = (TAU * (inSlot % cyc)) / cyc - Math.PI / 2;
758	      x.l0 = Math.atan2(Math.sin(ang) * 66, Math.cos(ang) * 30);
759	    }
760	  } else if (e.ai0 === 2) { // 能量球扫射(:37347-37447)
761	    const ax = core.cx + 220 * side + side * 100;   // vector168
762	    const ay = core.cy - 60 - 50;
763	    const swx = 400 * side, swy = -60;              // vector169
764	    if (inSlot < 30) {
765	      handApproach(e, ax, ay, 8, 0.2);
766	    } else if (inSlot < 210) {
767	      frameT = 1;
768	      if ((inSlot - 30) % 30 === 0 && player) { // :37372-37380 每 30t 一发 454(40 伤)
769	        const k = Math.floor((inSlot - 30) / 30);
770	        let vx = 5 * side + (k - 3.5) * side * 3;
771	        let vy = -8 + (k - 4.5);
772	        vx *= 1.2; vy *= 1.2;
773	        shoot(game, e.cx, e.cy, vx, vy, 40, 454, 600);
774	      }
775	      const t = smoothAmt((inSlot - 30) / 180);
776	      handSeek(e, ax + swx * t, ay + swy * t, 20, 0.5); // :37381-37387
777	    } else if (inSlot < 282) {
778	      frameT = 0;
779	      e.vx *= 0.9; e.vy *= 0.9;
780	    } else if (inSlot < 287) {
781	      frameT = 1;
782	      e.vx *= 0.9; e.vy *= 0.9;
783	    } else if (inSlot < 292) {
784	      frameT = 2;
785	      e.vx *= 0.9; e.vy *= 0.9;
786	    } else if (inSlot < 300) {
787	      frameT = 3;
788	      // :37407-37427 原版在此把本手全部 454 弹转向玩家(12 速);本工程投射物无寻的,
789	      // 近似为朝玩家补射 6 发 454(40 伤)
790	      if (inSlot === 292 && player) {
791	        for (let k = 0; k < 6; k++) {
792	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
793	          const d = Math.hypot(dx, dy) || 1;
794	          const ang = Math.atan2(dy, dx) + (k - 2.5) * 0.18;
795	          shoot(game, e.cx, e.cy, Math.cos(ang) * 12, Math.sin(ang) * 12, 40, 454, 600);
796	        }
797	      }
798	      const t = 1 - (inSlot - 270) / 30;
799	      handSeek(e, ax + swx * smoothAmt(t), ay + swy * smoothAmt(t), 14, 0.1); // :37428-37434
800	    } else {
801	      frameT = 3;
802	      handApproach(e, ax, ay, 8, 0.2); // :37436-37446 归位
803	    }
804	  } else if (e.ai0 === 3 && player) { // 三连幻影矢(:37448-37472)
805	    frameT = 0;
806	    const pvx = (player as unknown as { vx: number }).vx ?? 0;
807	    const pvy = (player as unknown as { vy: number }).vy ?? 0;
808	    const dx = player.cx + pvx * 20 - e.cx, dy = player.cy + pvy * 20 - e.cy; // :37455 预判 20t
809	    x.l0 = angleLerp(x.l0, Math.atan2(dy, dx), 0.5);
810	    x.l1 = Math.min(1, x.l1 + 0.05);
811	    if (inSlot === dur - 35) game.playSfx('roar', 0.5); // :37462-37465
812	    if (inSlot === dur - 14 || inSlot === dur - 7 || inSlot === dur) {
813	      // :37466-37471 从眼球位置射 462(30 伤,8 速)
814	      const exx = Math.cos(x.l0) * 30 * x.l1, eyy = Math.sin(x.l0) * 66 * x.l1;
815	      const d = Math.hypot(dx, dy) || 1;
816	      shoot(game, e.cx + exx, e.cy + eyy, (dx / d) * 8, (dy / d) * 8, 30, 462, 600);
817	    }
818	  }
819	
820	  // 睁闭眼帧推进(:37493-37509):每 tick 向目标帧走 1,dontTakeDamage = frame>=21
821	  const frameTarget = frameT * 7;
822	  if (frameTarget > x.frame) x.frame += 1;
823	  else if (frameTarget < x.frame) x.frame -= 1;
824	  x.frame = clamp(x.frame, 0, 21);
825	
826	  // 位置钳制(:37473-37492):下一位置锁在核心侧上方盒内
827	  let minX = core.cx + 220 * side + 110 * side, minY = core.cy - 60 - 150;
828	  let maxX = minX + 370 * side, maxY = minY + 150;
829	  if (minX > maxX) { const t = minX; minX = maxX; maxX = t; }
830	  if (minY > maxY) { const t = minY; minY = maxY; maxY = t; }
831	  const nx = clamp(e.cx + e.vx, minX, maxX);
832	  const ny = clamp(e.cy + e.vy, minY, maxY);
833	  e.x = nx - e.w / 2;
834	  e.y = ny - e.h / 2;
835	
836	  // 无敌:闭眼(frame>=21)或残肢态;可受击时不写 iframes,保留 hurt() 的 8t 受击免疫
837	  if (x.frame >= 21 || e.ai0 === -2) e.iframes = 2;
838	  e.spin = x.l0; // 手部眼球角度(渲染朝向)
839	}
840	
841	/** 手部悬停(:37266-37279 / :37289-37302):核心侧上方 (350*side, -100),6 速/0.3 步进+半程混合 */
842	function handHover(e: Enemy, core: Enemy, side: number) {
843	  const dx = core.cx + 350 * side - e.cx;
844	  const dy = core.cy - 100 - e.cy;
845	  const d = Math.hypot(dx, dy);
846	  if (d > 20) flyLerp(e, (dx / d) * 6, (dy / d) * 6, 0.3);
847	}
848	/** SmoothStep 趋近(:37358-37367 / :37438-37445):velocity = SmoothStep(v, normalize(delta)*min(spd,|delta|), k) */
849	function handApproach(e: Enemy, tx: number, ty: number, spd: number, k: number) {
850	  const dx = tx - e.cx, dy = ty - e.cy;
851	  const d = Math.hypot(dx, dy);
852	  if (d < 0.01) return;
853	  const m = Math.min(spd, d);
854	  e.vx = vSmoothStep(e.vx, (dx / d) * m, k);
855	  e.vy = vSmoothStep(e.vy, (dy / d) * m, k);
856	}
857	/** 扫射段追随(:37381-37387 / :37428-37434):Lerp(v, normalize(delta)*min(spd,|delta|), k) */
858	function handSeek(e: Enemy, tx: number, ty: number, spd: number, k: number) {
859	  const dx = tx - e.cx, dy = ty - e.cy;
860	  const d = Math.hypot(dx, dy);
861	  if (d < 0.01) return;
862	  e.vx = lerp(e.vx, (dx / d) * Math.min(spd, d), k);
863	  e.vy = lerp(e.vy, (dy / d) * Math.min(spd, d), k);
864	}
865	/** 眼球环射一发 452(:37326-37334):从眼球椭圆外沿射出,沿眼球朝向 8 速,30 伤 */
866	function handFireEye(e: Enemy, game: GameHooks, x: HandX, side: number) {
867	  const exx = Math.cos(x.l0) * 30 * x.l1, eyy = Math.sin(x.l0) * 66 * x.l1;
868	  const d = Math.hypot(exx, eyy) || 1;
869	  const px = e.cx + (exx / d) * 72.46 * 0.4 - side; // |vector159|=√(30²+66²)≈72.46(:37330)
870	  const py = e.cy + (eyy / d) * 72.46 * 0.4 + 3;
871	  shoot(game, px, py, (exx / d) * 8, (eyy / d) * 8, 30, 452, 600);
872	}
873	
874	// ---------------------------------------------------------------------------
875	// 月亮领主 aiStyle 79 头(NPC 396,NPC.cs:37712-38128)
876	// ---------------------------------------------------------------------------
877	// 恒定悬停在核心正上方 400px(无自主移动);攻击表 MoonLordAttacksArray[0,2](:6874-6883):
878	//   [矢180, 闭30, 吸血435, 矢180, 光375]。
879	// 攻击:0 睁眼瞄准(无敌)/ 1 死亡之光 455(75 伤,:37902-37916)/ 2 月噬 456(0 伤,:37957-37973)
880	//   / 3 三连幻影矢 462(30 伤,:37991-38015)。-2 闭眼残肢(80 接触伤)/ -3 核心死亡后永闭。
881	// 无敌语义:dontTakeDamage = localAI[3]>=15(:37724)。
882	
883	const ML_HEAD_ATTACKS: ReadonlyArray<readonly [number, number]> = [
884	  [3, 180], [0, 30], [2, 435], [3, 180], [1, 375],
885	];
886	
887	export function moonLordHeadAI(e: Enemy, game: GameHooks, player: Player | null) {
888	  const core = (game.enemies() as Enemy[]).find((n) => n.id === e.ai3 && n.vanillaId === 398);
889	  if (!core || core.dead) { e.dead = true; return; } // :37714-37719
890	  // checkDead(:78845-78857)同手:血尽 → ai0=-2 闭眼残肢
891	  if (e.hp <= 0 && e.ai0 !== -2 && e.ai0 !== -3) { e.ai0 = -2; e.ai1 = 0; e.ai2 = 0; e.hp = e.maxHp; e.iframes = 2; }
892	
893	  const x = headOf(e);
894	  e.vx = 0; e.vy = 0; // :37725
895	  e.x = core.cx - e.w / 2; // :37726 恒定在核心上方 400px
896	  e.y = core.cy - 400 - e.h / 2;
897	
898	  // 攻击表推进(:37732-37762;ai0<0 不参与)
899	  let inSlot = 0, dur = 0;
900	  if (e.ai0 >= 0) {
901	    e.ai1 += 1;
902	    const s = attackSlot(e, ML_HEAD_ATTACKS);
903	    e.ai0 = s.atk; // :37756 原版 ai[0] 即攻击号(亦为头部状态)
904	    inSlot = s.inSlot; dur = s.dur;
905	  }
906	  let f2T = 0, f3T = 0; // num1262/num1263(帧目标 = f2T*7 / f3T*5)
907	
908	  if (e.ai0 === -3) { // 核心死亡后永闭(:37763-37781;由 -2 分支转入 :37784-37788)
909	    e.def.damage = 0;
910	    e.spin = lerp(e.spin, Math.PI / 12, 0.07);
911	    if (e.ai1 >= 32) e.ai1 = 0;
912	    if (x.f2 < 14) x.f2 += 1;
913	    e.iframes = 2;
914	    return;
915	  }
916	  if (e.ai0 === -2) { // 闭眼残肢(:37782-37844)
917	    if (core.ai0 === 2) { e.ai0 = -3; return; } // :37784-37788
918	    e.def.damage = 80;
919	    e.iframes = 2;
920	    if (e.ai1 >= 32) e.ai1 = 0;
921	    e.ai2 += 1;
922	    if (e.ai2 >= 555) e.ai2 = 0;
923	    if (e.ai2 >= 120 && player) { // :37805-37843 残肢期月噬循环
924	      const lt = e.ai2 - 120;
925	      if (lt === 0) { // :37811-37827 从额前 216px 发月噬 456(0 伤,纯吸血视觉)
926	        const dx = player.cx - e.cx, dy = player.cy - (e.cy + 216);
927	        const d = Math.hypot(dx, dy) || 1;
928	        shoot(game, e.cx, e.cy + 216, (dx / d) * 6, (dy / d) * 6, 0, 456, 600);
929	      }
930	      // :37828-37842 原版在 lt=120/180/240 于玩家处召 401 月噬怪;不在本次范围,略
931	    }
932	    return;
933	  }
934	
935	  if (e.ai0 === 0 && player) { // 睁眼瞄准(:37845-37864)
936	    f3T = 3;
937	    const dx = player.cx - e.cx, dy = player.cy + 22 - e.cy;
938	    const d = Math.hypot(dx, dy) || 1;
939	    x.l0 = Math.atan2(dy, dx);
940	    x.l1 = Math.min(1, Math.max(0, (1 - Math.min(1, d / 500)) * 2)); // :37850-37860
941	    x.l2 = lerp(x.l2, 1, 0.2);
942	  } else if (e.ai0 === 1 && player) { // 死亡之光(:37865-37952)
943	    if (inSlot < 180) {
944	      x.l1 = Math.max(0, x.l1 - 0.05);
945	      if (inSlot >= 60) { // :37876-37898 聚能尘
946	        game.spawnParticles(
947	          e.cx + (Math.random() - 0.5) * 27, e.cy + (Math.random() - 0.5) * 59, '#B040C0', 2, 1.2, { life: 24 });
948	      }
949	    } else if (inSlot < dur - 15) {
950	      // :37902-37916 原版发射 455 死亡之光(75 伤)并以 2π/540 每t 扫射;
951	      // 本工程投射物无持续扫射,按发射方向(∓60° 预偏)直飞近似,逐t 扫射略
952	      if (inSlot === 180) {
953	        const dx = player.cx - e.cx, dy = player.cy - e.cy;
954	        const d = Math.hypot(dx, dy) || 1;
955	        const n = dx / d < 0 ? 1 : -1; // num1278
956	        const ang = Math.atan2(dy, dx) - n * (TAU / 6);
957	        shoot(game, e.cx, e.cy, Math.cos(ang) * 9, Math.sin(ang) * 9, 75, 455, 600);
958	        game.playSfx('roar', 0.8);
959	      }
960	      x.l1 = Math.min(1, x.l1 + 0.05);
961	    } else {
962	      f3T = 3;
963	      x.l1 = Math.max(0, x.l1 - 0.07);
964	    }
965	  } else if (e.ai0 === 2) { // 月噬(:37953-37990)
966	    f2T = 2;
967	    f3T = 3;
968	    if (inSlot === 0 && player) { // :37958-37973 额前 216px 朝玩家月噬 456(0 伤)
969	      const dx = player.cx - e.cx, dy = player.cy - (e.cy + 216);
970	      const d = Math.hypot(dx, dy) || 1;
971	      shoot(game, e.cx, e.cy + 216, (dx / d) * 6, (dy / d) * 6, 0, 456, 600);
972	    }
973	    // :37975-37989 原版在 inSlot=120/180/240 召 401;不在本次范围,略
974	  } else if (e.ai0 === 3 && player) { // 三连幻影矢(:37991-38015)
975	    const pvx = (player as unknown as { vx: number }).vx ?? 0;
976	    const pvy = (player as unknown as { vy: number }).vy ?? 0;
977	    const dx = player.cx + pvx * 20 - e.cx, dy = player.cy + pvy * 20 - e.cy;
978	    x.l0 = angleLerp(x.l0, Math.atan2(dy, dx), 0.5);
979	    x.l1 = Math.min(1, x.l1 + 0.05);
980	    if (inSlot === dur - 35) game.playSfx('roar', 0.5);
981	    if (inSlot === dur - 14 || inSlot === dur - 7 || inSlot === dur) {
982	      // 眼球椭圆 (27,59)(:37727 vector200),8 速 30 伤
983	      const exx = Math.cos(x.l0) * 27 * x.l1, eyy = Math.sin(x.l0) * 59 * x.l1;
984	      const d = Math.hypot(dx, dy) || 1;
985	      shoot(game, e.cx + exx, e.cy + eyy, (dx / d) * 8, (dy / d) * 8, 30, 462, 600);
986	    }
987	  }
988	
989	  // 帧推进(:38016-38049;注:原版 :38042-38048 钳制误写 localAI[2],此处按语义钳 [3])
990	  const f2Target = f2T * 7, f3Target = f3T * 5;
991	  if (f2Target > x.f2) x.f2 += 1; else if (f2Target < x.f2) x.f2 -= 1;
992	  x.f2 = clamp(x.f2, 0, 14);
993	  if (f3Target > x.f3) x.f3 += 1; else if (f3Target < x.f3) x.f3 -= 1;
994	  x.f3 = clamp(x.f3, 0, 15);
995	  if (x.f3 >= 15) e.iframes = 2; // dontTakeDamage = localAI[3]>=15(闭眼无敌)
996	  e.spin = x.l0;
997	}
998	

```


---

## 🤖 Assistant · 2026-08-10T06:46:11.735Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the _mechprobe.mts for the probe template, plus Enemy.ts to understand Enemy fields (fromVanilla, aiT, etc.).
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:46:11.736Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/_mechprobe.mts"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:11.744Z

**📎 ToolResult**

```
1	// 机械三王冒烟:双子 125/126、Prime 127+4 部件、毁灭者 134+80 段链
2	import { Enemy } from '../src/entities/Enemy.ts';
3	import { TileStore } from '../src/world/TileStore.ts';
4	import { World } from '../src/world/World.ts';
5	
6	const st = new TileStore(200, 300);
7	const world = new World(200, 300, 1, 't');
8	world.store = st;
9	world.groundLevel = 60;
10	world.rockLevel = 190;
11	for (let x = 0; x < 200; x++) st.setTileSilent(x, 150, 1); // 地板
12	const enemies: Enemy[] = [];
13	const projectiles: unknown[] = [];
14	const game = {
15	  world,
16	  player: { cx: 100 * 16, cy: 140 * 16, x: 100 * 16 - 10, y: 140 * 16, w: 20, h: 42, dead: false } as never,
17	  enemies: () => enemies,
18	  spawnDrop: () => null, damagePlayer: () => {}, addDamageNumber: () => {}, cutTile: () => {},
19	  onEnemyKilled: () => {}, spawnEnemy: () => {}, notifyInventoryChanged: () => {}, showPickupLabel: () => {},
20	  spawnParticles: () => {}, playSfx: () => {}, playSfxFiles: () => {},
21	  entities: (() => {
22	    const wrap = {
23	      nextId: 2,
24	      add: (e: Enemy, b?: string) => {
25	        e.id = wrap.nextId++;
26	        if (b === 'projectiles') projectiles.push(e); else enemies.push(e);
27	      },
28	    };
29	    return wrap;
30	  })(),
31	} as never;
32	let ok = 0, bad = 0;
33	const check = (n: string, c: boolean, x?: unknown) => { if (c) { ok++; console.log('  ✓ ' + n); } else { bad++; console.log('  ✗ ' + n, x ?? ''); } };
34	const run = (ticks: number) => { for (let i = 0; i < ticks; i++) for (const e of [...enemies]) e.fixedUpdate(1 / 60, game); };
35	world.clock.timeOfDay = 0.0; // 夜晚
36	
37	// 1) 双子 125(雷神之眼)
38	console.log('== Twins 125 ==');
39	{
40	  enemies.length = 0; projectiles.length = 0;
41	  const twin = Enemy.fromVanilla(125, 100 * 16, 80 * 16)!;
42	  twin.id = 1; enemies.push(twin);
43	  run(1);
44	  check('初始化 ai0=0', twin.ai0 === 0, twin.ai0);
45	  run(300);
46	  check('悬浮靠拢玩家上方', Math.abs(twin.cx - 100 * 16) < 500 && twin.cy < 140 * 16, [Math.round(twin.cx / 16), Math.round(twin.cy / 16)]);
47	  check('悬浮态 ai1=0', twin.ai1 === 0, twin.ai1);
48	  twin.ai2 = 599;
49	  run(1);
50	  check('600t 切冲撞', twin.ai1 === 1, twin.ai1);
51	  run(300); // 一阶段 4 连冲(每轮 1+70t),300t 后应回悬浮
52	  check('4 连冲后回悬浮', twin.ai1 === 0, [twin.ai1, twin.ai3]); // ai3=悬浮弹幕计数(原版 ai[3] 双用,合法)
53	  check('旋转角有值', Math.abs(twin.spin) > 0.01, twin.spin.toFixed(2));
54	  // 打到 40% 以下 → 变身(各 100t)→ 三阶段
55	  twin.hp = twin.maxHp * 0.3;
56	  run(220);
57	  check('变身进三阶段 ai0=3', twin.ai0 === 3, twin.ai0);
58	  check('三阶段伤害×1.5', twin.def.damage === Math.round(Enemy.fromVanilla(125, 0, 0)!.def.damage * 1.5), twin.def.damage);
59	  const before = projectiles.length;
60	  run(200);
61	  check('三阶段发射激光', projectiles.length > before, projectiles.length);
62	}
63	// 2) 魔神之眼 126
64	console.log('== Twins 126 ==');
65	{
66	  enemies.length = 0; projectiles.length = 0;
67	  const spaz = Enemy.fromVanilla(126, 100 * 16, 80 * 16)!;
68	  spaz.id = 1; enemies.push(spaz);
69	  run(400);
70	  check('悬浮移动/存活', !spaz.dead && Math.abs(spaz.vx) + Math.abs(spaz.vy) > 0.01, [spaz.vx.toFixed(2), spaz.vy.toFixed(2)]);
71	  spaz.hp = spaz.maxHp * 0.3;
72	  run(220);
73	  check('变身进三阶段', spaz.ai0 === 3, spaz.ai0);
74	  const before = projectiles.length;
75	  run(100);
76	  check('三阶段火焰弹幕', projectiles.length > before, projectiles.length);
77	}
78	// 3) Prime 127 + 部件
79	console.log('== Prime 127 ==');
80	{
81	  enemies.length = 0; projectiles.length = 0;
82	  const head = Enemy.fromVanilla(127, 100 * 16, 100 * 16)!;
83	  head.id = 1; enemies.push(head);
84	  run(1);
85	  const parts = enemies.filter((e) => e.vanillaId && e.vanillaId >= 128 && e.vanillaId <= 131);
86	  check('生成 4 部件', parts.length === 4, parts.map((p) => p.vanillaId));
87	  check('部件锚定头 id', parts.every((p) => p.ai1 === head.id));
88	  check('部件侧别 ±1', parts.some((p) => p.ai0 === -1) && parts.some((p) => p.ai0 === 1));
89	  check('130/131 ai3=150 预热', enemies.filter((e) => e.vanillaId === 130 || e.vanillaId === 131).every((p) => p.ai3 === 150));
90	  run(300);
91	  check('头悬浮 ai1=0 且逼近', head.ai1 === 0 && Math.abs(head.cy - 140 * 16) < 500, [head.ai1, Math.round(head.cy / 16)]);
92	  head.ai2 = 599;
93	  run(2);
94	  check('600t 切旋冲', head.ai1 === 1, head.ai1);
95	  check('旋冲防伤×2', head.def.defense === (Enemy.fromVanilla(127, 0, 0)!.def.defense ?? 0) * 2, head.def.defense);
96	  // 白天 → 狂暴
97	  world.clock.timeOfDay = 0.5;
98	  run(2);
99	  check('白天狂暴 ai1=2', head.ai1 === 2, head.ai1);
100	  check('狂暴伤/防 9999', head.def.damage === 9999 && head.def.defense === 9999, [head.def.damage, head.def.defense]);
101	  world.clock.timeOfDay = 0.0;
102	  // 头死 → 部件自毁
103	  head.dead = true;
104	  run(2);
105	  check('头死部件自毁', enemies.filter((e) => e.vanillaId && e.vanillaId >= 128 && e.vanillaId <= 131).every((p) => p.dead));
106	}
107	// 4) 毁灭者 134 + 80 段链
108	console.log('== Destroyer 134 ==');
109	{
110	  enemies.length = 0; projectiles.length = 0;
111	  const head = Enemy.fromVanilla(134, 100 * 16, 100 * 16)!;
112	  head.id = 1; enemies.push(head);
113	  run(1);
114	  const segs = enemies.filter((e) => e.vanillaId === 135 || e.vanillaId === 136);
115	  check('生成 80 段链', segs.length === 80, segs.length);
116	  check('尾段 136 存在', segs.some((s) => s.vanillaId === 136));
117	  run(200);
118	  // 段链收缩跟随:每段与前段距离 ≈ 44(linkDist)~44+每tick头位移
119	  let maxDist = 0;
120	  for (const s of segs) {
121	    const f = s.wormFollow!;
122	    maxDist = Math.max(maxDist, Math.hypot(f.cx - s.cx, f.cy - s.cy));
123	  }
124	  check('链距收缩 ≤ 60px', maxDist <= 60, Math.round(maxDist));
125	  check('头在移动', Math.abs(head.vx) + Math.abs(head.vy) > 0.1, [head.vx.toFixed(2), head.vy.toFixed(2)]);
126	  // 白天下坠过岩石层 → 整链消散
127	  world.clock.timeOfDay = 0.5;
128	  head.y = 200 * 16; // 已过 rockLevel(190)
129	  head.vy = 0;
130	  run(2);
131	  check('白天过岩石层整链消散', enemies.every((e) => e.dead));
132	}
133	console.log(`\n结果: ${ok} 通过, ${bad} 失败`);
134	process.exit(bad ? 1 : 0);
135	

```


---

## 🤖 Assistant · 2026-08-10T06:46:13.286Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now Enemy.ts — I need to understand fields: aiT, ai0..ai3, bInit, spawnAlpha, iframes, dead, vanillaId, vanilla, fromVanilla, fixedUpdate dispatch. Let me read key parts of Enemy.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:46:13.884Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle\\|fixedUpdate\\|fromVanilla\\|ai0\\|aiT\\|iframes\\|spawnAlpha\\|onGround\\|bInit\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -80",
 "description": "Grep Enemy fields and dispatch"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:13.908Z

**📎 ToolResult**

```
25:/** 原版路径 key（v_*）的占位 def，fromVanilla 会整体覆写 */
36:  // ---- 蠕虫多段体（AI_006，NPC.cs:18046）：头 aiStyle 6，编号约定 头+1=身 头+2=尾 ----
50:    else { dx = Math.cos(this.aiT * 0.02) * 10; dy = Math.sin(this.aiT * 0.013) * 10; }
84:      const s = Enemy.fromVanilla(id, head.cx, head.cy);
96:  static fromVanilla(id: number, x: number, y: number): Enemy | null {
104:    const flying = v.noGravity || v.aiStyle === 2 || v.aiStyle === 5 || v.aiStyle === 14;
113:      nightOnly: v.aiStyle === 2 || v.aiStyle === 5, underground: false,
123:    e.spawnAlpha = v.alpha ?? 0; // 原版 SetDefaults alpha（静态不透明度，NPC.Opacity=1-alpha/255）
125:    // 钳到 254 并置 alphaFade,由 fixedUpdate 逐 tick 减回 0（原版 AI_006 渐显）
126:    if (e.spawnAlpha >= 255) { e.spawnAlpha = 254; e.alphaFade = true; }
136:  iframes = 0;
139:  aiT = 0;               // 通用 AI 计时
168:  spawnAlpha = 0;
172:  ai0 = -1120;
180:  /** AI 首帧初始化标记（原版 ai[0]==0 门在 ai0 初值 -1120 的史莱姆语义下不可用） */
186:  bInit = false;
199:  fixedUpdate(dt: number, game: GameHooks) {
201:    this.aiT++;
202:    if (this.iframes > 0) this.iframes--;
210:      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
211:      if (this.spawnAlpha === 0) this.alphaFade = false;
217:    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----
224:      switch (this.vanilla.aiStyle) {
229:        // 冲刺计时合法冻结;传 null 会让 aiT 照走、状态机停摆 → 首冲时长翻倍)
312:        if ((day && this.def.nightOnly) || (day && this.vanilla?.aiStyle === 2)) {
347:    if (jumpV && this.onGround) this.vy = -jumpV;
349:    this.vx *= this.onGround ? 0.8 : 0.98;
354:   *  阶段判定（num54=-1000）：ai0>=0 → 小跳（vy=-6, vx+=2*dir, ai0=-1120）；
355:   *  -1000..-500 → 小跳（ai0=-2120）；-2000..-1500 → 大跳（vy=-8, vx+=3*dir, ai0=-200）。
359:   *  蚱蜢(377/446) 复用本 AI（ai0 额外 +3，跳得更频繁） */
375:    const grounded = this.onGround || (inWater && Math.abs(this.vy) < 0.8);
386:      this.ai0 += 1 + (flag3 ? 1 : 0) + (grasshopper ? 3 : 0);
390:      if (this.ai0 >= 0) stage = 1;
391:      else if (this.ai0 >= num54 && this.ai0 <= num54 * 0.5) stage = 2;
392:      else if (this.ai0 >= num54 * 2 && this.ai0 <= num54 * 1.5) stage = 3;
398:          this.ai0 = -200;
403:          this.ai0 = stage === 1 ? -120 + num54 : -120 + num54 * 2;
414:    if (this.onGround && this.hitWall && player) {
427:      if (this.onGround && this.hitWall) this.vy = -6;
429:    } else if (this.hitWall && this.onGround) {
509:    if (this.onGround) this.vx *= 0.85;
520:    // 撞墙反弹（collideX/Y → hitWall/hitHead/onGround + 上一帧速度近似 oldVelocity）
564:    if (this.hitHead || this.onGround) {
577:  /** AI_013 植物/攀爬者族(NPC.cs:22604-22700 一比一):锚点格(ai0/ai1)固定,
583:    if (this.ai0 < 0 || this.ai1 < 0 || !st.inBounds(this.ai0, this.ai1)
584:      || st.type[st.idx(this.ai0, this.ai1)] === 0) {
597:    const ax = this.ai0 * 16 + 8, ay = this.ai1 * 16 + 8;
666:      this.ai0 += 1;
667:      if (this.ai0 > 200) this.ai0 = -200;
668:      this.vy += this.ai0 > 0 ? 0.023 : -0.023;
669:      this.vx += Math.abs(this.ai0) > 100 ? 0.023 : -0.023;
671:      this.ai0 = 0; // 近距无摆动
699:    if (this.onGround) this.vy = -Math.abs(this.vy) * bounce - 0.5;
705:   *  <250 环绕摆动（ai[0] +=0.9、vy ±0.019、|ai0|>100 时 vx 反向，L21636-21651）；
720:      this.ai0 += 0.9;
721:      this.vy += this.ai0 > 0 ? 0.019 : -0.019;
722:      this.vx += Math.abs(this.ai0) > 100 ? 0.019 : -0.019;
723:      if (this.ai0 > 200) this.ai0 = -200;
746:    if (!this.aiInit) { this.aiInit = true; this.ai0 = 1; } // 初始化（L21910；68 无手 NPC）
777:      this.ai0 = 1;
784:    if (this.ai0 >= 1 && this.ai0 < phaseLen) {
786:      this.ai0 += 1;
787:    } else if (this.ai0 >= phaseLen) {
791:      this.ai0 = -1;
814:      this.ai0 = 1;
818:    const collideY = this.onGround || this.hitHead;
820:      if (collideY) this.ai0 = 2;
821:      if (!collideY && this.ai0 === 2) { this.facing *= -1; this.ai1 = 1; this.ai0 = 1; }
824:      if (collideX) this.ai0 = 2;
825:      if (!collideX && this.ai0 === 2) { this.dirY *= -1; this.ai1 = 0; this.ai0 = 1; }
885:    // 不能带 fighterAI 的 onGround *=0.9，否则平衡点被压到 0.63 远低于 6
929:    if (this.hitHead || this.onGround) {
960:      if (this.onGround && this.aiT % 30 === 0) {   // 拍打：小跳 + 随机方向
975:      if (++this.aiT % 90 === 0 && player) {
985:      if (this.onGround && this.aiT % 30 === 0) this.vy = -2.5; // 拍打
989:    if (this.onGround && inWater) this.vy = -Math.abs(this.vy) - 0.5;
1015:    if (this.ai0 === 0) {
1019:      if (this.onGround && this.aiT % 60 === 0) this.vx = (Math.random() < 0.5 ? -1 : 1) * 0.7;
1020:      if (this.onGround) this.vx *= 0.85;
1022:      if ((flee || this.iframes > 0) && this.onGround) {

```


---

## 🤖 Assistant · 2026-08-10T06:46:16.086Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 150,
 "offset": 196
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:16.098Z

**📎 ToolResult**

```
196	    this.y = y - this.h / 2;
197	  }
198	
199	  fixedUpdate(dt: number, game: GameHooks) {
200	    this.prevX = this.x; this.prevY = this.y;
201	    this.aiT++;
202	    if (this.iframes > 0) this.iframes--;
203	    if (this.hpBarT > 0) this.hpBarT--;
204	    if (this.squash !== 0) this.squash *= 0.85;
205	    this.animT++;
206	    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
207	
208	    // EoW 族出生渐显（每 tick alpha-1;原版 AI_006）——静态半透明不受影响
209	    if (this.alphaFade) {
210	      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
211	      if (this.spawnAlpha === 0) this.alphaFade = false;
212	    }
213	
214	    const player = (game as unknown as { player: Player }).player;
215	    const hasPlayer = !!player && !player.dead;
216	
217	    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----
218	    // 蠕虫身体段（wormFollow 非空）无 AI：位置由头部 wormAI 沿链驱动，但仍走共享尾段（接触伤害等）
219	    // 小动物（critter）优先走被动游荡，绝不落入 default 的追击 fallback
220	    if (this.vanilla && !this.wormFollow && this.vanilla.critter) {
221	      this.critterWanderAI(game, hasPlayer ? player : null);
222	    } else if (this.vanilla && !this.wormFollow) {
223	      const p = hasPlayer ? player : null;
224	      switch (this.vanilla.aiStyle) {
225	        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
226	        case 2: this.floatEyeAI(game, p); break;                        // AI_002 飘浮眼（原版核）
227	        case 3: this.fighterAI(game, p); break;                        // AI_003 战士族（原版通用核）
228	        // EoC 传参例外:玩家死亡也要传原对象(cs:19931 dead 判定走逃离分支,
229	        // 冲刺计时合法冻结;传 null 会让 aiT 照走、状态机停摆 → 首冲时长翻倍)
230	        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）
231	        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
232	        case 6: this.wormAI(game, p); break;                           // AI_006 蠕虫族（头）
233	        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
234	        case 10: this.cursedSkullAI(game, p); break;                     // AI_010 诅咒头骨（地牢飞行族）
235	        case 11:
236	          // 68 守卫走专用分支（bossAI.skeletronBossAI 注释"守卫分支已在 skeletronHeadAI"
237	          // 即此拆分：守卫恒速追击与骷髅王战斗状态机互不混用）
238	          if (this.vanillaId === 68) this.dungeonGuardianAI(game, p);
239	          else skeletronBossAI(this, game, p);
240	          break;                                                         // AI_011 骷髅王头战斗核/地牢守卫
241	        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
242	        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
243	        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
244	        case 14: this.batAI(game, p); break;                            // AI_014 蝙蝠/飞行族（1.4.5.6 原版核）
245	        case 16: this.swimAI(game, p); break;                           // AI_016 游泳族（鲨鱼/食人鱼）
246	        case 18: this.jellyfishAI(game, p); break;                      // AI_018 水母族（脉冲游动）
247	        case 22: this.ghostAI(game, p); break;                          // AI_022 幽灵族（穿墙缓速）
248	        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
249	        case 15: kingSlimeAI(this, game, p); break;                       // AI_015 史莱姆王(大跳+小史莱姆)
250	        case 54: brainOfCthulhuAI(this, game, p); break;                  // AI_054 克脑(爬行者环→瞬移冲刺)
251	        case 55: creeperAI(this, game, p); break;                         // AI_055 爬行者(环绕漂移)
252	        case 30: twinsAI(this, game, p, false); break;                    // AI_030 雷神之眼 125(悬浮/连冲/变身/激光)
253	        case 31: twinsAI(this, game, p, true); break;                     // AI_031 魔神之眼 126(诅咒焰/火焰喷射)
254	        case 32: skeletronPrimeAI(this, game, p); break;                  // AI_032 机械骷髅王头 127(4 部件/旋冲/白天狂暴)
255	        case 33: case 34: case 35: case 36: primePartAI(this, game, p); break; // AI_033-036 Prime 部件(锯/激光/钳/炮)
256	        case 37: destroyerAI(this, game, p); break;                       // AI_037 毁灭者 134(80 段链穿地/探针激光)
257	        case 27: wallOfFleshAI(this, game, (game as unknown as { player: Player }).player ?? null); break; // AI_027 血肉墙(空腔扫描/速度血量档/Leech 轮)
258	        case 28: wofEyeAI(this, game, p); break;                          // AI_028 血肉墙之眼(钉墙吸附/激光连射 83)
259	        case 29: hungryAI(this, game, p); break;                          // AI_029 饥饿者(挂墙环绕→受击脱落扑咬)
260	        case 84: lunaticCultistAI(this, game, p); break;                  // AI_084 拜月教邪教徒(瞬移+四系弹幕轮换)
261	        case 120: empressOfLightAI(this, game, p); break;                 // AI_120 光之女皇(连段选招/半血变身)
262	        case 121: queenSlimeAI(this, game, p); break;                     // AI_121 史莱姆皇后(走路四连跳→飞行二阶段)
263	        case 43: queenBeeAI(this, game, p); break;                        // AI_043 蜂后(悬浮俯冲/蜜蜂机枪/毒刺)
264	        case 50: planteraHookAI(this, game, p); break;                    // AI_050 真菌孢子 261/孢子 265
265	        case 51: planteraAI(this, game, p); break;                        // AI_051 世纪之花(钩蔓牵引→二阶段)
266	        case 52: planteraTentacleAI(this, game, p); break;                // AI_052 钩蔓 263(抓墙换锚收线)
267	        case 53: planteraTentacle2AI(this, game, p); break;               // AI_053 触须 264(二阶段环绕)
268	        case 69: dukeFishronAI(this, game, p); break;                     // AI_069 猪鲨(冲撞/泡泡/龙卷,半血变身)
269	        case 70: dukeBubbleAI(this, game, p); break;                      // AI_070 爆裂泡泡 371
270	        case 77: moonLordCoreAI(this, game, p); break;                    // AI_077 月总核心 398(双手死前无敌)
271	        case 78: moonLordHandAI(this, game, p); break;                    // AI_078 月总手 397(攻表/睁眼可击)
272	        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
273	        case 26: this.chargerAI(game, p); break;                        // AI_026 独角兽/冲锋族（原版核）
274	        case 107: this.chargerAI(game, p, 1); break;                    // AI_107 ImprovedWalkers（0.07/±1.0 walker 档，NPC.145.cs:43153 引擎核同构）
275	        default: this.zombieAI(game, p); break;                        // 其余家族待逐个移植
276	      }
277	    } else switch (this.key) {
278	      case 'slime_green':
279	      case 'slime_blue': this.slimeAI(game, hasPlayer ? player : null); break;
280	      case 'zombie': this.zombieAI(game, hasPlayer ? player : null); break;
281	      case 'demon_eye':
282	      case 'cave_bat': this.flyAI(game, hasPlayer ? player : null, 0.09); break;
283	      case 'servant_of_cthulhu': this.flyAI(game, hasPlayer ? player : null, 0.22); break;
284	      case 'eye_of_cthulhu': this.eocAI(game, player ?? null); break;
285	    }
286	
287	    // 入水溅落声（与主角一致）：音量随与主角距离衰减，Boss 更响
288	    const eli = game.world.store.liquid[game.world.store.idx(
289	      Math.floor(this.cx / TILE), Math.floor(this.cy / TILE),
290	    )];
291	    const wasWater = this.inWater;
292	    this.inWater = eli > 80;
293	    if (this.inWater && !wasWater && hasPlayer) {
294	      const d = Math.hypot(player.cx - this.cx, player.cy - this.cy);
295	      const vol = Math.max(0.12, Math.min(1, 1 - d / (TILE * 45))) * (this.def.boss ? 1.2 : 0.9);
296	      game.playSfx('splash', vol);
297	    }
298	
299	    // 接触伤害（带上攻击者引用，供荆棘反伤）。damage=0（小动物等友好生物）不触发——
300	    // 否则 damagePlayer(0) 仍会击退/闪红，表现为"兔子撞我有攻击性"
301	    if (hasPlayer && this.aabbOverlaps(player) && this.def.damage > 0) {
302	      game.damagePlayer(this.def.damage, this.cx, this.cy, this);
303	    }
304	
305	    // Despawn 系统（原版 timeLeft/EncourageDespawn L7228-7241）：
306	    // 飘浮眼(2) 白天 DespawnEncouraged_AIStyle2（L19147）→ EncourageDespawn(10)；
307	    // 夜行怪白天离屏清除；其余离屏 timeLeft 递减到 0 清除（原版默认 7500 tick，回屏重置）
308	    const day = game.world.clock.isDay;
309	    if (hasPlayer) {
310	      const d = Math.hypot(player.cx - this.cx, player.cy - this.cy);
311	      if (!this.def.boss) {
312	        if ((day && this.def.nightOnly) || (day && this.vanilla?.aiStyle === 2)) {
313	          // 白天夜行怪/飘浮眼：离屏 >90 格即清
314	          if (d > TILE * 90) this.dead = true;
315	        } else if (d > TILE * 120) {
316	          this.despawnTimer--;
317	          if (this.despawnTimer <= 0) this.dead = true;
318	        } else {
319	          this.despawnTimer = 7500; // 原版默认 timeLeft，回屏重置
320	        }
321	      }
322	    }
323	  }
324	
325	  private groundPhysics(game: GameHooks, jumpV = 0, accel = 0.12, maxSpd = 1, buoyant = false) {
326	    // 浮力生物（史莱姆）：水中上浮 + 阻尼，漂在水面而不是沉底
327	    if (buoyant) {
328	      const st = game.world.store;
329	      const li = st.liquid[st.idx(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE))];
330	      if (li > 80) {
331	        if (this.state === 1) {
332	          // 跳跃中：弱重力助其跃出水面（浮力阻尼会把起跳速度吃掉导致困在水里）
333	          this.vy = Math.min(this.vy + GRAVITY * 0.3, MAX_FALL_SPEED);
334	          moveAndCollide(this, game.world, this.vx, this.vy);
335	          this.vx *= 0.98;
336	          return;
337	        }
338	        this.vy -= 0.32;
339	        this.vy *= 0.92;
340	        this.vx *= 0.95;
341	        moveAndCollide(this, game.world, this.vx, this.vy);
342	        return;
343	      }
344	    }
345	    this.vy = Math.min(this.vy + GRAVITY, MAX_FALL_SPEED);

```


---

## 🤖 Assistant · 2026-08-10T06:46:21.787Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I understand the structure. The dispatch switch is in Enemy.ts, which I'm forbidden to modify — the main session will wire case 45/46/47/48.

Now I need to know how gravity/collision works for the body. The body 245 needs walking + jumping with ground collision. bossAI.ts's collideGround is private there; I'll copy a version into bossAI_golem.ts (task says allowed: "落地判定可在自己文件里复制一份 collideGround——bossAI.ts 里那份是 private").

Important: does Enemy.fixedUpdate apply gravity automatically? The AI functions call moveAndCollide or manually add vx/vy. King slime AI adds its own gravity and calls collideGround. For the golem body, vanilla AI_045: the body walks on ground; velocity.Y == 0 means grounded. Gravity applied by... In vanilla, gravity is applied via `noGravity=false` + Collision. In our port, I'll do like kingSlimeAI: apply gravity when not onGround, then move, then collideGround. Actually the vanilla body uses velocity.Y==0 check as grounded. Our onGround flag from collideGround approximates.

Let me check Enemy fields more: `vx`, `vy`, `def.defense` exists? check def structure. Let me look at lines 100-196 of Enemy.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:46:22.033Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 110,
 "offset": 1
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:22.039Z

**📎 ToolResult**

```
1	// 敌人实体：统一类 + 按 key 分支行为（史莱姆/僵尸/恶魔眼/蝙蝠/克苏鲁之眼及其仆从）
2	// + 原版 NPC 数据驱动路径（vanillaId）：属性/AI/音效/贴图来自 vanilla-npcs.json（SetDefaults 提取）
3	import { Entity } from './Entity';
4	import type { GameHooks } from './types';
5	import type { Player } from './Player';
6	import { ENEMY_DEFS, EnemyDef } from '../data/enemies';
7	import { vanillaNpc, vanillaSoundName, vanillaNpcDrops, type VanillaNpc } from '../data/vanillaNpcs';
8	import { GRAVITY, MAX_FALL_SPEED, TILE } from '../core/constants';
9	import { moveAndCollide } from '../physics/TileCollision';
10	import { Dart } from './Dart';
11	import { avoidWater } from './waterAvoid';
12	import { bindEnemyCtor, skeletronBossAI, skeletronHandAI, kingSlimeAI, brainOfCthulhuAI, creeperAI, twinsAI, skeletronPrimeAI, primePartAI, destroyerAI } from './bossAI';
13	import { wallOfFleshAI, wofEyeAI, hungryAI } from './bossAI_wof';
14	import { lunaticCultistAI, empressOfLightAI, queenSlimeAI } from './bossAI_lategame';
15	import { queenBeeAI, planteraHookAI, planteraAI, planteraTentacleAI, planteraTentacle2AI } from './bossAI_queenbee_plantera';
16	import { dukeFishronAI, dukeBubbleAI, moonLordCoreAI, moonLordHandAI, moonLordHeadAI } from './bossAI_duke_moonlord';
17	import { RNG } from '../core/rng';
18	
19	/** 原版 Boss 头/主体 id（部件不标记:击杀部件不应出 Boss 退场流程）。
20	 *  EoC4/世吞13-15(头13 为 Boss,身14尾15 不标)/骷髅王35+手36/地牢守卫68/史莱姆王50/
21	 *  血肉墙113/双子125,126/骷髅Prime127/毁灭者134/蜂后222/石巨人245/世纪之花262/克脑266/
22	 *  猪鲨370/月总核心398/异教徒439/光皇636/史莱姆皇后657 */
23	const VANILLA_BOSS_IDS = new Set([4, 13, 35, 50, 68, 113, 125, 126, 127, 134, 222, 245, 262, 266, 370, 398, 439, 636, 657]);
24	
25	/** 原版路径 key（v_*）的占位 def，fromVanilla 会整体覆写 */
26	const PLACEHOLDER_DEF: EnemyDef = {
27	  key: 'v_placeholder', name: '?', hp: 1, damage: 0, knockbackResist: 0.5,
28	  width: 16, height: 16, mapColor: '#9A8FA0', gore: ['#9A8FA0', '#5E5566', '#C4BACC'],
29	  hitSound: ['NPC_Hit_1'], killedSound: ['NPC_Killed_1'], drops: [],
30	};
31	
32	export class Enemy extends Entity {
33	  /** 原版 NPC id（数据驱动路径启用时非空） */
34	  vanillaId: number | null = null;
35	  vanilla: VanillaNpc | null = null;
36	  // ---- 蠕虫多段体（AI_006，NPC.cs:18046）：头 aiStyle 6，编号约定 头+1=身 头+2=尾 ----
37	  /** 链上紧随本段的一段（头 → 身×n → 尾） */
38	  wormNext: Enemy | null = null;
39	  /** 本段跟随的前一段（非空 = 本段是身体段，跳过 AI 只做跟随） */
40	  wormFollow: Enemy | null = null;
41	  /** 上一 tick 位置（段跟随用：段复制前一段的旧位置 = 经典贪吃蛇链） */
42	  prevX = 0; prevY = 0;
43	
44	  /** AI_006 头部（L18645 通用常数 maxSpd=8 accel=0.07；穿墙直行；段链跟随） */
45	  private wormAI(game: GameHooks, player: Player | null) {
46	    const maxSpd = 8, accel = 0.07;
47	    // 朝向：有玩家朝玩家，无玩家缓慢巡游
48	    let dx: number, dy: number;
49	    if (player) { dx = player.cx - this.cx; dy = player.cy - this.cy; }
50	    else { dx = Math.cos(this.aiT * 0.02) * 10; dy = Math.sin(this.aiT * 0.013) * 10; }
51	    const d = Math.hypot(dx, dy) || 1;
52	    this.vx += (dx / d) * accel;
53	    this.vy += (dy / d) * accel;
54	    const spd = Math.hypot(this.vx, this.vy);
55	    if (spd > maxSpd) { this.vx = (this.vx / spd) * maxSpd; this.vy = (this.vy / spd) * maxSpd; }
56	    this.facing = this.vx > 0 ? 1 : -1;
57	    // 蠕虫穿墙：直接位移（原版 noTileCollide）
58	    this.x += this.vx;
59	    this.y += this.vy;
60	    // 段链跟随（原版 L52271-52308）：方向向量收缩维持 linkDist 间距——
61	    // shrink = (dist - linkDist)/dist；position += dxC*shrink（原版 num63/num64）
62	    for (let s = this.wormNext; s; s = s.wormNext) {
63	      const fx = s.wormFollow!;
64	      const dxC = fx.cx - s.cx;
65	      const dyC = fx.cy - s.cy;
66	      const dist = Math.hypot(dxC, dyC);
67	      if (dist > 0.01) {
68	        const linkDist = s.w;               // 原版 num64 = width
69	        const shrink = (dist - linkDist) / dist;
70	        s.x += dxC * shrink;
71	        s.y += dyC * shrink;
72	        s.facing = dxC < 0 ? 1 : -1;         // 原版 spriteDirection（L52305）
73	      }
74	    }
75	  }
76	
77	  /** 由头生成段链（原版各 worm 的 NewNPC 链，NPC.cs:18174+）：body×n + tail */
78	  static spawnWormChain(head: Enemy, segCount: number): Enemy[] {
79	    const segs: Enemy[] = [];
80	    const bodyId = head.vanillaId! + 1, tailId = head.vanillaId! + 2;
81	    let prev = head;
82	    for (let k = 0; k < segCount; k++) {
83	      const id = k === segCount - 1 ? tailId : bodyId;
84	      const s = Enemy.fromVanilla(id, head.cx, head.cy);
85	      if (!s) continue;
86	      s.wormFollow = prev;
87	      prev.wormNext = s;
88	      prev = s;
89	      segs.push(s);
90	    }
91	    return segs;
92	  }
93	
94	
95	  /** 用原版数据造怪：属性/碰撞/音效全部来自 SetDefaults 提取值 */
96	  static fromVanilla(id: number, x: number, y: number): Enemy | null {
97	    const v = vanillaNpc(id);
98	    if (!v) return null;
99	    const e = new Enemy(`v_${id}`, x, y);
100	    e.vanillaId = id;
101	    e.vanilla = v;
102	    const hit = vanillaSoundName(v.HitSound) ?? 'NPC_Hit_1';
103	    const kill = vanillaSoundName(v.DeathSound) ?? 'NPC_Killed_1';
104	    const flying = v.noGravity || v.aiStyle === 2 || v.aiStyle === 5 || v.aiStyle === 14;
105	    e.def = {
106	      ...e.def,
107	      name: v.name, hp: v.lifeMax, damage: v.damage, defense: v.defense,
108	      // 原版 knockBackResist 是"承受击退的比例"（0.5=吃一半）；本仓库语义是
109	      // "抗性"（hurt(): resist<0.9 才生效，kbx*(1-resist)）→ 换算 1-比例
110	      knockbackResist: Math.max(0, Math.min(0.89, 1 - (v.knockBackResist ?? 0.5))),

```


---

## 🤖 Assistant · 2026-08-10T06:46:24.285Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me see the rest of fromVanilla (lines 110-196) and the Enemy field declarations 130-196.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:46:24.525Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 90,
 "offset": 110
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:24.531Z

**📎 ToolResult**

```
110	      knockbackResist: Math.max(0, Math.min(0.89, 1 - (v.knockBackResist ?? 0.5))),
111	      width: v.width, height: v.height, flying,
112	      boss: VANILLA_BOSS_IDS.has(id),
113	      nightOnly: v.aiStyle === 2 || v.aiStyle === 5, underground: false,
114	      mapColor: '#9A8FA0', gore: ['#9A8FA0', '#5E5566', '#C4BACC'],
115	      hitSound: [hit], killedSound: [kill], drops: v.critter ? [] : vanillaNpcDrops(id),
116	      // 小动物：无接触伤害、不夜行
117	      ...(v.critter ? { damage: 0, nightOnly: false } : {}),
118	    };
119	    e.hp = v.lifeMax;
120	    e.maxHp = v.lifeMax;
121	    e.w = v.width;
122	    e.h = v.height;
123	    e.spawnAlpha = v.alpha ?? 0; // 原版 SetDefaults alpha（静态不透明度，NPC.Opacity=1-alpha/255）
124	    // EoW 族 alpha=255 = 出生全透明渐显标记（其余 alpha 为静态不透明度,勿动）：
125	    // 钳到 254 并置 alphaFade,由 fixedUpdate 逐 tick 减回 0（原版 AI_006 渐显）
126	    if (e.spawnAlpha >= 255) { e.spawnAlpha = 254; e.alphaFade = true; }
127	    e.colorRGBA = v.color ? [v.color[0], v.color[1], v.color[2], v.color[3] ?? 255] : null; // 原版 color 字段
128	    e.x = x - e.w / 2;
129	    e.y = y - e.h / 2;
130	    return e;
131	  }
132	
133	  def: EnemyDef;
134	  hp: number;
135	  maxHp: number;
136	  iframes = 0;
137	  animT = 0;
138	  facing = 1;
139	  aiT = 0;               // 通用 AI 计时
140	  state = 0;             // 行为状态
141	  phase = 1;             // Boss 阶段
142	  target: { x: number; y: number } | null = null;
143	  squash = 0;            // 史莱姆挤压动画 -1..1
144	  stuckT = 0;            // 飞行怪卡墙计时（脱困用）
145	  stuckCd = 0;           // 脱困后的游荡冷却
146	  jumpStartX = 0;        // 史莱姆本次起跳的 x（落地时判定是否白跳）
147	  chargesLeft = 0;       // EoC 剩余冲撞次数
148	  dashing = false;       // EoC 冲撞中（无视地形）
149	  visAngle = Math.PI;    // EoC 显示角度（平滑追踪移动方向；素材默认朝左）
150	  spin = 0;              // EoC 变身旋转进度 0..1
151	  hpBarT = 0;            // 受击后血条显示计时（tick）
152	  // ---- EoC(AI_004)专属 ----
153	  servantT = 0;          // 悬浮时"位于玩家上方"累计(110t 召仆从)
154	  spinSpeed = 0;         // 自旋角速度(cs ai[2]:0.005 步进钳 0.5)
155	  spinPhase = 0;         // 自旋段:0 加速 / 1 减速
156	  walkCycleT = 0;        // 行走帧累加器（≈原版 frameCounter，按 |vx| 推进）
157	  /** 原版 netID 变种（负数 SetDefaultsFromNetId）：scale/颜色/属性覆盖 */
158	  vanillaScale = 1;
159	  /** 实际生效的负 netID（SetDefaultsFromNetId；凝胶染色过滤用） */
160	  vanillaNetId = 0;
161	  /** 原版 NPC.color 当前值（SetDefaults/SetDefaultsFromNetId 初值，AI_001 逐 tick 渐变）。
162	   *  渲染语义（Main.cs:24527 + NPC.GetColor L94903）：color≠default 时用同贴图二次绘制，
163	   *  逐像素乘 color（贴轮廓）；通道 A 决定该 pass 强度 */
164	  colorRGBA: [number, number, number, number] | null = null;
165	  /** 原版 SetDefaults alpha：每类型静态不透明度基线（渲染 1-alpha/255，NPC.Opacity）。
166	   *  多数为 0=不透明；史莱姆 175/120=半透明凝胶、水母 20、蝙蝠 30 等。
167	   *  无通用渐隐——仅特定家族（幽灵/怨灵等）在自己的 AI 内衰减 */
168	  spawnAlpha = 0;
169	  /** 出生渐显中（仅原版 alpha=255 的 EoW 族）;静态半透明(史莱姆 175 等)不参与 */
170	  alphaFade = false;
171	  /** 原版 ai[0] 跳跳计数器（史莱姆 hop 节奏）；ai[2] 卡墙禁追冷却 */
172	  ai0 = -1120;
173	  ai2 = 0;
174	  /** 原版 ai[1]（史莱姆体内物品 id，驱动 SLIME_ITEM_COLORS 渐变色；0=无） */
175	  ai1 = 0;
176	  /** 原版 ai[3]（地牢 AI 族用：诅咒头骨状态/火轮速度档/刺球相位） */
177	  ai3 = 0;
178	  /** 原版 directionY（火轮/刺球对角弹跳的纵向方向） */
179	  dirY = 1;
180	  /** AI 首帧初始化标记（原版 ai[0]==0 门在 ai0 初值 -1120 的史莱姆语义下不可用） */
181	  aiInit = false;
182	  /** 原版 timeLeft（默认 7500 tick，离屏递减；飘浮眼白天 EncourageDespawn(10)） */
183	  despawnTimer = 7500;
184	  inWater = false;       // 入水检测（溅落声用）
185	  /** Boss 专属初始化标记(部件生成等一次性动作;aiN 默认值有歧义故独立字段) */
186	  bInit = false;
187	
188	  constructor(public key: string, x: number, y: number) {
189	    super();
190	    this.def = ENEMY_DEFS[key] ?? PLACEHOLDER_DEF;
191	    this.hp = this.def.hp;
192	    this.maxHp = this.def.hp;
193	    this.w = this.def.width;
194	    this.h = this.def.height;
195	    this.x = x - this.w / 2;
196	    this.y = y - this.h / 2;
197	  }
198	
199	  fixedUpdate(dt: number, game: GameHooks) {

```


---

## 🤖 Assistant · 2026-08-10T06:46:44.953Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important: Enemy fields — `flying` def flag is set from `v.noGravity`, so the golem head/fists (noGravity: true) will be `flying`. That matters for rendering maybe but not AI dispatch. Fine.

Also note `spawnAlpha` for golem = 255 → clamped to 254 with alphaFade=true (fade in). The vanilla alpha is 255 and AI reduces alpha by 10 per tick (`alpha -= 10`). In our port alphaFade decreases by 1/tick, and alpha decrement semantics: in vanilla, `alpha > 0` → alpha -= 10, and ai[1]=0. I'll approximate using spawnAlpha/10 tracking? Simpler: treat the fade-in as visual; but the ai[1]=0 reset on spawn-fade matters little. I'll track a WeakMap "spawnFade" that mirrors alpha decrease by 10 per tick until 0 (alpha=255→25 ticks). During fade, set ai1 = 0 each tick per vanilla.

Now, what about gravity for the fists/head? noGravity → def.flying. In Enemy fixedUpdate after AI there's no automatic gravity; AIs handle movement themselves. Good.

Now design the port. Key mappings:

- Enemy.ai0..ai3 ↔ vanilla ai[0..3].
- localAI[0..3] → WeakMap per instance (golemX).
- golemBoss: static int index of body NPC. In our port, I need a module-level `golemBossId: number | null` mapping to an Enemy. Simpler: maintain module-level `let golemBoss: Enemy | null = null`. Body's golemAI sets `golemBoss = e` each tick. Head/fists/headFree find it via game.enemies() by id. But careful: if the body dies (hp<=0 → death transition), vanilla head 246 becomes 249 via checkDead (NewNPC 249). In our port the task wants: body hp→0 → head 246 becomes free-flying (phase 2) — the head continues fighting autonomously.

Vanilla semantics I'll port:
1. Body 245 (aiStyle 45, AI_045_Golem NPC.cs:19447):
   - golemBoss = self
   - localAI[0]==0 first frame: spawn 247 at center-84, 248 at center+78, 246 at center-3,-57. Spawn offsets are absolute px: (int)Center.X - 84. Note these are NewNPC positions where x,y are top-left? In vanilla NewNPC(x,y) is the position (top-left). Yes, NewNPC uses position directly.
   - If player dead → noTileCollide... simplified: if player null we just do nothing/degrade.
   - alpha fade (alpha-=10, ai[1]=0)
   - flag (246 active), flag2 (247 active), flag3 (248 active)
   - dontTakeDamage = flag (body invulnerable while head attached!) — this is vanilla phase 1 semantics: while the head 246 is attached/alive, the body takes no damage. Hmm wait — that means in vanilla phase 1 you damage the head and fists, not the body. And when head dies (hp 0), checkDead spawns 249 (head free), and then the body becomes damageable? dontTakeDamage = flag where flag = 246 active. When 246 dies, 249 spawns; 246 no longer active; so body can be damaged. But wait — can the body even die? In vanilla, after head 249 dies... 249's checkDead: else branch (type==249): dusts + gore. But who kills the fight? Let me check what makes the golem fight end. Hmm, 249 dying: does it kill 245? Since fist/head AI self-destruct when golemBoss < 0, and golemBoss is reset... where is golemBoss set to -1? grep only showed line 6052 declaration and assignments at 19449 (golemBoss = whoAmI). Hmm, and 31285 check `if (golemBoss < 0)`. So golemBoss is never reset to -1? Then after the fight ends, leftover? Actually `if (golemBoss < 0)` — since it's never reset, the check never triggers... unless golemBoss is set elsewhere (e.g. in UpdateNPC when npc[golemBoss] inactive). grep found nothing else. Hmm, there might be code in NPC.UpdateNPC: `if (golemBoss >= 0 && !Main.npc[golemBoss].active) golemBoss = -1`? grep says no. Whatever — the fight: you kill 249 (head free, dontTakeDamage initial true but AI 48 doesn't set dontTakeDamage... it's initialized true in SetDefaults. Hmm, dontTakeDamage=true initially for 249 — when is it cleared? In vanilla NPC.UpdateNPC there's probably `if (dontTakeDamage) ...`? Actually dontTakeDamage gets reset each tick in NPC.VanillaUpdate? There is code in AI dispatch reset: for each NPC, `dontTakeDamage`... hmm. Many AI styles set it each tick. 249 sets it in SetDefaults only; presumably there's a per-tick reset in UpdateNPC (line 18340/18616: `type >= 245 && type <= 249` — let me check those two spots! They may be: 18340: `else if (type >= 245 && type <= 249) { ... dontTakeDamage = false? }` and 18616 similar in expert scaling.

Let me look at those two locations to understand what they do — maybe they handle the "player above golem" or scale.

Actually line 94193: `if (type == 245 && target >= 0 && Main.player[target].position.Y > position.Y + height)` — interesting. Let me check lines 18340 and 18616 and 94193.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:46:45.861Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '18335,18360p;18610,18630p;94185,94205p;80140,80155p;81275,81290p;80800,80820p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check misc 245-249 branches"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:46:45.894Z

**📎 ToolResult**

```
		else if (type == 636)
		{
			num2 = 0.7;
			num3 *= CommonMasterBossLifeReduction;
		}
		else if (type >= 245 && type <= 249)
		{
			num2 = 0.75;
			num3 *= CommonMasterBossLifeReduction;
			num = 0.8;
		}
		else if (type == 370)
		{
			num2 = 0.65;
			num3 *= CommonMasterBossLifeReduction;
			num = 0.7;
		}
		else if (type == 371 || type == 372 || type == 373)
		{
			if (type != 371)
			{
				num2 = 0.75;
			}
			num = 0.75;
		}
		else if (type == 439 || type == 440 || (type >= 454 && type <= 459) || type == 522 || type == 523)
			num *= (double)balance;
		}
		if (type == 636)
		{
			num *= (double)balance;
		}
		if (type >= 245 && type <= 249)
		{
			num *= (double)balance;
		}
		if (type == 370)
		{
			num *= (double)balance;
		}
		if (type == 439 || type == 440 || (type >= 454 && type <= 459) || type == 523)
		{
			num *= (double)balance;
		}
		if (type == 397 || type == 396 || type == 398)
		{
			num *= (double)balance;
		case 493:
			downedTowerStardust = true;
			TowerActiveStardust = false;
			WorldGen.UpdateLunarApocalypse();
			WorldGen.MessageLunarApocalypse();
			break;
		case 245:
			SetEventFlagCleared(ref downedGolemBoss, 6);
			break;
		case 370:
			SetEventFlagCleared(ref downedFishron, 7);
			break;
		case 636:
			SetEventFlagCleared(ref downedEmpressOfLight, 23);
			break;
		case 668:
				if (m != whoAmI && Main.npc[m].active && Main.npc[m].type >= 127 && Main.npc[m].type <= 131)
				{
					Main.npc[m].ApplyInteraction(player);
				}
			}
		}
		if (type >= 245 && type <= 249)
		{
			for (int n = 0; n < Main.maxNPCs; n++)
			{
				if (n != whoAmI && Main.npc[n].active && Main.npc[n].type >= 245 && Main.npc[n].type <= 249)
				{
					Main.npc[n].ApplyInteraction(player);
				}
			}
		}
		if ((type == 396 || type == 397) && Main.npc[(int)ai[3]].active && Main.npc[(int)ai[3]].type == 398)
		{
			Main.npc[(int)ai[3]].ApplyInteraction(player);
		}
		if ((type == 393 || type == 394) && Main.npc[(int)ai[0]].active && Main.npc[(int)ai[0]].type == 395)
		if (Main.netMode == 1 || (npcType == 262 && AnyNPCs(262)))
		{
			return;
		}
		switch (npcType)
		{
		case 245:
			if (AnyNPCs(245))
			{
				return;
			}
			try
			{
				int num2 = (int)Main.player[plr].Center.X / 16;
				int num3 = (int)Main.player[plr].Center.Y / 16;
				int num4 = 0;
		if (aiStyle == 26 && target >= 0 && Main.player[target].Bottom.Y - velocity.Y > base.Bottom.Y)
		{
			result = true;
		}
		if (type == 247 || type == 248)
		{
			result = true;
		}
		if (type == 245 && target >= 0 && Main.player[target].position.Y > position.Y + (float)height)
		{
			result = true;
		}
		if (type >= 542 && type <= 545)
		{
			result = true;
		}
		if (aiStyle == 107 && directionY == 1)
		{
			result = true;
		}
		if (type == 418)

```


---

## 🤖 Assistant · 2026-08-10T06:48:49.262Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
These are mostly master/expert scaling and event flags. Fine.

Now the fight-end semantics in vanilla: the head 246 (attached, 25000hp) is the target in phase 1; fists 247/248 (10000 each) must be killed to make head vulnerable? Actually no — head is damageable always in phase 1 (body is invulnerable, not head). Wait, dontTakeDamage = flag where flag = "246 exists". So body takes no damage while the attached head lives. Head and fists are damageable. When head 246 dies → spawns 249 free head (16000 hp), body becomes damageable. Then... who ends the fight? Killing 249 gives case 245 flag? No — checkDead for 245 sets downedGolemBoss when 245 dies. And 249's death sets flag? Line 80146 case 245: SetEventFlagCleared(downedGolemBoss) — this is by npcType in some checkDead-ish. Actually line 80146 is in a switch on npcType — probably in `OnKill` or `NPCLoot_DropItems`. Hmm, when 245 dies, downedGolemBoss is set. But how does 245 die? Player damages the body after the head is free, and the body also continues walking/jumping. And when 245 dies... the fists and 249 check `golemBoss < 0` — but golemBoss never resets. Hmm, that means after 245 dies the parts keep fighting? That can't be. Let me check UpdateNPC reset for golemBoss — maybe in `NPC.UpdateNPC` in another file? grep showed all references in NPC.cs; golemBoss appears only at those lines. So vanilla 1.4.5.6 might have a quirk. Actually wait — maybe checkDead for 245 (type==245 branch in that 245-249 block) does something; the block I read: `if (type >= 245 && type <= 249) { if (life > 0) {dust} else if (type == 246) { spawn 249 } else { dusts + gore per type } }`. That's just visuals (this is in HitEffect probably, not checkDead — it uses `dmg` param). Line 85833 block takes dmg/life — that's HitEffect. OK so 246 death → spawn 249 happens in HitEffect.

Hmm, so where does the actual death happen? checkDead (NPC.cs:~84000?). Let me not go too deep. The task explicitly dictates the behavior structure:

- 本体 245: hp→0 → 头 246 起飞进入二阶段 (头脱离本体自主战斗;本体死透后头继续)
- 头 246: hover-charge + fireballs/eye lasers
- 拳 247/248: anchor body (or head), charge then return
- 头死 → 全族自毁

So they've designed: the body 245 is the phase-1 HP pool (vanilla: the body IS invulnerable and the head is the pool...). Given the probe requirements: ③本体 hp→0 后头存活进入自主战斗 ⑤头死→全族自毁. So the port must have:
- body hp<=0 → mark body "dead" (visually dead? "本体死透后头继续") — set some state; head 246 switches to free mode (aiStyle 48 behavior) anchored to nothing.
- head hp<=0 (in free mode) → whole family dies.

Given the checkDead pattern (moon lord), implement:

golemAI (body 245):
- first frame: bInit → ai0=0, ai1=0; spawn 247 (x-84, y-9), 248 (x+78, y-9), 246 (x-3, y-57). Store golemBoss reference (module-level WeakRef-like: keep `let golemBossRef: Enemy | null`), and set parts' ai3 = body id? The vanilla fists use golemBoss global index. In our port, head/fists find body by searching enemies for vanillaId===245. That's the "find-head 模式". I'll do: `findBody(game)` = enemies.find(vanillaId===245 && !dead). Module-level cache to avoid per-tick find? Fine to find each tick (small arrays).

- hp<=0 handling at top: if e.hp <= 0 && e.ai0 !== 1 (use ai0 as "dead" state? vanilla ai0 is 0=ground,1=jump). I'll add a WeakMap state with `dying` flag. Set e.hp = e.maxHp? No — task says "本体死透后头继续". For moon lord: hp<=0 → set state, refill hp. For golem body: hp<=0 → enter dying state (explode/dust), body becomes non-functional and dies (e.dead = true after a short time), head enters phase 2. Simplest faithful-to-instruction: on hp<=0: spawn particles, set head 246's ai0... hmm head 246's ai0 is vanilla phase flag (0 = mouth fireballs, 1 = eye lasers) driven by life < lifeMax/2. I need an extra field for "free mode". I'll use a WeakMap `golemX` with `free: boolean` for the head, or use ai3 as a mode marker: ai3 = 0 (attached) / 1 (free). ai3 is unused by head AI in vanilla (ai[2] used, ai[3] not). Actually let me check: head 46 uses ai[0], ai[1], ai[2], localAI[0], localAI[1]. ai[3] unused. So head ai3 = mode (0=attached,1=free). And fists use ai[0..1]; ai[3] unused → but I'd rather keep WeakMap for clarity... but probe needs observable state. The probe can observe position changes. I'll still set ai3 for testability.

Also body dying → fists: vanilla fists anchor golemBoss regardless. Task says "锚定本体(或头)". If body dead → anchor head? But head is flying high; fists charging from a flying head is weird but acceptable: "蓄力冲拳(直线冲出后回位)". Hmm. Simplest: if body missing/dead → fists anchor to head 246 (if free) else self-destruct. Probe ⑤: 头死→全族自毁 — so fists must self-destruct when head dies AND body dead. Rule: anchor = body if alive(dying ok?) else head; if neither → dead. Careful: if body is in dying state but not yet dead=true, fists anchor body; when body fully dead and head free, fists anchor head; when head dies → fists self-destruct. Good.

Body death handling: body hp<=0 → go into dying animation: stop AI movement, spawn particles, mark `dying=true` in WeakMap, and notify head (head.ai3 = 1 when it sees body dying). After e.g. 60t → e.dead = true. During dying: e.iframes = 2 (can't be hit further), damage 0? Keep simple: invulnerable, no movement, dust particles, then dead.

Hmm, but wait: vanilla 246 death spawns 249 — the free head has separate stats (lifeMax 16000, damage 80, defense 32). In our port, head 246 continues as itself (task: "头 246 起飞进入二阶段"). When switching to free mode, should I apply 249's stats? The vanilla behavior is a new NPC 249 with lifeMax 16000 damage 80 defense 32. Data JSON has 249 entry. To be faithful and simple: when body dies, head enters free mode using aiStyle 48 logic (ported), and upgrade damage/defense to 249's values? Damage 80 vs 64. I could apply: e.def.damage = 80, e.def.defense = 32 via base-cache swap. Nice touch: baseStats swap when entering free mode. And head's hp: vanilla 249 spawns with full 16000 hp; our head 246 may be damaged. Task ③ says "头存活进入自主战斗" — no requirement on hp. I'll refill hp to lifeMax (like vanilla new NPC full HP). Hmm, is that right? In vanilla, the attached head 246 dying spawns 249 with FULL hp. Yes! In vanilla phase 1 you kill the attached head (25000 hp), then the free head 249 appears with 16000 fresh HP. So refilling is faithful. But in our task's structure, the phase-1 HP pool is the BODY (per probe ③: body hp→0 → head survives). So refill head hp on transition = faithful to vanilla 249 spawn. I'll do that: on transition, hp = maxHp (16000 per JSON 246... hmm 246's lifeMax in JSON is 16000 already, and 249's is 11000).

JSON: 246 lifeMax 16000, 249 lifeMax 11000. Vanilla 1.4.5.6: 246 lifeMax 25000, 249 16000 (expert scaling: classic 16000/... whatever, extracted data is authoritative for this project). I'll refill to e.maxHp on transition (head's own maxHp = 16000). Reasonable.

Now the free head AI (aiStyle 48) references Main.npc[golemBoss].life for pacing — in free mode with body dead, I'll use head's own hp ratio instead? Vanilla: body alive (damaged) drives speed. In our structure, the body is dead in phase 2, so vanilla's golemBoss.life checks are meaningless. I'll use the head's own hp ratio as the pacing driver (documented simplification). Also flag49 (no LOS between golemBoss and player) → use losClear(head, player) as the substitute. Reasonable 1:1-ish adaptation, documented.

Now port each:

### golemAI (245, AI_045, NPC.cs:19447-19690)

Vanilla structure:
1. golemBoss = whoAmI (module ref).
2. num = GetMyBalance() — balance value; classic = 1. (GetMyBalance returns scaling based on player count? For classic single player = 1). getGoodWorld +2 — skip (comment). Zone temple/jungle or above surface → num *= 2 (enrage out of temple) — keep: if player not in jungle/temple zone... we don't have ZoneLihzhardTemple; we have world surface check: player.Center.Y < worldSurface*16 → num *= 2. I'll implement: if (player.cy < (game.world.groundLevel*TILE)) num *= 2 (documented; biome zone check omitted since no temple zone API). Actually GameHooks has world.groundLevel (used in destroyerAI). I'll use that.

3. localAI[0]==0 → spawn parts (positions: NewNPC at Center.X-84, Center.Y-9 for 247; +78 for 248; -3,-57 for 246). NewNPC x,y is top-left. Our spawnPart(game, src, id) uses Enemy.fromVanilla(id, src.cx, src.cy) then places at center. I'll adjust positions after spawn: fist.x = body.cx - 84 - fist.w/2? Vanilla: position.X = Center.X - 84 (absolute top-left). To mirror exactly: p.x = e.cx - 84; p.y = e.cy - 9 (top-left semantics). Hmm fromVanilla sets x = x - w/2 (centers). I'll set p.x = e.cx - 84 (vanilla position) then... to keep it simple and visually symmetric, I'll compute vanilla-style top-left: p.x = (e.cx - 84) - p.w/2 ... no. Vanilla NewNPC(x, y) puts position at (x, y) exactly — top-left of hitbox. Our Enemy x is top-left too. So: p.x = e.cx - 84; p.y = e.cy - 9. But spawnPart placed it centered at (cx, cy); I'll overwrite after. Fine.

   For each part set: ai0 (fist side: vanilla fists have no explicit ai0 set at spawn — AI_047 uses `type == 247` checks, not ai0. Task says "ai0=侧别" for fists — the task instructs ai0=侧别. But vanilla fist AI uses ai[0] as its state machine (0=idle,1=charge-windup,2=flying,3=...). Conflict! The task says "拳 247/248:锚定本体(或头),蓄力冲拳(直线冲出后回位),ai0=侧别". If ai0 = side, then I can't use ai0 for the state machine. Hmm. Options: keep vanilla ai0 as state, derive side from vanillaId (247 → -1, 248 → +1). But the task explicitly asks ai0=侧别. And the wiring note in the report: "拳 247/248:ai0=侧别". Since spawnPart for Prime sets ai0=side, consistent. But then where's the state? I'll use WeakMap for fist state (fistX: state, timer, spawnFade). Hmm, but then probes observe... probe observes displacement, fine.

   Actually — hold on. In vanilla AI_047, ai[0] IS the state (0 homing to shoulder, 1 windup at shoulder, 2 punch flying, 3 ??? Actually ai[0]==3 branch is the "fly to player" branch — reachable? ai[0] set to 0/1/2 only in code I saw. The 3 branch may be legacy/unreachable). I'll keep fidelity by using a WeakMap `fistX.state` mirroring vanilla ai[0], and set e.ai0 = side (-1 for 247, +1 for 248) per task. And e.ai1 = timer (vanilla ai[1]).

   Wait but vanilla ai[1] usage in fist: charge timer. And head 246 uses ai1 as timer too. OK.

4. Player dead handling: `if (target >= 0 && Main.player[target].dead) { TargetClosest(); if dead → noTileCollide = true; }` — simplified: if player dead/missing → wander/despawn? I'll simplify: if !player → stand still (dust), return.

5. alpha fade: alpha -= 10 → until 0; while fading ai[1] = 0. Port: track spawnFade in WeakMap: fadeT counts down from 255/10≈26 ticks; while fading, e.spawnAlpha handled by alphaFade automatically (254→0 at 1/tick = 254 ticks, too slow vs vanilla 26). I'll implement my own: while fading (alpha > 0), alpha -= 10 per tick in WeakMap, and also drive e.spawnAlpha = alpha for rendering. Actually e.spawnAlpha already 254 + alphaFade ticking it down 1/tick. To be 1:1 I'll disable alphaFade (e.alphaFade = false) and drive spawnAlpha myself: spawnAlpha = max(0, spawnAlpha - 10). And set ai1 = 0 while > 0. Vanilla also has `alpha = 255` initial → Opacity = 1 - 255/255 = 0 → invisible. spawnAlpha=254 initially (fromVanilla clamps). Then -10/tick: 26 ticks to visible. OK: on bInit: e.alphaFade = false; then per tick spawnAlpha -= 10 (min 0). Do for head & fists too.

6. Scan for parts: flag (246 exists), flag2 (247), flag3 (248). dontTakeDamage = flag → if attached head alive → body invulnerable (e.iframes = 2 each tick). Also in vanilla phase 2 (after head 246 dead → 249 exists, 246 gone) body becomes damageable.

Hmm — this conflicts with task's design where the BODY is the phase-1 pool and the head enters phase 2 when the body dies. If the body is invulnerable while the head is attached, the player can never kill the body first... unless the head dies first. In vanilla the intended kill order: fists → head (246 dies → 249 spawns) → kill 249 (ends fight? no, downed flag from 245). Hmm honestly vanilla golem: you kill fists and head; head becomes free; kill the free head AND the body? The body keeps walking around invulnerable-while-246... after 246 dies, body is damageable. Players usually kill body or 249? In Terraria wiki: "Golem's body is invulnerable until the head is destroyed"... Actually the wiki says: the Head must be destroyed first? No — Golem: you damage the head and fists while body is invulnerable; once the head is destroyed it detaches and flies; then the body becomes vulnerable. Killing the body (or head?) — the fight ends when the BODY is killed? downedGolemBoss from case 245. And 249's checkDead probably also triggers. Let me check checkDead quickly for 249/245 to get it right. Search "checkDead" and nearby type checks.

Given the task's explicit structure though, I should follow the task (body = phase-1 pool, head continues). But I also want vanilla fidelity. Compromise: keep vanilla's dontTakeDamage semantics? No — that would break probe ③ (need body hp→0 → head phase 2; if body is invulnerable while head alive, the probe would set hp manually anyway — probe sets hp directly so it works either way, and manual hp set bypasses iframes). Hmm, the probe sets body.hp = 0 directly. So dontTakeDamage doesn't matter for the probe.

But design-wise: with vanilla semantics (body invulnerable while attached head alive), the player kills the head first → head free phase 2 → body damageable. That's actually the vanilla fight and ALSO gives "头死→?" — task says 头死→全族自毁. In vanilla, 246 dying doesn't end the fight (it becomes 249). In our port, "头死" means the FREE head dies → 全族自毁 (fight over). And the body: if body dies while head attached → head goes free (task ③). Both paths lead to free head. That's a faithful + flexible structure:

- Attached head alive & body alive: body invulnerable (vanilla), head/fists damageable.
- Body hp<=0 (possible via scripts/edge) OR attached head hp<=0 → head enters free mode (refill hp, 249 stats), body: if it died → dying state then dead; if head died → body becomes damageable (vanilla) and keeps walking; when body later dies → nothing special (head already free).
- Free head hp<=0 → head dies → 全族自毁 (fists dead, body dead if still alive).

That covers everything. Probe ⑤ "头死→全族自毁": kill free head → body & fists dead.

Now, vanilla attached head 246 AI (aiStyle 46):
- noTileCollide = true (flies).
- vector from head to body: target = body.Center + (body.velocity) + (0,-9*scale); X offset by -3*scale (i.e., head anchors 3px left of body center, 57 up... wait: num722 = body.Center.X - head.Center.X; num723 = body.Center.Y - head.Center.Y - 57*scale... then num722 -= 3*scale. So target = body.Center + (-3, -57)*scale. Head moves toward that at max 100 speed: if dist < 100 → snap velocity = delta (moves fully); else normalize*100.
- rotation = 0 when close; rotation = velocity.X * 0.1 when far.
- ai[0] = 0 (life >= half): mouth fireball loop: ai[1] += 1 (+ extra 2*(num-1)/3 in first/last 20 ticks of the 300 window, localAI[0]=1 = "mouth open" frame); at ai[1] >= 300: TargetClosest, ai[1]=0, shoot proj 258 from (Center + (0,+10*scale)) speed 8, damage 18.
- ai[0] = 1 (life < half): eye phase: TargetClosest each tick; vector85 = Center + (0,10*scale); localAI[1] = side depending on player X relative to head ± width; ai[1] += num733 = (num720+3)/4 (classic 1 → 1); + same if life < 0.4, 0.2; frame open in first/last 20 of 300; at ai[1] >= 300: shoot proj 258 damage 24 speed 8 from vector85.
- ai[2] += num733 (+ extra at life < 1/3, 1/4, 1/5, +4 if no LOS); when ai[2] > 60 + rand(600): ai[2] = 0, fire eye lasers proj 259 damage 28 speed 11: if localAI[1]==0 → two shots from (Center + (-18*scale, -22*scale)) and (+18): each velocity toward player *11, spawn pos + v*3, timeLeft 300; else one shot from ±30 offset, speed 12, timeLeft 300.
- Final: if life < lifeMax/2 → ai[0] = 1 else 0.

Note classic num720 = GetMyBalance() = 1? GetMyBalance returns float based on number of active players (1 for single). So num733 = (1+3)/4 = 1. num multipliers with (num+3)/4 → 1. Good — for single-player classic, most speed-ups are 1. I'll implement num as a constant 1 with the enrage doubling if above ground (player y < worldSurface). GameHooks: world.groundLevel exists (used in bossAI.ts destroyerAI). I'll use `(game.world.groundLevel || 0) * TILE` as worldSurface*16 approximation — documented.

Free head 249 (aiStyle 48):
- If no LOS head→player → noTileCollide = true, flag48 = true; else if noTileCollide && SolidTiles → false. (Head passes through walls when it can't see the player.)
- Movement: seek target = player + (0, -300): desired velocity normalize*7, accel 0.05 (double-step when sign flip) — the accelTo pattern!
- ai[1] += num761 = (num755+4)/5 = 1 (classic single); extra ticks when golemBoss.life below thresholds (use own hp thresholds): <0.8, <0.6, <0.2, <0.1.
- localAI[0] = 1 (mouth-open frame) in first/last 20 of 300; if flag48 (no LOS) → ai[1] = 20.
- At ai[1] >= 300: fire proj 258 damage 20 speed 8 from (Center + (0,-10*scale)).
- ai[2] += num755 (1) + thresholds (1/1.25, 1/1.5, 1/2 ... 1/6) + 10x if no LOS (flag49 = no LOS golemBoss→player; I'll use head→player).
- At ai[2] > 100 + rand(4800): fire 2 eye lasers proj 259: from Center + (±14*scale, -50*scale), speed 11 (num772) damage 24 (num773), +0.25 speed/+1 dmg per body-life threshold; if flag49: damage *1.5, speed *2.5, aim with player velocity lead `player.velocity * rand * 50`. Spawn pos += v*3, timeLeft 300.
- Dust visuals (skip/netOffset).
- scale: vanilla 0.5 (scale *= 0.5 for 245-249!). Note: scale = 0.5 for all golem parts, so all the scale multiplications are ×0.5. E.g., head anchor offset -57*scale = -28.5. And fist anchor (-84 or +78)*scale = -42/+39, -9*scale = -4.5. Interesting — the spawn offsets (Center.X - 84) are NOT scaled (raw). I'll define GOLEM_SCALE = 0.5 and apply faithfully.

Wait — check: does our Enemy apply vanillaScale? fromVanilla doesn't set scale (there's vanillaScale field default 1, set elsewhere for netIDs). JSON has no scale field? Let me check whether vanilla-npcs.json has a scale field for 245. The entry printed has no "scale" key. So scale not in data; I hardcode 0.5 as GOLEM_SCALE (vanilla SetDefaults scale *= 0.5).

Fists (AI_047, NPC.cs:19171-19446):
- If golemBoss < 0 → self-destruct. (Our: no body & no free head → dead.)
- alpha fade like body.
- vector = body.Center + body.velocity + (0,-9*scale) + ((type==247) ? -84 : 78)*scale → target shoulder point.
- num2 = dist from fist to target.
- ai[0]==0 (homing to shoulder): noTileCollide = true.
  - num3 = 14 (+3 if life<half, +3 if <quarter, +8 if body damaged) * (num+3)/4 → classic 14-28; cap 32.
  - if dist < 12 + num3: rotation=0; velocity = delta (snap toward shoulder, full move); ai[1] += num (1) [+1 half, +1 quarter, +10 if body damaged]; at ai[1] >= 60: TargetClosest; if (247 and Center.X + 100 > player.Center.X) or (248 and Center.X - 100 < player.Center.X) → ai[1]=0, ai[0]=1; else ai[1]=0.
    Meaning: 247 (left fist) punches only when player is to the LEFT (player.X < fist.X + 100... condition to punch: Center.X + 100 > player.Center.X — i.e. player within 100px left of fist... roughly player is left-ish). Wait for 247: punch if Center.X + 100 > player.Center.X (player left of fist+100). For 248: punch if Center.X - 100 < player.Center.X. Yes symmetric.
  - else: normalize delta to num3 speed, rotation = atan2 for the arm angle. Note 247/248 rotation sign swap (left fist sprite mirrored).
- ai[0]==1 (windup at shoulder): ai[1] += 1; Center = vector (snap to shoulder!); rotation = 0; velocity = 0; first 15 ticks spawn dust; at ai[1] >= 30: noTileCollide = true; ai[0] = 2, ai[1] = 0; num6 = 12 (+4 half, +4 quarter, +10 body damaged) * (num+3)/4, cap 48; velocity = normalize(player - Center) * num6; rotation.
- ai[0]==2 (punch flying): ai[1] += 1; ai[1]==1 → sound Item14; dust trail; if passed the player on the punch axis → noTileCollide = false (starts colliding); if num2 (dist to shoulder) > 700 or collideX/collideY → noTileCollide = true; ai[0] = 0.
- ai[0]==3 (unreachable legacy): fly toward player 12 speed accel 0.4.

Rotation semantics: Enemy.spin used for rotation. Renderer probably renders rotation for certain NPCs. Note vanilla rotation for 248: atan2(-vy, -vx); 247: atan2(vy, vx). I'll port exactly.

Also note: in state 0 else-branch: `velocity = x*num4...` where num4 = num3/num4(dist) → velocity = delta * (num3/dist) → speed num3 toward shoulder. And in state 0 if-branch (close): velocity = delta exactly (snap). Then position integration happens by the shared physics.

Collision: fists have noGravity (flying). Our move: x += vx; y += vy, plus custom collision? Since state 2 sets noTileCollide false mid-flight (to stop at walls)... For simplicity, I'll implement collision via a copied collideGround-like helper? That only handles axis-aligned walls — actually for the fist I need collideX/collideY detection to end the punch. I'll use a simple solid check: if the fist's AABB center enters a solid tile → treat as collide (end punch state, snap back a bit). I'll implement `hitSolid(game, e)` checking the tiles overlapped by the AABB. Use it for: ending punch when noTileCollide false; skip otherwise. Good.

Also body's jumping: AI_045:
- ai[0]==0 (grounded state):
  - if velocity.Y == 0: velocity.X *= 0.8; num4 = 1; if ai[1] > 0: num4 += 2 per missing part (fists/head), +1 if damaged, +4 if < half, +8 if < third; num4 *= num (1 or 2 enraged); (getGoodWorld +100 skip).
  - ai[1] += num4; if ai[1] >= 300: ai[1] = -20; frameCounter = 0.
  - else if ai[1] == -1: noTileCollide = true; TargetClosest; velocity.X = 4*direction; if life < lifeMax → velocity.Y = -12.1*(num+9)/10 (cap -19.1) else -12.1; ai[0] = 1; ai[1] = 0.
  
  Wait — where does ai[1] go from -20 to -1? The ai[1] += num4 happens in the `velocity.Y == 0` branch; so while grounded, ai[1] counts: starts -20 (after reaching 300), then -20 + 1 = -19... increments until it crosses... hmm, when ai[1] = -20, then next tick velocity.Y == 0 → ai[1] += num4 → -19 ... eventually reaches -1 → next tick ai[1] == -1 → jump! Wait but the check `else if (ai[1] == -1f)` — the else pairs with `if (velocity.Y == 0f)`. So while grounded ai[1] increments from -20 up; once ai[1] == -1 (i.e., after 19 ticks) the else branch fires? No — if velocity.Y == 0 is true, the else never runs. Hmm: when grounded, ai[1] increments: -20 → ... → -1 → 0 → 1... So when does the jump trigger? Let me re-read:

```
if (ai[0] == 0f)
{
    if (velocity.Y == 0f)
    {
        velocity.X *= 0.8f;
        float num4 = 1f;
        if (ai[1] > 0f) { ... num4 grows ... }
        ai[1] += num4;
        if (ai[1] >= 300f)
        {
            ai[1] = -20f;
            frameCounter = 0.0;
        }
        else if (ai[1] == -1f)
        {
            ... jump ...
        }
    }
}
```

Hmm wait, that's not what the code shows. Let me re-read the actual sed output around 19600-19630:

```
		if (ai[0] == 0f)
		{
			if (velocity.Y == 0f)
			{
				velocity.X *= 0.8f;
				float num4 = 1f;
				if (ai[1] > 0f) { ... }
				ai[1] += num4;
				if (ai[1] >= 300f)
				{
					ai[1] = -20f;
					frameCounter = 0.0;
				}
				else if (ai[1] == -1f)   <- wait this was "else if (ai[1] == -1f)"? 
```

The output shows:
```
				ai[1] += num4;
				if (ai[1] >= 300f)
				{
					ai[1] = -20f;
					frameCounter = 0.0;
				}
				else if (ai[1] == -1f)   -- hmm actually output shows "else if (ai[1] == -1f)"? 
```

Actually the first sed chunk (part 1) ended at:
```
				ai[1] += num4;
				if (ai[1] >= 300f)
				{
```
and part 2 began with:
```
				{
					ai[1] = -20f;
					frameCounter = 0.0;
				}
				else if (ai[1] == -1f)
				{
					noTileCollide = true;
					...
					ai[0] = 1f;
					ai[1] = 0f;
				}
```

Hmm wait, part 2's beginning shows:
```
			{
				ai[1] = -20f;
				frameCounter = 0.0;
			}
			else if (ai[1] == -1f)
```
Yes. But hold on — this structure is INSIDE `if (velocity.Y == 0f)`. So the sequence: grounded → ai[1] accumulates from 0 (or negative) upward; when it reaches >= 300 → ai[1] = -20. Next tick (still grounded): ai[1] += num4 → -20 + num4. If num4 == 1 → -19. When ai[1] == -1 → the else-if fires? No! It's `if (ai[1] >= 300) {...} else if (ai[1] == -1) {...}`. When ai[1] == -1 (after adding num4), the else-if check fires the SAME tick: -1 >= 300 false → check == -1 → true → jump! 

So: grounded accumulation: 0,1,2,...299,300 → set -20 → next tick ai[1] = -20 + num4; if num4 == 1: -19, not -1 → no jump; continues -18... after 19 ticks: -1 → jump! So there's a 20-tick "crouch" (frameCounter animation frames 0-4 over ai[1] -16..0 per FindFrame) then jump. So total grounded time = 300 + 20 ticks with num4 = 1. With damage/parts lost num4 grows (up to 1+2+2+2+1+4+8 = 20 per tick, ×2 enrage = 40).

But note the num4 growth only applies `if (ai[1] > 0f)` — during the negative (crouch) phase num4 = 1. OK.

So the port:
```
if (e.ai0 === 0) {
  if (grounded /* vy == 0 via onGround */) {
    e.vx *= 0.8;
    let num4 = 1;
    if (e.ai1 > 0) {
      if (!hasLeftFist) num4 += 2;
      if (!hasRightFist) num4 += 2;
      if (!hasHead) num4 += 2;
      if (e.hp < e.maxHp) num4 += 1;
      if (e.hp < e.maxHp/2) num4 += 4;
      if (e.hp < e.maxHp/3) num4 += 8;
      num4 *= num; // enrage
    }
    e.ai1 += num4;
    if (e.ai1 >= 300) { e.ai1 = -20; }
    else if (e.ai1 === -1) {
      // jump
      noTileCollide...; e.vx = 4 * dir; vy = -(12.1 or scaled); ai0 = 1; ai1 = 0;
    }
  }
}
```

Careful with num4 being fractional: `e.ai1 === -1` exact equality — with num4 integer values (1..40, possibly ×2 = still integer), ai1 stays integer. num = 1 or 2 → integer. Good.

Hmm wait — but what if num4 = 2 during crouch? During crouch ai1 <= 0 so num4 = 1 (unless enrage... num4 *= num happens INSIDE the ai1 > 0 block? Let me check: the code:
```
if (ai[1] > 0f)
{
    ... additions ...
    num4 *= num;
    if (Main.getGoodWorld) num4 += 100f;
}
ai[1] += num4;
```
Yes num4 *= num only inside ai1>0. OK.

Jump: velocity.X = 4 * direction. direction: vanilla NPC.direction = sign toward target (updated by TargetClosest). Our e.facing? Enemy.facing is sprite direction. In fighter AI facing is set. I'll compute direction = sign(player.cx - e.cx) each tick (TargetClosest approximation). e.facing = direction.

velocity.Y: if life < lifeMax → -12.1 * (num + 9)/10 → num=1: -13.31; enrage num=2: -13.31... (num+9)/10 with num=2 → 1.1 → -13.31? -12.1*1.1 = -13.31. Hmm vanilla damage jump is HIGHER: -12.1*(num+9)/10 where num here is the balance num (1) → -12.1*1 = -12.1. Wait (1+9)/10 = 1 → -12.1. With enrage num=2: (2+9)/10 = 1.1 → -13.31, cap -19.1.

- ai[0]==1 (jumping):
  - if velocity.Y == 0 (landed): sound Item14; ai[0] = 0; dusts + gores (spawn particles + playSfx).
  - else: TargetClosest; if player horizontally within body span → velocity.X *= 0.9; if body bottom above player top → velocity.Y += 0.2*(num+1)/2 (num=1 → 0.2); else: velocity.X += 0.2*direction; num7 = 3 (+1 damaged, +1 half, +1 quarter) * (num+1)/2 → classic 3..6; clamp vx to ±num7.
- Despawn: if no target or player dead → TargetClosest; if Manhattan dist > 3000 → TargetClosest, if still > 3000 → active = false. Port: if player null or manhattan dist > 3000 (after recheck) → e.dead = true? Careful: probe has player at fixed pos. Body will jump toward player, distance small. Fine — port it as despawn (e.dead = true). Hmm — with player null, TargetClosest fails → despawn. OK.

Body physics: gravity. Vanilla: noGravity is false for body → gravity applies via vanilla physics (0.3/tile? actual gravity 0.3 px/tick², max fall 10). Our GRAVITY constant — let me check constants: GRAVITY and MAX_FALL_SPEED exist (imported in Enemy.ts). I'll apply e.vy += GRAVITY clamped by MAX_FALL_SPEED when not onGround... but careful: vanilla checks `velocity.Y == 0f` for grounded, our onGround approximates. But there's subtlety: after landing, vanilla velocity.Y = 0 exactly. Our collideGround sets vy = 0 and onGround = true. But at jump start, vy = -12.1 → next tick gravity → -11.8 ≠ 0, so onGround false. Good.

But: in the jump state, the vanilla code adds +0.2 gravity manually?? No — vanilla gravity is applied by the shared NPC physics (gravity 0.3/tick for non-noGravity). Wait, actually vanilla applies gravity in UpdateNPC: `if (!noGravity) velocity.Y += 0.3f` (with maxFall). Hmm, vanilla gravity is 0.3. Let me check our GRAVITY constant value.

Also the vanilla jump speed -12.1 with gravity 0.3 → jump height = 12.1²/(2*0.3) = 244px ≈ 15 tiles. Golem jumps 15 tiles? That seems like a lot but temple is big; fine, 1:1.

Let me check constants GRAVITY value.

Another important detail: vanilla body walk speed 4*direction at jump; and during flight accel 0.2 toward direction up to num7 (3-6). The body doesn't walk on the ground otherwise (vx *= 0.8 each tick on ground). OK.

Also frameCounter-based FindFrame: body frames from ai[1] in state 0 (crouch animation) and frame.Y=1 in state 1 (jump). Our rendering uses Enemy animT/walkCycleT? Frame logic for boss NPCs probably handled in Renderer via ai1? Not my concern (rendering wired by main session). I can mention in report.

Now check GRAVITY & TILE constants.
````

</details>


---

## 🤖 Assistant · 2026-08-10T06:48:49.955Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"GRAVITY\\|MAX_FALL_SPEED\\|^export const TILE\" ~/Project/GLM/SandboxWorld/game/src/core/constants.ts",
 "description": "Check physics constants"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:48:49.974Z

**📎 ToolResult**

```
2:export const TILE = 16; // tile 尺寸（px）
5:export const GRAVITY = 0.36; // px/tick^2
6:export const MAX_FALL_SPEED = 9.5;
13:export const ENEMY_GRAVITY = 0.32;

```


---

## 🤖 Assistant · 2026-08-10T06:48:50.287Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,80p' ~/Project/GLM/SandboxWorld/game/src/entities/types.ts; grep -n \"groundLevel\\|rockLevel\\|clock\" ~/Project/GLM/SandboxWorld/game/src/entities/types.ts",
 "description": "Read GameHooks type"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:48:50.309Z

**📎 ToolResult**

```
// 实体与 Game 交互的接口（避免循环依赖，只放类型）
import type { World } from '../world/World';

export interface GameHooks {
  world: World;
  /** 主角(投射物命中判定用) */
  player: import('./Player').Player;
  /** 敌人列表(投射物命中判定用) */
  enemies(): unknown[];
  /** 小动物列表(弹幕命中判定用;近战挥砍在 Game 内直接遍历桶) */
  critters(): unknown[];
  /** 在世界上生成掉落物（返回实体便于染色等后处理） */
  spawnDrop(x: number, y: number, itemKey: string, count?: number, vx?: number, vy?: number): import('./ItemDrop').ItemDrop | null;
  /** 对玩家造成伤害（attacker 用于荆棘反伤） */
  damagePlayer(dmg: number, srcX: number, srcY: number, attacker?: unknown): void;
  /** 伤害数字飘字 */
  addDamageNumber(x: number, y: number, amount: number, crit: boolean, color?: string): void;
  /** 弹幕砍 tileCut 物（Projectile.CutTiles 语义：箭扫过杂草/瓦罐 → Game 内部分流） */
  cutTile(x: number, y: number): void;
  /** 敌人死亡 */
  onEnemyKilled(key: string): void;
  /** 出生敌人 */
  spawnEnemy(key: string, x: number, y: number): void;
  /** 粒子 */
  spawnParticles(
    x: number, y: number, color: string, count: number, speed?: number,
    opts?: { life?: number; damp?: number; grav?: number },
  ): void;
  /** 拾取物品后刷新 UI（掉落物实体调用） */
  notifyInventoryChanged(): void;
  /** 播放音效 */
  playSfx(name: string, vol?: number): void; // vol 0-1 按距离衰减
  playSfxFiles(files: string[], vol?: number): void; // 怪物专属声效（原版文件名列表）
  /** 拾取物品时在主角旁飘出物品名 */
  showPickupLabel(itemKey: string): void;
}

```


---

## 🤖 Assistant · 2026-08-10T06:48:52.976Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
GameHooks has no groundLevel; bossAI.ts destroyerAI uses `game.world.groundLevel` — so World has groundLevel (non-optional). Good, and `game.world.clock.isDay`. World also has rockLevel.

Now Enemy.hurt semantics for iframes — check quickly how iframes/dontTakeDamage works and how `dead` is set. Check hurt() in Enemy.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:48:53.494Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"hurt(\\|dead = true\\|hp <= 0\\|iframes\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -30",
 "description": "Check hurt/dead semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:48:53.521Z

**📎 ToolResult**

```
109:      // "抗性"（hurt(): resist<0.9 才生效，kbx*(1-resist)）→ 换算 1-比例
136:  iframes = 0;
202:    if (this.iframes > 0) this.iframes--;
316:          if (d > TILE * 90) this.dead = true;
319:          if (this.despawnTimer <= 0) this.dead = true;
587:      this.dead = true;
1024:      if ((flee || this.iframes > 0) && this.onGround) {
1101:    // 受击逃离（iframes 刚触发时朝远离玩家方向窜）
1102:    if (this.iframes > 6 && player) {
1273:      if (dist > T * 120) this.dead = true;   // 漂远后消失(原版按距玩家 40~80 格剔除)
1401:  hurt(dmg: number, kbx: number, kby: number, game: GameHooks): boolean {
1402:    // Critter 兼容：critters 桶的调用方按 Critter.hurt(game) 单参调用；
1408:    if (this.iframes > 0) return false;
1413:    this.iframes = 8;
1420:    if (this.hp <= 0) {
1424:      this.dead = true;
1429:        for (let s: Enemy | null = head; s; s = s.wormNext) s.dead = true;

```


---

## 🤖 Assistant · 2026-08-10T06:48:55.088Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 66,
 "offset": 1400
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:48:55.099Z

**📎 ToolResult**

```
1400	  /** 受击。返回是否死亡 */
1401	  hurt(dmg: number, kbx: number, kby: number, game: GameHooks): boolean {
1402	    // Critter 兼容：critters 桶的调用方按 Critter.hurt(game) 单参调用；
1403	    // 原版小动物是 Enemy 进该桶，这里把 Game 对象重映射回 game 参、伤害取固定 5
1404	    if (typeof dmg === 'object' && dmg !== null) {
1405	      game = dmg as unknown as GameHooks;
1406	      dmg = 5; kbx = 0; kby = 0;
1407	    }
1408	    if (this.iframes > 0) return false;
1409	    // 原版 Main.CalculateDamageNPCsTake：dmg - defense*0.5，下限 1
1410	    const def = this.def.defense ?? 0;
1411	    dmg = Math.max(1, Math.round(dmg - def * 0.5));
1412	    this.hp -= dmg;
1413	    this.iframes = 8;
1414	    this.hpBarT = 240; // 受击后血条持续显示 4 秒
1415	    const resist = this.def.knockbackResist;
1416	    if (resist < 0.9) {
1417	      this.vx += kbx * (1 - resist);
1418	      this.vy += kby * (1 - resist);
1419	    }
1420	    if (this.hp <= 0) {
1421	      // 月总族(396/397/398)血尽不直死:原版 checkDead(:78841-78867)转为闭眼残肢/死亡演出,
1422	      // 转换逻辑在各自 AI 首行(hp<=0 → ai0 置态+满血续命),此处放行让 AI 下一 tick 接管
1423	      if (this.vanillaId === 396 || this.vanillaId === 397 || this.vanillaId === 398) return false;
1424	      this.dead = true;
1425	      // 蠕虫任一段死亡 → 整链同死（原版 realLife 共享生命，L18152-18156）
1426	      if (this.wormNext || this.wormFollow) {
1427	        let head: Enemy = this;
1428	        while (head.wormFollow) head = head.wormFollow;
1429	        for (let s: Enemy | null = head; s; s = s.wormNext) s.dead = true;
1430	      }
1431	      // 掉落
1432	      const rng = new RNG(Math.floor(Math.random() * 1e9));
1433	      for (const d of this.def.drops) {
1434	        if (rng.next() < d.chance) {
1435	          const n = rng.int(d.min, d.max);
1436	          if (n > 0) {
1437	            const drop = game.spawnDrop(this.cx, this.cy, d.item, n, rng.range(-1.5, 1.5), -2);
1438	            // 凝胶染色（CommonCode.ModifyItemDropFromNPC）：gel(item 23) 由 type 1 掉落且
1439	            // netID∉{-1,-2,-5,-6} → item.color = npc.color（当前渐变色）
1440	            if (drop && d.item === 'gel' && this.vanillaId === 1
1441	              && this.vanillaNetId !== -1 && this.vanillaNetId !== -2
1442	              && this.vanillaNetId !== -5 && this.vanillaNetId !== -6 && this.colorRGBA) {
1443	              drop.color = [...this.colorRGBA];
1444	            }
1445	          }
1446	        }
1447	      }
1448	      game.onEnemyKilled(this.key);
1449	      // 死亡专属声：Boss 咆哮；普通怪优先专属 killedSound，无则通用
1450	      if (this.def.boss) game.playSfx('roar');
1451	      else if (this.def.killedSound.length) game.playSfxFiles(this.def.killedSound);
1452	      else game.playSfx('killed');
1453	      // 死亡碎裂：与主角同款物理粒子（喷溅/落地反弹/停驻淡出），颜色按怪物类型
1454	      const [c1, c2, c3] = this.def.gore;
1455	      const big = this.def.boss || this.w > 40;
1456	      game.spawnParticles(this.cx, this.y + this.h * 0.3, c1, big ? 26 : 12, big ? 3.4 : 2.6, { life: 240, damp: 0.988, grav: 0.09 });
1457	      game.spawnParticles(this.cx, this.cy, c2, big ? 18 : 8, big ? 2.6 : 2.0, { life: 220, damp: 0.985, grav: 0.09 });
1458	      game.spawnParticles(this.cx, this.cy - this.h * 0.2, c3, big ? 12 : 6, big ? 3.0 : 2.3, { life: 200, damp: 0.988, grav: 0.09 });
1459	      return true;
1460	    }
1461	    // 受击：少量碎屑零散溅落（不大面积）
1462	    game.spawnParticles(this.cx, this.cy, this.def.gore[0], 5, 1.4, { life: 60 });
1463	    return false;
1464	  }
1465	

```


---

## 🤖 Assistant · 2026-08-10T06:51:20.232Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Important! `hurt()` sets dead=true when hp<=0 unless vanillaId in {396,397,398}. For golem (245/246/247/248), hp<=0 → dead immediately. So my AI's first-line checkDead handling would never fire for real gameplay damage (happens in hurt()). The main session will wire Enemy.ts (they said "主会话统一接线" and I must not modify Enemy.ts). So they'll presumably add 245-249 to that exemption list. My AI must still handle hp<=0 at the top line per the task ("本体/头血尽转换在各自 AI 首行处理(hp<=0 → 置态+按需满血续命)"). I'll do it and note in the report that Enemy.ts hurt() line 1423 needs 245/246/247/248 added for the conversion to be reachable in gameplay.

Wait, but careful: if hp<=0 and not exempted, dead=true and the enemy is removed from the list — the AI won't run. In the probe, I'll set hp manually (not via hurt), so AI runs. Fine. I'll note it in the wiring list.

Also for fists: vanilla fists when killed are dead (they drop nothing special). In our structure, fist hp<=0 → e.dead = true (normal death). But careful: if hurt() sets dead=true, then when the player kills a fist, it just dies — good. But probe: does anything need fist death handling? Task ⑤: head dies → whole family dies. OK.

Now, the head in attached mode: player damages head 246 (vanilla behavior — head is the phase-1 target). hp<=0 → checkDead-like: head enters free mode. But hurt() kills it... again wiring. In free mode, hp<=0 → head dies → whole family self-destructs.

So head AI top-line:
```
if (e.hp <= 0) {
  if (x.free) { // free head dead → kill family
    killFamily(game); e.dead = true; return;
  }
  // attached head dead → free mode (vanilla checkDead: 246 → spawn 249)
  enterFreeMode(e);  // hp refill, stats upgrade to 249 (dmg 80 def 32), ai3 = 1
}
```

Hmm wait — but if head dead triggers family kill via AI top-line, hurt() would have already set dead=true... The main session will add 245-248 to the exemption; then AI handles. Good.

Body top-line:
```
if (e.hp <= 0 && !x.dead) {
  x.dead = true; x.deadT = 0;  // dying animation; head will detect and go free
  e.hp = e.maxHp; // 续命 so it doesn't retrigger
  e.iframes = 2 (each tick)
}
```
Then body dying: particles, after 60t → e.dead = true.

Hmm, "本体死透后头继续" — head continues. Head detection: body.hp <= 0 handled how? If body refills hp to maxHp, head can't detect death via hp. Head needs to see x.dead. WeakMap is per-instance module-level — head can read body's WeakMap entry (same module!). Yes — golemX WeakMap is module-level, so head AI can check golemX.get(body)?.dead. 

Simpler and more observable: use body.ai3 as a dying flag (ai3 unused in vanilla body AI). Set e.ai3 = 1 when dying. Head checks body.ai3 === 1 → enter free mode. Fists check body.ai3 === 1 → anchor... hmm fists anchor body while dying? The body is exploding; vanilla anchors body regardless. I'll make fists anchor body while it's alive (not e.dead), including dying, then head after. That satisfies probe ④ (fist returns near "head" — wait probe ④ says "回位(记录拳位移峰值>100px 再回归头部附近)" — 回归头部附近 = near the head? "再回归头部附近" — hmm, "头部" here might loosely mean the anchor (shoulder). My fists anchor the body shoulder. The probe measures "回归头部附近" — distance to the head? To be safe: fist anchor = body if body not fully dead, else head. In probe ④, will the body be dead? Probe ④ runs the fist charge cycle — I control the probe order. I'll run the fist test while body alive, and measure return proximity to the SHOULDER point (body center + offset) — the task text says "回归头部附近" but shoulders are the actual anchor; I'll measure against both anchor and head to be lenient. Let me just measure distance to the anchor point (body-derived) < 100, and peak displacement > 100.

For probe ⑤: kill free head → all family dies. If body already dead (from ③), then family = fists. Check fists dead. But hmm — will fists punch during the test? They anchor head when body dead. When head dies, fists self-destruct. Good.

Actually wait, there's a subtlety in probe ⑤: after ③, head is free and body is dead. In ⑤, set head hp = 0 → head AI top: free && hp<=0 → kill family (fists) + head dead. Check all enemies dead. 

Now the fist punch condition requires the player to be on the correct side. Probe: player at (100*16, 140*16), body at (100*16, ~120*16) on floor y=150. Left fist 247 punches when player.Center.X < fist.Center.X + 100. If player is directly below, player.X == fist.X roughly → condition true for both. Good, so both fists will punch. But note: the punch trigger also requires ai1 >= 60 accumulation at the shoulder. The windup + charge: state 0 → 1 (windup 30t at shoulder) → 2 (fly at 12-48 speed until dist to shoulder > 700 or collide) → 0 (return at ≤32 speed). Punch speed num6: 12 (+4+4+10 if body damaged/half/quarter...). Body at full hp → 12. Distance to travel before returning: it flies until 700px from shoulder or hits a wall. Player is ~30 tiles below; world floor at y=150, body at y~140 (feet on 150). Fist at shoulder ~ (center). Punch toward player: downward-ish. Will it hit the floor? State 2 sets noTileCollide=false only after passing the player on the punch axis. Direction is mostly downward → passes player when Center.Y > player.Center.Y → then collision enabled → hits floor (y=150 solid) → collide → back to state 0. Displacement: from ~y 139*16 to 150*16 = 11 tiles = 176px > 100. 

But wait: the fake world in _mechprobe only sets floor at y=150 for x in 0..199, nothing else — open air. The fist punch downward will land on floor → good.

Hmm, but one thing: the fist state 0 homing: if dist < 12 + num3 → snap; it accumulates ai1; punches when ai1 >= 60 AND player on correct side. At 60 ticks of shoulder rest, punch triggers (player below → both conditions true). Then windup 30t (snapped to shoulder, dust), then launch 12 speed toward player, fly ~15 ticks to cover 176px... then pass player Y? Punch direction: player below fist by ~(140-139)*16... wait let me compute geometry. Body: 140 wide, 140 tall. Spawn at (100*16, 120*16) → center (1600, 1920+70=1990?) hmm — fromVanilla(id, x, y) sets center = (x, y)? `e.x = x - e.w/2; e.y = y - e.h/2;` → center at (x,y). So body center (1600, 1920). Floor top at y = 150*16 = 2400. Body bottom = 1920 + 70 = 1990 → falls to 2400-140 = 2260 (y), center 2330.

Player in mechprobe: cx 1600, cy 140*16 = 2240. So player is roughly at body level. Fine.

Fist shoulder: body.Center + (-42, -4.5) for 247 → (1558, ~2325). Player at (1600, 2240): player is BELOW-RIGHT of left fist. Punch dir mostly down. Passes player Y quickly (only ~85px below... fist at 2325, player cy 2240 → player is ABOVE the fist!). Hmm: player cy = 140*16 = 2240; body center cy after landing = 2400-70 = 2330; fist at 2325. So the player is 85px ABOVE the left fist → punch direction is UP-RIGHT toward the player. Fist flies up... passes player when Center.Y < player.Y → collision enabled → continues up into open air (no ceiling in fake world) → travels until dist to shoulder > 700 → then returns. 700px at 12 px/t = ~58 ticks. Peak displacement from shoulder ~700 > 100 ✓. Return at speed ≤32 → returns near shoulder ✓.

In the real game there's usually a ceiling, but fine.

Left fist punch condition: `type==247 && Center.X + 100 > player.Center.X` → 1558 + 100 = 1658 > 1600 ✓ punches.

Right fist 248: `Center.X - 100 < player.Center.X` → 1658-100... right fist shoulder x = 1600+39 = 1639 → 1639-100 = 1539 < 1600 ✓ punches.

Both punch. Peak displacement ~700. Good.

Now check: does the fist at state 0 keep ai1 accumulating only when close to shoulder? `if (num4 < 12f + num3)` where num4 = dist. When snapped (velocity = delta), it stays close → accumulates. Good.

Note the state 2 return condition uses `num2 > 700f` where num2 = dist to the CURRENT shoulder target computed at top of AI each tick (shoulder moves with body). Body is stationary on ground → fine.

Now — head free mode in probe ③: after body hp=0 → body dying → head goes free. Head free AI: seeks player + (0,-300) with speed 7, accel 0.05. Movement happens → "头的位移/状态变化" observable ✓. ai3 becomes 1 ✓.

Also, hmm — probe ③: "本体 hp→0 后头存活进入自主战斗". Body hp=0: my body AI top-line: hp<=0 → dying state + refill hp (so hurt()... probe sets hp directly). Also I should make sure body dying → head detects. Head check: `if (!x.free && (body missing || body dying)) enterFree`.

Wait — careful ordering: the body AI runs (sets dying), then head AI runs — order depends on array order (body pushed first). In the probe, enemies array order: body first, then spawned parts appended. So body AI runs first → dying set → head sees it same tick ✓.

But in the real game, order could be arbitrary — head checks each tick anyway. Fine.

Another subtlety: attached head while body alive — vanilla anchors head to body.Center + (-3, -57)*scale. Head follows the body. In probe ② (jump): body jumps toward player; head follows. ✓.

Now, the head's vanilla fireball loop in attached mode: 300-tick cycle, fires at end. Damage 18 proj 258 speed 8 from Center + (0, +10*scale). Head's ai[0] phase 1 (eye) at life < half.

Also vanilla head velocity: `if (num724 < num721) { velocity = delta }` — SNAP to anchor when within 100px (i.e., teleport-ish follow: velocity = full delta, applied next integration). Note: velocity = delta means it moves the full delta in one tick once — then next tick dist ~0 → velocity = 0-ish. Actually if velocity = delta and dist < 100, it moves by delta → arrives at anchor exactly, then dist ≈ 0 → delta ≈ 0 → velocity ≈ 0. So the head rides at the anchor. With body moving (jump vx=4), dist = 4px per tick → head moves 4px/tick. Effectively locked. rotation = velocity.X * 0.1 when far.

OK. Now write the code. Structure of bossAI_golem.ts:

```ts
// 石巨人 Boss 族 AI 1:1 移植:aiStyle 45 本体 245 / 46 头 246(挂载) / 47 拳 247,248 / 48 自由头(二阶段)
import type { Enemy } from './Enemy';
import type { GameHooks } from './types';
import type { Player } from './Player';
import { TILE, GRAVITY, MAX_FALL_SPEED } from '../core/constants';
import { spawnPart, shoot, accelTo, losClear, addEnemy } from './bossAI';
```

Wait: seek? The task says import spawnPart, shoot, seek, accelTo, losClear, addEnemy "从 './bossAI' 导入". I'll import what I use: spawnPart, shoot, accelTo, losClear. Maybe seek not needed since free-head uses custom target (player + (0,-300)) with accelTo — I can use accelTo directly. addEnemy needed? spawnPart already adds. Not needed unless I spawn the free head as new NPC (I don't — head transforms in place). I'll import only used ones to avoid unused-import lint (tsc noEmit with noUnusedLocals? check tsconfig). Let me check tsconfig for noUnusedLocals.

Constants:
```
const SCALE = 0.5; // SetDefaults: type 245-249 scale *= 0.5(NPC.cs:17943-17960)
```

Helper: family scan:
```
interface GolemFam { body, head (246), fistL(247), fistR(248) }
const scanFamily = (game) => {...}
```
Each AI needs different members; I'll write small helpers: findBody(game), findHead(game), findFists(game). Use `game.enemies() as Enemy[]`.

WeakMap state:
```
interface BodyX { dying: boolean; deadT: number; alpha: number; }
interface HeadX { free: boolean; alpha: number; l0: number; l1: number; }
interface FistX { state: number; alpha: number; noTC: boolean; }
```
But ai1 (Enemy field) is used as timers (vanilla ai[1]), ai2 for head eye-laser timer. Fist state in WeakMap per task's ai0=side decision.

Hmm wait — actually, reconsider: should fist state live in ai1..? Vanilla fist uses ai[0] state and ai[1] timer. Task demands ai0=侧别. So state in WeakMap, timer in ai1. And alpha per-instance in WeakMap (vanilla alpha field).

Enrage num: 
```
const balanceNum = (game, player) => {
  let num = 1;
  // getGoodWorld +2 (expert, 注释略)
  // 玩家不在神庙/丛林带 或 在地表以上 → num *= 2(NPC.cs:19453-19457)
  // 本工程无 ZoneLihzhardTemple/ZoneJungle 判定,退化为"玩家在地表以上"单条件
  if (player && player.cy < (game.world.groundLevel ?? 0) * TILE) num *= 2;
  return num;
};
```
Hmm `game.world.groundLevel` — World type has groundLevel? destroyerAI uses `game.world.groundLevel * TILE` directly and dukeEnraged uses `game.world.groundLevel || Math.floor(st.h*0.3)`. So it's a number on World. Good.

Now write golemAI (body):

```ts
export function golemAI(e, game, player) {
  const x = bodyXOf(e);
  // ---- checkDead 首行(原版无;本族语义:本体血尽 → 进入死亡演出,头转自由态继续) ----
  if (e.hp <= 0 && !x.dying) {
    x.dying = true; x.deadT = 0; e.hp = e.maxHp; e.ai3 = 1; // ai3=1 死亡标记(头/拳据此转锚)
    game.playSfx('roar', 0.9);
  }
  if (!e.bInit) {
    e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai3 = 0;
    e.alphaFade = false; x.alpha = 255;
    // localAI[0]==0 首帧生成(:19459-19467):拳 247(Center-84,-9)/248(+78,-9)/头 246(-3,-57)
    const mk = (id, ox, oy, side) => { const p = spawnPart(game, e, id); if (p) { p.x = e.cx + ox - p.w/2... }}
  }
```
Hmm positions: vanilla NewNPC((int)Center.X - 84, (int)Center.Y - 9, 247) → top-left = (cx-84, cy-9). Our p.x is top-left. So p.x = e.cx - 84; p.y = e.cy - 9. But spawnPart placed center at (cx,cy); overwrite p.x/p.y directly.

For fists set ai0 = side (-1/+1), bInit = true (so their own bInit doesn't reset alpha handling... they have their own bInit logic for alpha; set bInit = true and let their AI handle). Actually I'll let each part's AI do its own bInit (alpha init). Set p.ai0 = side for fists; head p.ai3 = 0.

Wait, but there's a catch: spawnPart assigns `p` from enemyCtor with id; ai0 default -1120 → fist AI reads e.ai0 as side. I set p.ai0 = side (-1 for 247, 1 for 248). But careful: fist AI also uses bInit to init. OK.

Continue body:

```
  // alpha 渐显(:19478-19485):alpha>0 → -10/tick,期间 ai[1]=0(蓄力计时冻结)
  if (x.alpha > 0) { x.alpha = Math.max(0, x.alpha - 10); e.spawnAlpha = Math.min(254, x.alpha); e.ai1 = 0; }
```
Hmm spawnAlpha: fromVanilla set spawnAlpha = 254 and alphaFade = true (fades 1/tick). I set e.alphaFade = false at bInit, drive myself. e.spawnAlpha = x.alpha (255→ but 254 clamp for rendering? renderer maps spawnAlpha to opacity presumably 1 - a/255). I'll set e.spawnAlpha = Math.min(254, x.alpha). Fine.

Dying branch:
```
  if (x.dying) {
    e.iframes = 2;            // dontTakeDamage
    e.vx *= 0.9; e.vy = 0;
    x.deadT++;
    if (x.deadT % 4 === 0) game.spawnParticles(...'#B04030'...);
    if (x.deadT >= 60) { e.dead = true; return; }   // 本体死透;头由自身 AI 继续
    return;  // 不再走战斗状态机
  }
```
Hmm — should the body keep physics during dying (fall to ground)? If dying mid-air it'd float. Add gravity: e.vy += GRAVITY... but vx*=0.9 and move + collide. I'll apply gravity + collideGround so it lands. OK.

Then the main body AI:

```
  const num = balanceNum(game, player);
  // 部件存活扫描(:19490-19512)
  const fam = scanFamily(game, e);  // hasHead/hasL/hasR
  // dontTakeDamage = 挂载头存活(:19513)——头 246 在场时本体无敌(原版一阶段语义)
  if (fam.hasHead) e.iframes = 2;
  
  // getGoodWorld 火把破坏(:19514-19534)略;拳缺失的断臂尘(:19544-19595)简化为粒子
  if (!fam.hasL) dust stub...
  if (!fam.hasR) ...
```
Dust for missing fists: simplified to spawnParticles occasionally. I'll include lightweight version: if (!hasL && aiT%10===0) spawnParticles at shoulder. OK.

```
  // 玩家缺失/死亡(:19468-19477):原版 TargetClosest 落空 → noTileCollide;此处近似静止
  if (!player) { gravity+collide; return; }
  const dir = Math.sign(player.cx - e.cx) || e.facing;  // TargetClosest direction
  e.facing = dir;

  if (e.ai0 === 0) {
    if (e.onGround || e.vy === 0) {
      e.vx *= 0.8;
      let num4 = 1;
      if (e.ai1 > 0) {
        if (!fam.hasL) num4 += 2;
        if (!fam.hasR) num4 += 2;
        if (!fam.hasHead) num4 += 2;
        if (e.hp < e.maxHp) num4 += 1;
        if (e.hp < e.maxHp / 2) num4 += 4;
        if (e.hp < e.maxHp / 3) num4 += 8;
        num4 *= num;
      }
      e.ai1 += num4;
      if (e.ai1 >= 300) { e.ai1 = -20; }
      else if (e.ai1 === -1) {
        // 跳(:19622-19637):vx=4*dir;受伤后跳更高 -12.1*(num+9)/10 钳 -19.1
        e.vx = 4 * dir;
        e.vy = e.hp < e.maxHp ? Math.max(-19.1, -12.1 * ((num + 9) / 10)) : -12.1;
        e.ai0 = 1; e.ai1 = 0;
      }
    }
  } else if (e.ai0 === 1) {
    if (e.onGround || e.vy === 0) {
      // 落地(:19641-19656):音效+尘+gore
      game.playSfx('roar', 0.4);
      game.spawnParticles(e.cx, e.y + e.h, '#9A8FA0', 14, 2.4, {life: 40});
      e.ai0 = 0;
    } else {
      if (e.x < player.x + player.w && e.x + e.w > player.x) {
        e.vx *= 0.9;
        if (e.y + e.h < player.y) e.vy += 0.2 * ((num + 1) / 2);
      } else {
        e.vx += 0.2 * dir;
        let num7 = 3;
        if (e.hp < e.maxHp) num7 += 1;
        if (e.hp < e.maxHp/2) num7 += 1;
        if (e.hp < e.maxHp/4) num7 += 1;
        num7 *= (num + 1) / 2;
        e.vx = clamp(e.vx, -num7, num7);
      }
    }
  }
  // 离场(:19676-19689):曼哈顿距离 > 3000 → 清除
  if (Math.abs(e.cx - player.cx) + Math.abs(e.cy - player.cy) > 3000) { e.dead = true; return; }
  // 重力+移动+落地(本族自积分)
  if (!e.onGround) { e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED); }  hmm
```

Wait gravity semantics: vanilla non-noGravity NPC: velocity.Y += 0.3 each tick (with max fall 10? actually vanilla gravity 0.3, max 10 for most, but NPC max fall = 10). Our GRAVITY = 0.36, MAX_FALL_SPEED 9.5 — used by other AIs. Vanilla golem gravity — actually vanilla gravity for NPCs is 0.3. Jump -12.1 with 0.3 → 244px height. With 0.36 → 203px. Meh. Which to use? kingSlimeAI used 0.35 custom. I'll use GRAVITY (0.36) for consistency with the engine, note as simplification? Actually to be closer to vanilla, use 0.3. Hmm, but jump height affects probe only via onGround toggling. I'll use vanilla 0.3 with cap 10 (vanilla NPC max fall speed 10). I'll define GOLEM_GRAVITY = 0.3, GOLEM_MAX_FALL = 10. Cleaner 1:1.

Grounded detection: vanilla `velocity.Y == 0f`. Our onGround from collideGround. But there's a subtle issue: when standing on ground, my code should apply gravity each tick so it keeps pressing down, then collideGround sets vy=0, onGround=true. So: always e.vy += 0.3 (before move), clamp 10, move, collide. Then `e.vy === 0` when grounded. I'll use (e.vy === 0) as the vanilla-accurate condition, since collideGround zeroes it. And onGround also set. Use `e.vy === 0` primarily.

collideGround copy: I'll copy the bossAI.ts private version (allowed explicitly) but maybe extend for the wide body: the bossAI version samples only center-x column for floor and ceiling, and single points for walls. Golem is 140px wide (8.75 tiles) — single-column collision will let it sink into floors at edges? Floor check at center column only: if the center column has floor, it snaps on top; edges overhang — acceptable (bossAI uses it for King Slime 84px). But a better approach: sample multiple columns. The vanilla Collision uses full AABB. I'll write a slightly extended collideGround sampling left/center/right columns for the floor and ceiling. That stays within my file. Walls: sample at cy (mid) and maybe top/bottom. Keep it simple: floor/ceiling across 3 columns (x, x+w/2, x+w), walls at cy.

Careful with snapping when multiple columns: take the highest floor top among solid columns? If any column solid at foot row and vy >= 0 → snap y to min(ty*TILE) - h among solid ones... vanilla snaps to the tile it collides with; with 3 samples, snapping to the smallest ty (highest floor) prevents sinking. I'll compute minY over solid columns: e.y = minTy*TILE - e.h.

Now the head AI (golemHeadAI, aiStyle 46 + free mode 48):

```ts
export function golemHeadAI(e, game, player) {
  const x = headXOf(e);
  const body = findBody(game);   // vanilla golemBoss(Main.npc[golemBoss])
  // ---- checkDead 首行 ----
  if (e.hp <= 0) {
    if (x.free) {
      // 自由头血尽 → 全族自毁(战斗结束;原版 245 死亡置 downedGolemBoss)
      e.dead = true;
      for (const n of game.enemies() as Enemy[]) if (!n.dead && n.vanillaId >= 245 && n.vanillaId <= 248) n.dead = true;
      return;
    }
    // 挂载头血尽 → 自由态(原版 checkDead HitEffect :85842-85847 在原地 NewNPC 249;
    //  本工程头原体变身,属性对齐 249 SetDefaults)
    enterFree(e, game);
  }
  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; e.alphaFade = false; x.alpha = 255; }
  // alpha 渐显(:31287-31294 / :31541-31548):期间 ai[1]=30(自由头)或 0(挂载头)
  if (x.alpha > 0) { x.alpha -= 10...; e.ai1 = x.free ? 30 : 0; }
```
Wait vanilla head 46: alpha>0 → ai[1] = 30. Free head 48: no alpha handling (249 spawns with alpha default 0? 249 SetDefaults has no alpha → 0). So only attached head fades. And attached: ai[1] = 30 while fading.

Free-mode detection: if !x.free && (!body || bodyDeadFlag) → enterFree. Where bodyDeadFlag = body.ai3 === 1 (my dying flag) or !body (missing). Also if body.hp <= 0 (in case wiring refill didn't happen... hp<=0 handled by body itself). I'll check `!body || body.ai3 === 1 || body.hp <= 0`.

enterFree:
```
const enterFree = (e, game) => {
  const x = headXOf(e);
  x.free = true; e.ai3 = 1;
  e.hp = e.maxHp;            // 原版 NewNPC 249 满血
  const b = baseOf(e); b.dmg = 80; b.def = 32;  // 249 SetDefaults damage/defense(NPC.cs:12139-12149)
  e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
  game.spawnParticles(e.cx, e.cy, '#C04030', 16, 2.5, { life: 30 });
};
```

Attached mode (vanilla 46):
```
if (!x.free) {
  // vanilla: noTileCollide = true(飞行,穿墙)
  const num = balanceNum(game, player);
  // 锚点 = 本体.Center + 本体.velocity + (-3*scale, -57*scale)(:31292-31296)
  let dx = (body.cx + body.vx) - e.cx - 3 * SCALE;
  let dy = (body.cy + body.vy) - e.cy - 57 * SCALE;
  const dist = Math.hypot(dx, dy);
  if (dist < 100) { e.spin = 0; e.vx = dx; e.vy = dy; }
  else { e.vx = dx / dist * 100; e.vy = dy / dist * 100; e.spin = e.vx * 0.1; }
  ...
}
```
Hmm wait — velocity = delta when close means the head teleports to anchor in one tick. Vanilla does exactly that (velocity = delta, integrated same tick). OK.

Then the fireball/eye logic (ai[0] = 0 or 1 phase) — vanilla at the END sets ai[0] = life < lifeMax/2 ? 1 : 0. And the attack logic branches on ai[0]. Port in same order: anchor movement, alpha, then attack logic using current ai0, then re-derive ai0 from hp at the end.

For player null in attached mode: skip attacks.

Phase 0 (mouth fireball, :31310-31347):
```
e.ai1 += 1;
const n = 300;
if (e.ai1 < 20 || e.ai1 > n - 20) { e.ai1 += 2 * (num - 1) / 3; x.l0 = 1; }  // localAI[0] = 1(张嘴帧)
else { e.ai1 += 1 * (num - 1) / 2; x.l0 = 0; }
if (e.ai1 >= n) {
  e.ai1 = 0;
  // vector84 = Center + (0, 10*scale);proj 258 速 8 伤 18
  shootMouth(e, game, player, 10 * SCALE, 8, 18);
}
```

Phase 1 (eye, :31348-31464):
```
const ox0 = player.cx < e.cx - e.w ? -1 : player.cx > e.cx + e.w ? 1 : 0;  // localAI[1]
x.l1 = ox0;
let v85x = e.cx + (ox0 === -1 ? -40*SCALE : ox0 === 1 ? +40*SCALE : 0);
let v85y = e.cy + 10 * SCALE;
const num733 = (num + 3) / 4;
e.ai1 += num733;
if (e.hp < e.maxHp*0.4) e.ai1 += num733;
if (e.hp < e.maxHp*0.2) e.ai1 += num733;
x.l0 = (e.ai1 < 20 || e.ai1 > 280) ? 1 : 0;
if (e.ai1 >= 300) { e.ai1 = 0; shootFireball from v85 speed 8 dmg 24 }
e.ai2 += num733;
if (e.hp < e.maxHp/3) e.ai2 += num733;
if (e.hp < e.maxHp/4) e.ai2 += num733;
if (e.hp < e.maxHp/5) e.ai2 += num733;
if (!losClear(game, e.cx, e.cy, player.cx, player.cy)) e.ai2 += 4;
if (e.ai2 > 60 + Math.random() * 600) {
  e.ai2 = 0;
  fire eye lasers proj 259 dmg 28 speed 11 (or 12)
}
```
Eye laser firing details: if localAI[1] == 0 → two projectiles from (cx ± 18*scale, cy - 22*scale), speed 11, aim player center; spawn offset += v*3; timeLeft 300. Else one from (cx + (localAI[1]==-1 ? -30 : +30)*scale, cy - 22*scale), speed 12. Note the vanilla: `float num745 = 11f` for the two-shot branch, `float num750 = 12f` for the single. Damage num742 = 28 both.

Aim: `Main.player[target].position.X + width*0.5 - vector85.X` → aim at player center. velocity = normalize * speed; spawn at vector85 + velocity*3.

Then ai[0] re-derivation: `if (life < lifeMax/2) ai[0] = 1 else 0`.

Free mode (vanilla 48) — as analyzed, with own-hp-driven pacing:
```
} else {
  // noTileCollide / flag48(:31503-31514)
  const noLos = !losClear(game, e.cx, e.cy, player.cx, player.cy);
  // 穿墙(原版 flag48 → noTileCollide=true;flag49 联动弹幕预判)
  const num = balanceNum(game, player);
  // 移动(:31521-31564):目标 = 玩家 + (0,-300),7 速/0.05 步进
  e.vx = accelTo(e.vx, dx/d*7, 0.05); e.vy = accelTo(e.vy, dy/d*7, 0.05);
  const num761 = (num + 4) / 5;
  e.ai1 += num761;
  // 原版按 golemBoss.life 分档;二阶段本体已亡 → 用头自身血量分档(简化项)
  const r = e.hp / e.maxHp;
  if (r < 0.8) e.ai1 += num761; ... 0.6, 0.2, 0.1
  x.l0 = (e.ai1 < 20 || e.ai1 > 280) ? 1 : 0;
  if (noLos) e.ai1 = 20;
  if (e.ai1 >= 300) { fire proj 258 dmg 20 speed 8 from (cx, cy - 10*SCALE) }
  // 眼激光
  e.ai2 += num;   // num755 = balance num (1 or 2)
  thresholds 1/1.25(0.8), 1/1.5(0.667), 1/2, 1/3, 1/4, 1/5, 1/6
  if (noLos) e.ai2 += num * 10;
  if (e.ai2 > 100 + Math.random()*4800) {
    e.ai2 = 0;
    for (i in 0..1) {
      let dmg = 24, spd = 11;
      if (r < 0.5) { dmg++; spd += 0.25 }
      if (r < 0.4) ... 0.3, 0.2, 0.1
      aim = player center (+lead if noLos: px += player.vx * Math.random() * 50)
      if (noLos) { dmg = Math.floor(dmg*1.5); spd *= 2.5; }
      spawn at (cx + (i===0?-14:14)*SCALE, cy - 50*SCALE) + v*3, timeLeft 300, proj 259
    }
  }
}
e.x += e.vx; e.y += e.vy;
```

Note Math.random()*4800 each tick — vanilla uses Main.rand.Next(4800) → fresh random each tick, threshold effectively random. Keep.

Also free head `flag49` in vanilla = no LOS between golemBoss and player. I use head↔player LOS (noLos). Slight difference; document.

Fist AI (golemFistAI, aiStyle 47, NPC.cs:19171):

```
export function golemFistAI(e, game, player) {
  const x = fistXOf(e);
  if (!e.bInit) { e.bInit = true; e.ai0 = side(e); e.ai1 = 0; e.alphaFade = false; x.alpha = 255; }
  const side = e.ai0 || (e.vanillaId === 247 ? -1 : 1);
  const body = findBody(game);
  const head = findHead(game);
  // 锚主:本体存活(含死亡演出中)→ 本体;本体死透 → 自由头;皆无 → 自毁(:19182-19186)
  let anchor: Enemy | null = body && !body.dead ? body : (head && !head.dead ? head : null);
  // 头死(全族终结)→ 自毁
  if (!anchor) { e.dead = true; return; }
  ...
}
```
Hmm: careful — head reference: findHead finds 246 which is the same head entity always (free mode in place). When head dead → anchor null → fist dies ✓ (probe ⑤, though in probe ⑤ the body may already be dead so anchor = head; head dies → anchor null → fist dead ✓).

Edge: body dead && head missing because body spawned without head? anchor = head... fine.

Continue:
```
  const num = balanceNum(game, player);
  if (x.alpha > 0) { x.alpha = max(0, x.alpha-10); e.spawnAlpha = ...; e.ai1 = 0; }
  // 肩锚点(:19197-19199):锚主.Center + 锚主.velocity + (side 偏移, -9*scale)
  const offX = e.vanillaId === 247 ? -84 : 78;
  const tx = anchor.cx + anchor.vx + offX * SCALE;
  const ty = anchor.cy + anchor.vy - 9 * SCALE;
  let dx = tx - e.cx, dy = ty - e.cy;
  const dist = Math.hypot(dx, dy);
  e.facing = -side;  // 镜像朝向(渲染)
  if (!player) { e.x += e.vx; e.y += e.vy; return; }   // 玩家缺失:保持
  
  switch (x.state) {
    case 0: { // 归位/待机蓄力(:19208-19263)
      // noTileCollide = true(穿墙)
      let num3 = 14;
      if (e.hp < e.maxHp/2) num3 += 3;
      if (e.hp < e.maxHp/4) num3 += 3;
      if (anchor.hp < anchor.maxHp) num3 += 8;
      num3 *= (num + 3) / 4;
      if (num3 > 32) num3 = 32;
      if (dist < 12 + num3) {
        e.spin = 0; e.vx = dx; e.vy = dy;
        let inc = num;
        e.ai1 += inc;
        if (e.hp < e.maxHp/2) e.ai1 += inc;
        if (e.hp < e.maxHp/4) e.ai1 += inc;
        if (anchor.hp < anchor.maxHp) e.ai1 += 10 * inc;
        if (e.ai1 >= 60) {
          if ((e.vanillaId === 247 && e.cx + 100 > player.cx) || (e.vanillaId === 248 && e.cx - 100 < player.cx)) {
            e.ai1 = 0; x.state = 1;
          } else e.ai1 = 0;
        }
      } else {
        e.vx = dx / dist * num3; e.vy = dy / dist * num3;
        e.spin = e.vanillaId === 247 ? Math.atan2(e.vy, e.vx) : Math.atan2(-e.vy, -e.vx);
      }
      break;
    }
    case 1: { // 蓄力(贴肩 30t,:19264-19324)
      e.ai1 += 1;
      e.x = tx - e.w/2; e.y = ty - e.h/2;   // Center = vector
      e.spin = 0; e.vx = 0; e.vy = 0;
      if (e.ai1 <= 15) spawn dust (simplified particles)
      if (e.ai1 >= 30) {
        x.noTC = true;
        x.state = 2; e.ai1 = 0;
        let num6 = 12;
        if (e.hp < e.maxHp/2) num6 += 4;
        if (e.hp < e.maxHp/4) num6 += 4;
        if (anchor.hp < anchor.maxHp) num6 += 10;
        num6 *= (num+3)/4; if (num6 > 48) num6 = 48;
        const pdx = player.cx - e.cx, pdy = player.cy - e.cy;
        const pd = Math.hypot(pdx, pdy) || 1;
        e.vx = pdx/pd*num6; e.vy = pdy/pd*num6;
        e.spin = e.vanillaId === 247 ? Math.atan2(-e.vy, -e.vx) : Math.atan2(e.vy, e.vx);
      }
      break;
    }
```
Wait, careful with the rotation sign conventions in state 0 vs 2! Let me re-read:

State 0 else branch (:19254-19262):
```
num4 = num3 / num4;   // num4 was dist
velocity.X = x * num4; velocity.Y = y * num4;
rotation = Atan2(0 - velocity.Y, 0 - velocity.X);   // = atan2(-vy, -vx) for 248
if (type == 247) rotation = Atan2(velocity.Y, velocity.X);  // 247: atan2(vy, vx)
```
So state 0 (returning): default atan2(-vy,-vx); 247 → atan2(vy,vx).

State 2 launch (:19322-19328):
```
rotation = Atan2(velocity.Y, velocity.X);
if (type == 247) rotation = Atan2(-velocity.Y, -velocity.X);
```
So state 2: default atan2(vy,vx); 247 → atan2(-vy,-vx). Opposite of state 0! Interesting (sprite orientation: when returning the fist faces outward...). Port exactly as above (I had it backwards; fix).

State 2 (flying, :19329-19404):
```
x.state===2:
  e.ai1 += 1;
  if (e.ai1 === 1) game.playSfx('roar', 0.5);  // SoundID.Item14
  dust trail (simplified)
  // 过轴判定(:19363-19388):冲过玩家主轴 → 关闭穿墙
  if (Math.abs(e.vx) > Math.abs(e.vy)) {
    if (e.vx > 0 && e.cx > player.cx) x.noTC = false;
    if (e.vx < 0 && e.cx < player.cx) x.noTC = false;
  } else {
    if (e.vy > 0 && e.cy > player.cy) x.noTC = false;
    if (e.vy < 0 && e.cy < player.cy) x.noTC = false;
  }
  if (dist > 700 || (x.collide && !x.noTC)) { x.noTC = true; x.state = 0; }
```
Hmm vanilla: `if (num2 > 700f || collideX || collideY) { noTileCollide = true; ai[0] = 0f; }`. collideX/collideY only occur when noTileCollide false (after passing player). So: if (!x.noTC && hitSolid(game, e)) → return to state 0. Port:
```
const hit = !x.noTC && hitSolid(game, e);
if (dist > 700 || hit) { x.noTC = true; x.state = 0; }
```

State 3 (unreachable legacy :19406-19446): keep ported for completeness with a comment (vanilla never sets ai[0]=3 in this build). Actually should I include? The dispatch `else { if (ai[0] != 3f) return; ... }`. It's dead code in vanilla (nothing sets 3). I'll include a compact port for 1:1 completeness.

State 3: noTileCollide = true; fly toward player at 12 speed with 0.4 accel (double-step on sign flip = accelTo); rotation like state 0's convention (atan2(-vy,-vx), 247 flipped). Let me verify: state 3 (:19437-19444):
```
rotation = Atan2(velocity.Y, velocity.X);
if (type == 247) rotation = Atan2(0 - velocity.Y, 0 - velocity.X);
```
Same as state 2 convention.

Movement: x.state 0/2/3 integrate position: e.x += vx; e.y += vy. State 1 sets position directly.

Also the fist during flight with noTC: pass through walls. With !noTC: collide — my hitSolid check plus maybe pushback. Simple: if hit solid and !noTC → end punch. Additionally prevent embedding: if hitSolid while noTC... nothing.

Now — a question: does e.spin need normalization? Renderer may use spin for rotation. Leave raw.

findBody/findHead/findFists:
```
const findBody = (game) => (game.enemies() as Enemy[]).find(n => !n.dead && n.vanillaId === 245) ?? null;
const findHead = (game) => (game.enemies() as Enemy[]).find(n => !n.dead && n.vanillaId === 246) ?? null;
```
For the body AI itself, scanning family: count 246/247/248 among enemies (excluding self — self is 245 so fine).

baseOf WeakMap:
```
const baseStats = new WeakMap<Enemy, {dmg:number; def:number}>();
```

Also for the head when entering free: update e.def.damage/defense directly from base cache each tick (like other AIs set from base). In free mode set e.def.damage = 80, defense = 32 each tick (from mutated base). In attached mode restore base values. Simpler: each tick at top of head AI: `const b = baseOf(e); if (x.free) { e.def.damage = 80; e.def.defense = 32 } else { e.def.damage = b.dmg; e.def.defense = b.def }` — but 80/32 should come from data (vanillaNpc(249))? I can import vanillaNpc from '../data/vanillaNpcs' — check its export path & VanillaNpc type. Enemy.ts imports { vanillaNpc } from '../data/vanillaNpcs'. I'll do the same: `const free = vanillaNpc(249); if (free) { damage: free.damage, defense: free.defense }`. That's data-driven and clean. 

Let me check data/vanillaNpcs.ts exports quickly.

Also Enemy type has `vanilla?: VanillaNpc` — VanillaNpc has damage?: number. Check.

Sound effects: game.playSfx('roar', vol) used elsewhere; the fist launch uses SoundID.Item14 — approximate with 'roar'? Meh — check available sfx names... bossAI uses 'roar' only. I'll use game.playSfx('roar', 0.5). Fine, documented.

Body landing sound Item14 → 'roar' 0.4.

Now — one more vanilla detail for the body: `noTileCollide = true` is set at jump start (:19623) — meaning the golem jumps THROUGH walls (temple). And later `if (noTileCollide && !player.dead) { if (velocity.Y > 0 && Bottom.Y > player.Top.Y) noTileCollide = false; else if (CanHit && !SolidTiles) noTileCollide = false; }` (:19601-19613). So during the jump it phases through tiles until falling below the player's top or having clear LOS. Port:
```
if (x.noTC && player && !player.dead) {
  if (e.vy > 0 && e.y + e.h > player.y) x.noTC = false;
  else if (losClear(game, e.cx, e.cy, player.cx, player.cy) && !inSolidBox(game, e)) x.noTC = false;
}
```
inSolidBox ≈ Collision.SolidTiles(position, width, height) — check if any solid tile overlaps AABB. I'll write solidTiles(game, e) helper. But note: my collideGround will fight with noTC: when noTC, skip collision (just move). When !noTC, collide. And gravity always.

Also vanilla sets noTileCollide=true at jump start each jump; my x.noTC default false; at jump: x.noTC = true. After landing, noTC stays false. Vanilla leaves noTileCollide=true until the check clears it. Fine.

Also vanilla body movement during phase: when noTC the body passes through the floor? It jumps up through ceiling — yes that's the temple behavior (jumps through the temple floor/ceiling). OK.

Now — the probe: player.dead false, world clock night (golem doesn't flee anyway). Note Enemy.fixedUpdate's despawn: `if (!this.def.boss)` — golem body 245 is in VANILLA_BOSS_IDS → def.boss = true → no despawn ✓. Fists/head not boss → they're subject to despawn if d > TILE*120! In the probe, distances are small ✓. In gameplay, the head flying -300 above player could exceed 120 tiles? No, -300px is fine.

Wait, actually there's a real issue: fists during a 700px punch → d to player maybe > 120 tiles? No, 700px < 120*16=1920 ✓.

Another important check: Enemy.fixedUpdate dispatch — since I can't modify Enemy.ts, in the probe the AI functions won't be dispatched by aiStyle! The probe calls fixedUpdate which routes aiStyle 45/46/47 to `default: zombieAI`. So the probe must call golemAI etc. directly. Look at _mechprobe: it relies on Enemy.ts dispatch (case 30-37 wired). For golem, not wired yet. So my probe must call the exported functions directly:

```
import { golemAI, golemHeadAI, golemFistAI } from '../src/entities/bossAI_golem.ts';
const run = (ticks) => { for (...) for (const e of [...enemies]) { e.fixedUpdate(1/60, game); if (e.vanilla?.aiStyle === 45) golemAI(e, game, player); ... } };
```
Careful: fixedUpdate already ran zombieAI for these (aiStyle 45 default → zombieAI) which may move them! zombieAI applies gravity/walk — that would corrupt the state. Hmm. Look at how _dukemlprobe.mts handles this (duke/moonlord were also unwired at probe time?). Let me check _dukemlprobe.mts.
````

</details>


---

## 🤖 Assistant · 2026-08-10T06:51:20.592Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,60p' ~/Project/GLM/SandboxWorld/game/scripts/_dukemlprobe.mts",
 "description": "Read duke/moonlord probe header"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:51:20.617Z

**📎 ToolResult**

```
// 猪鲨鱼龙 370(AI_069)+ 月亮领主 398/397/396(aiStyle 77/78/79)冒烟探针
// 直接驱动 bossAI_duke_moonlord 的导出 AI(Enemy.ts 分发由主会话统一接线,此处不依赖)
import { Enemy } from '../src/entities/Enemy.ts';
import { TileStore } from '../src/world/TileStore.ts';
import { World } from '../src/world/World.ts';
import { dukeFishronAI, dukeBubbleAI, moonLordCoreAI, moonLordHandAI, moonLordHeadAI } from '../src/entities/bossAI_duke_moonlord.ts';

const st = new TileStore(200, 300);
const world = new World(200, 300, 1, 't');
world.store = st;
world.groundLevel = 60;
world.rockLevel = 190;
for (let x = 0; x < 200; x++) st.setTileSilent(x, 150, 1); // 地板
const enemies: Enemy[] = [];
const projectiles: unknown[] = [];
const game = {
  world,
  player: null as never,
  enemies: () => enemies,
  spawnDrop: () => null, damagePlayer: () => {}, addDamageNumber: () => {}, cutTile: () => {},
  onEnemyKilled: () => {}, spawnEnemy: () => {}, notifyInventoryChanged: () => {}, showPickupLabel: () => {},
  spawnParticles: () => {}, playSfx: () => {}, playSfxFiles: () => {},
  entities: (() => {
    const wrap = {
      nextId: 2,
      add: (e: Enemy, b?: string) => {
        e.id = wrap.nextId++;
        if (b === 'projectiles') projectiles.push(e); else enemies.push(e);
      },
    };
    return wrap;
  })(),
} as never;

let ok = 0, bad = 0;
const check = (n: string, c: boolean, x?: unknown) => { if (c) { ok++; console.log('  ✓ ' + n); } else { bad++; console.log('  ✗ ' + n, x ?? ''); } };

/** 玩家桩(x/y tile 坐标可变) */
const mkPlayer = (tx: number, ty: number) => ({
  x: tx * 16, y: ty * 16, w: 20, h: 42,
  cx: tx * 16 + 10, cy: ty * 16 + 21, vx: 0, vy: 0, dead: false,
});
let player: ReturnType<typeof mkPlayer> = mkPlayer(100, 140);
(game as unknown as { player: unknown }).player = player;

/** aiStyle 局部分发(等同主会话将接入 Enemy.fixedUpdate 的映射) */
const aiByStyle: Record<number, (e: Enemy, g: never, p: unknown) => void> = {
  69: (e, g, p) => dukeFishronAI(e, g as never, p as never),
  70: (e, g, p) => dukeBubbleAI(e, g as never, p as never),
  77: (e, g, p) => moonLordCoreAI(e, g as never, p as never),
  78: (e, g, p) => moonLordHandAI(e, g as never, p as never),
  79: (e, g, p) => moonLordHeadAI(e, g as never, p as never),
};
const run = (ticks: number) => {
  for (let i = 0; i < ticks; i++) {
    for (const e of [...enemies]) {
      if (e.dead) continue;
      // 模拟 Enemy.fixedUpdate 头段:每 tick 先递减 iframes(直接调 AI 不会走共享尾段)
      if (e.iframes > 0) e.iframes--;
      const fn = aiByStyle[e.vanilla?.aiStyle ?? -1];

```


---

## 🤖 Assistant · 2026-08-10T06:51:21.294Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"export function vanillaNpc\\|export interface VanillaNpc\\|damage\\|defense\" ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts | head",
 "description": "Check vanillaNpcs data module"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:51:21.315Z

**📎 ToolResult**

```
42:export function vanillaNpcDrops(id: number): Array<{ item: string; min: number; max: number; chance: number }> {
57:export interface VanillaNpc {
62:  damage: number;
63:  defense: number;
85:export function vanillaNpc(id: number): VanillaNpc | null {

```


---

## 🤖 Assistant · 2026-08-10T06:51:23.046Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '60,140p' ~/Project/GLM/SandboxWorld/game/scripts/_dukemlprobe.mts",
 "description": "Read duke probe run loop and assertions"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:51:23.065Z

**📎 ToolResult**

```
      const fn = aiByStyle[e.vanilla?.aiStyle ?? -1];
      if (fn) fn(e, game as never, player);
    }
  }
};
const movePlayer = (tx: number, ty: number) => {
  player = mkPlayer(tx, ty);
  (game as unknown as { player: unknown }).player = player;
};
world.clock.timeOfDay = 0.0; // 夜晚
const DUKE_T = { spawnPlus: 80 } as const; // 出生 75t + 余量(与源文件 DUKE.spawnT 一致)

// =============== 1) 猪鲨 370 ===============
console.log('== Duke Fishron 370 ==');
{
  movePlayer(100, 55); // 地表上方(非狂暴:不在太空/地下/海洋带外)
  enemies.length = 0; projectiles.length = 0;
  const duke = Enemy.fromVanilla(370, 100 * 16, 30 * 16)!;
  duke.id = 1; enemies.push(duke);
  run(1);
  check('首帧 ai0=-1 出生态', duke.ai0 === -1, duke.ai0);
  run(DUKE_T.spawnPlus); // 出生 75t + 余量
  check('出生后进入悬浮 ai0=0', duke.ai0 === 0, duke.ai0);
  const startProj = projectiles.length;
  const startBub = enemies.filter((e) => e.vanillaId === 371).length;
  run(1400); // 一阶段整循环:5 连冲→泡泡弹→4 冲→鲨鱼龙卷
  check('发生位移', Math.abs(duke.cx - 100 * 16) > 8 || Math.abs(duke.cy - 30 * 16) > 8,
    [Math.round(duke.cx / 16), Math.round(duke.cy / 16)]);
  check('发射过弹幕(385/407)', projectiles.length > startProj, projectiles.length - startProj);
  check('吐过爆裂泡泡(371)', enemies.filter((e) => e.vanillaId === 371).length > startBub,
    enemies.filter((e) => e.vanillaId === 371).length - startBub);
  check('身体旋转角有值', Math.abs(duke.spin) > 0.01, duke.spin.toFixed(2));

  // ② 半血 → 二阶段(4 变身 → 5 循环;伤害 1.2×/防御 0.8×)
  const baseDmg = Enemy.fromVanilla(370, 0, 0)!.def.damage;
  const baseDef = Enemy.fromVanilla(370, 0, 0)!.def.defense ?? 0;
  duke.hp = Math.floor(duke.maxHp * 0.4);
  let entered = false;
  for (let i = 0; i < 400 && !entered; i++) { run(1); if (duke.ai0 === 4 || duke.ai0 >= 5) entered = true; }
  check('半血触发变身(ai0=4/5)', entered, duke.ai0);
  for (let i = 0; i < 400 && duke.ai0 !== 5; i++) run(1);
  check('进入二阶段 ai0=5', duke.ai0 === 5, duke.ai0);
  run(1); // 修正值在状态切换的下一 tick 生效(原版 damage/defense 置顶计算)
  check('二阶段伤害×1.2', duke.def.damage === Math.round(baseDmg * 1.2), [duke.def.damage, baseDmg]);
  check('二阶段防御×0.8', duke.def.defense === Math.round(baseDef * 0.8), [duke.def.defense, baseDef]);
  const p2 = projectiles.length;
  run(1200); // 二阶段循环:3 连冲→旋转泡泡冲刺→龙卷
  check('二阶段持续发射', projectiles.length > p2, projectiles.length - p2);
  const phases = new Set<number>();
  for (let i = 0; i < 1600; i++) { run(1); phases.add(duke.ai0); }
  check('二阶段状态集含 6/7/8', [6, 7, 8].every((s) => phases.has(s)), [...phases].sort().join(','));
}

// =============== 2) 月亮领主 398 核心 + 397 手 + 396 头 ===============
console.log('== Moon Lord 398 ==');
{
  movePlayer(100, 140);
  enemies.length = 0; projectiles.length = 0;
  const core = Enemy.fromVanilla(398, 100 * 16, 80 * 16)!;
  core.id = 1; enemies.push(core);
  run(1);
  check('首帧 ai0=-1 出生演出', core.ai0 === -1, core.ai0);
  run(60); // 60t 演出结束 → 生成部件
  const hands = enemies.filter((e) => e.vanillaId === 397);
  const heads = enemies.filter((e) => e.vanillaId === 396);
  check('生成双手 397×2', hands.length === 2, hands.length);
  check('生成头 396', heads.length === 1, heads.length);
  check('部件锚定核心(ai3=core.id)', [...hands, ...heads].every((p) => p.ai3 === core.id));
  check('双手侧别 ±1(ai2=0/1)', hands.some((h) => h.ai2 === 0) && hands.some((h) => h.ai2 === 1));
  check('核心转 ai0=0 一阶段', core.ai0 === 0, core.ai0);
  const c0 = { x: core.x, y: core.y };
  run(120);
  // ④ 双手+头存活期间核心无敌
  check('部件存活时核心无敌(iframes>0)', core.iframes > 0, core.iframes);
  check('核心向玩家+(0,130)悬停移动', Math.hypot(core.x - c0.x, core.y - c0.y) > 4,
    [Math.round(core.cx / 16), Math.round(core.cy / 16)]);
  // 手部攻击调度:90t 内至少出现一个攻击态(1/2/3)
  const handAtk = new Set<number>();
  for (let i = 0; i < 600; i++) { run(1); for (const h of hands) if (!h.dead) handAtk.add(h.ai0); }
  check('手部进入过攻击态', [1, 2, 3].some((a) => handAtk.has(a)), [...handAtk].join(','));
  const projBefore = projectiles.length;

```


---

## 🤖 Assistant · 2026-08-10T06:52:13.378Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
The duke probe bypasses fixedUpdate entirely and calls the AI directly (with manual iframes decrement). I'll follow that pattern.

Now let me check `World` construction & clock & TileStore setTileSilent signature (from mechprobe). Already seen.

Also `game.world.groundLevel` — World class has groundLevel property? mechprobe sets world.groundLevel = 60 ✓.

One concern: `losClear` uses game.world.store. TileStore has isSolid/inBounds. Fine.

Another: `spawnPart` requires enemyCtor bound — Enemy.ts imports bindEnemyCtor? Enemy.ts imports from bossAI: `bindEnemyCtor` is imported? In Enemy.ts line 12: `import { bindEnemyCtor, skeletronBossAI, ... } from './bossAI';` — yes bindEnemyCtor imported. But when is it called? Probably at module bottom: `bindEnemyCtor(Enemy)`. Let me check. If the probe imports Enemy.ts, the binding happens → spawnPart works ✓ (mechprobe relies on it).

Now check TileStore.setTileSilent signature and st.flags/st.liquid used in destroyerAI. Only need isSolid/inBounds/idx.

Let me now verify a few remaining source details I need exactly:

1. AI_045 lines 19468-19477 (player dead handling) — got it.
2. The jump branch: "velocity.X = 4 * direction" — got it.
3. num4 jump: `velocity.Y = -12.1f * (num + 9f) / 10f; if < -19.1 → -19.1`. Note num here is the enrage num (could be 2).

Wait — actually there's a subtlety: vanilla applies damage-based jump boost when `life < lifeMax`. And the (num+9)/10 multiplier: num=1 → 12.1. Hmm that gives damaged jump = -12.1 vs full-health -12.1?? Look:
```
if (life < lifeMax)
{
    velocity.Y = -12.1f * (num + 9f) / 10f;
    if ((double)velocity.Y < -19.1) velocity.Y = -19.1;
}
else velocity.Y = -12.1f;
```
With num=1: -12.1*1 = -12.1, same. With enrage num=2: -13.31. OK so the formula is for balance scaling. Fine — port exactly.

4. Landing branch: `if (velocity.Y == 0f)` inside ai[0]==1 → Item14 + dust/gore, ai[0]=0.

Wait, exact structure: ai[0]==1: `if (velocity.Y == 0f) { sound; ai[0]=0; dusts } else { steering }`. ✓.

5. There's also `frameCounter = 0.0` at jump trigger (animation). Skip (rendering).

Now — vanilla alpha: SetDefaults alpha=255 for 245/246/247/248. The AI reduces alpha by 10 per tick while > 0. Note that this also gates ai[1] (body: ai[1]=0 while fading; head: ai[1]=30; fist: ai[1]=0). 255/10 = 25.5 → 26 ticks of fade-in.

Our spawnAlpha for rendering: set to min(254, alpha). Initially fromVanilla set spawnAlpha=254 & alphaFade. I disable alphaFade and drive from 254? To be vanilla: start at 255 (invisible). Renderer probably treats 254 max. I'll set e.spawnAlpha = Math.min(254, x.alpha) each tick while fading; and once alpha hits 0, spawnAlpha = 0. Fine.

Now think about probe ② "本体跳跃位移(onGround 切换)": body spawns at (1600, 1920) center; falls to floor (collideGround) → onGround true. Then accumulates ai1 to 300 (300 ticks at num4=1) then crouch 20 ticks then jumps (vy=-12.1, gravity 0.3 → height 244px, airtime ~81 ticks) → lands → onGround true again. Probe: run ~700 ticks, record min cy during flight and check onGround toggled false at some point, and that body displaced horizontally toward player. Player is at same x → dir = sign(0) → fallback facing=1 → vx = 4 → moves right ~4px/tick * 81 ticks ≈ 324px?? Hmm, during flight the steering: player within body span (player x=1600, body x after spawn=1530..1670 → yes within) → vx *= 0.9 each tick (damps to ~0). Actually vx starts 4, then *0.9 per tick for 81 ticks → total horizontal ≈ 4*(1-0.9^81)/0.1 ≈ 40px. And vy += 0.2*(num+1)/2 = 0.2 each tick while Bottom.Y < player.y: body bottom 2330 vs player.y = 2240 → bottom > player.y → false → no extra gravity. OK.

So the body will jump ~244px up and land. onGround toggles ✓.

But careful: my grounded check `e.vy === 0`: during crouch (ai1 negative accumulation) the body is on ground, vy == 0 ✓ (gravity added then collide resets to 0 — I add gravity before move: vy = 0.3 → move down 0.3 → collide snaps & vy=0 ✓).

Wait — actually there's an issue with collideGround snapping: e.y = ty*TILE - e.h requires the foot to be inside the solid tile row. With vy=0.3 moving down 0.3px, foot enters the tile ✓.

Ceiling check: ty2 = floor(e.y / TILE) — with e.y snapped to ty*TILE - e.h, e.y/TILE is integer-ish → floor gives the row just above foot row... standard. Since bossAI uses it, copy the multi-column version.

6. For the head anchored offset: num722 -= 3f * scale → target = body.Center + velocity + (-3*scale, -57*scale)? Wait: num722 = body.Center.X - head.Center.X; then num722 -= 3*scale. So target delta = (body.cx - head.cx - 3*scale, body.cy - head.cy - 57*scale) → target point = body.Center + (-3*scale, -57*scale) ✓ (plus body.velocity? No! The head AI 46 does NOT add body velocity — only the fist does (`nPC.Center + nPC.velocity`). Head: `Main.npc[golemBoss].Center.X - vector83.X` plain. ✓

7. Fist anchor: `nPC.Center + nPC.velocity + (0,-9*scale)` then `vector.X += (type==247 ? -84 : 78) * scale` ✓.

Let me now double check AI_047's `if (golemBoss < 0) StrikeNPCNoInteraction` — self-destruct. ✓ handled by anchor null.

8. Body spawning positions — verify vanilla: `NewNPC(src, (int)Center.X - 84, (int)Center.Y - 9, 247)`. NewNPC(x, y, type) → position = (x, y) top-left ✓. So fist 247 top-left = (cx-84, cy-9). Fist w=40 h=30 → center at (cx-64, cy+6). Shoulder anchor = body.Center + (-42, -4.5) — consistent-ish.

Head: top-left (cx-3, cy-57); head 70x70 → center (cx+32, cy-22). Anchor target = body.Center + (-1.5, -28.5) — head will snap there quickly (dist < 100 → velocity = delta → 1 tick). OK.

Now, when the body dies (dying) then e.dead=true, the fists anchor the free head. The head in free mode moves (player + (0,-300)) — fists anchor its shoulders. Punch condition etc. works.

One more consideration for probe ⑤: "头死→全族自毁" — in free mode, hp<=0 → head.dead = true + all 245-248 dead. Body already dead in that scenario. Fists: they'd also detect anchor missing → dead. Both paths. ✓

Also: what if head (attached) dies but body alive → head free, body damageable (iframes not set). Then when body later dies → dying → dead. Head free continues until killed. Then family kill — body already dead. ✓ consistent.

Now what about the reverse concern: head free & alive, body hp<=0 → body dying (60t) → dead. My head free check `!x.free && (bad body)` — already free, no change ✓.

Now, another vanilla check — the free head (249) "dontTakeDamage = true" initially in SetDefaults, cleared... In vanilla UpdateNPC there's likely `dontTakeDamage` reset each tick for bosses? Hmm. If 249 stayed invulnerable forever the fight would be broken; vanilla must clear it somewhere. Probably in `NPC.VanillaAI`/`AI()` reset block: many AI styles set dontTakeDamage=false at top. aiStyle 48 doesn't set it... Search for where dontTakeDamage is reset globally. Actually likely in NPC.UpdateNPC: `if (dontTakeDamage) { ... }`? Whatever — I won't give the free head invulnerability. Not needed.

Now write the probe assertions:

① 245 首帧生成头 246+双拳 247/248:
```
const body = Enemy.fromVanilla(245, 100*16, 120*16)!; body.id=1; enemies.push(body);
run(1);
check head/fists spawned (vanillaId 246/247/248 present, one each)
check fist ai0 side: 247 → -1, 248 → +1
```
Note: my run() must dispatch style 45→golemAI, 46→golemHeadAI, 47→golemFistAI.

② 本体跳跃: run(100) to settle on ground; record sawGround/sawAir across ~700 ticks; check both true and vertical displacement (min cy < start cy - 100).

Actually ai1 accumulates 300 + 20 crouch = 320 ticks before first jump at full HP. Then next cycle 320 again. Run 500 ticks, sample. Then continue.

③ body hp→0: body.hp = 0; run a few ticks → body.ai3 === 1 (dying), head alive, head.ai3 === 1 (free). run(70) → body.dead true. Then run 200 → head moved (position changed & free behavior: distance from original anchor > some px) and head hp refilled (hp === maxHp).

④ fist punch: track fist position peak displacement from shoulder > 100 then returns within ~150px of shoulder (or head). Need enough ticks: fist needs ai1>=60 at shoulder, then windup 30, then fly up to 700px (58 ticks at 12 speed... plus return at ≤32 speed ~30 ticks). Total ~200 ticks. Run 400 and track.

During ④ the body may jump (ai0 cycling 320t) — the shoulder moves with body; fine.

Note: while the body is dying/dead (from ③), can't test ④ — order: run ①②④③⑤? The task lists ⑤ last; I can reorder internally as long as all 5 assertions exist. But ③ says "本体 hp→0 后头存活进入自主战斗" — needs body alive first. And ④ needs body alive (or head-anchoring works too). Simplest order: ①②④ on fresh spawns, then ③, then ⑤. But ③⑤ on the same instance after ④ is fine. Hmm — after ④, the body may be mid-jump; setting hp=0 works regardless.

Let me structure: Section A: spawn, ①, settle+②, then ④ (fist punch cycle), then ③ (body hp=0 → head free), then ⑤ (head hp=0 → family dead). All in one continuous world. Clean.

One risk in ④: during the fist punch, condition `anchor.hp < anchor.maxHp` false (full HP) → num3 = 14, num6 = 12. OK.

But watch out: while the body is jumping (state 1), the shoulder moves; when the fist is in state 0 and dist >= 12+num3=26, it homes at 14 speed. Body jumps at vx 4 → fine.

Another risk: punch trigger requires `e.ai1 >= 60` accumulated while close to the shoulder. ai1 increments only in the `dist < 12+num3` branch. Since the body moves slowly, fine. 60 ticks then punch. But wait — there's an important interplay: at the very start, the fist is at spawn pos (top-left = cx-84 → center (1536, 1911)) vs shoulder (1558, 1915.5)... dist ~22 < 26 ✓ accumulates immediately.

Then windup: position snapped to shoulder each tick (Center = vector): e.x = tx - w/2 = shoulder.x - 20, e.y = ty - 15.

Launch: toward player (1600, 2240): from (1558, 1915) → direction (42, 325) normalized * 12 → mostly downward! Wait player cy 2240, fist cy 1915 → player is 325px BELOW. Yes downward. Earlier I miscalculated (I used the landed body position). The body hasn't landed at first: body spawns center y=1920, floor at 2400 → body falls to center 2330. Let me redo: I'll let the body settle (run 100) before measuring ④. After settle: body center (1600, 2330), shoulder left fist (1558, 2325.5), player (1600, 2240) → player is 85px ABOVE fist. Punch up: passes player when cy < player.cy → noTC false → then continues up into open sky (no ceiling) until dist > 700 → return. Peak displacement ~700px ✓. Hmm, but wait — punch upward 700px from y≈2325 → y≈1625 (tile 101) — within the 300-tile world ✓.

Actually careful: the "dist > 700" is measured to the shoulder which is fixed-ish. ✓

Then state 0: home back at 14-28 speed; needs to close ~700px at ~14px/t (until within 26, then snap) → ~50 ticks. Peak > 100 ✓, return within 150 of shoulder ✓.

⑤: after ③ (body dead), set head.hp = 0 → run(2) → all dead.

Hmm wait — in ③, head enters free mode and refills hp to maxHp. Then I directly set head.hp = 0 → free && hp<=0 → family kill ✓.

Also for ③ assertion "头的位移/状态变化": record head position at transition, run 200 ticks (head seeks player+(0,-300) at 7 speed) → displacement > 50px ✓ and ai3===1 ✓ and hp === maxHp ✓.

Careful: in free mode, my head must not anchor to the body anymore ✓.

One more thing — the attached head's fireball loop could fire projectiles during the test; harmless.

Also note: probe's fake game has no `damagePlayer`... it has. Fine, spawnParticles/playSfx are stubs.

Edge: my body AI calls game.spawnParticles with opts {life}. Stub ignores args ✓.

Now, another important consideration: `Enemy.fixedUpdate` is NOT called in my probe run loop (I call AI directly like _dukemlprobe). But `spawnPart` → addEnemy → entities.add assigns id ✓.

Wait — but spawnPart uses `enemyCtor` bound via bindEnemyCtor — where's it called in Enemy.ts? Let me verify it's called at module scope, else spawnPart returns null and the probe fails. grep.
````

</details>


---

## 🤖 Assistant · 2026-08-10T06:52:14.145Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"bindEnemyCtor\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts; grep -n \"noUnusedLocals\\|strict\" ~/Project/GLM/SandboxWorld/game/tsconfig.json; grep -rn \"clock\" ~/Project/GLM/SandboxWorld/game/src/world/World.ts | head -5",
 "description": "Check ctor binding and tsconfig"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:52:14.188Z

**📎 ToolResult**

```
12:import { bindEnemyCtor, skeletronBossAI, skeletronHandAI, kingSlimeAI, brainOfCthulhuAI, creeperAI, twinsAI, skeletronPrimeAI, primePartAI, destroyerAI } from './bossAI';
1468:bindEnemyCtor(Enemy);
7:    "strict": true,
9:    "noUnusedLocals": false,
~/Project/GLM/SandboxWorld/game/src/world/World.ts:36:  clock: Clock;
~/Project/GLM/SandboxWorld/game/src/world/World.ts:80:    this.clock = new Clock(30 * 60 * 1000);
~/Project/GLM/SandboxWorld/game/src/world/World.ts:93:    w.clock.timeOfDay = p.clock.timeOfDay;
~/Project/GLM/SandboxWorld/game/src/world/World.ts:94:    w.clock.dayCount = p.clock.dayCount;

```


---

## 🤖 Assistant · 2026-08-10T06:52:16.092Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. bindEnemyCtor(Enemy) at Enemy.ts:1468 module scope ✓. noUnusedLocals false ✓ (unused imports OK, but I'll only import what I use anyway).

Check World.groundLevel exists:
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:52:16.383Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"groundLevel\\|rockLevel\" ~/Project/GLM/SandboxWorld/game/src/world/World.ts | head",
 "description": "Check World fields"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:52:16.412Z

**📎 ToolResult**

```
33:  groundLevel = 0; rockLevel = 0;   // tile 坐标
53:   *  缺省 0=未知，使用处以 groundLevel 回退 */
90:    w.groundLevel = p.groundLevel; w.rockLevel = p.rockLevel; w.lavaLine = p.lavaLine;

```


---

## 🤖 Assistant · 2026-08-10T06:52:22.823Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now let me also verify the exact vanilla line numbers I'll cite in comments:
- AI_045_Golem: 19447-19690 (ends before SpawnMechQueen at ~19691). Let me confirm end line: the despawn block ended at 19689 "}". SpawnMechQueen starts 19691. So AI_045 = 19447-19690.
- AI_047_GolemFist: 19171-19446.
- aiStyle 46 dispatch: 31273-31495.
- aiStyle 48 dispatch: 31500-31752ish.

Let me get precise line numbers for sub-blocks I cite. I'll use approximate citations from the sed outputs:
Body:
- golemBoss=whoAmI: 19449
- balance/enrage: 19450-19457
- spawn parts: 19458-19467
- player dead: 19468-19477
- alpha: 19478-19485
- part scan: 19487-19512
- dontTakeDamage: 19513
- getGoodWorld torch: 19514-19534
- missing-fist dust: 19544-19595
- noTileCollide clear: 19597-19613 (position += netOffset... let me verify: 19597ish)
- ai0==0 ground: 19615-19640
- ai0==1 jump: 19641-19675 (the else if (ai[0] == 1f) block — from sed part2: starts right after. In part 2 output, first lines were `{ ai[1] = -20f; frameCounter = 0.0; } else if (ai[1] == -1f) {...}` then `} } else if (ai[0] == 1f) {`. The part-2 sed started at 19620. So ai0==0 block ≈ 19615-19639, ai0==1 ≈ 19640-19674, despawn 19676-19689.

Let me get exact numbers with grep for a few anchors.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:52:23.742Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (ai\\[0\\] == 0f)\\|else if (ai\\[0\\] == 1f)\\|int num8 = 3000\\|noTileCollide = false;\\|position += netOffset\\|if (alpha > 0)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>19440 && $1<19700'",
 "description": "Get exact line anchors in AI_045"
}
```


---

## 🤖 Assistant · 2026-08-10T06:52:24.785Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (ai\\[0\\] == 0f)\\|else if (ai\\[0\\] == 1f)\\|else if (ai\\[0\\] == 2f)\\|if (ai\\[0\\] != 3f)\\|if (golemBoss < 0)\\|Vector2 vector = nPC.Center\\|float num2 = vector2.Length\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>19160 && $1<19450'",
 "description": "Get exact line anchors in AI_047"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:52:27.685Z

**📎 ToolResult**

```
19477:		if (alpha > 0)
19528:		position += netOffset;
19573:				noTileCollide = false;
19577:				noTileCollide = false;
19580:		if (ai[0] == 0f)
19646:		else if (ai[0] == 1f)

```


---

## 👤 User(sidechain) · 2026-08-10T06:52:37.807Z

**📎 ToolResult**

```
19182:		if (golemBoss < 0)
19198:		Vector2 vector = nPC.Center + nPC.velocity + new Vector2(0f, -9f * scale);
19201:		float num2 = vector2.Length();
19202:		if (ai[0] == 0f)
19271:		else if (ai[0] == 1f)
19333:		else if (ai[0] == 2f)
19394:			if (ai[0] != 3f)

```


---

## 🤖 Assistant · 2026-08-10T06:52:40.315Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good:
- AI_047: states 0 (19202-19270), 1 (19271-19332), 2 (19333-19393), 3 (19394-19446).
- AI_045: ai0==0 ground block 19580-19645, ai0==1 jump 19646-19675(ish), then despawn. noTileCollide clearing at 19571-19578.

Let me check 19560-19580 for the noTileCollide block and the despawn block end line.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:52:41.272Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19558,19582p;19666,19695p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | cat -n; echo ---; awk 'NR>=19666 && NR<=19695 {printf \"%d\\t%s\\n\", NR, $0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read noTileCollide and despawn blocks with line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:52:44.678Z

**📎 ToolResult**

```
     1						num3 = Dust.NewDust(new Vector2(base.Center.X + 62f * scale, base.Center.Y - 9f), 8, 8, 6);
     2						if (Main.rand.Next(20) != 0)
     3						{
     4							Main.dust[num3].noGravity = true;
     5							Main.dust[num3].scale *= 1f + (float)Main.rand.Next(10) * 0.1f;
     6							Main.dust[num3].velocity.Y -= 1f;
     7						}
     8					}
     9				}
    10			}
    11			position -= netOffset;
    12			if (noTileCollide && !Main.player[target].dead)
    13			{
    14				if (velocity.Y > 0f && base.Bottom.Y > Main.player[target].Top.Y)
    15				{
    16					noTileCollide = false;
    17				}
    18				else if (Collision.CanHit(position, width, height, Main.player[target].Center, 1, 1) && !Collision.SolidTiles(position, width, height))
    19				{
    20					noTileCollide = false;
    21				}
    22			}
    23			if (ai[0] == 0f)
    24			{
    25				if (velocity.Y == 0f)
    26					if (position.X < Main.player[target].position.X && position.X + (float)width > Main.player[target].position.X + (float)Main.player[target].width)
    27					{
    28						velocity.X *= 0.9f;
    29						if (base.Bottom.Y < Main.player[target].position.Y)
    30						{
    31							velocity.Y += 0.2f * (num + 1f) / 2f;
    32						}
    33					}
    34					else
    35					{
    36						if (direction < 0)
    37						{
    38							velocity.X -= 0.2f;
    39						}
    40						else if (direction > 0)
    41						{
    42							velocity.X += 0.2f;
    43						}
    44						float num7 = 3f;
    45						if (life < lifeMax)
    46						{
    47							num7 += 1f;
    48						}
    49						if (life < lifeMax / 2)
    50						{
    51							num7 += 1f;
    52						}
    53						if (life < lifeMax / 4)
    54						{
    55							num7 += 1f;
---
19666					if (position.X < Main.player[target].position.X && position.X + (float)width > Main.player[target].position.X + (float)Main.player[target].width)
19667					{
19668						velocity.X *= 0.9f;
19669						if (base.Bottom.Y < Main.player[target].position.Y)
19670						{
19671							velocity.Y += 0.2f * (num + 1f) / 2f;
19672						}
19673					}
19674					else
19675					{
19676						if (direction < 0)
19677						{
19678							velocity.X -= 0.2f;
19679						}
19680						else if (direction > 0)
19681						{
19682							velocity.X += 0.2f;
19683						}
19684						float num7 = 3f;
19685						if (life < lifeMax)
19686						{
19687							num7 += 1f;
19688						}
19689						if (life < lifeMax / 2)
19690						{
19691							num7 += 1f;
19692						}
19693						if (life < lifeMax / 4)
19694						{
19695							num7 += 1f;

```


---

## 🤖 Assistant · 2026-08-10T06:52:46.476Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=19695 && NR<=19730 {printf \"%d\\t%s\\n\", NR, $0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read end of AI_045"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:52:53.994Z

**📎 ToolResult**

```
19695							num7 += 1f;
19696						}
19697						num7 *= (num + 1f) / 2f;
19698						if (velocity.X < 0f - num7)
19699						{
19700							velocity.X = 0f - num7;
19701						}
19702						if (velocity.X > num7)
19703						{
19704							velocity.X = num7;
19705						}
19706					}
19707				}
19708			}
19709			if (target <= 0 || target == 255 || Main.player[target].dead)
19710			{
19711				TargetClosest();
19712			}
19713			int num8 = 3000;
19714			if (Math.Abs(base.Center.X - Main.player[target].Center.X) + Math.Abs(base.Center.Y - Main.player[target].Center.Y) > (float)num8)
19715			{
19716				TargetClosest();
19717				if (Math.Abs(base.Center.X - Main.player[target].Center.X) + Math.Abs(base.Center.Y - Main.player[target].Center.Y) > (float)num8)
19718				{
19719					active = false;
19720				}
19721			}
19722		}
19723	
19724		public static bool SpawnMechQueen(int onWhichPlayer)
19725		{
19726			if (AnyNPCs(127) || AnyNPCs(134) || AnyNPCs(125) || AnyNPCs(126))
19727			{
19728				return false;
19729			}
19730			if (!SpecialSeedFeatures.Mechdusa)

```


---

## 🤖 Assistant · 2026-08-10T06:52:55.941Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
AI_045 = 19447-19722. AI_047 = 19171-19446.

Now the exact ai0==0 ground block 19580-19645 — let me get 19596-19645 with numbers for citation accuracy.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:52:56.357Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=19580 && NR<=19660 {printf \"%d\\t%s\\n\", NR, $0}' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read ground/jump blocks with line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:53:01.855Z

**📎 ToolResult**

```
19580			if (ai[0] == 0f)
19581			{
19582				if (velocity.Y == 0f)
19583				{
19584					velocity.X *= 0.8f;
19585					float num4 = 1f;
19586					if (ai[1] > 0f)
19587					{
19588						if (!flag2)
19589						{
19590							num4 += 2f;
19591						}
19592						if (!flag3)
19593						{
19594							num4 += 2f;
19595						}
19596						if (!flag)
19597						{
19598							num4 += 2f;
19599						}
19600						if (life < lifeMax)
19601						{
19602							num4 += 1f;
19603						}
19604						if (life < lifeMax / 2)
19605						{
19606							num4 += 4f;
19607						}
19608						if (life < lifeMax / 3)
19609						{
19610							num4 += 8f;
19611						}
19612						num4 *= num;
19613						if (Main.getGoodWorld)
19614						{
19615							num4 += 100f;
19616						}
19617					}
19618					ai[1] += num4;
19619					if (ai[1] >= 300f)
19620					{
19621						ai[1] = -20f;
19622						frameCounter = 0.0;
19623					}
19624					else if (ai[1] == -1f)
19625					{
19626						noTileCollide = true;
19627						TargetClosest();
19628						velocity.X = 4 * direction;
19629						if (life < lifeMax)
19630						{
19631							velocity.Y = -12.1f * (num + 9f) / 10f;
19632							if ((double)velocity.Y < -19.1)
19633							{
19634								velocity.Y = -19.1f;
19635							}
19636						}
19637						else
19638						{
19639							velocity.Y = -12.1f;
19640						}
19641						ai[0] = 1f;
19642						ai[1] = 0f;
19643					}
19644				}
19645			}
19646			else if (ai[0] == 1f)
19647			{
19648				if (velocity.Y == 0f)
19649				{
19650					SoundEngine.PlaySound(SoundID.Item14, position);
19651					ai[0] = 0f;
19652					for (int l = (int)position.X - 20; l < (int)position.X + width + 40; l += 20)
19653					{
19654						for (int m = 0; m < 4; m++)
19655						{
19656							int num5 = Dust.NewDust(new Vector2(position.X - 20f, position.Y + (float)height), width + 20, 4, 31, 0f, 0f, 100, default(Color), 1.5f);
19657							Main.dust[num5].velocity *= 0.2f;
19658						}
19659						int num6 = Gore.NewGore(new Vector2(l - 20, position.Y + (float)height - 8f), default(Vector2), Main.rand.Next(61, 64));
19660						Main.gore[num6].velocity *= 0.4f;

```


---

## 🤖 Assistant · 2026-08-10T06:53:06.122Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have all details. Now write bossAI_golem.ts.

Also need exact anchors for the head (46) dispatch lines: 31273-31495 and 48: 31500-31752. Let me get a few exact numbers for citations within 31273-31500 (already have from sed: alpha at 31287? grep gave "if (alpha > 0)" at 31287? The earlier grep for alpha > 0 only in 19440-19700 range. I'll cite approximate: anchor 31292-31308, alpha 31287-31294, phase0 31310-31347, phase1 31348-31464, ai0 derive 31491-31495. Good enough — let me quickly verify boundaries with grep.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:53:07.010Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (this.ai\\[0\\] == 0f)\\|else if (this.ai\\[0\\] == 1f)\\|if (life < lifeMax / 2)\\|if (alpha > 0)\\|noTileCollide = true;\\|float num721 = 100f\" ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs | awk -F: '$1>31270 && $1<31500'",
 "description": "Anchors in aiStyle 46 block"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:53:21.560Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terrarria1456/Terraria/NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-10T06:53:22.794Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Typo: Terarria1456. Retry.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:53:23.800Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (this.ai\\[0\\] == 0f)\\|else if (this.ai\\[0\\] == 1f)\\|if (life < lifeMax / 2)\\|if (alpha > 0)\\|noTileCollide = true;\\|float num721 = 100f\\|else if (aiStyle == 48)\\|else if (aiStyle == 49)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>31270 && $1<31800'",
 "description": "Anchors in aiStyle 46/48 blocks"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:53:28.302Z

**📎 ToolResult**

```
31284:			noTileCollide = true;
31290:			float num721 = 100f;
31310:			if (alpha > 0)
31319:			if (this.ai[0] == 0f)
31353:			else if (this.ai[0] == 1f)
31487:			if (life < lifeMax / 2)
31500:		else if (aiStyle == 48)
31514:				noTileCollide = true;
31742:		else if (aiStyle == 49)

```


---

## 🤖 Assistant · 2026-08-10T06:53:44.657Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So aiStyle 46 = 31273-31499, aiStyle 48 = 31500-31741.

Now write the file. Also decide the exports: golemAI, golemHeadAI, golemFistAI. (The free-head logic lives inside golemHeadAI keyed by free flag — wiring note: aiStyle 48 / NPC 249 not needed since 246 transforms in place; but I could also handle 249 if spawned: if e.vanillaId === 249 → treat as free from birth. Nice for completeness: `const x = headXOf(e); if (e.vanillaId === 249) x.free = true;` I'll add that so a spawned 249 works.)

Hmm — but if someone spawns 249, findHead (246) won't find it... anchor for fists uses findHead which looks for 246. Keep findHead matching vanillaId 246 or 249. I'll do that.

Write the code now. Careful details:

- `balanceNum`: vanilla condition `(!ZoneLihzhardTemple && !ZoneJungle) || player.Center.Y < worldSurface*16` → num *= 2. We only implement the surface check (no zone data) — if player above ground → num *= 2. Hmm, that makes the boss enraged whenever fought near surface; in the temple (underground) → num = 1. Given no zone API, I'll implement: `player.cy < groundLevel*TILE → num*=2` and note that the temple/jungle zone check is dropped (simplification, no Zone API). In the probe groundLevel = 60 → player at tile 140 → deep underground → num = 1 ✓ good for deterministic probe.

- Head `ai1` while fading = 30 (vanilla :31310-31317). My alpha handling: x.alpha starts 255, -10/tick → while > 0: e.ai1 = 30.

Careful about ordering: vanilla sets velocity from anchor FIRST, then alpha (ai1=30), then attack logic. I'll keep that order.

- Attached head: what if body missing (shouldn't happen since head self-destroys... vanilla: if golemBoss < 0 → strike self). For attached head: if no body → go free? Vanilla would self-destruct (246 without body). But our structure: body missing (e.g. killed outright by hurt() without exemption... or despawned) → attached head should... Task: "本体死透后头继续" — head continues. So if body missing → head goes free (not self-destruct). That's the intended adaptation. I'll do that: body missing/dead → free.

But careful with the self-destruct for fists: "拳 247/248:锚定本体(或头)" — both dead → fist self-destruct ✓ (vanilla 19182).

- e.iframes = 2 for body invulnerability while attached head alive (dontTakeDamage = flag :19513). Note vanilla also sets dontTakeDamage=false then = flag each tick. Port: `if (hasAttachedHead) e.iframes = 2;`

Now write. Also `seek` import: do I use seek? The free-head uses accelTo on both axes — I can implement inline with accelTo twice. No need for seek. Task said "从 './bossAI' 导入:spawnPart、shoot、seek、accelTo、losClear、addEnemy" — these are the available helpers; using a subset is fine.

Let me also double check `shoot` signature: shoot(game, x, y, vx, vy, dmg, projId, life = 300) ✓ Arrow-based.

Projectile ids: 258 (fireball), 259 (eye laser). Check that Projectile_258.png exists in public/sprites/vanilla/.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:53:45.032Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ | grep -E \"^Projectile_(258|259)\" ",
 "description": "Verify golem projectile textures exist"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:53:45.087Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-10T06:53:47.040Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ | head -20; ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ | wc -l; find ~/Project/GLM/SandboxWorld/game/public -name \"*258*\" -o -name \"*259*\" | head",
 "description": "Find projectile sprite files"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:53:47.144Z

**📎 ToolResult**

```
Actuator.png
Background_0.png
Background_1.png
Background_10.png
Background_100.png
Background_101.png
Background_102.png
Background_103.png
Background_104.png
Background_105.png
Background_106.png
Background_107.png
Background_108.png
Background_109.png
Background_11.png
Background_110.png
Background_111.png
Background_112.png
Background_113.png
Background_114.png
    8429
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui/Armor_Armor_259.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui/Armor_Armor_258.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui/Armor_Head_258.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui/Armor_Head_259.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_2584.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_2590.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_1258.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_1259.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_2591.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_2585.png

```


---

## 🤖 Assistant · 2026-08-10T06:53:49.529Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ | grep -iE \"projectile\" | head -8; ls ~/Project/GLM/SandboxWorld/game/public/sprites/ | head",
 "description": "Locate projectile sprites naming"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:53:49.584Z

**📎 ToolResult**

```
Projectile_1.png
Projectile_10.png
Projectile_100.png
Projectile_1000.png
Projectile_101.png
Projectile_1012.png
Projectile_1019.png
Projectile_102.png
annotations.json
atlas.json
resources.json
vanilla
vanilla-npcgore.json
vanilla-npcloot.json
vanilla-npcs.json
vanilla-ui
vanilla-ui.json
vanilla.json

```


---

## 🤖 Assistant · 2026-08-10T06:53:51.441Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ | grep -xE \"Projectile_(2[0-9]{2}|6[0-9]{2})\\.png\" | sort -t_ -k2 -n | head -30",
 "description": "List low-id projectile sprites"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:53:57.883Z

**📎 ToolResult**

```
Projectile_206.png
Projectile_212.png
Projectile_213.png
Projectile_214.png
Projectile_215.png
Projectile_216.png
Projectile_217.png
Projectile_218.png
Projectile_219.png
Projectile_220.png
Projectile_222.png
Projectile_223.png
Projectile_224.png
Projectile_228.png
Projectile_229.png
Projectile_237.png
Projectile_243.png
Projectile_247.png
Projectile_250.png
Projectile_252.png
Projectile_253.png
Projectile_254.png
Projectile_260.png
Projectile_261.png
Projectile_262.png
Projectile_263.png
Projectile_265.png
Projectile_271.png
Projectile_272.png
Projectile_273.png

```


---

## 🤖 Assistant · 2026-08-10T06:54:03.200Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Projectile_258.png and 259.png are MISSING from vanilla sprites?! Let me check precisely.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:54:03.602Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ | grep -xE \"Projectile_25[0-9]\\.png\"",
 "description": "Check Projectile_25x files"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:54:03.652Z

**📎 ToolResult**

```
Projectile_250.png
Projectile_252.png
Projectile_253.png
Projectile_254.png

```


---

## 🤖 Assistant · 2026-08-10T06:54:05.799Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/ | head; find ~/Project/GLM/SandboxWorld/terraria-assets -maxdepth 2 -iname \"*projectile*\" 2>/dev/null | head",
 "description": "Look for asset sources"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:54:05.841Z

**📎 ToolResult**

```
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
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_203.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_565.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_571.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_1102.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_217.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_559.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_767.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_773.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_983.png
~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_997.png

```


---

## 🤖 Assistant · 2026-08-10T06:54:08.580Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-assets/Images/ | grep -xE \"Projectile_25[0-9]\\.png\"; ls ~/Project/GLM/SandboxWorld/terraria-assets/Images/ | wc -l; ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ | grep -cE \"^Projectile_\"",
 "description": "Compare asset source vs game copy for 25x projectiles"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:54:08.858Z

**📎 ToolResult**

```
Projectile_250.png
Projectile_251.png
Projectile_252.png
Projectile_253.png
Projectile_254.png
Projectile_255.png
Projectile_256.png
Projectile_257.png
Projectile_258.png
Projectile_259.png
   13908
336

```


---

## 🤖 Assistant · 2026-08-10T06:54:13.994Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The full source has Projectile_258/259, but the game copy only has 336 projectile sprites (whitelist subset). The task says "弹幕贴图 Projectile_N.png 已全量在 game/public/sprites/vanilla/" — but actually only 336 are copied; 258/259 are absent. Hmm — "只允许改这一个文件" (vanilla-npcs.json) — I cannot copy the PNGs? "先看 SetDefaults 源...补一条与 247 对称的数据到该 JSON(只允许改这一个文件)" — the "只允许改这一个文件" refers to the JSON data gap task. It says for the data gap, only that file may be modified. For sprites... the constraint list says "严禁修改 Enemy.ts / Game.ts / Renderer.ts / bossAI.ts / bossAI_*.ts / 其它已有文件". Copying two PNG files into public/sprites/vanilla/ doesn't modify existing files — it adds new asset files. The task asserts the textures are already there ("已全量"), which is wrong for 258/259. To make the boss render its projectiles, I should copy those two PNGs from terraria-assets. Adding new asset files is consistent with the spirit (main session wires rendering). But strictly "其它已有文件" forbids modifying existing ones — adding new PNGs is not modifying. I'll copy 258 and 259 (and note it in the report).

Wait — also check: is there a resources.json / atlas.json that must list sprites? Loading is probably by path convention (vanilla/Projectile_258.png). Let me check how Arrow loads projId textures.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:54:14.473Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Projectile_\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | grep -v \"^Binary\" | head -10",
 "description": "Find projectile texture loading"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:54:14.506Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-10T06:54:17.268Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Projectile_\" ~/Project/GLM/SandboxWorld/game/src | head -10",
 "description": "Find projectile texture loading"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:54:17.294Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:7:// 贴图统一 Projectile_N.png 懒加载（Arrow.projSprite 共享缓存）。
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:63:  'vanilla/Projectile_98.png',   // 毒镖 10×10
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:64:  'vanilla/Projectile_99.png',   // 巨石 32×32
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:65:  'vanilla/Projectile_184.png',  // 火焰陷阱 10×10
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:66:  'vanilla/Projectile_185.png',  // 尖刺球 14×14
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:67:  'vanilla/Projectile_186.png',  // 长矛机关 10×16
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:68:  'vanilla/Projectile_187.png',  // 超级飞镖 6×6
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:69:  'vanilla/Projectile_654.png',  // 热喷泉 16×16
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:3:// 原版贴图 Projectile_N.png；命中敌人伤害/击退/暴击（穿透>1 时同敌免疫防连击）；
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:12:/** 原版投射物贴图懒加载（Projectile_1.png = 木箭、Projectile_2.png = 燃烧箭，泛用所有 id） */

```


---

## 🤖 Assistant · 2026-08-10T06:54:19.310Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,60p' ~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts",
 "description": "Check Arrow projSprite loading"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:54:19.332Z

**📎 ToolResult**

```
// 箭矢/通用直飞·抛物线投射物（原版 Projectile type 1/2、aiStyle 1/2 主干，Projectile.cs:546-566 + AI_001/AI_002）：
// 重力 0.3/tick（aiStyle1/2 通用常量；直飞弹传 0）、timeLeft 1200、旋转 atan2(vy,vx)+π/2（AI_001 尾部 L54877）、
// 原版贴图 Projectile_N.png；命中敌人伤害/击退/暴击（穿透>1 时同敌免疫防连击）；
// 命中 tileCut 砍草/碎罐（Projectile.CutTiles）；命中实心块 1/3 概率回收掉落。
import { Entity } from './Entity';
import { hitCritters } from './projTargets';
import { TILE } from '../core/constants';
import type { GameHooks } from './types';
import type { Renderer } from '../render/Renderer';
import type { Camera } from '../render/Camera';

/** 原版投射物贴图懒加载（Projectile_1.png = 木箭、Projectile_2.png = 燃烧箭，泛用所有 id） */
const spriteCache = new Map<number, HTMLImageElement>();
export function projSprite(projId: number): HTMLImageElement | null {
  let img = spriteCache.get(projId);
  if (img !== undefined) return img ?? null;
  if (typeof Image === 'undefined') return null;
  img = new Image();
  img.src = `sprites/vanilla/Projectile_${projId}.png`;
  spriteCache.set(projId, img);
  return img;
}

export interface ArrowOpts {
  /** 重力/tick（aiStyle1/2 = 0.3；直飞魔法弹传 0）。默认 0.3 */
  grav?: number;
  /** 原版 timeLeft（Projectile.cs:554 默认 1200） */
  life?: number;
  /** 穿透次数（原版 penetrate：手里剑 4、箭 1；-1 视作 1） */
  pierce?: number;
}

export class Arrow extends Entity {
  w = 10; h = 10; // 原版 SetDefaults type 1：width/height = 10
  vx: number;
  vy: number;
  damage: number;
  knockback: number;
  /** 原版投射物类型（1=木箭 2=燃烧箭，PickAmmo projToShoot = ammo.shoot） */
  projId: number;
  /** 回收掉落的 item key（null = 不回收，如燃烧箭） */
  dropKey: string | null;
  grav: number;
  life: number;
  pierce: number;
  /** 穿透投射物的同敌免疫表（敌人 id 集合） */
  private hitSet = new Set<number>();
  dead = false;

  constructor(x: number, y: number, vx: number, vy: number, damage: number,
    knockback: number, projId = 1, dropKey: string | null = null, opts?: ArrowOpts) {
    super();
    this.x = x; this.y = y;
    this.vx = vx; this.vy = vy;
    this.damage = damage;
    this.knockback = knockback;
    this.projId = projId;
    this.dropKey = dropKey;
    this.grav = opts?.grav ?? 0.3;
    this.life = opts?.life ?? 1200;

```


---

## 🤖 Assistant · 2026-08-10T06:56:48.303Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Path-based lazy loading `sprites/vanilla/Projectile_258.png` — so I just need the PNG files present. I'll copy 258/259 from terraria-assets (adding new asset files, not modifying existing code). That's justified; I'll report it.

Now, write bossAI_golem.ts. Let me carefully draft.

```ts
// 石巨人 Boss 族 AI 1:1 移植(Terarria1456 1.4.5.6):
//   本体 245 aiStyle 45  AI_045_Golem      NPC.cs:19447-19722(行走/跳跃/蓄力节奏/离场)
//   头   246 aiStyle 46  挂载头            NPC.cs:31273-31499(锚本体+火焰弹/眼激光)
//   自由头 249 aiStyle 48 GolemHeadFree    NPC.cs:31500-31741(自主悬浮+火焰弹/眼激光)
//   拳   247/248 aiStyle 47 AI_047_GolemFist NPC.cs:19171-19446(肩锚/蓄力冲拳/回位)
// SetDefaults:NPC.cs:12095-12149(245-249 属性)、17943-17960(245-249 scale *= 0.5)。
// 经典模式主链 1:1;expert/getGoodWorld 分支保留注释;netcode/纯视觉尘跳过。
```

Details on scale: GOLEM_SCALE = 0.5.

Code:

```ts
import type { Enemy } from './Enemy';
import type { GameHooks } from './types';
import type { Player } from './Player';
import { TILE, GRAVITY, MAX_FALL_SPEED } from '../core/constants';
import { vanillaNpc } from '../data/vanillaNpcs';
import { spawnPart, shoot, accelTo, losClear } from './bossAI';
```

Wait: GRAVITY = 0.36 vs vanilla 0.3. I'll define GOLEM_GRAVITY = 0.3f? Vanilla NPC gravity: in UpdateNPC, `velocity.Y += 0.3f` unless noGravity — with maxFallSpeed 10 for most NPCs. I'll use 0.3/10 constants with a comment. Then don't import GRAVITY/MAX_FALL_SPEED. 

```ts
/** 原版 NPC 通用重力/maxFall(NPC.UpdateNPC 非 noGravity 族) */
const GRAV = 0.3;
const MAX_FALL = 10;
/** SetDefaults 245-249 scale *= 0.5(NPC.cs:17943-17960)——所有偏移量按此缩放 */
const SCALE = 0.5;
const clamp = (v: number, lo: number, hi: number) => (v < lo ? lo : v > hi ? hi : v);
```

State maps:

```ts
/** Boss 伤害/防御基值缓存(自由头变身 249 属性时从基值切换,防重复乘膨胀) */
const baseStats = new WeakMap<Enemy, { dmg: number; def: number }>();
const baseOf = (e: Enemy) => { ... };

interface BodyX { alpha: number; noTC: boolean; dying: boolean; deadT: number }
interface HeadX { alpha: number; free: boolean; l0: number; l1: number }
interface FistX { alpha: number; noTC: boolean; state: number }
```

Family lookup:
```ts
const isGolem = (n: Enemy) => !n.dead && n.vanillaId !== null && n.vanillaId >= 245 && n.vanillaId <= 249;
const findBody = (game: GameHooks): Enemy | null =>
  (game.enemies() as Enemy[]).find((n) => !n.dead && n.vanillaId === 245) ?? null;
const findHead = (game: GameHooks): Enemy | null =>
  (game.enemies() as Enemy[]).find((n) => !n.dead && (n.vanillaId === 246 || n.vanillaId === 249)) ?? null;
```

balance:
```ts
/** GetMyBalance + 脱离神庙/丛林加成(NPC.cs:19450-19457 / 19173-19180 / 31274-31282):
 *  经典单人 = 1;getGoodWorld +2/+3(expert,略);玩家不在神庙/丛林带 或 在地表以上 → ×2。
 *  本工程无 ZoneLihzhardTemple/ZoneJungle 判定 → 仅保留"玩家在地表以上"一支(简化项)。 */
const balanceNum = (game: GameHooks, player: Player | null): number => {
  let num = 1;
  if (player && player.cy < game.world.groundLevel * TILE) num *= 2;
  return num;
};
```

alpha helper:
```ts
/** 出生渐显(SetDefaults alpha=255;AI 内 alpha -= 10/2t,NPC.cs:19477-19485 等):
 *  期间 ai[1] 被冻结为固定值(本体/拳 0、挂载头 30)——蓄力计时不起跑 */
const fadeAlpha = (e: Enemy, x: { alpha: number }): number => {
  if (x.alpha <= 0) return 0;
  x.alpha = Math.max(0, x.alpha - 10);
  e.spawnAlpha = Math.min(254, x.alpha);
  return x.alpha;
};
```

Collision helpers (own copies since bossAI's collideGround is private):
```ts
/** 落地/碰墙判定(bossAI.collideGround 的多列扩展版——140px 宽本体单列采样会半悬空) */
function collideGround(e: Enemy, game: GameHooks): void {
  const st = game.world.store;
  const cols = [e.x + 2, e.cx, e.x + e.w - 2];
  if (e.vy >= 0) {
    const ty = Math.floor((e.y + e.h) / TILE);
    let top = Infinity;
    for (const cx of cols) {
      const tx = Math.floor(cx / TILE);
      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) top = Math.min(top, ty * TILE);
    }
    if (top < Infinity) { e.y = top - e.h; e.vy = 0; e.onGround = true; }
    else e.onGround = false;
  } else e.onGround = false;
  if (e.vy < 0) {
    const ty = Math.floor(e.y / TILE);
    let bottom = -Infinity;
    for (const cx of cols) {
      const tx = Math.floor(cx / TILE);
      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) bottom = Math.max(bottom, (ty + 1) * TILE);
    }
    if (bottom > -Infinity) { e.y = bottom; e.vy = 0; }
  }
  // 侧墙(取上下两采样点,近似 Collision 的 AABB)
  const rows = [e.y + 2, e.cy, e.y + e.h - 2];
  if (e.vx > 0) {
    const tx = Math.floor((e.x + e.w) / TILE);
    for (const ry of rows) {
      const ty = Math.floor(ry / TILE);
      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { e.x = tx * TILE - e.w; e.vx = 0; break; }
    }
  } else if (e.vx < 0) {
    const tx = Math.floor(e.x / TILE);
    for (const ry of rows) {
      const ty = Math.floor(ry / TILE);
      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { e.x = (tx + 1) * TILE; e.vx = 0; break; }
    }
  }
}
```
Hmm — careful: onGround is set false when vy < 0. But at rest vy is 0 → floor check runs each tick (after adding gravity vy=0.3>0 → floor branch) → onGround true. Good. Body AI uses `e.vy === 0` as the vanilla grounded condition anyway.

hitSolid:
```ts
/** AABB 与实心块相交(近似 Collision.SolidTiles;拳冲出段关 noTileCollide 后的撞停判定) */
function hitSolid(game: GameHooks, e: Enemy): boolean {
  const st = game.world.store;
  const x0 = Math.floor(e.x / TILE), x1 = Math.floor((e.x + e.w - 0.01) / TILE);
  const y0 = Math.floor(e.y / TILE), y1 = Math.floor((e.y + e.h - 0.01) / TILE);
  for (let tx = x0; tx <= x1; tx++) for (let ty = y0; ty <= y1; ty++) {
    if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) return true;
  }
  return false;
}
```

Body AI:

```ts
export function golemAI(e: Enemy, game: GameHooks, player: Player | null) {
  const x = bodyXOf(e);

  // ---- 血尽转换(本族约定,见文件头):进入死亡演出,头转自由态续战 ----
  if (e.hp <= 0 && !x.dying) {
    x.dying = true; x.deadT = 0; e.ai3 = 1;   // ai3=1 死亡标记(头/拳据此转锚/自由)
    e.hp = e.maxHp;                            // 满血续命,防止每 tick 重入
    game.playSfx('roar', 0.9);
  }

  // ---- 首帧:localAI[0]==0 生成部件(NPC.cs:19458-19467) ----
  if (!e.bInit) {
    e.bInit = true;
    e.ai0 = 0; e.ai1 = 0; e.ai3 = 0;
    e.alphaFade = false; x.alpha = 255;        // 接管渐显(原版 AI 内 alpha -= 10)
    const spawn = (id: number, ox: number, oy: number, side: number) => {
      const p = spawnPart(game, e, id);
      if (!p) return;
      p.x = e.cx + ox; p.y = e.cy + oy;        // 原版 NewNPC 传左上角坐标
      p.ai0 = side; p.bInit = false;           // 拳 ai0=侧别(-1 左/1 右);部件各自首帧初始化
    };
    spawn(247, -84, -9, -1);
    spawn(248, 78, -9, 1);
    spawn(246, -3, -57, 0);
  }

  // ---- 出生渐显(NPC.cs:19477-19485):期间 ai[1]=0(蓄力冻结) ----
  if (fadeAlpha(e, x) > 0) e.ai1 = 0;

  // ---- 死亡演出:无敌+碎裂尘,60t 后真死(头/拳由各自 AI 继续) ----
  if (x.dying) {
    e.iframes = 2;
    e.vx *= 0.9;
    e.vy = Math.min(e.vy + GRAV, MAX_FALL);
    e.x += e.vx; e.y += e.vy;
    collideGround(e, game);
    x.deadT++;
    if (x.deadT % 6 === 0) game.spawnParticles(e.cx + (Math.random() - 0.5) * e.w, e.cy + (Math.random() - 0.5) * e.h, '#B04030', 6, 2.4, { life: 36 });
    if (x.deadT >= 60) { e.dead = true; return; }
    return;
  }

  const num = balanceNum(game, player);

  // ---- 部件存活扫描(NPC.cs:19487-19512) ----
  let hasHead = false, hasL = false, hasR = false;
  for (const n of game.enemies() as Enemy[]) {
    if (n.dead) continue;
    if (n.vanillaId === 246) hasHead = true;
    else if (n.vanillaId === 247) hasL = true;
    else if (n.vanillaId === 248) hasR = true;
  }
  // dontTakeDamage = 挂载头在场(NPC.cs:19513):一阶段本体无敌,先打头/拳
  if (hasHead) e.iframes = 2;
  // getGoodWorld 火把破坏(19514-19534,expert 略)

  // ---- 断臂尘(NPC.cs:19536-19595):原版每 tick 两簇 Dust+Gore,此处每 10t 一簇粒子近似 ----
  if (!hasL && e.aiT % 10 === 0) game.spawnParticles(e.cx - 80 * SCALE, e.cy - 9, '#9A8FA0', 3, 1.2, { life: 40 });
  if (!hasR && e.aiT % 10 === 0) game.spawnParticles(e.cx + 62 * SCALE, e.cy - 9, '#9A8FA0', 3, 1.2, { life: 40 });

  // ---- 跳跃穿墙解除(NPC.cs:19569-19578) ----
  if (x.noTC && player && !player.dead) {
    if (e.vy > 0 && e.y + e.h > player.y) x.noTC = false;
    else if (losClear(game, e.cx, e.cy, player.cx, player.cy) && !hitSolid(game, e)) x.noTC = false;
  }

  const dir = player ? (Math.sign(player.cx - e.cx) || e.facing || 1) : 1;
  if (player) e.facing = dir;

  if (player && e.ai0 === 0) {
    // ---- 地面蓄力(19580-19645):ai[1] 攒 300 → -20 蹲 20t(蹲帧动画)→ ai[1]==-1 起跳 ----
    if (e.vy === 0) {
      e.vx *= 0.8;
      let num4 = 1;
      if (e.ai1 > 0) {
        if (!hasL) num4 += 2;
        if (!hasR) num4 += 2;
        if (!hasHead) num4 += 2;
        if (e.hp < e.maxHp) num4 += 1;
        if (e.hp < e.maxHp / 2) num4 += 4;
        if (e.hp < e.maxHp / 3) num4 += 8;
        num4 *= num;
        // getGoodWorld: num4 += 100(19613-19616,expert 略)
      }
      e.ai1 += num4;
      if (e.ai1 >= 300) e.ai1 = -20;
      else if (e.ai1 === -1) {
        // 起跳(19624-19643):穿墙跳,vx=4*dir;受伤跳更高 -12.1*(num+9)/10 钳 -19.1
        x.noTC = true;
        e.vx = 4 * dir;
        e.vy = e.hp < e.maxHp ? Math.max(-19.1, -12.1 * ((num + 9) / 10)) : -12.1;
        e.ai0 = 1; e.ai1 = 0;
      }
    }
  } else if (player && e.ai0 === 1) {
    // ---- 跳跃段(19646-19708) ----
    if (e.vy === 0) {
      // 落地(19648-19661):Item14 音效+落地尘
      game.playSfx('roar', 0.35);
      game.spawnParticles(e.cx, e.y + e.h, '#9A8FA0', 12, 2.2, { life: 40 });
      e.ai0 = 0;
    } else {
      if (e.x < player.x + player.w && e.x + e.w > player.x) {
        e.vx *= 0.9;
        if (e.y + e.h < player.y) e.vy += 0.2 * ((num + 1) / 2);
      } else {
        e.vx += 0.2 * dir;
        let num7 = 3;
        if (e.hp < e.maxHp) num7 += 1;
        if (e.hp < e.maxHp / 2) num7 += 1;
        if (e.hp < e.maxHp / 4) num7 += 1;
        num7 *= (num + 1) / 2;
        e.vx = clamp(e.vx, -num7, num7);
      }
    }
  }

  // ---- 离场(19709-19721):玩家缺失或曼哈顿距离 > 3000 → 清除 ----
  if (!player || Math.abs(e.cx - player.cx) + Math.abs(e.cy - player.cy) > 3000) { e.dead = true; return; }

  // ---- 重力+位移+落地(原版共享物理:noGravity=false → 0.3/2t,maxFall 10) ----
  e.vy = Math.min(e.vy + GRAV, MAX_FALL);
  e.x += e.vx;
  e.y += e.vy;
  if (!x.noTC) collideGround(e, game);
  else e.onGround = false;
}
```

Wait — issue: when player is null, my code skips both ai0 branches but continues to movement. Vanilla with player dead: `noTileCollide = true` then continues the state machine (with target 255?). Then despawn when dist > 3000 (target dead → TargetClosest fails → dist check → active=false). My version: player null → dead = true immediately. Hmm, that diverges: vanilla requires the 3000 check... with no valid target, Main.player[target] is player[255] (dummy at 0,0?) — actually TargetClosest leaves target=255 and Main.player[255] is a dummy. Then dist check: |center - dummy.center| > 3000 → despawn. In our engine player null means nobody. I'll keep: if !player → despawn (e.dead = true) — reasonable; note as simplification. Actually careful — despawned body means head goes free and fists anchor head... the fight continues without a target? With player null the whole fight should end. Hmm. My head/fist AIs with player null: head anchored follows body; free head: no movement. It's fine.

But careful in probe: player always exists ✓.

Another subtlety: vanilla checks `if (velocity.Y == 0f)` INSIDE ai[0]==0 — and importantly the jump-trigger `else if (ai[1] == -1f)` — my port ✓.

Landing sound: vanilla plays Item14 EVERY landing... plus ai[0]=0. ✓.

Now — hmm, one thing: vanilla body's vx *= 0.8 happens only when grounded. During the dying state I do vx *= 0.9. Fine.

Also — gravity: I add gravity every tick including when grounded (vy=0.3 then collide resets). But in the ai0===0 grounded branch I check `e.vy === 0` BEFORE adding gravity — order: vanilla applies gravity in shared physics AFTER AI. Vanilla: AI runs, then UpdateNPC applies gravity? Actually vanilla applies gravity BEFORE AI? In vanilla UpdateNPC: gravity applied, then ai. Hmm — vanilla NPC.UpdateNPC order: `if (!noGravity) velocity.Y += gravity` happens... In Terraria, gravity is applied in UpdateNPC before AI() I believe. Doesn't matter much: my order (AI reads vy, then gravity+move) matches "vy==0 at AI time when grounded" — since after collide vy=0. If gravity were applied before AI, grounded vy would be 0.3 → `velocity.Y == 0` false → golem would never charge/jump! So vanilla must apply gravity after AI or the body would never act... Vanilla: golem's vy is 0 on ground because gravity is applied then collision zeroes it within the same tick? In vanilla, Collision happens after AI too (position integration in UpdateNPC after AI). So during AI, velocity.Y is exactly 0 while standing ✓. My ordering matches vanilla: AI first, then gravity+integrate+collide.

Now the head AI:

```ts
export function golemHeadAI(e: Enemy, game: GameHooks, player: Player | null) {
  const x = headXOf(e);
  if (e.vanillaId === 249) x.free = true;   // 直接生成的自由头(原版 NewNPC 249)
  if (!e.bInit) {
    e.bInit = true;
    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = x.free ? 1 : 0;
    e.alphaFade = false; x.alpha = x.free ? 0 : 255;   // 249 SetDefaults 无 alpha
  }

  // ---- 血尽转换(文件头约定):自由头死=战斗结束全族自毁;挂载头死=转自由态 ----
  if (e.hp <= 0) {
    if (x.free) {
      e.dead = true;
      for (const n of game.enemies() as Enemy[]) {
        if (!n.dead && n.vanillaId !== null && n.vanillaId >= 245 && n.vanillaId <= 249 && n !== e) n.dead = true;
      }
      game.spawnParticles(e.cx, e.cy, '#C04030', 20, 3, { life: 40 });
      return;
    }
    golemHeadGoFree(e, game);
  }

  // ---- 属性:自由头按 249 SetDefaults(NPC.cs:12139-12149:damage 80/defense 32) ----
  const b = baseOf(e);
  if (x.free) {
    const free = vanillaNpc(249);
    e.def.damage = free?.damage ?? 80;
    e.def.defense = free?.defense ?? 32;
  } else {
    e.def.damage = b.dmg;
    e.def.defense = b.def;
  }

  const body = findBody(game);
  // 本体死亡/缺失 → 挂载头转自由态(本族约定:本体死透后头继续)
  if (!x.free && (!body || body.ai3 === 1 || body.hp <= 0)) golemHeadGoFree(e, game);

  const num = balanceNum(game, player);

  if (!x.free && body) {
    // ================= 挂载态 aiStyle 46(NPC.cs:31273-31499) =================
    // noTileCollide = true(:31284);锚点 = 本体.Center + (-3*scale, -57*scale)(:31290-31308)
    const dx = body.cx - 3 * SCALE - e.cx;
    const dy = body.cy - 57 * SCALE - e.cy;
    const dist = Math.hypot(dx, dy);
    if (dist < 100) { e.spin = 0; e.vx = dx; e.vy = dy; }        // 100 内直接贴锚
    else { e.vx = (dx / dist) * 100; e.vy = (dy / dist) * 100; e.spin = e.vx * 0.1; }
    // 渐显(:31310-31317):期间 ai[1]=30
    if (fadeAlpha(e, x) > 0) e.ai1 = 30;
    if (player) {
      if (e.ai0 === 0) {
        // ---- 嘴部火焰弹循环(:31319-31347):300t 一发 proj 258(伤 18 速 8) ----
        e.ai1 += 1;
        if (e.ai1 < 20 || e.ai1 > 280) { e.ai1 += (2 * (num - 1)) / 3; x.l0 = 1; }
        else { e.ai1 += (1 * (num - 1)) / 2; x.l0 = 0; }
        if (e.ai1 >= 300) {
          e.ai1 = 0;
          golemSpit(game, e, player, 0, 10 * SCALE, 8, 18, 258);
        }
      } else if (e.ai0 === 1) {
        // ---- 眼部阶段(:31353-31486):嘴弹伤 24 + 眼激光 259(伤 28) ----
        x.l1 = player.cx < e.cx - e.w ? -1 : player.cx > e.cx + e.w ? 1 : 0;   // localAI[1] 侧别
        const num733 = (num + 3) / 4;
        e.ai1 += num733;
        if (e.hp < e.maxHp * 0.4) e.ai1 += num733;
        if (e.hp < e.maxHp * 0.2) e.ai1 += num733;
        x.l0 = e.ai1 < 20 || e.ai1 > 280 ? 1 : 0;
        if (e.ai1 >= 300) {
          e.ai1 = 0;
          golemSpit(game, e, player, x.l1 * 40 * SCALE, 10 * SCALE, 8, 24, 258);
        }
        e.ai2 += num733;
        if (e.hp < e.maxHp / 3) e.ai2 += num733;
        if (e.hp < e.maxHp / 4) e.ai2 += num733;
        if (e.hp < e.maxHp / 5) e.ai2 += num733;
        if (!losClear(game, e.cx, e.cy, player.cx, player.cy)) e.ai2 += 4;     // :31456
        if (e.ai2 > 60 + Math.random() * 600) {
          e.ai2 = 0;
          golemEyeLasers(game, e, player, x.l1, 28, SCALE);
        }
      }
      // 阶段派生(:31487-31491):血 < 半 → 眼部阶段
      e.ai0 = e.hp < e.maxHp / 2 ? 1 : 0;
    }
  } else {
    // ================= 自由态 aiStyle 48 GolemHeadFree(NPC.cs:31500-31741) =================
    // flag48(:31503-31519):看不到玩家 → 穿墙
    const noLos = !player || !losClear(game, e.cx, e.cy, player.cx, player.cy);
    if (player) {
      // 悬浮(:31521-31564):目标 = 玩家 + (0,-300),7 速/0.05 步进(符号翻转双步进)
      e.vx = accelTo(e.vx, 0, 0.05);  // placeholder replaced below
      ...
    }
  }
  e.x += e.vx; e.y += e.vy;
}
```

Let me write the free branch concretely:

```ts
    if (player) {
      const dx = player.cx - e.cx, dy = player.cy - 300 - e.cy;
      const d = Math.hypot(dx, dy) || 1;
      e.vx = accelTo(e.vx, (dx / d) * 7, 0.05);
      e.vy = accelTo(e.vy, (dy / d) * 7, 0.05);
      const num761 = (num + 4) / 5;
      e.ai1 += num761;
      // 原版按 golemBoss.life 分档(:31570-31582);二阶段本体已亡 → 改按头自身血量分档(简化项)
      const r = e.hp / e.maxHp;
      if (r < 0.8) e.ai1 += num761;
      if (r < 0.6) e.ai1 += num761;
      if (r < 0.2) e.ai1 += num761;
      if (r < 0.1) e.ai1 += num761;
      x.l0 = e.ai1 < 20 || e.ai1 > 280 ? 1 : 0;   // 张嘴帧(:31584-31592)
      if (noLos) e.ai1 = 20;                       // :31593-31595
      if (e.ai1 >= 300) {                          // :31596-31617 嘴弹 proj 258(伤 20 速 8)
        e.ai1 = 0;
        golemSpit(game, e, player, 0, -10 * SCALE, 8, 20, 258);
      }
      // 眼激光(:31618-31717)
      e.ai2 += num;
      if (r < 1 / 1.25) e.ai2 += num;   // 0.8
      if (r < 1 / 1.5) e.ai2 += num;    // 0.667
      if (r < 1 / 2) e.ai2 += num;
      if (r < 1 / 3) e.ai2 += num;
      if (r < 1 / 4) e.ai2 += num;
      if (r < 1 / 5) e.ai2 += num;
      if (r < 1 / 6) e.ai2 += num;
      // flag49(:31646-31651):原版=本体↔玩家无视线;此处用头↔玩家(简化项)
      if (noLos) e.ai2 += num * 10;
      if (e.ai2 > 100 + Math.random() * 4800) {
        e.ai2 = 0;
        golemEyeLasersFree(game, e, player, noLos, r, SCALE);
      }
    }
```

golemSpit helper: shoot from (e.cx + ox, e.cy + oy) toward player center, speed, dmg, proj:
```ts
/** 嘴部/额前火焰弹(NPC.cs:31331-31347 / 31430-31447 / 31596-31617):
 *  从偏移点朝玩家中心 proj 258(原版 NewProjectile 后无 timeLeft 覆写 → 默认) */
function golemSpit(game, e, player, ox, oy, spd, dmg, projId) {
  const sx = e.cx + ox, sy = e.cy + oy;
  const dx = player.cx - sx, dy = player.cy - sy;
  const d = Math.hypot(dx, dy) || 1;
  shoot(game, sx, sy, (dx / d) * spd, (dy / d) * spd, dmg, projId);
}
```
Note life: default 300 in shoot ✓ (vanilla fireball 258 has timeLeft default 600? NewProjectile without timeLeft → timeLeft = 60? Actually projectile default timeLeft... shoot defaults life=300 like other boss AIs. Fine.)

golemEyeLasers (attached head, NPC.cs:31459-31484):
```ts
function golemEyeLasers(game, e, player, side, dmg, scale) {
  const fire = (ox: number, spd: number) => {
    const sx = e.cx + ox, sy = e.cy - 22 * scale;
    const dx = player.cx - sx, dy = player.cy - sy;
    const d = Math.hypot(dx, dy) || 1;
    const vx = (dx / d) * spd, vy = (dy / d) * spd;
    shoot(game, sx + vx * 3, sy + vy * 3, vx, vy, dmg, 259, 300);
  };
  if (side === 0) { fire(-18 * scale, 11); fire(18 * scale, 11); }
  else fire(side * 30 * scale, 12);
}
```
Check vanilla: two-shot branch vector85 = (cx ± 18*scale, cy - 22*scale), num745 = 11; spawn `vector85.X += num746*3` — note: it aims at `player.position.X + width*0.5 - vector85.X` computed BEFORE the offset? Look: num746 = player.cx - vector85.X; ... normalized; then `vector85.X += num746 * 3f` — vector85 gets modified after computing velocity, and NewProjectile uses the modified vector85. And the velocity uses num746 computed from the pre-offset vector85. Same as my implementation ✓.

golemEyeLasersFree (NPC.cs:31659-31717):
```ts
function golemEyeLasersFree(game, e, player, noLos, r, scale) {
  for (let i = 0; i < 2; i++) {
    const sx = e.cx + (i === 0 ? -14 : 14) * scale;
    const sy = e.cy - 50 * scale;
    let dmg = 24, spd = 11;
    if (r < 0.5) { dmg++; spd += 0.25; }
    if (r < 0.4) { dmg++; spd += 0.25; }
    if (r < 0.3) { dmg++; spd += 0.25; }
    if (r < 0.2) { dmg++; spd += 0.25; }
    if (r < 0.1) { dmg++; spd += 0.25; }
    let tx = player.cx, ty = player.cy;
    if (noLos) {
      dmg = Math.floor(dmg * 1.5);
      spd *= 2.5;
      const pvx = (player as unknown as { vx: number }).vx ?? 0;
      const pvy = (player as unknown as { vy: number }).vy ?? 0;
      tx += pvx * Math.random() * 50;
      ty += pvy * Math.random() * 50;
    }
    const dx = tx - sx, dy = ty - sy;
    const d = Math.hypot(dx, dy) || 1;
    const vx = (dx / d) * spd, vy = (dy / d) * spd;
    shoot(game, sx + vx * 3, sy + vy * 3, vx, vy, dmg, 259, 300);
  }
}
```

golemHeadGoFree:
```ts
/** 挂载头 → 自由态(原版 checkDead 语义:246 血尽在原地 NewNPC 249,NPC.cs:85842-85847;
 *  本工程头原体变身,满血+属性对齐 249 SetDefaults(NPC.cs:12139-12149)) */
function golemHeadGoFree(e: Enemy, game: GameHooks) {
  const x = headXOf(e);
  if (x.free) return;
  x.free = true;
  e.ai3 = 1;          // 自由态标记(探针/渲染可观测)
  e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
  e.hp = e.maxHp;     // 原版 249 满血登场
  e.vx *= 0.5; e.vy = Math.min(e.vy, 0);
  game.spawnParticles(e.cx, e.cy, '#C04030', 16, 2.6, { life: 30 });
  game.playSfx('roar', 0.8);
}
```

Fist AI:

```ts
export function golemFistAI(e: Enemy, game: GameHooks, player: Player | null) {
  const x = fistXOf(e);
  if (!e.bInit) {
    e.bInit = true;
    e.ai0 = e.vanillaId === 247 ? -1 : 1;   // ai0=侧别(-1 左拳 247 / 1 右拳 248;任务约定)
    e.ai1 = 0;
    e.alphaFade = false; x.alpha = 255;
  }
  const side = e.ai0 === 1 ? 1 : -1;
  const isLeft = e.vanillaId === 247;

  // ---- 锚主选择:golemBoss 缺失 → 自毁(NPC.cs:19182-19186) ----
  //  本体存活(含死亡演出)→ 锚本体;本体死透 → 锚自由头(任务约定"锚定本体(或头)")
  const body = findBody(game);
  const head = findHead(game);
  const anchor = body && !body.dead ? body : head;
  if (!anchor) { e.dead = true; return; }

  const num = balanceNum(game, player);
  // 渐显(:19187-19194):期间 ai[1]=0
  if (fadeAlpha(e, x) > 0) e.ai1 = 0;

  // ---- 肩锚点(:19197-19199):锚主.Center + 锚主.velocity + (±84/78*scale, -9*scale) ----
  const offX = isLeft ? -84 : 78;
  const tx = anchor.cx + anchor.vx + offX * SCALE;
  const ty = anchor.cy + anchor.vy - 9 * SCALE;
  const dx = tx - e.cx, dy = ty - e.cy;
  const dist = Math.hypot(dx, dy) || 0.0001;
  e.facing = -side;

  if (!player) { e.x += e.vx; e.y += e.vy; return; }

  if (x.state === 0) {
    // ---- 归位/待机蓄力(:19202-19270) ----
    x.noTC = true;
    let num3 = 14;
    if (e.hp < e.maxHp / 2) num3 += 3;
    if (e.hp < e.maxHp / 4) num3 += 3;
    if (anchor.hp < anchor.maxHp) num3 += 8;
    num3 *= (num + 3) / 4;
    if (num3 > 32) num3 = 32;
    if (dist < 12 + num3) {
      // 贴肩:整帧位移到锚点方向,蓄力计时
      e.spin = 0;
      e.vx = dx; e.vy = dy;
      e.ai1 += num;
      if (e.hp < e.maxHp / 2) e.ai1 += num;
      if (e.hp < e.maxHp / 4) e.ai1 += num;
      if (anchor.hp < anchor.maxHp) e.ai1 += 10 * num;
      if (e.ai1 >= 60) {
        // 出拳侧别判定(:19244-19256):左拳只在玩家偏左时出、右拳对称
        if ((isLeft && e.cx + 100 > player.cx) || (!isLeft && e.cx - 100 < player.cx)) {
          e.ai1 = 0; x.state = 1;
        } else e.ai1 = 0;
      }
    } else {
      e.vx = (dx / dist) * num3;
      e.vy = (dy / dist) * num3;
      e.spin = isLeft ? Math.atan2(e.vy, e.vx) : Math.atan2(-e.vy, -e.vx);   // :19260-19262
    }
  } else if (x.state === 1) {
    // ---- 蓄力(贴肩 30t,:19271-19332) ----
    e.ai1 += 1;
    e.x = tx - e.w / 2;      // Center = 肩锚点(原版 base.Center = vector)
    e.y = ty - e.h / 2;
    e.spin = 0; e.vx = 0; e.vy = 0;
    if (e.ai1 <= 15) game.spawnParticles(e.cx + (Math.random() - 0.5) * 30, e.cy + (Math.random() - 0.5) * 30, '#C8A040', 1, 0.8, { life: 26 });
    if (e.ai1 >= 30) {
      x.noTC = true;
      x.state = 2; e.ai1 = 0;
      let num6 = 12;
      if (e.hp < e.maxHp / 2) num6 += 4;
      if (e.hp < e.maxHp / 4) num6 += 4;
      if (anchor.hp < anchor.maxHp) num6 += 10;
      num6 *= (num + 3) / 4;
      if (num6 > 48) num6 = 48;
      const pdx = player.cx - e.cx, pdy = player.cy - e.cy;
      const pd = Math.hypot(pdx, pdy) || 1;
      e.vx = (pdx / pd) * num6; e.vy = (pdy / pd) * num6;
      e.spin = isLeft ? Math.atan2(-e.vy, -e.vx) : Math.atan2(e.vy, e.vx);   // :19325-19328
    }
  } else if (x.state === 2) {
    // ---- 冲拳飞行(:19333-19393) ----
    e.ai1 += 1;
    if (e.ai1 === 1) game.playSfx('roar', 0.4);   // SoundID.Item14
    if (e.aiT % 2 === 0) game.spawnParticles(e.cx + e.vx * 0.5, e.cy + e.vy * 0.5, '#E08040', 1, 0.6, { life: 20 });
    // 过轴判定(:19363-19388):主轴冲过玩家 → 关穿墙(开始撞墙)
    if (Math.abs(e.vx) > Math.abs(e.vy)) {
      if (e.vx > 0 && e.cx > player.cx) x.noTC = false;
      if (e.vx < 0 && e.cx < player.cx) x.noTC = false;
    } else {
      if (e.vy > 0 && e.cy > player.cy) x.noTC = false;
      if (e.vy < 0 && e.cy < player.cy) x.noTC = false;
    }
    // 撞墙/离锚 700 → 回位(:19389-19392)
    const hit = !x.noTC && hitSolid(game, e);
    if (dist > 700 || hit) { x.noTC = true; x.state = 0; }
  } else if (x.state === 3) {
    // ---- 直飞追击(:19394-19446;原版无处置 ai[0]=3,保留 1:1) ----
    x.noTC = true;
    const pdx = player.cx - e.cx, pdy = player.cy - e.cy;
    const pd = Math.hypot(pdx, pdy) || 1;
    e.vx = accelTo(e.vx, (pdx / pd) * 12, 0.4);
    e.vy = accelTo(e.vy, (pdy / pd) * 12, 0.4);
    e.spin = isLeft ? Math.atan2(-e.vy, -e.vx) : Math.atan2(e.vy, e.vx);
  }

  // 位移(状态 1 已直接贴锚;其余按速度积分)。冲拳非穿墙段撞墙即回位(state 2 内处理)
  if (x.state !== 1) {
    e.x += e.vx; e.y += e.vy;
    if (x.state === 2 && !x.noTC && hitSolid(game, e)) { x.noTC = true; x.state = 0; }
  }
}
```

Hmm the double hitSolid check is redundant; keep only one (in state 2). Actually the movement after position change could newly hit a wall; simpler: check hitSolid once after movement. Let me restructure: in state 2, after moving, `if (!x.noTC && hitSolid(...)) { ...state=0 }` plus the dist check before moving. I'll keep the dist check before movement and the solid check after movement.

Wait, also the fist punch direction when player is at the same position as fist → pd tiny → fine.

One issue: probe ④ expects "回归头部附近" (return near the head/anchor). After the punch, state 0 homes back at speed 14 (num3=14 since anchor full HP) — 700px takes 50 ticks at 14px/t. My probe runs enough ticks.

Another consideration: x.state for the fist in WeakMap — the probe can't observe state directly... it doesn't need to.

But hmm — one risk: two fists both punching upward simultaneously, both end state 2 → both return. Peak displacement: they fly until dist > 700. At 12 speed that's ~58 ticks. Then return. Total ≈ 60 (charge) + 30 (windup) + 58 + 55 ≈ 200 ticks. I'll run 400 and sample.

But WAIT — there's a subtle issue with the punch direction and the "过轴判定": punch is nearly straight up (player 85px above fist, 42px right). |vx| vs |vy|: vx = 42/327*12 ≈ 1.5, vy ≈ -11.9 → |vy| dominant → Y-axis check: vy < 0 && cy < player.cy → after ~7 ticks cy < player.cy → noTC = false → then collision ON. Flying up in open air (no ceiling) → no collision → continues to 700 → returns ✓.

In the real game there'd be a ceiling → collides → returns ✓.

Now, potential problem: while noTC false and passing through the floor region? Not here.

Next: the probe. Structure similar to _dukemlprobe: local dispatch map 45/46/47 → functions; player stub; run loop calling AI directly with iframes decrement.

Also — aiT: Enemy.aiT incremented in fixedUpdate; my AIs use e.aiT % 10 / % 2 — since probe doesn't call fixedUpdate, aiT stays 0 → `e.aiT % 10 === 0` true every tick → more particles (stub, fine).

Probe assertions:

```
① const body = Enemy.fromVanilla(245, 100*16, 120*16)!; body.id = 1; enemies.push(body);
run(1);
check('首帧生成头 246', enemies.some(e => e.vanillaId === 246));
check('首帧生成双拳 247/248', ... one each);
check('拳 ai0 侧别 ±1', fist247.ai0 === -1 && fist248.ai0 === 1);
check('本体 ai0=0 蓄力态', body.ai0 === 0);
```
Careful: run(1) — the first tick: body AI bInit spawns parts; parts also run their AI this same tick (they're appended to enemies during iteration? I iterate over [...enemies] copy taken at loop start — parts spawned during body's AI won't be updated this tick. Fine.

Note: parts spawn at e.cx-84 etc. — but the body hasn't fallen yet; all in air; head anchors to body ✓.

```
② settle & jump
run(120);  // 落地+蓄力
let sawAir = false, minY = body.cy;
const x0 = body.cx;
for (let i = 0; i < 500; i++) { run(1); if (!body.onGround) sawAir = true; minY = Math.min(minY, body.cy); }
check('本体起跳(离地)', sawAir);
check('跳起高度 > 150px', (2330? ...) use body landing baseline...
```
Simpler: record cyBase = body.cy after settle; then minY < cyBase - 150 ✓; and after the loop check onGround true again (landed). And horizontal movement: with the player at same x, dir fallback = facing (1) → vx=4 → some displacement. Check Math.abs(body.cx - x0) > 4? During flight, the player-within-span branch damps vx*0.9... vx=4 → total ≈ 40px. So > 8 ✓. Hmm, but wait: dir = Math.sign(0) || e.facing || 1 → e.facing initial 1 → dir=1 ✓.

Actually careful — is `body.onGround` true right after settle? My body AI only sets onGround via collideGround when !noTC. Initially noTC false → collide runs ✓.

Timeline check for the jump: settle ~30 ticks (fall 480px at 0.3 accel: t=sqrt(2*480/0.3)=56 ticks). run(120) enough. ai1 accumulates from 0 → 300 needs 300 ticks (num4=1, hp full... wait hp full → the `ai[1] > 0` branch runs (ai1 starts 0; first tick ai1 += 1 → 1 > 0 → num4 = 1 + bonuses (none, full hp, all parts) → 1). So 300 ticks → -20 → then 19 ticks to -1 → jump. So first jump at ~375 ticks after landing. run(120) + 500 loop = 620 ✓ saw jump.

During flight, when does it land? vy=-12.1, gravity 0.3 → airtime 2*12.1/0.3 = 80 ticks, height 244px. Land → ai0=0 → ai1=0 (set at jump) → accumulates again. ✓

③ body hp → 0:
```
body.hp = 0;
run(2);
check('本体进入死亡演出(ai3=1)', body.ai3 === 1);
const head = ...246;
check('头存活', !head.dead);
run(70);
check('本体 60t 后真死', body.dead);
check('头转自由态(ai3=1)', head.ai3 === 1);
check('自由头满血续命(249 语义)', head.hp === head.maxHp);
const hy0 = head.cy, hx0 = head.cx;
run(240);
check('自由头自主移动', Math.hypot(head.cx - hx0, head.cy - hy0) > 40, [...]);
```
Careful: head.hp = maxHp check must run AFTER the transition tick. run(2) after hp=0: tick1: head AI sees body.ai3? The body AI runs first (array order body, fists, head — spawn order: 247, 248, 246 appended after body). Body sets dying+ai3=1 on tick1; head AI tick1: body.ai3 is 1 (body ran earlier this tick since body is first in array) → goFree immediately. So head.ai3===1 after run(1) even. I'll check after run(2).

Wait — ordering: in run(), I iterate `[...enemies]` — array order: body(245), fist247, fist248, head246. Body first ✓. But careful — my head AI computes `body.ai3 === 1` — body.ai3 set in the same tick before head runs ✓.

Also check free head damage = 80 (249 data): head.def.damage === (vanillaNpc(249).damage). I can compute expected via Enemy.fromVanilla(249,0,0)!.def.damage. Nice extra check. But fromVanilla(249) requires the JSON entry (exists). def.damage = v.damage = 80 ✓. I'll assert head.def.damage === 80.

Also during ③→ run(70): body dead at 60t; my run loop skips dead entities (`if (e.dead) continue`) ✓.

Hmm wait — one problem: after body.dead, findBody returns null → head: `!x.free && (!body ...)` → already free ✓. Fists: anchor = head ✓.

④ fist punch — but wait, I planned ④ BEFORE ③ (body alive). Order in probe: ① → ② → ④ → ③ → ⑤.

For ④:
```
const fistL = enemies.find(e => e.vanillaId === 247)!;
const shoulder0 = () => { const b = body; return { x: b.cx - 84*0.5 + b.vx, y: b.cy - 9*0.5 + b.vy }; };
let peak = 0, returned = false;
for (let i = 0; i < 460; i++) {
  run(1);
  const s = shoulder0();
  const d = Math.hypot(fistL.cx - s.x, fistL.cy - s.y);
  peak = Math.max(peak, d);
  if (peak > 100 && d < 150) returned = true;
  if (returned) break;
}
check('拳蓄力冲出(峰值位移 > 100px)', peak > 100, Math.round(peak));
check('拳回位(肩锚 150px 内)', returned);
```
Hmm: the initial fist position: spawn top-left = (cx-84, cy-9) → fist center = (cx-84+20, cy-9+15) = (cx-64, cy+6) = (1536, 1926) at spawn (body center y=1920). Shoulder = (1600-42, 1920-4.5+vy) = (1558, 1915.5+vy). Initial dist = hypot(22, -10) ≈ 24 < 26 ✓.

But before ④ the body has been jumping around (from ②, 500+ ticks). By the time ④ starts, the body may be mid-air or grounded; the fist tracks the shoulder at 14 speed regardless ✓.

Peak displacement measured from the SHOULDER — during the punch, the fist goes 700 away ✓. But careful: peak might never exceed 100 if... the punch trigger needs ai1 >= 60 while within (12+num3=26) of shoulder — the body is jumping; when the body jumps, the shoulder moves up to 244px in Y quickly (vy up to -12/tick → fist homing 14/tick keeps up mostly). During the jump the fist may fall behind > 26 → ai1 freezes (doesn't reset though — ai1 only accumulates when close). Vanilla same. It'll get its 60 eventually. 460 ticks is plenty (jump cycle 320t ground + 80t air; plenty of grounded time).

One risk: the punch fires while the body is mid-jump: punch toward player from a moving shoulder — fine.

Another risk: `returned` requires d < 150 after peak > 100. After the punch ends (dist > 700), the fist homes back; when within 26 it snaps. ✓

Also both fists will punch; I check only the left one, maybe check both. I'll track both and require at least the left one (or both) — I'll check both punches happen? Right fist: player at 1600; right fist cx ≈ 1639; condition `cx - 100 < player.cx` → 1539 < 1600 ✓ punches. I'll check both for robustness.

Hmm — one thing to double check: at state 1 (windup), `e.x = tx - e.w/2` uses the shoulder computed at the TOP of the AI (before state machine) — which uses anchor.cx + anchor.vx. Body.vx is nonzero while walking? On ground vx *= 0.8 → decays. OK.

⑤:
```
head.hp = 0;
run(2);
check('头死 → 全族自毁', enemies.every(e => e.vanillaId === 245 || ... all dead));
```
After ③ the body is already dead; so check fists dead + head dead.

Also — projectile check: during the run, the attached head fires fireballs every 300 ticks. run total ticks: 1 + 120 + 500 + 460 + ... > 900 → at least 2 mouth fireballs fired. Check projectiles.length > 0 somewhere. The task doesn't require it but nice: add a check "头喷射火焰弹(258)" — projectiles array contains Arrow with projId 258. Let me add: `check('头/自由头发射过弹幕(258/259)', projectiles.some(p => (p as Arrow).projId === 258 || 259))`. Need Arrow import type — I can just cast. Let me include `(p as { projId: number }).projId`.

Free head also fires. Since total ticks > 1000, fireballs definitely fired (attached phase 300t cycle; also free phase). But note: the head's phase-0 fireball only fires if player is not null ✓.

Now — WAIT. One important check on the attached head fireball: it fires at ai1 >= 300, and ai1 is reset by the fade (`e.ai1 = 30` while alpha > 0, 26 ticks) — fine.

Also note the attached head only fires in phase ai0 === 0 (mouth) which is derived at the END: `e.ai0 = e.hp < e.maxHp/2 ? 1 : 0` — full HP → 0 → mouth fireballs ✓.

Now, one more important detail I should double check — `findHead` in the fist AI when the head is 246-in-free-mode: vanillaId is still 246 ✓ found.

And the head AI when vanillaId === 246 in free mode: my code path uses the free branch ✓.

Edge: what if BOTH 246 and 249 exist (someone spawns 249 separately)? findHead returns the first. Not a concern.

Now — big remaining question: the body's `ai3` is used as dying flag; vanilla body doesn't use ai[3] ✓ no conflict.

One more: Enemy.ai1 for the body is also used... vanilla body ai[1] is the charge timer ✓ same.

Now, about `e.facing` for the body: vanilla direction is toward target. I set facing = dir each tick (only when player). Renderers use facing for sprite flip ✓.

Potential trap: `Math.sign(player.cx - e.cx) || e.facing || 1` — Math.sign returns -1/0/1; if 0 → e.facing (±1 or 1 default) ✓.

TS strictness: `player.cy` — Player type has cy ✓ (Entity). The probe's player stub is a plain object cast — in the probe I pass `player as never`. In _dukemlprobe they cast via aiByStyle map typing. I'll do similar: `const aiByStyle: Record<number, (e: Enemy, g: GameHooks, p: Player | null) => void> = { 45: golemAI, 46: golemHeadAI, 47: golemFistAI }` and call `fn(e, game, player as Player)`. game is cast `as never` — passing `game as never` to GameHooks param works (never assignable to anything). The probe's game object lacks `critters()` — GameHooks requires critters? The mechprobe game lacks critters too but it's cast `as never` ✓.

For the probe's own calls like `golemAI(body, game, player)` — types: game is `never` ✓ fine; player stub typed structurally — mkPlayer returns object with x,y,w,h,cx,cy,vx,vy,dead — matches a minimal Player? Player is a class with many fields; passing it where `Player | null` expected — structural typing: the stub lacks required props → type error. Use `player as unknown as Player`. I'll import type { Player } in the probe? Simpler: cast to never like _dukemlprobe does with its map. I'll write:

```ts
const run = (ticks: number) => {
  for (let i = 0; i < ticks; i++) {
    for (const e of [...enemies]) {
      if (e.dead) continue;
      if (e.iframes > 0) e.iframes--;
      const fn = aiByStyle[e.vanilla?.aiStyle ?? -1];
      if (fn) fn(e, game as never, player as never);
    }
  }
};
```
with `const aiByStyle: Record<number, (e: Enemy, g: never, p: never) => void> = { 45: golemAI, 46: golemHeadAI, 47: golemFistAI };` — is `(e: Enemy, game: GameHooks, player: Player|null) => void` assignable to `(e: Enemy, g: never, p: never) => void`? Parameter bivariance for method-style... For function property types with strictFunctionTypes, parameters are checked contravariantly: target param `never` must be assignable to source param `GameHooks` — never is assignable to everything ✓. So OK.

 dukemlprobe did exactly this pattern ✓.

Now — one more consideration for ②: "本体跳跃位移(onGround 切换)" — my body uses `e.vy === 0` for state transitions but onGround for the probe. During noTC jump (x.noTC = true), collideGround is skipped → onGround = false ✓ sawAir true.

Wait — during the jump, noTC is set true at jump start; cleared when `e.vy > 0 && bottom > player.y` — player.y = 2240 (top). Body bottom during jump: starts 2400 (on ground) — wait body bottom when grounded = 2400 = floor top. Condition: vy > 0 (falling) && bottom > player.y (2400 > 2240 ✓) → noTC cleared immediately when starting to fall. Before that (rising), the else branch: losClear && !hitSolid → the body is in open air standing on floor → losClear true (line from body center to player center — player at (1600,2240) inside body's AABB... the losClear samples from e.cx,e.cy to player — no solid between ✓) && !hitSolid(body) — body AABB: y 2260..2400, floor row at ty=150 (2400..2416). Body's bottom edge exactly 2400 → floor((2400-0.01)/16)=149 → not solid (air) ✓ → noTC = false immediately on the FIRST tick of the jump?! Hmm — that kills the phase-through. Vanilla: `Collision.CanHit(position,width,height, player.Center,1,1) && !Collision.SolidTiles(position,width,height)` — SolidTiles checks if the NPC's CURRENT box overlaps solid tiles. Standing on the floor, the body's box touches the floor tile? position.Y + height = 2400 exactly = tile boundary → SolidTiles false (no overlap) → noTileCollide = false immediately. Same in vanilla! So vanilla golem only phases when its box is INSIDE tiles (e.g. jumping from inside a tight temple corridor). Fine — behavior matches.

BUT WAIT: the vanilla noTileCollide-clear block runs BEFORE the ai[0]==0/1 state machine and applies every tick including the grounded phase (noTC left over from a previous jump). And at jump start noTC = true, then... the clearing block already ran this tick (before ai0==0 branch) — order in vanilla: the noTC clear block (19569) comes BEFORE the state machine (19580). At the jump tick, noTC set true at 19626; next tick the clear block runs: body is now above floor, vy < 0 (rising) → first cond false; else losClear && !SolidTiles → true && true → noTC = false. So the body collides during the whole jump (normal case). ✓ matches mine.

So during flight my collideGround runs → the body collides with the floor on landing ✓ onGround toggles ✓.

Now, gravity during noTC: I apply gravity always ✓ (vanilla applies gravity regardless of noTileCollide).

One more check — during the jump, my code checks landing `e.vy === 0` in the ai0===1 branch; vy is 0 right after collideGround. ✓

Next: JSON patch for 248. Mirror 247 exactly with id 248 and name NPC_248:
```json
"248": {"id": 248, "name": "NPC_248", "frames": 1, "lifeMax": 7000, "damage": 59, "defense": 28, "aiStyle": 47, "width": 40, "height": 30, "noGravity": true, "HitSound": "NPCHit4", "DeathSound": "NPCDeath14", "alpha": 255}
```
Should I add knockBackResist 0? 247 lacks it; mirror exactly. OK.

Where in the file? JSON objects — key order doesn't matter; insert after "247" for readability. The file is huge (628 entries); use python to insert and preserve formatting. Actually safer: use python json load → add → dump? That would reformat the entire file (risky — key order preserved in py3.7+ dict, but indentation might change). Better: targeted text insertion after the "247" line. Let me view the raw text around "247".
````

</details>


---

## 🤖 Assistant · 2026-08-10T06:56:48.544Z · glm-x-preview-260804

```
Now let me look at the raw JSON around entry 247 to patch it precisely.
```


---

## 🤖 Assistant · 2026-08-10T06:56:49.036Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n '\"247\"\\|\"248\"\\|\"249\"\\|\"246\"' ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json",
 "description": "Locate 246-249 lines in JSON"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:56:49.067Z

**📎 ToolResult**

```
<persisted-output>
Output too large (145.7KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/8f9c7b63-58b1-49de-a435-85fe12e156d6/tool-results/bqizrxfb0.txt

Preview (first 2KB):
1:{"1": {"id": 1, "name": "Blue Slime", "frames": 2, "lifeMax": 25, "damage": 7, "defense": 2, "aiStyle": 1, "width": 24, "height": 18, "HitSound": "NPCHit1", "DeathSound": "NPCDeath1", "alpha": 175, "color": [0, 80, 255, 100]}, "2": {"id": 2, "name": "Demon Eye", "frames": 2, "lifeMax": 60, "damage": 18, "defense": 2, "knockBackResist": 0.8, "aiStyle": 2, "width": 30, "height": 32, "HitSound": "NPCHit1", "DeathSound": "NPCDeath1"}, "3": {"id": 3, "name": "Zombie", "frames": 3, "lifeMax": 45, "damage": 14, "defense": 6, "knockBackResist": 0.5, "aiStyle": 3, "width": 18, "height": 40, "HitSound": "NPCHit1", "DeathSound": "NPCDeath2"}, "4": {"id": 4, "name": "Eye of Cthulhu", "frames": 6, "lifeMax": 2800, "damage": 15, "defense": 12, "knockBackResist": 0, "aiStyle": 4, "width": 100, "height": 110, "npcSlots": 5, "noGravity": true, "noTileCollide": true, "HitSound": "NPCHit1", "DeathSound": "NPCDeath1"}, "5": {"id": 5, "name": "Servant of Cthulhu", "frames": 2, "lifeMax": 8, "damage": 12, "defense": 0, "aiStyle": 5, "width": 20, "height": 20, "noGravity": true, "noTileCollide": true, "HitSound": "NPCHit1", "DeathSound": "NPCDeath1"}, "6": {"id": 6, "name": "Eater of Souls", "frames": 2, "lifeMax": 40, "damage": 22, "defense": 8, "knockBackResist": 0.5, "aiStyle": 5, "width": 30, "height": 30, "npcSlots": 1, "noGravity": true, "HitSound": "NPCHit1", "DeathSound": "NPCDeath1"}, "7": {"id": 7, "name": "Devourer", "frames": 1, "lifeMax": 100, "damage": 31, "defense": 2, "knockBackResist": 0, "aiStyle": 6, "width": 22, "height": 22, "npcSlots": 3.5, "noGravity": true, "noTileCollide": true, "HitSound": "NPCHit1", "DeathSound": "NPCDeath1", "behindTiles": true}, "8": {"id": 8, "name": "NPC_8", "frames": 1, "lifeMax": 100, "damage": 16, "defense": 6, "knockBackResist": 0, "aiStyle": 6, "width": 22, "height": 22, "noGravity": true, "noTileCollide": true, "HitSound": "NPCHit1", "DeathSound": "NPCDeath1", "behindTiles": true}, "9": {"id": 9, "name": "NPC_9", "frames": 1, "lifeMa
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-10T06:56:54.073Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The JSON is one huge single line. I'll do a targeted string insertion with python: find the "247" entry text and insert "248" after it. Let me extract the exact "247" entry substring.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:56:54.095Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 - <<'EOF'\nimport re\np='~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'\ns=open(p).read()\nm=re.search(r'\"247\": \\{[^}]*\\}, ', s)\nprint(repr(m.group(0)))\nprint('has 248 key:', '\"248\":' in s)\nEOF",
 "description": "Extract exact 247 entry text"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:57:01.013Z

**📎 ToolResult**

```
'"247": {"id": 247, "name": "NPC_247", "frames": 1, "lifeMax": 7000, "damage": 59, "defense": 28, "aiStyle": 47, "width": 40, "height": 30, "noGravity": true, "HitSound": "NPCHit4", "DeathSound": "NPCDeath14", "alpha": 255}, '
has 248 key: False

```


---

## 🤖 Assistant · 2026-08-10T06:57:05.230Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 - <<'EOF'\nimport re, json\np='~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'\ns=open(p).read()\nold='\"247\": {\"id\": 247, \"name\": \"NPC_247\", \"frames\": 1, \"lifeMax\": 7000, \"damage\": 59, \"defense\": 28, \"aiStyle\": 47, \"width\": 40, \"height\": 30, \"noGravity\": true, \"HitSound\": \"NPCHit4\", \"DeathSound\": \"NPCDeath14\", \"alpha\": 255}, '\nassert s.count(old)==1\nnew=old+'\"248\": {\"id\": 248, \"name\": \"NPC_248\", \"frames\": 1, \"lifeMax\": 7000, \"damage\": 59, \"defense\": 28, \"aiStyle\": 47, \"width\": 40, \"height\": 30, \"noGravity\": true, \"HitSound\": \"NPCHit4\", \"DeathSound\": \"NPCDeath14\", \"alpha\": 255}, '\ns=s.replace(old,new)\nopen(p,'w').write(s)\nd=json.load(open(p))\nprint('248 =', json.dumps(d['248'],ensure_ascii=False))\nprint('total', len(d))\nEOF",
 "description": "Insert 248 entry into vanilla-npcs.json"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:57:20.891Z

**📎 ToolResult**

```
248 = {"id": 248, "name": "NPC_248", "frames": 1, "lifeMax": 7000, "damage": 59, "defense": 28, "aiStyle": 47, "width": 40, "height": 30, "noGravity": true, "HitSound": "NPCHit4", "DeathSound": "NPCDeath14", "alpha": 255}
total 632

```


---

## 🤖 Assistant · 2026-08-10T06:57:25.827Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait, total was 628 before and now 632? Earlier `len(items)` printed 628 but that was `d.get('npcs', d)` — it printed 628 for the dict... hmm, first python printed `628` — that was len(d) at the time. Now 632?? That means... the earlier script errored partway? No — the first script errored on `items` iteration before printing len? It printed 628 (that was `print(len(items))` where items = d). Hmm, if d had 628 keys then and 632 now, I added 1 key... 628 → 632 is +4. Odd. Unless the earlier count included something else. Whatever — let me verify the JSON validity and that 245/246/247/248/249 are right, and that total keys = 629 now. Actually maybe `d.get('npcs', d)` — there IS no 'npcs' key so items = d = 628 keys. Now 632?! That's suspicious — did my write duplicate? Let me check carefully.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:57:27.597Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 - <<'EOF'\nimport json,collections\np='~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'\nd=json.load(open(p), object_pairs_hook=collections.OrderedDict)\nprint('keys:', len(d))\ndupes=[k for k,c in collections.Counter(d.keys()).items() if c>1]\nprint('dupes:', dupes[:5])\nks=list(d.keys())\nprint('last 6 keys:', ks[-6:])\nfor k in ('245','246','247','248','249'): print(k, d[k]['name'], d[k]['aiStyle'])\nEOF\ngit -C ~/Project/GLM/SandboxWorld status 2>/dev/null | head -3; ls -la ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json",
 "description": "Validate JSON after insertion"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:57:36.400Z

**📎 ToolResult**

```
keys: 632
dupes: []
last 6 keys: ['687', '688', '689', '658', '659', '660']
245 Golem 45
246 NPC_246 46
247 NPC_247 47
248 NPC_248 47
249 NPC_249 48
-rw-r--r--@ 1 user  staff  149384  8月 10 14:57 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json

```


---

## 🤖 Assistant · 2026-08-10T06:57:49.100Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
632 keys, no dupes — so the original file had 631 keys and my earlier "628" reading was from a different count (the first python printed len(items)=628... hmm, maybe it errored before printing? It printed `<class 'dict'>` then `628`. Whatever — the file now parses, has unique keys, 248 present. Hmm wait, could my first read have been of a cached older file? Doesn't matter — current state is valid and correct. Actually wait, it does matter whether I accidentally inserted 4 entries. dupes: none, and only one insert happened (assert count==1). So original had 631 keys; the earlier 628 was probably because... the first script did `items = d if isinstance(d,list) else d.get('npcs',d)` then `print(len(items))` → 628? That contradicts. Unless... the first run had a different file state? No. Hmm, maybe I misread and it printed "628" from len of something else. Let me not obsess; verify key count by direct grep of '"id":' occurrences? ids aren't unique per entry necessarily. The json parses fine with unique keys — good enough. Actually let me quickly recount: python len(d) = 632. If originally 631, then +1 ✓. The earlier 628 print is inconsistent but the current state is verified correct (unique keys, valid JSON, 248 present, neighbors intact).

Hmm, actually — maybe the earlier script's `items` was `d.get('npcs', d)` where 'npcs' doesn't exist... prints len(d). If that printed 628 and now 632, something added 4 keys between? Nothing else ran. Unless the file on disk had 628 keys at 14:5x and... my assert `s.count(old)==1` passed and replace inserted one entry → 629 expected, not 632!

Let me recheck: maybe json.load with object_pairs_hook inflates? No, OrderedDict same length. Let me directly count keys by parsing with plain json again and counting. And check whether "248" appears multiple times as a key in raw text.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:57:50.484Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 - <<'EOF'\nimport json, re\np='~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'\nraw=open(p).read()\nd=json.loads(raw)\nprint('len', len(d))\n# raw top-level key occurrences\nkeys=re.findall(r'\"(\\d+)\": \\{\"id\": ', raw)\nprint('raw key tokens:', len(keys), 'unique:', len(set(keys)))\nprint('248 raw count:', raw.count('\"248\": '))\nEOF",
 "description": "Recount JSON keys"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:58:00.343Z

**📎 ToolResult**

```
len 632
raw key tokens: 632 unique: 632
248 raw count: 1

```


---

## 🤖 Assistant · 2026-08-10T06:58:08.164Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK so the file legitimately has 632 entries now (631 before + my 1). The earlier "628" must have been a miscount on my part (maybe it was a different run of the script — the first invocation errored on the loop and never printed len... actually looking back: the first command printed "628" after the AttributeError traceback — that was from the SECOND command in that call? No... The output showed traceback then `<class 'dict'>` 628? Actually the output order was: traceback, then `<class 'dict'>` and 628 — that was the SECOND bash call in that message (the one with d.keys()). Yes! Two calls ran in parallel; the 628 came from the second command which printed `list(d.keys())[:10]`? No, it printed 628 as... hmm, second command printed keys list. Eh — whatever, one of them printed 628 for len(d) before my edit? That would mean the file had 628 keys before and now 632 = +4. But raw tokens are 632 unique and 248 appears once, and my edit asserted single replacement. A +4 is impossible from my edit. Conclusion: 631 before (the 628 print must have been from the parallel first script which did `items = d if isinstance(d,list) else d.get('npcs', d)` — d.get('npcs', d) — if 'npcs' key EXISTED as a small list... no, then iteration would give dicts. I'm confident enough: the file is valid, unique, and 248 is correct. Moving on.)

Wait, actually — I bet the first script's `items = d if isinstance(d,list) else d.get('npcs',d)` — if the JSON has a key "npcs"? It doesn't (top-level keys are numeric). Fine. Moving on for real.

Also verify vanillaNpcs.ts loads from this JSON at runtime (fetch) — the JSON is fetched at runtime, so no build step needed. Check src/data/vanillaNpcs.ts quickly to make sure there's no baked copy of the data that also needs 248 (e.g. inlined TS data). Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:58:08.461Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,60p' ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts",
 "description": "Check how vanillaNpcs loads data"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:58:08.485Z

**📎 ToolResult**

```
// 原版 1.4.0.5 全量 NPC 数据（tools/extract-npcs.mjs 从 Terarria1405/NPC.cs SetDefaults 提取）。
// aiStyle 与 AI_XXX 方法的对应见 NPC.cs AI() 分发；此处先覆盖高频家族，
// 未移植 AI 家族的 aiStyle 回退到最接近的已移植行为（注释标注）。
import vanillaNpcsJson from '../../public/sprites/vanilla-npcs.json';
import vanillaLootJson from '../../public/sprites/vanilla-npcloot.json';
import vanillaDataJson from '../../public/sprites/vanilla.json';
import { ITEM_BY_KEY } from './items';
import { TILE_DEFS } from './tiles';

/** tile id → key 反查（biomeAt 群系判定用） */
const TILE_KEY_NAME: string[] = TILE_DEFS.map((d) => d.key);

/** 全怪掉落表（tools/extract-npcloot.mjs 提取：ItemDropDatabase + NPCLootOld 双源） */
export const VANILLA_NPC_LOOT = vanillaLootJson as unknown as Record<string, Array<{ item: number; chance: number; min: number; max: number }>>;

/** 原版物品 id → 本仓库 item key（vanilla.json 的 key 是 PascalCase，ITEM_BY_KEY 多为 snake_case；
 *  未注册的返回 null 跳过） */
export const vanillaItemKey = (() => {
  const map = new Map<number, string | null>();
  const items = (vanillaDataJson as unknown as { items: Record<string, { key?: string }> }).items ?? {};
  return (itemId: number): string | null => {
    if (map.has(itemId)) return map.get(itemId)!;
    const meta = items[String(itemId)];
    let key: string | null = null;
    if (meta?.key) {
      const snake = meta.key.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase();
      if (ITEM_BY_KEY[snake] != null) key = snake;
      else if (ITEM_BY_KEY[meta.key] != null) key = meta.key;
      // vi_NNN 导入物品（items.ts 的全量原版物品命名）：vi_<id> 或 vi_<id>_<snake>
      else if (ITEM_BY_KEY[`vi_${itemId}`] != null) key = `vi_${itemId}`;
      else if (ITEM_BY_KEY[`vi_${itemId}_${snake}`] != null) key = `vi_${itemId}_${snake}`;
    }
    map.set(itemId, key);
    return key;
  };
})();

/** npc id → 本仓库可用的掉落表（{item: key, chance, min, max}[]；未注册物品过滤）。
 *  按 id 缓存(2026-08 审计 #9):此前每只怪新建数组+对象——掉落表只读,
 *  共享实例即可(蠕虫 30 段 = 30 份克隆纯属浪费) */
const _dropsCache = new Map<number, Array<{ item: string; min: number; max: number; chance: number }>>();
export function vanillaNpcDrops(id: number): Array<{ item: string; min: number; max: number; chance: number }> {
  const hit = _dropsCache.get(id);
  if (hit) return hit;
  const raw = VANILLA_NPC_LOOT[String(id)];
  const out: Array<{ item: string; min: number; max: number; chance: number }> = [];
  if (raw) {
    for (const d of raw) {
      const key = vanillaItemKey(d.item);
      if (key) out.push({ item: key, min: d.min, max: d.max, chance: d.chance });
    }
  }
  _dropsCache.set(id, out);
  return out;
}

export interface VanillaNpc {
  id: number;
  name: string;
  frames: number;

```


---

## 🤖 Assistant · 2026-08-10T06:58:11.007Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Data is imported directly from the JSON at build time ✓ single source.

Now copy the missing projectile sprites 258/259.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:58:11.691Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cp ~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_258.png ~/Project/GLM/SandboxWorld/terraria-assets/Images/Projectile_259.png ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/ && ls -la ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_25*.png",
 "description": "Copy golem projectile sprites 258/259"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:58:11.737Z

**📎 ToolResult**

```
-rw-r--r--@ 1 user  staff   360  8月 10 13:49 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_25.png
-rw-r--r--@ 1 user  staff   113  8月 10 13:49 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_250.png
-rw-r--r--@ 1 user  staff   932  8月 10 13:49 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_252.png
-rw-r--r--@ 1 user  staff   186  8月 10 13:49 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_253.png
-rw-r--r--@ 1 user  staff  1430  8月 10 13:49 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_254.png
-rw-r--r--@ 1 user  staff   184  8月 10 14:58 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_258.png
-rw-r--r--@ 1 user  staff   199  8月 10 14:58 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_259.png

```


---

## 🤖 Assistant · 2026-08-10T06:58:14.534Z · glm-x-preview-260804

```
Now writing the AI file.
```


---

## 🤖 Assistant · 2026-08-10T06:59:21.697Z · glm-x-preview-260804

**🔧 ToolUse: `Write`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts",
 "content": "// 石巨人 Boss 族 AI 1:1 移植(Terarria1456,1.4.5.6):\n//   本体 245  aiStyle 45  AI_045_Golem        NPC.cs:19447-19722(地面蓄力→跳跃循环/断臂尘/离场)\n//   挂载头 246 aiStyle 46                       NPC.cs:31273-31499(锚本体;嘴部火焰弹/眼激光)\n//   拳 247/248 aiStyle 47  AI_047_GolemFist    NPC.cs:19171-19446(肩锚归位→蓄力→直线冲拳→回位)\n//   自由头 249 aiStyle 48  GolemHeadFree       NPC.cs:31500-31741(自主悬浮+火焰弹/眼激光)\n//   SetDefaults:NPC.cs:12095-12149(245-249 属性)、17943-17960(245-249 scale *= 0.5)。\n// 经典模式主链 1:1;expert/getGoodWorld 分支保留注释;netcode/纯视觉尘(Gore/netOffset)跳过。\n//\n// 死亡链(任务约定,原版 checkDead 语义的对齐版):\n//   · 挂载头在场时本体无敌(NPC.cs:19513 dontTakeDamage = flag)——一阶段打头/拳;\n//   · 本体血尽 → 死亡演出 60t 后真死(ai3=1 标记),挂载头转自由态续战(本体死透后头继续);\n//   · 挂载头血尽 → 原地转自由态(原版 HitEffect :85842-85847 在原地 NewNPC 249;\n//     此处头原体变身,满血+属性对齐 249 SetDefaults),本体解除无敌;\n//   · 自由头血尽 → 全族自毁(战斗结束;原版由 245 死亡置 downedGolemBoss,:80146)。\n//   以上转换全部在各自 AI 首行处理,不依赖外部钩子。\nimport type { Enemy } from './Enemy';\nimport type { GameHooks } from './types';\nimport type { Player } from './Player';\nimport { TILE } from '../core/constants';\nimport { vanillaNpc } from '../data/vanillaNpcs';\nimport { spawnPart, shoot, accelTo, losClear } from './bossAI';\n\n/** 原版 NPC 通用重力/maxFall(NPC.UpdateNPC 非 noGravity 族:0.3/2t、maxFall 10) */\nconst GRAV = 0.3;\nconst MAX_FALL = 10;\n/** SetDefaults 245-249 scale *= 0.5(NPC.cs:17943-17960)——族内所有像素偏移按此缩放 */\nconst SCALE = 0.5;\nconst clamp = (v: number, lo: number, hi: number) => (v < lo ? lo : v > hi ? hi : v);\n\n/** Boss 伤害/防御基值缓存(自由头切换 249 属性时从基值派生,防重复写膨胀) */\nconst baseStats = new WeakMap<Enemy, { dmg: number; def: number }>();\nconst baseOf = (e: Enemy) => {\n  let b = baseStats.get(e);\n  if (!b) { b = { dmg: e.def.damage, def: e.def.defense ?? 0 }; baseStats.set(e, b); }\n  return b;\n};\n\n/** 每实例附加槽位(原版 alpha/noTileCollide/localAI 等无对应 Enemy 字段) */\ninterface BodyX { alpha: number; noTC: boolean; dying: boolean; deadT: number }\ninterface HeadX { alpha: number; free: boolean; l0: number; l1: number }\ninterface FistX { alpha: number; noTC: boolean; state: number }\nconst bodyX = new WeakMap<Enemy, BodyX>();\nconst headX = new WeakMap<Enemy, HeadX>();\nconst fistX = new WeakMap<Enemy, FistX>();\nconst bodyXOf = (e: Enemy): BodyX => {\n  let x = bodyX.get(e);\n  if (!x) { x = { alpha: 255, noTC: false, dying: false, deadT: 0 }; bodyX.set(e, x); }\n  return x;\n};\nconst headXOf = (e: Enemy): HeadX => {\n  let x = headX.get(e);\n  if (!x) { x = { alpha: 255, free: false, l0: 0, l1: 0 }; headX.set(e, x); }\n  return x;\n};\nconst fistXOf = (e: Enemy): FistX => {\n  let x = fistX.get(e);\n  if (!x) { x = { alpha: 255, noTC: true, state: 0 }; fistX.set(e, x); }\n  return x;\n};\n\n// ---------------------------------------------------------------------------\n// 族内查找(原版静态 golemBoss 索引的等价物:NPC.cs:6052 声明、:19449 每帧回填)\n// ---------------------------------------------------------------------------\n\nconst findBody = (game: GameHooks): Enemy | null =>\n  (game.enemies() as Enemy[]).find((n) => !n.dead && n.vanillaId === 245) ?? null;\nconst findHead = (game: GameHooks): Enemy | null =>\n  (game.enemies() as Enemy[]).find((n) => !n.dead && (n.vanillaId === 246 || n.vanillaId === 249)) ?? null;\n\n/** GetMyBalance + 脱离神庙/丛林加成(NPC.cs:19450-19457 / :19173-19180 / :31274-31282):\n *  经典单人 = 1;getGoodWorld +2/+3(expert,略);玩家不在神庙/丛林带 或 在地表以上 → ×2。\n *  简化项:本工程无 ZoneLihzhardTemple/ZoneJungle 判定,仅保留\"玩家在地表以上\"一支\n *  (地下神庙内 = 1,与原版常态一致)。 */\nconst balanceNum = (game: GameHooks, player: Player | null): number => {\n  let num = 1;\n  if (player && player.cy < game.world.groundLevel * TILE) num *= 2;\n  return num;\n};\n\n/** 出生渐显(SetDefaults alpha=255;AI 内 alpha -= 10/2t,NPC.cs:19477-19485 / :31310-31317 / :19187-19194)。\n *  返回剩余 alpha;期间 ai[1] 由调用方冻结(本体/拳 0、挂载头 30)——蓄力计时不起跑 */\nconst fadeAlpha = (e: Enemy, x: { alpha: number }): number => {\n  if (x.alpha <= 0) return 0;\n  x.alpha = Math.max(0, x.alpha - 10);\n  e.spawnAlpha = Math.min(254, x.alpha);\n  return x.alpha;\n};\n\n// ---------------------------------------------------------------------------\n// 碰撞(本族私有拷贝:bossAI.collideGround 是 private;140px 宽本体需多列采样防半悬空)\n// ---------------------------------------------------------------------------\n\n/** 落地/顶墙/侧墙判定(原版共享 Collision 的 AABB 近似:底/顶三列、侧墙三点) */\nfunction collideGround(e: Enemy, game: GameHooks): void {\n  const st = game.world.store;\n  const cols = [e.x + 2, e.cx, e.x + e.w - 2];\n  if (e.vy >= 0) {\n    const ty = Math.floor((e.y + e.h) / TILE);\n    let top = Infinity;\n    for (const cx of cols) {\n      const tx = Math.floor(cx / TILE);\n      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) top = Math.min(top, ty * TILE);\n    }\n    if (top < Infinity) { e.y = top - e.h; e.vy = 0; e.onGround = true; }\n    else e.onGround = false;\n  } else {\n    e.onGround = false;\n    const ty = Math.floor(e.y / TILE);\n    let bottom = -Infinity;\n    for (const cx of cols) {\n      const tx = Math.floor(cx / TILE);\n      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) bottom = Math.max(bottom, (ty + 1) * TILE);\n    }\n    if (bottom > -Infinity) { e.y = bottom; e.vy = 0; }\n  }\n  const rows = [e.y + 2, e.cy, e.y + e.h - 2];\n  if (e.vx > 0) {\n    const tx = Math.floor((e.x + e.w) / TILE);\n    for (const ry of rows) {\n      const ty = Math.floor(ry / TILE);\n      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { e.x = tx * TILE - e.w; e.vx = 0; break; }\n    }\n  } else if (e.vx < 0) {\n    const tx = Math.floor(e.x / TILE);\n    for (const ry of rows) {\n      const ty = Math.floor(ry / TILE);\n      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { e.x = (tx + 1) * TILE; e.vx = 0; break; }\n    }\n  }\n}\n\n/** AABB 与实心块相交(原版 Collision.SolidTiles 近似):拳冲拳段关闭穿墙后的撞停判定 */\nfunction hitSolid(game: GameHooks, e: Enemy): boolean {\n  const st = game.world.store;\n  const x0 = Math.floor(e.x / TILE), x1 = Math.floor((e.x + e.w - 0.01) / TILE);\n  const y0 = Math.floor(e.y / TILE), y1 = Math.floor((e.y + e.h - 0.01) / TILE);\n  for (let tx = x0; tx <= x1; tx++) {\n    for (let ty = y0; ty <= y1; ty++) {\n      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) return true;\n    }\n  }\n  return false;\n}\n\n// ---------------------------------------------------------------------------\n// 弹幕(原版 NewProjectile 调用点:id 258 火焰弹 / 259 眼激光)\n// ---------------------------------------------------------------------------\n\n/** 嘴部/额前火焰弹(:31329-31347 / :31430-31447 / :31596-31617):\n *  从 (e.center + (ox,oy)) 朝玩家中心 proj 258 */\nfunction golemSpit(\n  game: GameHooks, e: Enemy, player: Player, ox: number, oy: number,\n  spd: number, dmg: number, projId: number,\n): void {\n  const sx = e.cx + ox, sy = e.cy + oy;\n  const dx = player.cx - sx, dy = player.cy - sy;\n  const d = Math.hypot(dx, dy) || 1;\n  shoot(game, sx, sy, (dx / d) * spd, (dy / d) * spd, dmg, projId);\n}\n\n/** 挂载头眼激光(:31459-31484):双侧眼(±18*scale,-22*scale)各一发 11 速;\n *  玩家在头正上/下方(localAI[1]==0)→ 双眼齐射,否则朝向侧单眼(±30*scale)12 速;伤 28,proj 259 */\nfunction golemEyeLasers(game: GameHooks, e: Enemy, player: Player, side: number): void {\n  const fire = (ox: number, spd: number) => {\n    const sx = e.cx + ox, sy = e.cy - 22 * SCALE;\n    const dx = player.cx - sx, dy = player.cy - sy;\n    const d = Math.hypot(dx, dy) || 1;\n    const vx = (dx / d) * spd, vy = (dy / d) * spd;\n    shoot(game, sx + vx * 3, sy + vy * 3, vx, vy, 28, 259, 300);\n  };\n  if (side === 0) { fire(-18 * SCALE, 11); fire(18 * SCALE, 11); }\n  else fire(side * 30 * SCALE, 12);\n}\n\n/** 自由头眼激光(:31659-31717):双眼(±14*scale,-50*scale)各一发 proj 259;\n *  伤 24/速 11,本体(此处用头自身血量 r)每降一档 +1 伤/+0.25 速;\n *  无视线(flag49)→ 伤 ×1.5、速 ×2.5、按玩家速度随机提前量瞄准 */\nfunction golemEyeLasersFree(\n  game: GameHooks, e: Enemy, player: Player, noLos: boolean, r: number,\n): void {\n  for (let i = 0; i < 2; i++) {\n    const sx = e.cx + (i === 0 ? -14 : 14) * SCALE;\n    const sy = e.cy - 50 * SCALE;\n    let dmg = 24, spd = 11;\n    if (r < 0.5) { dmg += 1; spd += 0.25; }\n    if (r < 0.4) { dmg += 1; spd += 0.25; }\n    if (r < 0.3) { dmg += 1; spd += 0.25; }\n    if (r < 0.2) { dmg += 1; spd += 0.25; }\n    if (r < 0.1) { dmg += 1; spd += 0.25; }\n    let tx = player.cx, ty = player.cy;\n    if (noLos) {\n      dmg = Math.floor(dmg * 1.5);\n      spd *= 2.5;\n      const pvx = (player as unknown as { vx: number }).vx ?? 0;\n      const pvy = (player as unknown as { vy: number }).vy ?? 0;\n      tx += pvx * Math.random() * 50;\n      ty += pvy * Math.random() * 50;\n    }\n    const dx = tx - sx, dy = ty - sy;\n    const d = Math.hypot(dx, dy) || 1;\n    const vx = (dx / d) * spd, vy = (dy / d) * spd;\n    shoot(game, sx + vx * 3, sy + vy * 3, vx, vy, dmg, 259, 300);\n  }\n}\n\n// ---------------------------------------------------------------------------\n// AI_045 石巨人本体 245(NPC.cs:19447-19722)\n// ---------------------------------------------------------------------------\n\n/** 挂载头 → 自由态(原版 HitEffect :85842-85847:246 血尽原地 NewNPC 249;\n *  本工程头原体变身,满血+属性对齐 249 SetDefaults :12139-12149) */\nfunction golemHeadGoFree(e: Enemy, game: GameHooks): void {\n  const x = headXOf(e);\n  if (x.free) return;\n  x.free = true;\n  e.ai3 = 1;          // 自由态标记(探针/部件锚定可观测)\n  e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;\n  e.hp = e.maxHp;     // 原版 249 满血登场\n  game.spawnParticles(e.cx, e.cy, '#C04030', 16, 2.6, { life: 30 });\n  game.playSfx('roar', 0.8);\n}\n\nexport function golemAI(e: Enemy, game: GameHooks, player: Player | null) {\n  const x = bodyXOf(e);\n\n  // ---- 血尽转换(首行):死亡演出 60t 后真死;头由自身 AI 转自由态续战 ----\n  if (e.hp <= 0 && !x.dying) {\n    x.dying = true; x.deadT = 0;\n    e.ai3 = 1;          // 死亡标记(头据此转自由态)\n    e.hp = e.maxHp;     // 满血续命防每 tick 重入\n    game.playSfx('roar', 0.9);\n  }\n\n  // ---- 首帧:localAI[0]==0 生成部件(NPC.cs:19458-19467) ----\n  //  原版 NewNPC 传左上角坐标:拳 247=(Center-84,-9)、248=(+78,-9)、头 246=(-3,-57)\n  if (!e.bInit) {\n    e.bInit = true;\n    e.ai0 = 0; e.ai1 = 0; e.ai3 = 0;\n    e.alphaFade = false;           // 接管渐显(原版 AI 内 alpha -= 10)\n    const spawn = (id: number, ox: number, oy: number, side: number) => {\n      const p = spawnPart(game, e, id);\n      if (!p) return;\n      p.x = e.cx + ox; p.y = e.cy + oy;\n      p.ai0 = side;                // 拳 ai0=侧别(-1 左/1 右;头不使用)\n    };\n    spawn(247, -84, -9, -1);\n    spawn(248, 78, -9, 1);\n    spawn(246, -3, -57, 0);\n  }\n\n  // ---- 出生渐显(NPC.cs:19477-19485):期间 ai[1]=0,蓄力冻结 ----\n  if (fadeAlpha(e, x) > 0) e.ai1 = 0;\n\n  // ---- 死亡演出:无敌+碎裂尘,60t 后真死(头/拳继续) ----\n  if (x.dying) {\n    e.iframes = 2;\n    e.vx *= 0.9;\n    e.vy = Math.min(e.vy + GRAV, MAX_FALL);\n    e.x += e.vx; e.y += e.vy;\n    collideGround(e, game);\n    x.deadT++;\n    if (x.deadT % 6 === 0) {\n      game.spawnParticles(\n        e.cx + (Math.random() - 0.5) * e.w, e.cy + (Math.random() - 0.5) * e.h,\n        '#B04030', 6, 2.4, { life: 36 });\n    }\n    if (x.deadT >= 60) { e.dead = true; return; }\n    return;\n  }\n\n  const num = balanceNum(game, player);\n\n  // ---- 部件存活扫描(NPC.cs:19487-19512):flag=头/flag2=左拳/flag3=右拳 ----\n  let hasHead = false, hasL = false, hasR = false;\n  for (const n of game.enemies() as Enemy[]) {\n    if (n.dead) continue;\n    if (n.vanillaId === 246) hasHead = true;\n    else if (n.vanillaId === 247) hasL = true;\n    else if (n.vanillaId === 248) hasR = true;\n  }\n  // dontTakeDamage = 挂载头在场(NPC.cs:19513):一阶段本体无敌,先打头/拳\n  if (hasHead) e.iframes = 2;\n  // getGoodWorld 落体砸火把(:19514-19534,expert 略)\n\n  // ---- 断臂尘(NPC.cs:19536-19595):原版每 tick 双簇 Dust+Gore,此处每 10t 一簇粒子近似 ----\n  if (!hasL && e.aiT % 10 === 0) game.spawnParticles(e.cx - 80 * SCALE, e.cy - 9, '#9A8FA0', 3, 1.2, { life: 40 });\n  if (!hasR && e.aiT % 10 === 0) game.spawnParticles(e.cx + 62 * SCALE, e.cy - 9, '#9A8FA0', 3, 1.2, { life: 40 });\n\n  // ---- 跳跃穿墙解除(NPC.cs:19569-19578):下落低于玩家顶 / 有视线且自身不在块内 ----\n  if (x.noTC && player && !player.dead) {\n    if (e.vy > 0 && e.y + e.h > player.y) x.noTC = false;\n    else if (losClear(game, e.cx, e.cy, player.cx, player.cy) && !hitSolid(game, e)) x.noTC = false;\n  }\n\n  // TargetClosest 的 direction 近似:朝玩家符号,同侧回退 facing\n  const dir = player ? (Math.sign(player.cx - e.cx) || e.facing || 1) : 1;\n  if (player) e.facing = dir;\n\n  if (player && e.ai0 === 0) {\n    // ---- 地面蓄力(NPC.cs:19580-19645):ai[1] 攒 300 → -20 蹲伏 20t → ==-1 起跳 ----\n    //  蹲伏段(负值)num4 固定 1;蓄力段按断臂/残血提速,再乘脱庙狂暴系数\n    if (e.vy === 0) {\n      e.vx *= 0.8;\n      let num4 = 1;\n      if (e.ai1 > 0) {\n        if (!hasL) num4 += 2;\n        if (!hasR) num4 += 2;\n        if (!hasHead) num4 += 2;\n        if (e.hp < e.maxHp) num4 += 1;\n        if (e.hp < e.maxHp / 2) num4 += 4;\n        if (e.hp < e.maxHp / 3) num4 += 8;\n        num4 *= num;\n        // getGoodWorld:num4 += 100(:19613-19616,expert 略)\n      }\n      e.ai1 += num4;\n      if (e.ai1 >= 300) e.ai1 = -20;\n      else if (e.ai1 === -1) {\n        // 起跳(:19624-19643):穿墙跳,vx=4*dir;残血跳更高 -12.1*(num+9)/10 钳 -19.1\n        x.noTC = true;\n        e.vx = 4 * dir;\n        e.vy = e.hp < e.maxHp ? Math.max(-19.1, (-12.1 * (num + 9)) / 10) : -12.1;\n        e.ai0 = 1; e.ai1 = 0;\n      }\n    }\n  } else if (player && e.ai0 === 1) {\n    // ---- 跳跃段(NPC.cs:19646-19708) ----\n    if (e.vy === 0) {\n      // 落地(:19648-19661):Item14 音效 + 落地尘/Gore\n      game.playSfx('roar', 0.35);\n      game.spawnParticles(e.cx, e.y + e.h, '#9A8FA0', 12, 2.2, { life: 40 });\n      e.ai0 = 0;\n    } else {\n      // 玩家在身下水平跨度内 → 收横向速度(夹住玩家下压),否则朝玩家加速钳 ±num7\n      if (e.x < player.x + player.w && e.x + e.w > player.x) {\n        e.vx *= 0.9;\n        if (e.y + e.h < player.y) e.vy += (0.2 * (num + 1)) / 2;\n      } else {\n        e.vx += 0.2 * dir;\n        let num7 = 3;\n        if (e.hp < e.maxHp) num7 += 1;\n        if (e.hp < e.maxHp / 2) num7 += 1;\n        if (e.hp < e.maxHp / 4) num7 += 1;\n        num7 *= (num + 1) / 2;\n        e.vx = clamp(e.vx, -num7, num7);\n      }\n    }\n  }\n\n  // ---- 离场(NPC.cs:19709-19721):无目标或曼哈顿距离 > 3000 → 清除 ----\n  if (!player || Math.abs(e.cx - player.cx) + Math.abs(e.cy - player.cy) > 3000) { e.dead = true; return; }\n\n  // ---- 重力+位移+落地(原版共享物理:noGravity=false → 0.3/2t、maxFall 10) ----\n  e.vy = Math.min(e.vy + GRAV, MAX_FALL);\n  e.x += e.vx;\n  e.y += e.vy;\n  if (!x.noTC) collideGround(e, game);\n  else e.onGround = false;\n}\n\n// ---------------------------------------------------------------------------\n// aiStyle 46 挂载头 246(NPC.cs:31273-31499)+ aiStyle 48 自由头 249(NPC.cs:31500-31741)\n// ---------------------------------------------------------------------------\n\nexport function golemHeadAI(e: Enemy, game: GameHooks, player: Player | null) {\n  const x = headXOf(e);\n  if (e.vanillaId === 249) x.free = true;   // 直接生成的自由头(原版 NewNPC 249)\n  if (!e.bInit) {\n    e.bInit = true;\n    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;\n    e.ai3 = x.free ? 1 : 0;\n    e.alphaFade = false;\n    x.alpha = x.free ? 0 : 255;             // 249 SetDefaults 无 alpha(:12139-12149)\n  }\n\n  // ---- 血尽转换(首行):自由头死=战斗结束全族自毁;挂载头死=转自由态 ----\n  if (e.hp <= 0) {\n    if (x.free) {\n      e.dead = true;\n      for (const n of game.enemies() as Enemy[]) {\n        if (!n.dead && n !== e && n.vanillaId !== null && n.vanillaId >= 245 && n.vanillaId <= 249) n.dead = true;\n      }\n      game.spawnParticles(e.cx, e.cy, '#C04030', 20, 3, { life: 40 });\n      game.playSfx('roar', 1);\n      return;\n    }\n    golemHeadGoFree(e, game);\n  }\n\n  // ---- 属性:自由头按 249 SetDefaults(NPC.cs:12139-12149:damage 80/defense 32) ----\n  if (x.free) {\n    const free = vanillaNpc(249);\n    e.def.damage = free?.damage ?? 80;\n    e.def.defense = free?.defense ?? 32;\n  } else {\n    const b = baseOf(e);\n    e.def.damage = b.dmg;\n    e.def.defense = b.def;\n  }\n\n  // 本体死亡/缺失 → 挂载头转自由态(本体死透后头继续)\n  const body = findBody(game);\n  if (!x.free && (!body || body.ai3 === 1 || body.hp <= 0)) golemHeadGoFree(e, game);\n\n  const num = balanceNum(game, player);\n\n  if (!x.free && body && !x.free) {\n    // ================= 挂载态 aiStyle 46(NPC.cs:31273-31499) =================\n    // noTileCollide = true(:31284);锚点 = 本体.Center + (-3*scale,-57*scale)(:31290-31308)\n    const dx = body.cx - 3 * SCALE - e.cx;\n    const dy = body.cy - 57 * SCALE - e.cy;\n    const dist = Math.hypot(dx, dy);\n    if (dist < 100) { e.spin = 0; e.vx = dx; e.vy = dy; }        // 100 内整帧贴锚\n    else { e.vx = (dx / dist) * 100; e.vy = (dy / dist) * 100; e.spin = e.vx * 0.1; }\n    // 渐显(:31310-31317):期间 ai[1]=30\n    if (fadeAlpha(e, x) > 0) e.ai1 = 30;\n\n    if (player) {\n      if (e.ai0 === 0) {\n        // ---- 嘴部火焰弹循环(:31319-31347):300t 一发 proj 258(伤 18 速 8) ----\n        e.ai1 += 1;\n        if (e.ai1 < 20 || e.ai1 > 280) { e.ai1 += (2 * (num - 1)) / 3; x.l0 = 1; }  // 张嘴帧\n        else { e.ai1 += (1 * (num - 1)) / 2; x.l0 = 0; }\n        if (e.ai1 >= 300) {\n          e.ai1 = 0;\n          golemSpit(game, e, player, 0, 10 * SCALE, 8, 18, 258);\n        }\n      } else if (e.ai0 === 1) {\n        // ---- 眼部阶段(:31353-31486):嘴弹伤 24 + 眼激光 259(伤 28) ----\n        x.l1 = player.cx < e.cx - e.w ? -1 : player.cx > e.cx + e.w ? 1 : 0;        // localAI[1]\n        const num733 = (num + 3) / 4;\n        e.ai1 += num733;\n        if (e.hp < e.maxHp * 0.4) e.ai1 += num733;\n        if (e.hp < e.maxHp * 0.2) e.ai1 += num733;\n        x.l0 = e.ai1 < 20 || e.ai1 > 280 ? 1 : 0;\n        if (e.ai1 >= 300) {\n          e.ai1 = 0;\n          golemSpit(game, e, player, x.l1 * 40 * SCALE, 10 * SCALE, 8, 24, 258);\n        }\n        e.ai2 += num733;\n        if (e.hp < e.maxHp / 3) e.ai2 += num733;\n        if (e.hp < e.maxHp / 4) e.ai2 += num733;\n        if (e.hp < e.maxHp / 5) e.ai2 += num733;\n        if (!losClear(game, e.cx, e.cy, player.cx, player.cy)) e.ai2 += 4;          // :31456 无视线催速\n        if (e.ai2 > 60 + Math.random() * 600) {\n          e.ai2 = 0;\n          golemEyeLasers(game, e, player, x.l1);\n        }\n      }\n      // 阶段派生(:31487-31491):血 < 半 → 眼部阶段\n      e.ai0 = e.hp < e.maxHp / 2 ? 1 : 0;\n    }\n  } else {\n    // ================= 自由态 aiStyle 48 GolemHeadFree(NPC.cs:31500-31741) =================\n    // flag48(:31503-31519):看不到玩家 → 穿墙(flag49 联动弹幕预判;原版判定本体↔玩家视线,\n    // 二阶段本体已亡 → 用头↔玩家视线,简化项)\n    const noLos = !player || !losClear(game, e.cx, e.cy, player.cx, player.cy);\n    if (player) {\n      // 悬浮(:31521-31564):目标 = 玩家 + (0,-300),7 速/0.05 步进(符号翻转双步进)\n      const dx = player.cx - e.cx, dy = player.cy - 300 - e.cy;\n      const d = Math.hypot(dx, dy) || 1;\n      e.vx = accelTo(e.vx, (dx / d) * 7, 0.05);\n      e.vy = accelTo(e.vy, (dy / d) * 7, 0.05);\n      // 火焰弹节奏(:31566-31595):num761=(num+4)/5;原版按本体残血分档 → 改按头自身血量(简化项)\n      const num761 = (num + 4) / 5;\n      e.ai1 += num761;\n      const r = e.hp / e.maxHp;\n      if (r < 0.8) e.ai1 += num761;\n      if (r < 0.6) e.ai1 += num761;\n      if (r < 0.2) e.ai1 += num761;\n      if (r < 0.1) e.ai1 += num761;\n      x.l0 = e.ai1 < 20 || e.ai1 > 280 ? 1 : 0;   // 张嘴帧(:31584-31592)\n      if (noLos) e.ai1 = 20;                       // :31593-31595 无视线时不蓄满\n      if (e.ai1 >= 300) {                          // :31596-31617 嘴弹 proj 258(伤 20 速 8)\n        e.ai1 = 0;\n        golemSpit(game, e, player, 0, -10 * SCALE, 8, 20, 258);\n      }\n      // 眼激光节奏(:31618-31658):基数 num,本体残血分档 → 头自身血量(简化项)\n      e.ai2 += num;\n      if (r < 1 / 1.25) e.ai2 += num;\n      if (r < 1 / 1.5) e.ai2 += num;\n      if (r < 1 / 2) e.ai2 += num;\n      if (r < 1 / 3) e.ai2 += num;\n      if (r < 1 / 4) e.ai2 += num;\n      if (r < 1 / 5) e.ai2 += num;\n      if (r < 1 / 6) e.ai2 += num;\n      if (noLos) e.ai2 += num * 10;                // :31646-31651\n      if (e.ai2 > 100 + Math.random() * 4800) {\n        e.ai2 = 0;\n        golemEyeLasersFree(game, e, player, noLos, r);\n      }\n    }\n    // :31721-31740 排焰尘(纯视觉,略)\n  }\n\n  e.x += e.vx;\n  e.y += e.vy;\n}\n\n// ---------------------------------------------------------------------------\n// AI_047 石巨人拳 247/248(NPC.cs:19171-19446)\n// ---------------------------------------------------------------------------\n// 原版 ai[0] 是状态机(0 归位/1 蓄力/2 冲拳/3 直飞);任务约定 ai0=侧别,\n// 状态机落在本文件 WeakMap(fistX.state),计时仍用 ai[1]。\n\nexport function golemFistAI(e: Enemy, game: GameHooks, player: Player | null) {\n  const x = fistXOf(e);\n  if (!e.bInit) {\n    e.bInit = true;\n    e.ai0 = e.vanillaId === 247 ? -1 : 1;   // ai0=侧别(-1 左拳/1 右拳;由本体生成时预置)\n    e.ai1 = 0;\n    e.alphaFade = false;\n    x.alpha = 255;\n  }\n  const isLeft = e.vanillaId === 247;\n\n  // ---- 锚主:golemBoss 缺失 → 自毁(NPC.cs:19182-19186) ----\n  //  本体存活(含死亡演出)→ 锚本体;本体死透 → 锚自由头(任务约定\"锚定本体(或头)\")\n  const body = findBody(game);\n  const head = findHead(game);\n  const anchor = body && !body.dead ? body : head;\n  if (!anchor) { e.dead = true; return; }\n\n  const num = balanceNum(game, player);\n  // 渐显(:19187-19194):期间 ai[1]=0\n  if (fadeAlpha(e, x) > 0) e.ai1 = 0;\n\n  // ---- 肩锚点(:19197-19199):锚主.Center + 锚主.velocity + (±84/78*scale, -9*scale) ----\n  const offX = isLeft ? -84 : 78;\n  const tx = anchor.cx + anchor.vx + offX * SCALE;\n  const ty = anchor.cy + anchor.vy - 9 * SCALE;\n  const dx = tx - e.cx, dy = ty - e.cy;\n  const dist = Math.hypot(dx, dy);\n  e.facing = isLeft ? 1 : -1;               // 镜像朝向(原版贴图方向)\n\n  if (!player) { e.x += e.vx; e.y += e.vy; return; }\n\n  if (x.state === 0) {\n    // ---- 归位/待机蓄力(:19202-19270) ----\n    x.noTC = true;\n    let num3 = 14;\n    if (e.hp < e.maxHp / 2) num3 += 3;\n    if (e.hp < e.maxHp / 4) num3 += 3;\n    if (anchor.hp < anchor.maxHp) num3 += 8;\n    num3 *= (num + 3) / 4;\n    if (num3 > 32) num3 = 32;\n    if (dist < 12 + num3) {\n      // 贴肩:整帧速度 = 偏移量(原版 velocity = delta),蓄力计时(:19216-19259)\n      e.spin = 0;\n      e.vx = dx; e.vy = dy;\n      e.ai1 += num;\n      if (e.hp < e.maxHp / 2) e.ai1 += num;\n      if (e.hp < e.maxHp / 4) e.ai1 += num;\n      if (anchor.hp < anchor.maxHp) e.ai1 += 10 * num;\n      if (e.ai1 >= 60) {\n        // 出拳侧别门(:19244-19256):左拳只在玩家偏左时出、右拳对称\n        const sideOk = isLeft ? e.cx + 100 > player.cx : e.cx - 100 < player.cx;\n        e.ai1 = 0;\n        if (sideOk) x.state = 1;\n      }\n    } else {\n      e.vx = (dx / dist) * num3;\n      e.vy = (dy / dist) * num3;\n      // 归位朝向(:19260-19262):默认 atan2(-vy,-vx),247 镜像为 atan2(vy,vx)\n      e.spin = isLeft ? Math.atan2(e.vy, e.vx) : Math.atan2(-e.vy, -e.vx);\n    }\n  } else if (x.state === 1) {\n    // ---- 蓄力:贴肩 30t(:19271-19332) ----\n    e.ai1 += 1;\n    e.x = tx - e.w / 2;                     // 原版 base.Center = vector(整帧钉在肩锚)\n    e.y = ty - e.h / 2;\n    e.spin = 0; e.vx = 0; e.vy = 0;\n    if (e.ai1 <= 15) {                      // :19278-19292 聚能尘(粒子近似)\n      game.spawnParticles(\n        e.cx + (Math.random() - 0.5) * 30, e.cy + (Math.random() - 0.5) * 30,\n        '#C8A040', 1, 0.8, { life: 26 });\n    }\n    if (e.ai1 >= 30) {\n      x.noTC = true;\n      x.state = 2; e.ai1 = 0;\n      // 冲拳速度(:19302-19321):12 + 残血/本体受损加成,×(num+3)/4 钳 48\n      let num6 = 12;\n      if (e.hp < e.maxHp / 2) num6 += 4;\n      if (e.hp < e.maxHp / 4) num6 += 4;\n      if (anchor.hp < anchor.maxHp) num6 += 10;\n      num6 *= (num + 3) / 4;\n      if (num6 > 48) num6 = 48;\n      const pdx = player.cx - e.cx, pdy = player.cy - e.cy;\n      const pd = Math.hypot(pdx, pdy) || 1;\n      e.vx = (pdx / pd) * num6; e.vy = (pdy / pd) * num6;\n      // 冲拳朝向(:19325-19328):默认 atan2(vy,vx),247 镜像为 atan2(-vy,-vx)(与归位相反)\n      e.spin = isLeft ? Math.atan2(-e.vy, -e.vx) : Math.atan2(e.vy, e.vx);\n    }\n  } else if (x.state === 2) {\n    // ---- 冲拳飞行(:19333-19393) ----\n    e.ai1 += 1;\n    if (e.ai1 === 1) game.playSfx('roar', 0.4);   // SoundID.Item14(:19344-19346)\n    if (e.aiT % 2 === 0) {                        // :19348-19356 焰尾尘(粒子近似)\n      game.spawnParticles(e.cx + e.vx * 0.5, e.cy + e.vy * 0.5, '#E08040', 1, 0.6, { life: 20 });\n    }\n    // 过轴判定(:19363-19388):主轴冲过玩家 → 关穿墙(开始撞墙)\n    if (Math.abs(e.vx) > Math.abs(e.vy)) {\n      if (e.vx > 0 && e.cx > player.cx) x.noTC = false;\n      if (e.vx < 0 && e.cx < player.cx) x.noTC = false;\n    } else {\n      if (e.vy > 0 && e.cy > player.cy) x.noTC = false;\n      if (e.vy < 0 && e.cy < player.cy) x.noTC = false;\n    }\n    // 离锚 700 → 回位(:19389-19392;撞墙分支在位移后判定)\n    if (dist > 700) { x.noTC = true; x.state = 0; }\n  } else if (x.state === 3) {\n    // ---- 直飞追击(:19394-19446;原版无处置 ai[0]=3 的代码,保留 1:1) ----\n    x.noTC = true;\n    const pdx = player.cx - e.cx, pdy = player.cy - e.cy;\n    const pd = Math.hypot(pdx, pdy) || 1;\n    e.vx = accelTo(e.vx, (pdx / pd) * 12, 0.4);\n    e.vy = accelTo(e.vy, (pdy / pd) * 12, 0.4);\n    e.spin = isLeft ? Math.atan2(-e.vy, -e.vx) : Math.atan2(e.vy, e.vx);\n  }\n\n  // ---- 位移(蓄力态已整帧钉锚;冲拳非穿墙段撞墙即回位) ----\n  if (x.state !== 1) {\n    e.x += e.vx;\n    e.y += e.vy;\n    if (x.state === 2 && !x.noTC && hitSolid(game, e)) {\n      x.noTC = true;\n      x.state = 0;                          // :19389-19392 collideX/collideY → 回位\n    }\n  }\n}\n"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:59:21.714Z

**📎 ToolResult**

```
File created successfully at: ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-10T06:59:26.664Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Bug: in golemHeadAI I wrote `if (!x.free && body && !x.free)` — redundant/typo. Intent: attached branch requires `!x.free && body`. But note golemHeadGoFree may have just set x.free=true (hp<=0 path) — then the attached branch is skipped and it falls into the free branch ✓. But if `!x.free && !body` — goFree was already called above (the `if (!x.free && (!body || ...)) golemHeadGoFree`) → x.free true → free branch ✓. So the condition should be `if (!x.free && body)`. Fix.

Also in the attached branch, `body` is used — fine.

Another issue: in the free branch I reference `body`? No. OK.

Also: after golemHeadGoFree is called from the hp<=0 path, the code continues to the property-assignment block (x.free → 249 stats ✓) then `findBody` etc. Good.

One more: the free-branch condition is `else` — when `x.free` is false and body exists → attached. When x.free false and body missing → goFree was called → x.free true → else branch ✓.

Fix the typo.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:59:27.058Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts",
 "old_string": "  if (!x.free && body && !x.free) {",
 "new_string": "  if (!x.free && body) {"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:59:27.070Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-10T06:59:28.488Z · glm-x-preview-260804

```
Now the probe script.
```


---

## 🤖 Assistant · 2026-08-10T06:59:45.896Z · glm-x-preview-260804

**🔧 ToolUse: `Write`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/_golemprobe.mts",
 "content": "// 石巨人 Boss 族冒烟:本体 245 + 头 246 + 双拳 247/248(挂载态/自由态/冲拳循环/全族自毁)\n// 直接驱动 bossAI_golem 的导出 AI(Enemy.ts 分发由主会话统一接线,此处不依赖)\nimport { Enemy } from '../src/entities/Enemy.ts';\nimport { TileStore } from '../src/world/TileStore.ts';\nimport { World } from '../src/world/World.ts';\nimport { golemAI, golemHeadAI, golemFistAI } from '../src/entities/bossAI_golem.ts';\n\nconst st = new TileStore(200, 300);\nconst world = new World(200, 300, 1, 't');\nworld.store = st;\nworld.groundLevel = 60;   // 玩家在地下(神庙层)→ 脱庙狂暴系数 num=1,行为确定\nworld.rockLevel = 190;\nfor (let x = 0; x < 200; x++) st.setTileSilent(x, 150, 1); // 地板\nconst enemies: Enemy[] = [];\nconst projectiles: unknown[] = [];\nconst game = {\n  world,\n  player: null as never,\n  enemies: () => enemies,\n  spawnDrop: () => null, damagePlayer: () => {}, addDamageNumber: () => {}, cutTile: () => {},\n  onEnemyKilled: () => {}, spawnEnemy: () => {}, notifyInventoryChanged: () => {}, showPickupLabel: () => {},\n  spawnParticles: () => {}, playSfx: () => {}, playSfxFiles: () => {},\n  entities: (() => {\n    const wrap = {\n      nextId: 2,\n      add: (e: Enemy, b?: string) => {\n        e.id = wrap.nextId++;\n        if (b === 'projectiles') projectiles.push(e); else enemies.push(e);\n      },\n    };\n    return wrap;\n  })(),\n} as never;\n\nlet ok = 0, bad = 0;\nconst check = (n: string, c: boolean, x?: unknown) => { if (c) { ok++; console.log('  ✓ ' + n); } else { bad++; console.log('  ✗ ' + n, x ?? ''); } };\n\n/** 玩家桩(x/y tile 坐标可变) */\nconst mkPlayer = (tx: number, ty: number) => ({\n  x: tx * 16, y: ty * 16, w: 20, h: 42,\n  cx: tx * 16 + 10, cy: ty * 16 + 21, vx: 0, vy: 0, dead: false,\n});\nlet player: ReturnType<typeof mkPlayer> = mkPlayer(100, 140);\n(game as unknown as { player: unknown }).player = player;\n\n/** aiStyle 局部分发(等同主会话将接入 Enemy.fixedUpdate 的映射) */\nconst aiByStyle: Record<number, (e: Enemy, g: never, p: never) => void> = {\n  45: golemAI as never,\n  46: golemHeadAI as never,\n  47: golemFistAI as never,\n};\nconst run = (ticks: number) => {\n  for (let i = 0; i < ticks; i++) {\n    for (const e of [...enemies]) {\n      if (e.dead) continue;\n      // 模拟 Enemy.fixedUpdate 头段:每 tick 先递减 iframes(直接调 AI 不会走共享尾段)\n      if (e.iframes > 0) e.iframes--;\n      const fn = aiByStyle[e.vanilla?.aiStyle ?? -1];\n      if (fn) fn(e, game as never, player as never);\n    }\n  }\n};\nworld.clock.timeOfDay = 0.0; // 夜晚(石巨人神庙 Boss 不逃夜,此值无行为影响)\nconst fam = () => ({\n  body: enemies.find((e) => e.vanillaId === 245)!,\n  head: enemies.find((e) => e.vanillaId === 246)!,\n  fistL: enemies.find((e) => e.vanillaId === 247)!,\n  fistR: enemies.find((e) => e.vanillaId === 248)!,\n});\nconst shoulder = (anchor: Enemy, isLeft: boolean) => ({\n  x: anchor.cx + anchor.vx + (isLeft ? -84 : 78) * 0.5,\n  y: anchor.cy + anchor.vy - 9 * 0.5,\n});\n\n// =============== ① 首帧生成部件 ===============\nconsole.log('== Golem 245 spawn ==');\n{\n  const body = Enemy.fromVanilla(245, 100 * 16, 120 * 16)!;\n  body.id = 1; enemies.push(body);\n  run(1);\n  const { head, fistL, fistR } = fam();\n  check('首帧生成头 246', !!head);\n  check('首帧生成左拳 247', !!fistL);\n  check('首帧生成右拳 248', !!fistR);\n  check('拳 ai0 侧别 ±1', fistL.ai0 === -1 && fistR.ai0 === 1, [fistL.ai0, fistR.ai0]);\n  check('本体 ai0=0 地面蓄力态', body.ai0 === 0, body.ai0);\n  check('头出生位置在本体上方', head.cy < body.cy, [Math.round(head.cy / 16), Math.round(body.cy / 16)]);\n}\n\n// =============== ② 本体跳跃(onGround 切换) ===============\nconsole.log('== Golem 245 jump ==');\n{\n  const { body } = fam();\n  run(140); // 落地 + 蓄力(首跳 ≈300+20t)\n  const baseY = body.cy, x0 = body.cx;\n  let sawAir = false, minY = baseY;\n  for (let i = 0; i < 560; i++) {\n    run(1);\n    if (!body.onGround) sawAir = true;\n    minY = Math.min(minY, body.cy);\n  }\n  check('发生起跳(离地)', sawAir);\n  check('跳起高度 > 150px', baseY - minY > 150, Math.round(baseY - minY));\n  check('起跳后落地(onGround)', body.onGround);\n  check('跳跃有水平位移', Math.abs(body.cx - x0) > 4, Math.round(body.cx - x0));\n}\n\n// =============== ④ 拳蓄力冲出后回位 ===============\nconsole.log('== Golem fist 247/248 punch ==');\n{\n  const { body, fistL, fistR } = fam();\n  const track = (fist: Enemy, isLeft: boolean) => {\n    let peak = 0, returned = false;\n    for (let i = 0; i < 500; i++) {\n      run(1);\n      const s = shoulder(body, isLeft);\n      const d = Math.hypot(fist.cx - s.x, fist.cy - s.y);\n      peak = Math.max(peak, d);\n      if (peak > 100 && d < 150) { returned = true; break; }\n    }\n    return { peak, returned };\n  };\n  const L = track(fistL, true);\n  check('左拳蓄力冲出(峰值位移 > 100px)', L.peak > 100, Math.round(L.peak));\n  check('左拳回位(肩锚 150px 内)', L.returned, Math.round(L.peak));\n  const R = track(fistR, false);\n  check('右拳蓄力冲出(峰值位移 > 100px)', R.peak > 100, Math.round(R.peak));\n  check('右拳回位(肩锚 150px 内)', R.returned, Math.round(R.peak));\n  check('拳存活', !fistL.dead && !fistR.dead);\n}\n\n// =============== ③ 本体血尽 → 头转自由态续战 ===============\nconsole.log('== Golem body slain -> head free ==');\n{\n  const { body, head } = fam();\n  body.hp = 0;\n  run(2);\n  check('本体进入死亡演出(ai3=1)', body.ai3 === 1, body.ai3);\n  check('头存活', !head.dead);\n  check('头转自由态(ai3=1)', head.ai3 === 1, head.ai3);\n  run(70);\n  check('本体 60t 后真死', body.dead);\n  check('头继续存活(本体死透后头继续)', !head.dead);\n  check('自由头满血续命(249 语义)', head.hp === head.maxHp, [head.hp, head.maxHp]);\n  const dmg249 = Enemy.fromVanilla(249, 0, 0)!.def.damage;\n  check('自由头属性对齐 249', head.def.damage === dmg249, [head.def.damage, dmg249]);\n  const hx = head.cx, hy = head.cy;\n  run(240); // 自由头悬浮(目标 = 玩家 + (0,-300))+ 弹幕循环\n  check('自由头自主战斗位移', Math.hypot(head.cx - hx, head.cy - hy) > 40,\n    [Math.round(head.cx / 16), Math.round(head.cy / 16)]);\n  check('拳改锚自由头存活', fam().fistL !== undefined && !enemies.find((e) => e.vanillaId === 247)!.dead);\n}\n\n// =============== ⑤ 头死 → 全族自毁 ===============\nconsole.log('== Golem head slain -> family despawn ==');\n{\n  const { head, fistL, fistR } = fam();\n  head.hp = 0;\n  run(2);\n  check('头死亡', head.dead);\n  check('全族自毁(拳全灭)', fistL.dead && fistR.dead, [fistL.dead, fistR.dead]);\n  check('无存活的石巨人族成员', enemies.every((e) => e.dead || (e.vanillaId !== 245 && e.vanillaId !== 246 && e.vanillaId !== 247 && e.vanillaId !== 248)));\n}\n\n// =============== 弹幕(258 火焰弹 / 259 眼激光) ===============\n{\n  const ids = projectiles.map((p) => (p as { projId: number }).projId);\n  check('发射过火焰弹 258', ids.includes(258), ids.slice(0, 8));\n}\n\nconsole.log(`\\n结果: ${ok} 通过, ${bad} 失败`);\nprocess.exit(bad ? 1 : 0);\n"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:59:45.903Z

**📎 ToolResult**

```
File created successfully at: ~/Project/GLM/SandboxWorld/game/scripts/_golemprobe.mts (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-10T06:59:47.501Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "./node_modules/.bin/vite-node scripts/_golemprobe.mts 2>&1 | tail -40",
 "description": "Run golem probe"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:59:56.099Z

**📎 ToolResult**

```
== Golem 245 spawn ==
  ✓ 首帧生成头 246
  ✓ 首帧生成左拳 247
  ✓ 首帧生成右拳 248
  ✓ 拳 ai0 侧别 ±1
  ✓ 本体 ai0=0 地面蓄力态
  ✓ 头出生位置在本体上方
== Golem 245 jump ==
  ✓ 发生起跳(离地)
  ✓ 跳起高度 > 150px
  ✓ 起跳后落地(onGround)
  ✓ 跳跃有水平位移
== Golem fist 247/248 punch ==
  ✓ 左拳蓄力冲出(峰值位移 > 100px)
  ✓ 左拳回位(肩锚 150px 内)
  ✓ 右拳蓄力冲出(峰值位移 > 100px)
  ✓ 右拳回位(肩锚 150px 内)
  ✓ 拳存活
== Golem body slain -> head free ==
  ✓ 本体进入死亡演出(ai3=1)
  ✓ 头存活
  ✓ 头转自由态(ai3=1)
  ✓ 本体 60t 后真死
  ✓ 头继续存活(本体死透后头继续)
  ✓ 自由头满血续命(249 语义)
  ✓ 自由头属性对齐 249
  ✓ 自由头自主战斗位移
  ✓ 拳改锚自由头存活
== Golem head slain -> family despawn ==
  ✓ 头死亡
  ✓ 全族自毁(拳全灭)
  ✓ 无存活的石巨人族成员
  ✓ 发射过火焰弹 258

结果: 28 通过, 0 失败

```


---

## 🤖 Assistant · 2026-08-10T06:59:57.450Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All 28 pass on the first run. Now run tsc check.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:59:58.000Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "./node_modules/.bin/tsc --noEmit 2>&1 | grep -E \"bossAI_golem|_golemprobe\" ; echo \"exit grep: $?\"; ./node_modules/.bin/tsc --noEmit 2>&1 | tail -5",
 "description": "Typecheck for golem files"
}
```


---

## 👤 User(sidechain) · 2026-08-10T07:00:08.381Z

**📎 ToolResult**

```
exit grep: 1
src/i18n/Lang.ts(8,141): error TS2724: '"./idNames.generated"' has no exported member named 'TILE_NAME_ZH_BY_ID'. Did you mean 'TILE_NAME_BY_ID'?
src/i18n/Lang.ts(8,161): error TS2724: '"./idNames.generated"' has no exported member named 'TILE_NAME_EN_BY_ID'. Did you mean 'TILE_NAME_BY_ID'?
src/i18n/Lang.ts(120,31): error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.

```


---

## 🤖 Assistant · 2026-08-10T07:00:11.684Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No errors in bossAI_golem.ts or _golemprobe.mts (grep found nothing). The remaining tsc errors are pre-existing in src/i18n/Lang.ts (unrelated to my change — probably from a parallel session or stale generated file). Let me verify those errors are pre-existing and not caused by my JSON edit. My JSON edit only added an entry; Lang.ts errors are about TILE_NAME_ZH_BY_ID in idNames.generated — unrelated. Let me double-check by confirming nothing else references vanilla-npcs in a way my change could break — e.g. `resolveJsonModule` typing of the JSON import (vanillaNpcs.ts imports the JSON; TS may check the import shape). The errors listed are only Lang.ts ones — let me see the full tsc output to make sure there aren't errors mentioning vanillaNpcs.
```

</details>


---

## 🤖 Assistant · 2026-08-10T07:00:12.309Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "./node_modules/.bin/tsc --noEmit 2>&1 | sort | uniq -c | awk '{$1=\"\";print}' | sed 's/(.*//' | sort | uniq -c | sort -rn | head",
 "description": "Summarize tsc error files"
}
```


---

## 👤 User(sidechain) · 2026-08-10T07:00:28.214Z

**📎 ToolResult**

```
   3  src/i18n/Lang.ts

```


---

## 🤖 Assistant · 2026-08-10T07:00:49.602Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Only 3 pre-existing errors in src/i18n/Lang.ts, unrelated to my work (they reference idNames.generated exports, not NPC data). Good.

Let me also double check a couple of subtle porting details I want to verify before reporting:

1. In `golemFistAI`, when `dist` is 0 (fist exactly at shoulder), `dist < 12 + num3` branch — Math.hypot(0,0)=0 fine.

2. `e.facing = isLeft ? 1 : -1` — I dropped the `side` variable; I use isLeft directly. Fine.

3. Unused import check: `clamp` used ✓; `baseOf` used in head ✓; `losClear` ✓; `accelTo` ✓; `vanillaNpc` ✓; `spawnPart` ✓; `shoot` ✓; TILE ✓.

4. One more vanilla fidelity check — the head's `x.l0` (localAI[0]) is used for frame rendering; I set it in the AI. It's stored in WeakMap; Renderer can't see it. For the report: the mouth-open frame state is in headX (not observable by Renderer). Main session wiring would need to map it or use ai fields. Hmm — actually I could expose l0 via a field the Renderer already reads... e.spquash? No. I'll note in the wiring report that 张嘴帧(localAI[0])与侧别(localAI[1])在 WeakMap 里,如需渲染可改用 ai 字段(如 ai2 之外的空闲槽)。Actually — is there a spare observable slot? Head uses ai0 (phase), ai1 (fireball timer), ai2 (laser timer), ai3 (free flag). l0/l1 have no home. I'll note it.

Also frame info for the body: vanilla FindFrame case 245 uses ai[1] (crouch frames) and ai[0] — both observable on Enemy ✓ good. Case 246 uses ai0/localAI[0]/localAI[1] — ai0 observable; localAI not. Case 249 uses localAI[0]. Note it.

5. Check the vanilla detail in head attached phase-1 branch: `vector85.X -= 40f * scale` when player left, `+= 40f` when right — I used `x.l1 * 40 * SCALE` ✓. And mouth shot origin: vector85 = (Center.X, Center.Y + 10*scale) ✓ I pass oy = 10*SCALE ✓.

Phase-0 mouth shot origin: vector84 = (Center.X, Center.Y + 10*scale) ✓.

Free head mouth shot: vector87 = Center + (0, -10*scale) ✓.

6. One thing I should double check — head attached: vanilla applies the phase logic only under `if (this.ai[0] == 0f) {...} else if (this.ai[0] == 1f) {...}` and then `if (life < lifeMax/2) ai[0]=1 else 0`. On the very first tick ai0 = 0 → phase 0 ✓. But note: vanilla phase 1 does NOT run while ai0==0 — matches mine.

7. Another check: vanilla head (46) — when player is dead, Main.player[target] is dummy; my version skips attacks when !player ✓.

8. `golemSpit` for the free head when player is null — guarded by `if (player)` ✓.

Now — also verify the vanilla fireball projectile 258's damage numbers in classic: 18 (phase 0), 24 (phase 1), 20 (free). These come straight from the decompiled source ✓.

One more sanity check on my claim about `Enemy.ts` wiring: the dispatch switch will need `case 45/46/47`. And the hurt() exemption for 245/246/247/248 must be added at Enemy.ts:1423 for the AI-first-line conversions to be reachable in gameplay. Also `VANILLA_BOSS_IDS` already includes 245 ✓ (no despawn). Also Renderer will need rotation rendering for 246/247/248 (spin) — the "旋转 NPC id" wiring item: fists use spin (rotation), head uses spin (velocity-based tilt) — I'll report ids 246/247/248 use e.spin rotation.

One more: the head in free mode — vanilla 249's noTileCollide gating uses flag48/SolidTiles; I skip actual collision entirely (head never collides in my port — I just move). Vanilla when flag48 false and noTileCollide true && SolidTiles → noTileCollide = false → then it collides with tiles and can be blocked. My port ignores that (head always passes through). Simplification — document it. Actually wait: should the free head collide? Vanilla: `if (!CanHit) { noTileCollide = true; flag48 = true } else if (noTileCollide && SolidTiles) { noTileCollide = false }`. So when it has LOS and is inside tiles → collide on. My port: always no-collide. It's a simplification worth noting (头始终穿墙,不做 SolidTiles 回落).

Also the attached head never collides (vanilla noTileCollide = true unconditionally at :31284) ✓.

Fists: vanilla noTileCollide managed per state ✓ ported.

Let me double check one more potential issue in the fist punch return: after the punch ends (state 0), num3 = 14 → homing at 14px/t; the shoulder may be 700px away; also the anchor body jumps around. My probe showed return ✓.

Now also double-check the body's despawn interplay: with player present, Manhattan distance < 3000 in the probe ✓.

One more possible issue: `world.clock.isDay` — golem doesn't use it ✓ (temple boss, no day flee). The task says "石巨人白天不逃(神庙 Boss)" ✓ nothing to do.

Let me also re-verify that my head AI doesn't break when the head is spawned standalone (no body) — used in probe? No, but robustness: head standalone → goFree → free branch ✓. Fists standalone → no anchor → dead ✓.

Finally, check git-less environment: no repo. Fine.

Let me run the probe once more plus a quick stress: run the whole probe a second time to ensure deterministic? It passed. Also verify vite-node exit code 0.
```

</details>


---

## 🤖 Assistant · 2026-08-10T07:00:50.055Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "./node_modules/.bin/vite-node scripts/_golemprobe.mts > /tmp/golemprobe.out 2>&1; echo \"exit=$?\"; tail -2 /tmp/golemprobe.out",
 "description": "Verify probe exit code"
}
```


---

## 👤 User(sidechain) · 2026-08-10T07:01:41.664Z

**📎 ToolResult**

```
exit=0

结果: 28 通过, 0 失败

```


---

## 🤖 Assistant · 2026-08-10T07:01:50.143Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All green. Let me do a final self-review of the AI file for any remaining issues before reporting:

1. In golemAI dying branch: I `return` before the despawn check — fine.

2. In golemAI, when player exists and ai0===0 but vy !== 0 (falling after spawn): no accumulation — vanilla same (velocity.Y != 0 → nothing). ✓

3. Body: vanilla `velocity.X = 4 * direction` — direction is int; ✓.

4. One fidelity gap I want to double check — vanilla AI_045 handles `target` selection each tick via TargetClosest inside branches; my `dir` recompute approximates ✓ documented.

5. `hasHead` for dontTakeDamage: vanilla checks 246 active. When the head goes free (246 still alive, in-place) — vanilla 246 dies and 249 spawns; 246 inactive → body vulnerable. In MY port, the head stays as 246 (alive) when free → hasHead true → body stays invulnerable! BUG: after head goes free, `hasHead` (vanillaId 246) is still true → body invulnerable forever → the body can never be killed in real gameplay (only via the head dying first, which is... actually fine? No — the body should become damageable after the head detaches, per vanilla, and also per my own design "挂载头血尽 → 本体解除无敌").

Fix: `hasHead` should count only ATTACHED heads: `n.vanillaId === 246 && headX.get(n)?.free !== true`... but WeakMap access from body AI — same module, fine. Or use the observable flag: head.ai3 === 0 means attached (I set ai3=1 on free). Use: `if (n.vanillaId === 246 && n.ai3 !== 1) hasHead = true;`. Clean and observable. Also then the body's num4 bonus `if (!hasHead) num4 += 2` matches vanilla (head gone → faster).

Let me apply that fix.

Also the fist punch speed bonus uses `anchor.hp < anchor.maxHp` — vanilla uses `Main.npc[golemBoss].life < lifeMax` i.e. the BODY's hp even when anchoring the body ✓ (anchor = body in phase 1). When anchoring the free head, vanilla wouldn't apply (golemBoss is body)... minor; fine as adapted.

Apply the hasHead fix.
```

</details>


---

## 🤖 Assistant · 2026-08-10T07:01:52.608Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts",
 "old_string": "  // ---- 部件存活扫描(NPC.cs:19487-19512):flag=头/flag2=左拳/flag3=右拳 ----\n  let hasHead = false, hasL = false, hasR = false;\n  for (const n of game.enemies() as Enemy[]) {\n    if (n.dead) continue;\n    if (n.vanillaId === 246) hasHead = true;\n    else if (n.vanillaId === 247) hasL = true;\n    else if (n.vanillaId === 248) hasR = true;\n  }",
 "new_string": "  // ---- 部件存活扫描(NPC.cs:19487-19512):flag=头/flag2=左拳/flag3=右拳 ----\n  //  注意头原体变身自由态后(ai3=1)视为\"挂载头已失\"——本体解除无敌且蓄力提速,\n  //  对齐原版\"246 死亡 → NewNPC 249\"后 flag 为假的语义\n  let hasHead = false, hasL = false, hasR = false;\n  for (const n of game.enemies() as Enemy[]) {\n    if (n.dead) continue;\n    if (n.vanillaId === 246 && n.ai3 !== 1) hasHead = true;\n    else if (n.vanillaId === 247) hasL = true;\n    else if (n.vanillaId === 248) hasR = true;\n  }"
}
```


---

## 👤 User(sidechain) · 2026-08-10T07:01:52.623Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-10T07:01:58.887Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Also add a probe check for this: after the head goes free (③), the body should NOT be invulnerable — but the body is dead by then in the probe... Order: in ③, head goes free at tick 1-2 while body still dying (60t). I can check body.iframes === 0 after the head went free but before the body dies. Let me add: in section ③ after run(2) (head free), check `body.iframes === 0`(挂载头失联后本体解除无敌). But careful: the body sets iframes=2 in the dying branch every tick! So iframes will be 2 while dying. Hmm — the dying branch sets iframes=2 (invulnerable during death animation) — that's fine semantically but blocks the check. I could check before setting hp=0: kill the HEAD first in a separate scenario... Simpler: reorder the check — in ③ after head free (ai3=1) and before body death... iframes is 2 due to dying.

Alternative: test the invulnerability semantics in the ②/④ window instead: while the attached head is alive, body.iframes should hit 2 every tick → check body.iframes > 0 at some point during ②. That validates the dontTakeDamage = flag behavior. And for the "head free → body vulnerable" path I can rely on code reading. Let me add to ②: check('挂载头在场时本体无敌(iframes>0)', body.iframes > 0). Note: my run() decrements iframes at the start of each enemy's update, and the body AI sets it to 2 after → so after run(1), body.iframes === 2 ✓.

Add that check after the settle (run(140)).
```

</details>


---

## 🤖 Assistant · 2026-08-10T07:02:00.720Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/_golemprobe.mts",
 "old_string": "  const { body } = fam();\n  run(140); // 落地 + 蓄力(首跳 ≈300+20t)\n  const baseY = body.cy, x0 = body.cx;",
 "new_string": "  const { body, head } = fam();\n  run(140); // 落地 + 蓄力(首跳 ≈300+20t)\n  check('挂载头在场时本体无敌(dontTakeDamage=flag)', body.iframes > 0, body.iframes);\n  head.hp = Math.floor(head.maxHp * 0.3); // 头残血 → 眼部阶段(ai0=1)与激光\n  run(1);\n  check('头血 < 半 → 眼部阶段 ai0=1', head.ai0 === 1, head.ai0);\n  head.hp = head.maxHp; // 复原,后续断言不依赖残血分档\n  run(1);\n  const baseY = body.cy, x0 = body.cx;"
}
```


---

## 👤 User(sidechain) · 2026-08-10T07:02:00.737Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/scripts/_golemprobe.mts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-10T07:02:02.654Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "./node_modules/.bin/vite-node scripts/_golemprobe.mts 2>&1 | sed -n '1,20p'; ./node_modules/.bin/vite-node scripts/_golemprobe.mts > /tmp/g.out 2>&1; echo \"exit=$?\"; tail -1 /tmp/g.out",
 "description": "Rerun probe with new checks"
}
```


---

## 👤 User(sidechain) · 2026-08-10T07:02:13.117Z

**📎 ToolResult**

```
== Golem 245 spawn ==
  ✓ 首帧生成头 246
  ✓ 首帧生成左拳 247
  ✓ 首帧生成右拳 248
  ✓ 拳 ai0 侧别 ±1
  ✓ 本体 ai0=0 地面蓄力态
  ✓ 头出生位置在本体上方
== Golem 245 jump ==
  ✓ 挂载头在场时本体无敌(dontTakeDamage=flag)
  ✓ 头血 < 半 → 眼部阶段 ai0=1
  ✓ 发生起跳(离地)
  ✓ 跳起高度 > 150px
  ✓ 起跳后落地(onGround)
  ✓ 跳跃有水平位移
== Golem fist 247/248 punch ==
  ✓ 左拳蓄力冲出(峰值位移 > 100px)
  ✓ 左拳回位(肩锚 150px 内)
  ✓ 右拳蓄力冲出(峰值位移 > 100px)
  ✓ 右拳回位(肩锚 150px 内)
  ✓ 拳存活
exit=0
结果: 30 通过, 0 失败

```


---

## 🤖 Assistant · 2026-08-10T07:02:20.759Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "./node_modules/.bin/tsc --noEmit 2>&1 | grep -c \"bossAI_golem\\|_golemprobe\"; echo \"---\"; ./node_modules/.bin/tsc --noEmit 2>&1 | wc -l",
 "description": "Final typecheck for golem files"
}
```


---

## 👤 User(sidechain) · 2026-08-10T07:03:02.767Z

**📎 ToolResult**

```
0
---
       3

```


---

## 🤖 Assistant · 2026-08-10T07:03:22.023Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
tsc: 0 errors mentioning bossAI_golem/_golemprobe; only the 3 pre-existing Lang.ts errors remain (unrelated — they reference idNames.generated, untouched by me; let me quickly confirm they're pre-existing by checking if Lang.ts or idNames.generated were modified recently... they're not files I touched. Also possible a parallel agent is editing them. Not my concern.)

Final report in Chinese covering:
1. 移植内容
2. 简化项(带行号)
3. 248 数据补了什么
4. 探针结果
5. 接线清单(aiStyle→函数、旋转 NPC id、召唤 key)

Files:
- ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts (new)
- ~/Project/GLM/SandboxWorld/game/scripts/_golemprobe.mts (new)
- ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json (+248)
- ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Projectile_258.png, Projectile_259.png (copied — task claimed they were全量 but they were missing)

Wiring notes:
- Enemy.ts dispatch: case 45 → golemAI; case 46 → golemHeadAI; case 47 → golemFistAI (247/248 同 aiStyle 47)。case 48(249)若直接生成也走 golemHeadAI(内部按 vanillaId===249 进自由态)。
- Enemy.ts hurt() 行 1423 的月总豁免列表需追加 245/246/247/248,否则血尽会被 hurt() 直接置 dead,各 AI 首行的转换不可达。
- 旋转 NPC id:246(头,spin = vx*0.1 远距倾斜/0 贴锚)、247/248(拳,spin = atan2 手臂角,247 镜像)、245 本体不用 spin。
- 渲染帧:本体 245 帧可由 ai0/ai1 派生(原版 FindFrame :73581);头 246/249 的张嘴帧 localAI[0] 与侧别 localAI[1] 在本文件 WeakMap(headX.l0/l1),Renderer 如需可改读。
- 召唤 key:Enemy.fromVanilla(245, x, y) 即可(首帧自动生成 246/247/248);vanillaNpcs 数据 aiStyle 45-47 已就绪。
- 弹幕:258(火焰弹)、259(眼激光),Projectile_258/259.png 已补入 public/sprites/vanilla/(任务说已全量,实际缺失,从 terraria-assets/Images 拷入)。

简化项 list with行号:
1. balanceNum(:19450-19457 等):无 ZoneLihzhardTemple/ZoneJungle API,仅保留"玩家在地表以上 ×2"一支(神庙地下=1 与原版常态一致);getGoodWorld +2/+3/+100 系全略。
2. getGoodWorld 落体砸火把(:19514-19534 / :19337-19362)略。
3. 断臂尘/落地 Gore(:19536-19595 / :19659)、拳聚能/焰尾尘(:19278-19292 / :19348-19356)以 spawnParticles 低频近似。
4. 自由头(249)的节奏分档原版读 golemBoss.life(:31570-31582 / :31620-31644)→ 二阶段本体已亡,改读头自身血量比例;flag49 原版=本体↔玩家无视线(:31646-31651)→ 改头↔玩家。
5. 自由头穿墙回落(:31509-31519 else-if SolidTiles → noTileCollide=false)未做,自由头恒穿墙。
6. 死亡链与原版差异(任务指定):原版 246 血尽原地 NewNPC 249(HitEffect :85842-85847)→ 本工程 246 原体变身(满血+249 属性);本体血尽原版无特殊处理 → 本工程 60t 死亡演出;自由头血尽 → 全族自毁(原版由 245 死亡置 downedGolemBoss :80146)。
7. 拳 ai0 按任务约定=侧别,原版 ai[0] 状态机移到 WeakMap fistX.state(ai[1] 计时保留);状态 3(:19394-19446,原版无入口)保留移植。
8. netOffset/纯 netcode、Item14/NPCHit4 音效以 playSfx('roar') 近似。
9. 本体 TargetClosest(direction)用 sign(player.cx-e.cx) 近似。

Probe: 30/30 绿,exit 0;断言覆盖任务 ①-⑤ + 附加(无敌语义/眼部阶段/249 属性对齐/258 弹幕)。

Also mention: tsconfig tsc → bossAI_golem/_golemprobe 0 错(仅剩 3 个既有 Lang.ts 错,与本次无关)。

Mention 248 data: 与 247 完全对称:id 248、name NPC_248、aiStyle 47、lifeMax 7000、damage 59、defense 28、width 40、height 30、noGravity、HitSound NPCHit4、DeathSound NPCDeath14、alpha 255、frames 1(原版 SetDefaults :12119-12133 247/248 同分支)。JSON 现共 632 条。
```

</details>


---

## 🤖 Assistant · 2026-08-10T07:03:46.110Z · glm-x-preview-260804

```
移植完成，探针 30/30 全绿。以下为汇报。

## 移植内容(`game/src/entities/bossAI_golem.ts`,新建,未动任何既有 ts)

- **本体 245 / aiStyle 45 → `golemAI`**:AI_045_Golem(NPC.cs:19447-19722)。首帧生成头 246+双拳 247/248(NewNPC 左上角坐标 -84/+78/-3、-9/-57,:19458-19467);挂载头在场本体无敌(dontTakeDamage=flag,:19513,`iframes=2`);地面蓄力 ai1 攒 300 → -20 蹲 20t → ==-1 起跳(穿墙跳 vx=4·dir、残血 -12.1·(num+9)/10 钳 -19.1,:19580-19645);空中夹玩家/侧向加速钳 ±num7(:19646-19708);断臂/残血提速表;曼哈顿 >3000 离场(:19709-19721)。重力 0.3/钳 10、自积分;`collideGround` 为本文件私有拷贝(多列采样版,140px 宽本体单列会半悬空)。
- **挂载头 246 / aiStyle 46 → `golemHeadAI`**:NPC.cs:31273-31499。锚本体 Center+(-3,-57)·scale,100 内整帧贴锚、远距 100 速+spin=vx·0.1;阶段 0 嘴部火焰弹 300t 循环 proj 258(伤 18 速 8),阶段 1(血<半)嘴弹伤 24+眼激光 259(伤 28,双眼 11 速/侧眼 12 速,发射点+3·v 前置);血量分档与无视线催速 1:1。
- **自由头 249 / aiStyle 48**:NPC.cs:31500-31741,折入 `golemHeadAI` 自由态(目标=玩家+(0,-300),7 速/0.05 步进 accelTo;嘴弹 258 伤 20;双眼激光 259 伤 24/速 11,每档 +1 伤/+0.25 速,无视线 ×1.5 伤/×2.5 速+玩家速度提前量)。
- **拳 247/248 / aiStyle 47 → `golemFistAI`**:AI_047(NPC.cs:19171-19446)。肩锚=锚主 Center+velocity+(∓84/78,-9)·scale;状态机 0 归位(14-32 速,贴肩蓄力 60t+侧别门 :19244-19256)→1 蓄力(整帧钉肩 30t)→2 冲拳(12-48 速直线,过玩家主轴关穿墙,离锚 700/撞墙回位)→3 直飞(原版无入口,保留)。247 旋转镜像约定 1:1。锚主:本体存活(含演出)→本体,本体死透→自由头,皆无→自毁(:19182)。
- **死亡链(各 AI 首行,不依赖外部钩子)**:本体血尽→ai3=1+60t 演出后真死;头(挂载)血尽或本体死亡→原体变身自由态(满血+249 属性,对齐原版 NewNPC 249);自由头血尽→全族自毁。

## 简化项
① 脱庙狂暴系数(:19450-19457 等)无 ZoneLihzhardTemple/ZoneJungle API,仅留"玩家在地表以上 ×2";getGoodWorld(+2/+3/+100、砸火把 :19514-19534/:19337-19362)略。② 尘/Gore 系(断臂 :19536-19595、落地 :19659、拳聚能/焰尾)以低频 spawnParticles 近似;Item14 等音效以 roar 近似。③ 自由头节奏分档原版读 golemBoss.life(:31570-31582/:31620-31644)→改读头自身血量;flag49(:31646-3151)改头↔玩家视线;SolidTiles 穿墙回落(:31509-31519)未做(恒穿墙)。④ 死亡链按任务约定与原版差异已注释标明(246 原地 NewNPC 249 :85842-85847 → 原体变身;downedGolemBoss :80146 → 自由头死全族自毁)。⑤ 拳 ai0=侧别(任务约定),原版 ai[0] 状态机移入 WeakMap,ai1 计时保留。⑥ TargetClosest 以 sign 近似。

## 248 数据(`public/sprites/vanilla-npcs.json`,唯一改动的既有文件)
紧随 247 插入、字段完全对称:`{"id":248,"name":"NPC_248","frames":1,"lifeMax":7000,"damage":59,"defense":28,"aiStyle":47,"width":40,"height":30,"noGravity":true,"HitSound":"NPCHit4","DeathSound":"NPCDeath14","alpha":255}`(原版 SetDefaults :12119-12133 即 247/248 同分支)。JSON 校验通过、键无重复,共 632 条。**另**:任务称 Projectile_N 已全量,实测缺 258/259,已从 `terraria-assets/Images/` 拷入 `public/sprites/vanilla/Projectile_258.png、259.png`(新增资产文件,未改既有文件)。

## 探针(`game/scripts/_golemprobe.mts`,照抄 _mechprobe 模板:fake game+地板 y=150+夜晚+局部 aiStyle 分发)
`vite-node` 30/30 通过、exit 0:①首帧生成 246/247/248+拳 ai0=±1 ②跳跃(onGround 切换、跳高>150px、水平位移)③拳蓄力冲出峰值>100px 后回位肩锚 150px 内(双拳)④本体 hp→0 后头存活转自由态(ai3=1、满血续命、249 属性、自主位移)⑤头死→全族自毁;附加断言:挂载头在场本体无敌、头血<半切眼部阶段、发射过 proj 258。`tsc --noEmit` 中 bossAI_golem/_golemprobe 0 错(仅剩 3 个既有 src/i18n/Lang.ts 错,与本次无关)。

## 接线清单(主会话)
- **Enemy.ts 分发**:`case 45: golemAI`、`case 46: golemHeadAI`、`case 47: golemFistAI`(247/248 同 aiStyle);若直接生成 249 也可走 `golemHeadAI`(内部按 vanillaId===249 进自由态)。
- **Enemy.ts hurt():1423** 的月总豁免列表(396/397/398)需追加 **245/246/247/248**,否则血尽被 hurt() 直接置 dead,各 AI 首行转换在实战不可达(探针是直写 hp 绕过的)。
- **旋转 NPC id**:246(头,spin=vx·0.1/0)、247/248(拳,spin=atan2 手臂角,247 镜像);245 不用 spin。
- **渲染帧**:本体可直接由 ai0/ai1 派生(原版 FindFrame :73581);头 246/249 张嘴帧 localAI[0]/侧别 localAI[1] 在本文件 WeakMap(headX.l0/l1),Renderer 需要时建议改挂到空闲 Enemy 字段。
- **召唤 key**:`Enemy.fromVanilla(245, x, y)` 一只即可,首帧自动带出全族;245 已在 VANILLA_BOSS_IDS(不参与 despawn/白天不逃)。
```
