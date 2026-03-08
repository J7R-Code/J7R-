import discord
from discord.ext import commands
import os
import json
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="-", intents=intents)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

role_hierarchy = [
    1458919310230552690, 1458919308972523756, 1458919306745348279,
    1458919304631160980, 1458919303490306048, 1458919301531828507,
    1458919298339705055, 1458919297199112509, 1458919296192348312,
    1458919293411659926, 1458919289661816883, 1458919288378364128,
    1458919286415429789, 1458919285228437515, 1458919283789795461,
    1458919280820097308, 1458919279104888915, 1458919277447876671,
    1458919276139381008, 1458919274386030674, 1458919272939258122,
    1458919270867013848, 1458919268946149591, 1458919266714779863,
    1458919262705156182, 1458919259890647235, 1458919257688641628,
    1458919256950313238, 1458919252915650652, 1458919251711754250,
    1458919250109661410, 1458919248096395464, 1458919247412723884,
    1458919245952979065, 1458919242979217649, 1458919241670459525
]

JAIL_ROLE_ID = 1466820426524000399

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="made by : e_9b"))

@bot.command(name="سجن")
@commands.has_permissions(manage_roles=True)
async def jail(ctx, member: discord.Member, *, reason: str = "بدون سبب"):
    data = load_data()
    user_roles = [role.id for role in member.roles if role.name != "@everyone"]
    
    if "jailed" not in data:
        data["jailed"] = {}
    data["jailed"][str(member.id)] = user_roles
    save_data(data)
    
    try:
        jail_role = ctx.guild.get_role(JAIL_ROLE_ID)
        if jail_role:
            await member.edit(roles=[jail_role], reason=f"سجن: {reason}")
            await ctx.send(f"تم سجن العضو بنجاح ⛓🚨 \nالسبب: {reason}")
        else:
            await ctx.send("رتبة السجن غير موجودة.")
    except Exception as e:
        await ctx.send(f"حدث خطأ (تأكد أن رتبة البوت أعلى من رتبة العضو): {e}")

@bot.command(name="اعفاء")
@commands.has_permissions(manage_roles=True)
async def unjail(ctx, member: discord.Member):
    data = load_data()
    if "jailed" in data and str(member.id) in data["jailed"]:
        saved_roles = data["jailed"][str(member.id)]
        roles_to_add = [ctx.guild.get_role(r_id) for r_id in saved_roles if ctx.guild.get_role(r_id) is not None]
        
        try:
            await member.edit(roles=roles_to_add, reason="اعفاء")
            del data["jailed"][str(member.id)]
            save_data(data)
            await ctx.send(f"تم إعفاء العضو {member.mention} ✅")
        except Exception as e:
            await ctx.send(f"حدث خطأ: {e}")
    else:
        await ctx.send("لم أجد أي رتب محفوظة لهذا العضو. تأكد أنه مسجون وأن كود السجن قام بحفظ رتبه. ❌")

@bot.command(name="ترقية")
@commands.has_permissions(manage_roles=True)
async def promote(ctx, member: discord.Member):
    member_role_ids = [r.id for r in member.roles]
    current_index = -1
    
    for i, r_id in enumerate(role_hierarchy):
        if r_id in member_role_ids:
            current_index = i
            break
            
    if current_index == -1:
        await ctx.send("لم أجد أي رتبة لدى هذا العضو من ضمن قائمة رتب الترقية! ❌")
    elif current_index == len(role_hierarchy) - 1:
        await ctx.send("هذا العضو وصل إلى أعلى رتبة في التسلسل ولا يمكن ترقيته أكثر! 🛑")
    else:
        old_role = ctx.guild.get_role(role_hierarchy[current_index])
        new_role = ctx.guild.get_role(role_hierarchy[current_index + 1])
        try:
            if old_role: await member.remove_roles(old_role)
            if new_role: await member.add_roles(new_role)
            await ctx.send(f"تمت ترقية العضو {member.mention} بنجاح إلى الرتبة التالية! 🎉")
        except Exception as e:
            await ctx.send(f"حدث خطأ: {e}")

@bot.command(name="تخفيض")
@commands.has_permissions(manage_roles=True)
async def demote(ctx, member: discord.Member):
    member_role_ids = [r.id for r in member.roles]
    current_index = -1
    
    for i, r_id in enumerate(role_hierarchy):
        if r_id in member_role_ids:
            current_index = i
            break
            
    if current_index == -1:
        await ctx.send("لم أجد أي رتبة لدى هذا العضو من ضمن قائمة الرتب! ❌")
    elif current_index == 0:
        await ctx.send("هذا العضو في أدنى رتبة في التسلسل ولا يمكن تخفيضه أكثر! 🛑")
    else:
        old_role = ctx.guild.get_role(role_hierarchy[current_index])
        new_role = ctx.guild.get_role(role_hierarchy[current_index - 1])
        try:
...
