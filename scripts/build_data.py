import urllib.request
import json
import os

VERSION = "16.19.1"
CDN_BASE = f"https://ddragon.leagueoflegends.com/cdn/{VERSION}"

print("Downloading Russian runes...")
runes_req = urllib.request.urlopen(f"{CDN_BASE}/data/ru_RU/runesReforged.json")
runes_data = json.loads(runes_req.read().decode())

print("Downloading Russian champions...")
champs_req = urllib.request.urlopen(f"{CDN_BASE}/data/ru_RU/champion.json")
champs_data = json.loads(champs_req.read().decode())["data"]

# Map roles & builds heuristics
# Difficulty:
# 1-3: Новичок (Beginner-friendly)
# 4-7: Средний уровень (Intermediate)
# 8-10: Опытный игрок / Ветеран (Veteran / High Skill Cap)

# Lane assignment heuristics based on tags and typical champions
lane_assignments = {
    # Assassin
    "Zed": "MID", "Talon": "MID", "Katarina": "MID", "Qiyana": "MID", "Akali": "MID", "Fizz": "MID",
    "KhaZix": "JUNGLE", "Evelynn": "JUNGLE", "Rengar": "JUNGLE", "Shaco": "JUNGLE", "Kayn": "JUNGLE", "Nocturne": "JUNGLE",
    # Mages
    "Lux": "SUPPORT / MID", "Ahri": "MID", "Syndra": "MID", "Orianna": "MID", "Viktor": "MID", "Veigar": "MID", "Hwei": "MID",
    "Morgana": "SUPPORT", "Brand": "SUPPORT / JUNGLE", "Zyra": "SUPPORT", "Xerath": "SUPPORT / MID", "Anivia": "MID",
    # Marksman
    "Jinx": "BOT (ADC)", "Caitlyn": "BOT (ADC)", "Ashe": "BOT (ADC)", "MissFortune": "BOT (ADC)", "Ezreal": "BOT (ADC)",
    "KaiSa": "BOT (ADC)", "Vayne": "BOT (ADC)", "Samira": "BOT (ADC)", "Jhin": "BOT (ADC)", "Lucian": "BOT (ADC)",
    # Tank / Fighter
    "Garen": "TOP", "Darius": "TOP", "Aatrox": "TOP", "Mordekaiser": "TOP", "Sett": "TOP", "Fiora": "TOP", "Camille": "TOP",
    "Malphite": "TOP", "Ornn": "TOP", "Shen": "TOP", "Jax": "TOP / JUNGLE", "Irelia": "TOP / MID", "Riven": "TOP",
    "LeeSin": "JUNGLE", "Vi": "JUNGLE", "Amumu": "JUNGLE", "Warwick": "JUNGLE / TOP", "MasterYi": "JUNGLE", "Viego": "JUNGLE",
    # Support
    "Thresh": "SUPPORT", "Blitzcrank": "SUPPORT", "Leona": "SUPPORT", "Nautilus": "SUPPORT", "Lulu": "SUPPORT",
    "Nami": "SUPPORT", "Sona": "SUPPORT", "Yuumi": "SUPPORT", "Soraka": "SUPPORT", "Rakan": "SUPPORT", "Pyke": "SUPPORT",
    "Braum": "SUPPORT", "Milio": "SUPPORT", "Renata": "SUPPORT"
}

# Recommendation archetype:
# 'beginner' (новичок), 'experienced' (опытный/ветеран), 'universal' (универсал)
processed_champions = []

for cid, c in champs_data.items():
    diff = c["info"]["difficulty"]
    tier = "beginner" if diff <= 4 else ("veteran" if diff >= 8 else "intermediate")
    
    tags = c["tags"]
    primary_role = tags[0] if tags else "Fighter"
    
    lane = lane_assignments.get(cid, None)
    if not lane:
        if "Marksman" in tags:
            lane = "BOT (ADC)"
        elif "Support" in tags:
            lane = "SUPPORT"
        elif "Tank" in tags:
            lane = "TOP / SUPPORT"
        elif "Mage" in tags:
            lane = "MID / SUPPORT"
        elif "Assassin" in tags:
            lane = "MID / JUNGLE"
        else:
            lane = "TOP / JUNGLE"
            
    # Suggested runes based on class
    runes_rec = {}
    if "Marksman" in tags:
        runes_rec = {
            "primaryTree": "Precision",
            "primaryName": "Точность",
            "keystone": "Смертельный темп / Решительное наступление",
            "perks": ["Сверхлечение или Триумф", "Легенда: рвение", "Удар милосердия"],
            "secondaryTree": "Inspiration",
            "secondaryName": "Вдохновение",
            "secondaryPerks": ["Магическая обувь", "Доставка печенья"],
            "shards": ["+10% скорости атаки", "+9 адаптивной силы", "+65 здоровья"]
        }
        build_rec = ["Грань Бесконечности", "Скорострельная пушка", "Убийца кракенов", "Поклон лорда Доминика", "Кровопийца", "Наголенники берсерка"]
        playstyle = "Держите максимальную дистанцию в командных боях. Не идите вперед танков. Бейте ближайшую безопасную цель и кайтите (атака + шаг назад)."
    elif "Mage" in tags:
        runes_rec = {
            "primaryTree": "Sorcery",
            "primaryName": "Колдовство",
            "keystone": "Призыв Пушинки / Магическая комета",
            "perks": ["Поток маны", "Превосходство", "Ожог / Надвигающаяся буря"],
            "secondaryTree": "Inspiration",
            "secondaryName": "Вдохновение",
            "secondaryPerks": ["Магическая обувь", "Космическое знание"],
            "shards": ["+9 адаптивной силы", "+9 адаптивной силы", "+65 здоровья"]
        }
        build_rec = ["Эхо Людена / Буря Людена", "Сумрачное пламя", "Песочные часы Жони", "Смертельная шляпа Рабадона", "Посох Бездны", "Сапоги чародея"]
        playstyle = "Контролируйте волну крипов умениями с дистанции. Экономьте ману на ранних уровнях. В тимфайтах выдавайте прокаст способностей из-за спин союзников."
    elif "Assassin" in tags:
        runes_rec = {
            "primaryTree": "Domination",
            "primaryName": "Доминирование",
            "keystone": "Казнь электричеством / Темная жатва",
            "perks": ["Внезапный удар", "Коллекция глаз", "Ненасытный или Беспощадный охотник"],
            "secondaryTree": "Precision",
            "secondaryName": "Точность",
            "secondaryPerks": ["Триумф", "Удар милосердия"],
            "shards": ["+9 адаптивной силы", "+9 адаптивной силы", "+65 здоровья"]
        }
        build_rec = ["Призрачный клинок Йомуу", "Шакрам Аксиом", "Клык змея", "Грань ночи", "Черный секира", "Ионийские сапоги просветления"]
        playstyle = "Ищите возможность для внезапного нападения из засады или через стены. Ваша главная цель — вражеский стрелок (ADC) или маг. Не начинайте драку первым в лоб!"
    elif "Tank" in tags:
        runes_rec = {
            "primaryTree": "Resolve",
            "primaryName": "Храбрость",
            "keystone": "Хватка нежити / Дрожь земли",
            "perks": ["Удар щитом или Снос", "Второе дыхание / Костяная пластина", "Разрастание"],
            "secondaryTree": "Precision",
            "secondaryName": "Точность",
            "secondaryPerks": ["Триумф", "Стойкость"],
            "shards": ["+8 ускорения умений", "+65 здоровья", "+65 здоровья / броня"]
        }
        build_rec = ["Сердце стали", "Эгида солнечного пламени", "Шипованный доспех", "Облачение духов", "Броня мертвеца", "Бронированные сапоги"]
        playstyle = "Вы — живой щит команды и инициатор сражений. Впитывайте урон, защищайте керри союзников и контролируйте врагов стан-эффектами."
    elif "Support" in tags:
        runes_rec = {
            "primaryTree": "Resolve",
            "primaryName": "Храбрость",
            "keystone": "Ледяной нарост / Дрожь земли / Пушинка",
            "perks": ["Живой источник", "Костяная пластина", "Оживление"],
            "secondaryTree": "Inspiration",
            "secondaryName": "Вдохновение",
            "secondaryPerks": ["Доставка печенья", "Космическое знание"],
            "shards": ["+8 ускорения умений", "+65 здоровья", "+65 здоровья"]
        }
        build_rec = ["Атлас мира / Сани первопроходца", "Медальон Железных Солари", "Искупление", "Клятва рыцаря", "Пылающая каддильница", "Сапоги подвижности"]
        playstyle = "Обеспечивайте обзор тотемами вокруг объектов (Дракон, Барон). Спасайте и усиливайте союзного стрелка. Контролируйте перемещения вражеского лесника."
    else: # Fighter
        runes_rec = {
            "primaryTree": "Precision",
            "primaryName": "Точность",
            "keystone": "Завоеватель",
            "perks": ["Триумф", "Легенда: рвение или Стойкость", "Последний рубеж"],
            "secondaryTree": "Resolve",
            "secondaryName": "Храбрость",
            "secondaryPerks": ["Второе дыхание", "Разрастание"],
            "shards": ["+9 адаптивной силы", "+9 адаптивной силы", "+65 здоровья"]
        }
        build_rec = ["Тройственный союз / Ненасытная гидра", "Черный секира", "Танец смерти", "Испытание Стерака", "Зев Малмортиуса", "Бронированные сапоги"]
        playstyle = "Идеален для дуэлей 1 на 1 и сплит-пуша башен на боковых линиях. В командном бою ищите фланг для врыва на уязвимых врагов."

    # Specific beginner tips
    beginner_tip = ""
    if diff <= 3:
        beginner_tip = "⭐ Отличный выбор для новичка! Простые и понятные механики умений, высокая надежность, прощает ошибки позиционирования."
    elif diff <= 6:
        beginner_tip = "⚖️ Средний уровень сложности. Потребуется несколько игр, чтобы привыкнуть к таймингам способностей и комбо."
    else:
        beginner_tip = "🔥 Высокий порог входа! Рекомендуется опытным игрокам. Требует отличного микроконтроля, реакции и знания карты."

    processed_champions.append({
        "id": cid,
        "name": c["name"],
        "title": c["title"],
        "tags": tags,
        "primaryRole": primary_role,
        "lane": lane,
        "difficulty": diff,
        "tier": tier,
        "blurb": c["blurb"],
        "icon": f"{CDN_BASE}/img/champion/{c['image']['full']}",
        "splash": f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{cid}_0.jpg",
        "loading": f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{cid}_0.jpg",
        "info": c["info"],
        "beginnerTip": beginner_tip,
        "runes": runes_rec,
        "build": build_rec,
        "playstyle": playstyle
    })

# Sort champions by Russian name
processed_champions.sort(key=lambda x: x["name"])

# Clean up runesReforged data for UI
clean_runes = []
for r in runes_data:
    tree = {
        "id": r["id"],
        "key": r["key"],
        "name": r["name"],
        "icon": f"https://ddragon.leagueoflegends.com/cdn/img/{r['icon']}",
        "slots": []
    }
    for slot_idx, slot in enumerate(r["slots"]):
        runes_list = []
        for rune in slot["runes"]:
            # remove some lol-uikit tags from descriptions
            short_desc = rune["shortDesc"].replace("<lol-uikit-tooltipped-keyword key='LinkTooltip_Description_AdaptiveDmg'>", "").replace("</lol-uikit-tooltipped-keyword>", "").replace("<b>", "").replace("</b>", "")
            long_desc = rune["longDesc"]
            runes_list.append({
                "id": rune["id"],
                "key": rune["key"],
                "name": rune["name"],
                "icon": f"https://ddragon.leagueoflegends.com/cdn/img/{rune['icon']}",
                "shortDesc": short_desc,
                "longDesc": long_desc,
                "isKeystone": (slot_idx == 0)
            })
        tree["slots"].append(runes_list)
    clean_runes.append(tree)

data_bundle = {
    "version": VERSION,
    "champions": processed_champions,
    "runeTrees": clean_runes
}

with open("/home/user/lol_app/data.json", "w", encoding="utf-8") as f:
    json.dump(data_bundle, f, ensure_ascii=False, indent=2)

print(f"Saved {len(processed_champions)} champions and {len(clean_runes)} rune trees to data.json")
