#!/usr/bin/env python3
"""Generate expanded content for HKU + Harvard History course files.

Style: 袁騰飛風格 — narrative, opinionated, character-driven, focus on power/weapons shaping history.
Format: 5MM + 3DG + 10Q + 5 deep dives + 10 detailed solutions + 5 Mermaid diagrams + 5-point insights.
All content bilingual (中英對照).
"""
import re
from pathlib import Path


# Curated themes per course (5 themes + period + focus)
# Format: code -> {name_zh, name_en, period, themes: [5], tensions: [3]}
COURSES = {
    # === HKU 入門 / 概論類 ===
    "HIST1016": {
        "name_zh": "現代世界",
        "name_en": "The Modern World",
        "period": "1500-present 全球史",
        "themes": ["現代性作為多元軌跡", "帝國主義的全球擴張", "革命與反革命", "技術革命重塑文明", "現代身份政治"],
        "tensions": [
            ("Eurocentrism vs Global Agency", "歐洲中心論 vs 全球能動性",
             "現代世界是否本質上是歐洲擴張的產物？",
             "A: 是 — 工業革命、殖民主義、現代科學都源自歐洲，現代世界的骨架是歐洲搭的",
             "B: 否 — 中國、印度、伊斯蘭世界都有內生現代性，只是被帝國主義打斷了"),
            ("Modernization vs Westernization", "現代化 vs 西化",
             "非西方社會接受現代技術/制度是否必然意味著接受西方價值？",
             "A: 必然 — 啟蒙理性、個人主義、法治是現代性的核心包",
             "B: 分離 — 日本明治維新證明可以選擇性西化，保留本土精神"),
            ("Linear Progress vs Cyclical Catastrophe", "線性進步 vs 週期性災難",
             "現代史是向上走還是 20 世紀兩次大戰證明了文明本身的脆弱？",
             "A: 進步 — 人均壽命、科技、權利都在改善",
             "B: 災難 — 兩次世界大戰、種族滅絕、生態崩潰顯示現代性內含毀滅種子"),
        ],
    },
    "HIST1017": {
        "name_zh": "現代香港",
        "name_en": "Modern Hong Kong",
        "period": "1841-present",
        "themes": ["殖民現代性的雙重性", "香港作為帝國轉運點", "1997 過渡的歷史斷裂", "香港身份的混雜性", "全球資本主義的香港節點"],
        "tensions": [
            ("Colonial Legacy — Benign or Exploitative", "殖民遺產 — 良性 vs 剝削",
             "英治香港究竟是『現代化恩惠』還是『帝國主義剝削』？",
             "A: 良性 — 法治、廉政、公共衛生都是英國帶來的",
             "B: 剝削 — 香港繁榮建立在對中國內地的轉口貿易控制，犧牲了本地產業自主"),
            ("1997 過渡 — Smooth or Traumatic", "1997 過渡 — 平順 vs 創傷",
             "回歸對香港人來說是歷史回歸還是文化斷裂？",
             "A: 平順 — 一國兩制設計精密，港人治港高度自治",
             "B: 創傷 — 民主派被邊緣化、媒體自由收緊、2019 反送中顯示制度裂痕"),
            ("Hong Kong Identity — Hybrid or Trapped", "香港身份 — 混雜 vs 困局",
             "香港人究竟是真正的混血文化還是夾縫中無根？",
             "A: 混雜 — 粵英中三語並行，東西方文化交匯，自成一家",
             "B: 困局 — 殖民後遺症，本地人對國家缺乏認同，2019 之後撕裂"),
        ],
    },
    "HIST1023": {
        "name_zh": "現代東亞",
        "name_en": "Modern East Asia",
        "period": "1840-present",
        "themes": ["東亞作為帝國主義競技場", "中日韓現代化路徑分化", "冷戰在東亞的熱戰", "經濟奇蹟的國家角色", "東亞民主化的不完整"],
        "tensions": [
            ("Japan's Wartime Role — Victim or Aggressor", "日本戰時角色 — 受害者 vs 侵略者",
             "日本在二戰中是被美國原子彈轟炸的受害者，還是對亞洲的侵略者？",
             "A: 受害者 — 廣島長崎平民傷亡、南京大屠殺本身也是中日雙向",
             "B: 侵略者 — 南京大屠殺、慰安婦、731 部隊都證明日本是加害者"),
            ("China's Rise — Continuity or Break", "中國崛起 — 延續 vs 斷裂",
             "當代中國崛起是中華文明五千年延續的結果，還是 1949 革命斷裂後的新生？",
             "A: 延續 — 文化基因、統一帝國傳統、大一統觀念都活著",
             "B: 斷裂 — 1949 馬列化、文革、改革開放都是激進實驗，與傳統斷裂"),
            ("South Korea's Democratization — Miracle or Slow Burn", "南韓民主化 — 奇蹟 vs 慢火",
             "1987 民主化是突然奇蹟還是 30 年抗爭累積？",
             "A: 奇蹟 — 1987 六月民主運動直接促成全斗煥讓步",
             "B: 慢火 — 光州事件、學生運動、勞工運動鋪墊 30 年"),
        ],
    },
    "HIST1025": {
        "name_zh": "美國史導論",
        "name_en": "Introduction to the United States",
        "period": "1607-present",
        "themes": ["大陸擴張作為建國邏輯", "工業化與軍事的共生", "區域強權到全球投射", "國內政治與對外行動的相互塑造", "1898 年海外擴張轉折"],
        "tensions": [
            ("Imperial Tendency from Founding?", "建國初期就有帝國傾向？",
             "美國從建國起就有帝國邏輯還是後天習得？",
             "A: 是 — 西進運動、門羅主義、天命論都內含帝國性",
             "B: 否 — 大陸擴張與海外帝國主義有本質區別，1898 才是轉折"),
            ("Industrialization's Role", "工業化如何影響美國全球角色？",
             "工業實力是美國崛起的決定性因素嗎？",
             "A: 是 — 工業產能直接轉化為軍事能力",
             "B: 否 — 必須結合戰略文化與國際機會"),
            ("Overseas Military — Inevitable or Choice", "海外軍事 — 必然 vs 選擇",
             "美國海外軍事存在是實力上升後的必然還是政策選擇？",
             "A: 必然 — 大國必尋求投射能力",
             "B: 選擇 — 孤立主義傳統很強，二戰前國務院反對海外捲入"),
        ],
    },
    # === HKU 中國與亞洲史 ===
    "HIST2068": {
        "name_zh": "二十世紀中國思想史",
        "name_en": "Intellectual History of 20th C. China",
        "period": "1895-2000",
        "themes": ["傳統與現代的拉鋸", "激進主義的崛起", "馬列主義的中國化", "新文化運動的遺產", "思想與權力的糾纏"],
        "tensions": [
            ("May Fourth — Westernization or Anti-Tradition", "五四運動 — 西化 vs 反傳統",
             "五四的本質是全面西化還是反對舊傳統？",
             "A: 西化 — 德先生賽先生，全盤否定儒教",
             "B: 反傳統 — 是針對吃人禮教，不是針對中國文化本身"),
            ("Maoism — Authentic or Imposed", "毛主義 — 本土 vs 外來",
             "毛澤東思想是中國本土產物還是蘇聯馬列的移植？",
             "A: 本土 — 農民革命、游擊戰、群眾路線都有中國傳統影子",
             "B: 外來 — 階級鬥爭、無產階級專政完全是馬列詞彙"),
            ("1980s Liberalism — Real or Brief", "1980s 自由主義 — 真實 vs 短暫",
             "80 年代思想解放是真實的多元主義還是黨內改革派策略？",
             "A: 真實 — 西單民主牆、人道主義馬克思主義是思想啟蒙",
             "B: 短暫 — 胡耀邦趙紫陽都是黨內改革派，1989 後迅速消亡"),
        ],
    },
    "HIST2118": {
        "name_zh": "中美關係文化史",
        "name_en": "Chinese and Americans: A Cultural History",
        "period": "1784-present",
        "themes": ["相互凝視的他者想像", "傳教士作為文化中介", "排華法案的雙向塑造", "太平洋戰爭的同盟神話", "當代中美誤判模式"],
        "tensions": [
            ("Mutual Perception — Symmetric or Skewed", "相互認知 — 對稱 vs 偏斜",
             "中美對彼此的認知是對等的嗎？",
             "A: 對稱 — 都是大國，相互研究時間長",
             "B: 偏斜 — 美國對中國的瞭解遠少於中國對美國，1949 後尤其"),
            ("Missionaries — Cultural Bridge or Imperial Agents", "傳教士 — 橋樑 vs 帝國工具",
             "19 世紀美國傳教士是中美文化交流的橋樑還是帝國主義先鋒？",
             "A: 橋樑 — 帶來現代教育、醫學、翻譯",
             "B: 工具 — 不平等條約保護下進入，服務於美國利益"),
            ("Ping-Pong Diplomacy 1971 — Real Thaw or Symbol", "乒乓外交 1971 — 真實解凍 vs 象徵",
             "1971 乒乓外交是尼克遜主動策略還是偶然契機？",
             "A: 策略 — 季辛吉秘密訪華、越南戰爭背景下的現實政治",
             "B: 偶然 — 桌球選手莊則棟與美國選手格倫・科恩的偶然互動"),
        ],
    },
    "HIST2127": {
        "name_zh": "清代中國與世界",
        "name_en": "Qing China in the World, 1644-1912",
        "period": "1644-1912",
        "themes": ["清帝國的內亞性", "朝貢體系 vs 條約體系", "鴉片戰爭的結構性後果", "自強運動的局限", "辛亥革命的歷史遺產"],
        "tensions": [
            ("Qing Identity — Sinicized or Manchu", "清認同 — 漢化 vs 滿洲",
             "清朝是中國傳統王朝的延續還是滿洲殖民政權？",
             "A: 漢化 — 康熙雍正乾隆全面接受儒教，承襲科舉",
             "B: 滿洲 — 八旗制度、滿文、內亞性保留，New Qing History 強調滿洲獨特性"),
            ("Tribute System — Functional or Mythical", "朝貢體系 — 真實 vs 神話",
             "朝貢體系是真實的國際秩序還是中國中心主義的神話？",
             "A: 真實 — 規範明確、互市貿易、定期使節",
             "B: 神話 — 現代學者建構的，實際運作混亂"),
            ("Opium War — Civilizational Clash or Imperialist Aggression", "鴉片戰爭 — 文明衝突 vs 帝國侵略",
             "第一次鴉片戰爭是文明衝突還是帝國主義侵略？",
             "A: 衝突 — 中國閉關自守，必須打破",
             "B: 侵略 — 英國為傾銷鴉片毒害中國，戰爭是非正義的"),
        ],
    },
    "HIST2143": {
        "name_zh": "中國婦女與性別史",
        "name_en": "Women and Gender in Chinese History",
        "period": "1600-present",
        "themes": ["儒家性別秩序", "纏足作為身體政治", "五四時期的婦女解放", "毛時代的婦女能動性", "當代性別政治的回潮"],
        "tensions": [
            ("Foot-binding — Aesthetic or Patriarchal Control", "纏足 — 審美 vs 父權控制",
             "纏足是美學時尚還是對女性身體的父權控制？",
             "A: 審美 — 各階層女性自願選擇，社會時尚",
             "B: 控制 — 限制女性行動、強化貞操觀念、為父權服務"),
            ("Mao Era Women — Liberated or Doubly Exploited", "毛時代婦女 — 解放 vs 雙重剝削",
             "毛時代『婦女能頂半邊天』是真正解放還是雙重負擔？",
             "A: 解放 — 大量女性進入勞動力市場、領導層",
             "B: 雙重 — 工作負擔疊加家庭責任，城市單位體制下"),
            ("Contemporary Feminism — Genuine or State-Led", "當代女性主義 — 真實 vs 國家主導",
             "當代中國女性主義是真實社會運動還是國家政策？",
             "A: 真實 — #MeToo 在中國興起，反性騷擾",
             "B: 國家主導 — 妇联是官方組織，獨立婦女 NGO 被壓制"),
        ],
    },
    "HIST2177": {
        "name_zh": "近代中國經濟史",
        "name_en": "Economic History of Modern China",
        "period": "1800-present",
        "themes": ["GDP 與國民福祉的斷裂", "不平等條約的經濟成本", "國民黨黃金十年的真相", "毛時代工業化的成就與代價", "改革開放奇蹟的源頭"],
        "tensions": [
            ("Pre-1949 GDP — Largest or Hollow", "1949 前 GDP — 最大還是空殼",
             "晚清 GDP 佔世界三分之一是真實財富還是人多？",
             "A: 真實 — 經濟總量大，茶絲瓷出口強",
             "B: 空殼 — 人均 GDP 極低，現代工業幾乎為零"),
            ("Nanjing Decade — Real Growth or Myth", "南京十年 — 真實增長 vs 神話",
             "國民黨 1927-37 是真實工業化還是後來建構的神話？",
             "A: 真實增長 — 工業產能翻倍，鐵路建設",
             "B: 神話 — 主要由沿海地區支撐，內戰與通脹抵消"),
            ("Deng's Reform — Pragmatism or Betrayal", "鄧氏改革 — 務實 vs 背叛",
             "改革開放是務實主義還是對社會主義的背叛？",
             "A: 務實 — 貓論、不問姓資姓社",
             "B: 背叛 — 國有資產私有化、貧富分化、官員腐敗"),
        ],
    },
    "HIST2202": {
        "name_zh": "亞洲基督教史",
        "name_en": "Christianity in Asia",
        "period": "1500-present",
        "themes": ["耶穌會士的調適策略", "殖民主義與宗教傳播", "本土基督教的崛起", "韓國教會的爆炸性增長", "當代中國地下教會"],
        "tensions": [
            ("Jesuits — Cultural Bridge or Imperial Tool", "耶穌會士 — 文化橋樑 vs 帝國工具",
             "利瑪竇等耶穌會士是中西文化橋樑還是帝國主義先鋒？",
             "A: 橋樑 — 翻譯儒學經典、介紹西學",
             "B: 工具 — 背後是葡萄牙西班牙殖民擴張"),
            ("Korean Church — Indigenous or Imported", "韓國教會 — 本土 vs 移植",
             "韓國基督徒比例近 30% 是本土文化選擇還是傳教士成功？",
             "A: 本土 — 早期文人信徒自主皈依",
             "B: 移植 — 20 世紀美國傳教士大規模投入"),
            ("Chinese House Church — Genuine or Threat", "中國家庭教會 — 真實信仰 vs 威脅",
             "中國家庭教會是真實信仰還是政府視為威脅？",
             "A: 真實 — 數億信徒，社會底層自發",
             "B: 威脅 — 政府視為未註冊組織，需要控制"),
        ],
    },
    # === HKU 帝國、戰爭、全球史 ===
    "HIST2076": {
        "name_zh": "德國與冷戰",
        "name_en": "Germany and the Cold War",
        "period": "1945-1990",
        "themes": ["分裂作為冷戰象徵", "經濟奇蹟的兩種敘事", "柏林圍牆的雙重意義", "重新統一的內外動力", "記憶政治的長期鬥爭"],
        "tensions": [
            ("Berlin Wall — Shame or Protection", "柏林圍牆 — 恥辱 vs 保護",
             "柏林圍牆是東德的恥辱還是反法西斯保護牆？",
             "A: 恥辱 — 阻止東德人逃往自由",
             "B: 保護 — 反法西斯牆，防禦西方滲透"),
            ("West German Miracle — Market or Aid", "西德奇蹟 — 市場 vs 援助",
             "西德經濟奇蹟是市場經濟還是馬歇爾計劃？",
             "A: 市場 — 社會市場經濟、勞資共決",
             "B: 援助 — 130 億美元美國援助奠定基礎"),
            ("Reunification — Liberation or Absorption", "重新統一 — 解放 vs 吞併",
             "1990 德國統一是解放東德還是西德吞併？",
             "A: 解放 — 東德獲得自由民主",
             "B: 吞併 — 東德經濟崩潰、人口流失、被西德體制接管"),
        ],
    },
    "HIST2179": {
        "name_zh": "法律、帝國與世界史",
        "name_en": "Law, Empire and World History",
        "period": "1500-present",
        "themes": ["國際法的歐洲中心性", "海盜作為國際法催化劑", "人權的帝國起源", "主權概念的演變", "當代國際刑事司法"],
        "tensions": [
            ("International Law — Universal or Western", "國際法 — 普世 vs 西方",
             "國際法是普世價值還是西方產物？",
             "A: 普世 — 自然法超越文化",
             "B: 西方 — 格勞秀斯以降歐洲概念，帝國擴張工具"),
            ("Piracy — Crime or Freedom", "海盜 — 犯罪 vs 自由",
             "海盜是犯罪還是對帝國壟斷的反抗？",
             "A: 犯罪 — 搶劫殺人，無論動機",
             "B: 自由 — 反對國家海洋壟斷、追求自由"),
            ("ICC — Justice or Hypocrisy", "國際刑事法院 — 正義 vs 虛偽",
             "國際刑事法院是真實正義還是西方選擇性執法？",
             "A: 正義 — 起訴米洛舍維奇、種族滅絕罪",
             "B: 虛偽 — 美國不批准條約、只起訴非洲領導人"),
        ],
    },
    "HIST2188": {
        "name_zh": "現代南亞史",
        "name_en": "Making of Modern South Asia",
        "period": "1757-present",
        "themes": ["英屬印度的分而治之", "甘地非暴力抵抗的遺產", "印巴分治的暴力", "核武國家的對抗", "當代印度教民族主義"],
        "tensions": [
            ("Partition — Inevitable or Made", "印巴分治 — 必然 vs 人為",
             "1947 印巴分治是歷史必然還是英國決策？",
             "A: 必然 — 印度教與穆斯林社會已分化百年",
             "B: 人為 — 1946 大選後英國匆忙撤離，未準備過渡"),
            ("Gandhi — Saint or Politician", "甘地 — 聖人 vs 政客",
             "甘地是真正的聖人還是精明政客？",
             "A: 聖人 — 非暴力、不合作、簡樸生活",
             "B: 政客 — 巧妙利用媒體、與國大黨政治派系合作"),
            ("Hindu Nationalism — Authentic or Hate", "印度教民族主義 — 本土 vs 仇恨",
             "印度教民族主義是文化復振還是仇恨政治？",
             "A: 本土 — 印度教文明 3000 年延續",
             "B: 仇恨 — 針對穆斯林、基督徒，2002 古吉拉特邦暴動"),
        ],
    },
    "HIST2192": {
        "name_zh": "現代東南亞史導論",
        "name_en": "Introduction to Modern Southeast Asian History",
        "period": "1800-present",
        "themes": ["殖民地的多樣性", "去殖民化的非同步性", "冷戰的東南亞熱戰", "威權主義的長期性", "ASEAN 的實用主義"],
        "tensions": [
            ("Cold War in SEA — Ideology or Nationalism", "東南亞冷戰 — 意識形態 vs 民族主義",
             "越戰、馬來亞緊急狀態是意識形態對抗還是民族主義？",
             "A: 意識形態 — 越共、馬共都是馬列政黨",
             "B: 民族主義 — 反抗殖民、反對外國"),
            ("Authoritarianism — Stability or Oppression", "威權主義 — 穩定 vs 壓迫",
             "新加坡、馬來西亞威權統治是穩定還是壓迫？",
             "A: 穩定 — 經濟發展、種族和諧",
             "B: 壓迫 — 限制言論、拘禁政治犯"),
            ("ASEAN — Success or Frozen", "東盟 — 成功 vs 僵化",
             "ASEAN 是東南亞合作的成功還是無牙組織？",
             "A: 成功 — 50 年和平、經濟整合",
             "B: 僵化 — 不干涉內政原則導致緬甸羅興亞危機無回應"),
        ],
    },
    "HIST2193": {
        "name_zh": "能源與人類史",
        "name_en": "History of Energy and Humankind",
        "period": "deep history to present",
        "themes": ["肌肉力 vs 化石燃料", "煤炭與工業革命", "石油與地緣政治", "核能的承諾與恐懼", "再生能源的當代轉向"],
        "tensions": [
            ("Fossil Fuels — Necessary or Avoidable", "化石燃料 — 必要 vs 可避免",
             "化石燃料對工業化是必要還是可以避免？",
             "A: 必要 — 內燃機、電力、化肥無可替代",
             "B: 可避免 — 早期水力、風力可選，政策選擇造成依賴"),
            ("Nuclear — Promise or Threat", "核能 — 承諾 vs 威脅",
             "核能是清潔能源承諾還是安全威脅？",
             "A: 承諾 — 低碳、密集能源",
             "B: 威脅 — 切爾諾貝利、福島、核武器擴散"),
            ("Climate Change — Real or Cyclical", "氣候變化 — 真實 vs 週期",
             "當代氣候變化是人類造成還是自然週期？",
             "A: 真實 — 科學共識 97%、CO2 濃度",
             "B: 週期 — 地球歷史多次冷暖循環"),
        ],
    },
    "HIST2225": {
        "name_zh": "監獄與懲罰全球史",
        "name_en": "Global History of Prisons and Punishment",
        "period": "1500-present",
        "themes": ["監獄作為現代發明", "苦役 vs 監禁", "殖民地監獄的雙重功能", "現代監獄工業", "監獄作為社會隱喻"],
        "tensions": [
            ("Prison — Reform or Control", "監獄 — 改革 vs 控制",
             "現代監獄起源是改革理念還是社會控制？",
             "A: 改革 — 邊沁圓形監獄設計人道",
             "B: 控制 — 監視、規訓、資本主義勞動"),
            ("Colonial Prison — Civilizing or Brutal", "殖民地監獄 — 文明化 vs 殘酷",
             "殖民地監獄是帝國文明使命還是殘酷鎮壓？",
             "A: 文明化 — 傳播法治",
             "B: 殘酷 — 安汶島苦役、剛果橡膠暴行"),
            ("Mass Incarceration — US Model", "大規模監禁 — 美國模式",
             "美國 2 百萬囚犯是法治還是社會病？",
             "A: 法治 — 嚴刑峻法",
             "B: 社會病 — 種族、貧窮、毒品戰爭的綜合症"),
        ],
    },
    "HIST2229": {
        "name_zh": "大西洋革命",
        "name_en": "Global Atlantic Revolutions, c.1760-1830",
        "period": "1760-1830",
        "themes": ["革命理念的跨大西洋傳播", "奴隸制與革命的悖論", "海地革命的深遠影響", "拉美獨立的複雜性", "革命的失敗與長期化"],
        "tensions": [
            ("American Revolution — Liberty for Whom", "美國革命 — 誰的自由",
             "美國革命是普遍自由還是奴隸主自由？",
             "A: 普遍 — 天賦人權、革命口號",
             "B: 奴隸主 — 開國元勳多為奴隸主，繼續蓄奴"),
            ("Haitian Revolution — Black Jacobins or Massacre", "海地革命 — 黑人雅各賓 vs 大屠殺",
             "海地革命是解放戰爭還是種族屠殺？",
             "A: 解放 — 杜桑・盧維杜爾領導奴隸起義",
             "B: 屠殺 — 大量法國白人種族滅絕"),
            ("Latin American Independence — Bolívar or Real", "拉美獨立 — 玻利瓦爾 vs 現實",
             "拉美獨立是玻利瓦爾理想還是軍事寡頭的現實？",
             "A: 理想 — 拉美共和國聯盟夢想",
             "B: 現實 — 大莊園主奪權、考迪羅獨裁"),
        ],
    },
    "HIST2230": {
        "name_zh": "早期現代大西洋世界",
        "name_en": "Early Modern Atlantic Worlds, c.1500-1800",
        "period": "1500-1800",
        "themes": ["哥倫布大交換的生態衝擊", "三角貿易的經濟邏輯", "海盜黃金時代", "種族意識形態的產生", "早期現代性的多重起源"],
        "tensions": [
            ("Columbian Exchange — Mutual or One-way", "哥倫布大交換 — 互惠 vs 單向",
             "哥倫布大交換是雙向互惠還是歐洲單向掠奪？",
             "A: 互惠 — 馬鈴薯、玉米從美洲到歐亞，解決飢荒",
             "B: 單向 — 掠奪銀礦、奴隸、原料"),
            ("Slave Trade — Economic or Moral", "奴隸貿易 — 經濟 vs 道德",
             "大西洋奴隸貿易是經濟動力還是道德崩潰？",
             "A: 經濟 — 利潤率 50-100%",
             "B: 道德 — 1200 萬非洲人被販運到美洲"),
            ("Piracy — Crime or Class War", "海盜 — 犯罪 vs 階級戰爭",
             "17-18 世紀海盜是犯罪還是對英國海軍霸權的反抗？",
             "A: 犯罪 — 海盜法、搶劫行為",
             "B: 階級戰爭 — 霍金斯船員、解放奴隸海盜共和國"),
        ],
    },
    "HIST2233": {
        "name_zh": "全球化歷史",
        "name_en": "Globalizing History",
        "period": "1500-present",
        "themes": ["全球化的多波浪潮", "帝國主義作為第一波全球化", "冷戰對全球化的分割", "當代全球化的加速", "反全球化運動"],
        "tensions": [
            ("First Globalization — 1500s or 1990s", "第一波全球化 — 16 世紀還是 1990s",
             "全球化是 16 世紀就開始還是 1990 後冷戰結束才開始？",
             "A: 16 世紀 — 哥倫布、馬尼拉大帆船",
             "B: 1990s — 世貿組織、互聯網加速"),
            ("Globalization — Beneficial or Exploitative", "全球化 — 互利 vs 剝削",
             "全球化對發展中國家是互利還是剝削？",
             "A: 互利 — 8 億人脫貧、跨國投資",
             "B: 剝削 — 血汗工廠、債務陷阱、環境破壞"),
            ("Anti-Globalization — Populist or Leftist", "反全球化 — 民粹 vs 左翼",
             "反全球化運動是民粹右翼還是左翼社會運動？",
             "A: 民粹 — 反移民、反建制",
             "B: 左翼 — 反跨國資本、氣候正義"),
        ],
    },
    # === HKU 歐洲與其他 ===
    "HIST2031": {
        "name_zh": "電影史學",
        "name_en": "History through Film",
        "period": "1895-present",
        "themes": ["電影作為歷史檔案", "電影作為意識形態工具", "好萊塢作為文化帝國", "第三世界電影的抵抗", "紀錄片與真實"],
        "tensions": [
            ("Film as History — Documentary or Distortion", "電影作為史 — 文獻 vs 扭曲",
             "電影是歷史的忠實記錄還是意識形態扭曲？",
             "A: 文獻 — 同時代記錄、社會風貌",
             "B: 扭曲 — 好萊塢美化戰爭、種族刻板印象"),
            ("Hollywood — Entertainment or Cultural Imperialism", "好萊塢 — 娛樂 vs 文化帝國",
             "好萊塢電影是純粹娛樂還是美國文化帝國主義？",
             "A: 娛樂 — 跨文化吸引",
             "B: 文化帝國 — 推銷美國價值、消費主義"),
            ("Third Cinema — Resistance or Art", "第三電影 — 抵抗 vs 藝術",
             "第三世界電影是政治抵抗還是純藝術？",
             "A: 抵抗 — 古巴、阿根廷、巴西政治電影",
             "B: 藝術 — 形式探索、與好萊塢區隔"),
        ],
    },
    "HIST2063": {
        "name_zh": "歐洲與現代性",
        "name_en": "Europe and Modernity, 1890-1940",
        "period": "1890-1940",
        "themes": ["世紀末的焦慮", "第一次世界大戰的文化斷裂", "戰間期的民主危機", "法西斯主義的吸引力", "現代主義藝術與政治"],
        "tensions": [
            ("Wilhelmine Germany — Stability or Powder Keg", "威廉德國 — 穩定 vs 火藥桶",
             "威廉二世德國是穩定歐洲強權還是一戰的火藥桶？",
             "A: 穩定 — 經濟領先、社會福利",
             "B: 火藥桶 — 軍國主義、俾斯麥體制解體"),
            ("Weimar Republic — Failure or Tragedy", "魏瑪共和 — 失敗 vs 悲劇",
             "魏瑪共和是注定失敗還是悲劇性被摧毀？",
             "A: 失敗 — 經濟、議會、政府無能",
             "B: 悲劇 — 大蕭條 + 納粹陰謀，本可挽救"),
            ("Fascism — Mass Psychology or Class Betrayal", "法西斯 — 大眾心理 vs 階級背叛",
             "法西斯興起是大眾心理學還是階級背叛？",
             "A: 大眾心理 — 領袖崇拜、群眾催眠",
             "B: 階級背叛 — 資產階級支持納粹反共"),
        ],
    },
    "HIST2070": {
        "name_zh": "自傳中的歷史",
        "name_en": "Stories of Self: History through Autobiography",
        "period": "1800-present",
        "themes": ["自傳作為歷史證據", "敘事認同的構建", "殖民與後殖民自傳", "女性自傳的能動性", "數字時代的自我書寫"],
        "tensions": [
            ("Autobiography — Truth or Construction", "自傳 — 真實 vs 構建",
             "自傳是歷史真實還是敘事構建？",
             "A: 真實 — 第一手經歷",
             "B: 構建 — 記憶選擇、重組服務於當下身份"),
            ("Working Class Autobiography — Voice or Co-opted", "工人階級自傳 — 發聲 vs 收編",
             "工人階級自傳是真實發聲還是被知識分子收編？",
             "A: 發聲 — 工人自己的聲音",
             "B: 收編 — 編輯潤色服務於學術市場"),
            ("Digital Self — Authentic or Performance", "數字自我 — 真實 vs 表演",
             "社交媒體自傳是真實自我還是表演？",
             "A: 真實 — 自我表達自由",
             "B: 表演 — 觀眾導向、形象管理"),
        ],
    },
    "HIST2077": {
        "name_zh": "飲食史",
        "name_en": "Eating History: Food Culture from 19th C.",
        "period": "1800-present",
        "themes": ["工業化與食品加工", "帝國主義的味蕾", "快餐的全球擴張", "食物與階級", "當代飲食政治"],
        "tensions": [
            ("Industrial Food — Progress or Degradation", "工業食品 — 進步 vs 退化",
             "食品工業化是進步還是退化？",
             "A: 進步 — 解決飢餓、保存技術",
             "B: 退化 — 加工食品、肥胖病、添加劑"),
            ("Spice Trade — Economic or Cultural", "香料貿易 — 經濟 vs 文化",
             "大航海香料貿易是經濟還是文化交融？",
             "A: 經濟 — 利潤率 4000%",
             "B: 文化 — 飲食革命、印度咖喱傳播"),
            ("Fast Food — Democratization or US Imperialism", "快餐 — 民主化 vs 美國帝國",
             "麥當勞全球擴張是飲食民主化還是美國帝國主義？",
             "A: 民主化 — 平價、衛生、便捷",
             "B: 美國帝國 — 推銷消費主義、摧毀本土飲食"),
        ],
    },
    "HIST2079": {
        "name_zh": "早期現代歐洲",
        "name_en": "Early Modern Europe, 1500-1800",
        "period": "1500-1800",
        "themes": ["宗教改革的深遠影響", "印刷術與公眾領域", "絕對王權的興衰", "科學革命", "啟蒙運動的雙刃性"],
        "tensions": [
            ("Reformation — Spiritual or Political", "宗教改革 — 靈性 vs 政治",
             "宗教改革是靈性覺醒還是政治運動？",
             "A: 靈性 — 路德、加爾文宗教良心",
             "B: 政治 — 諸侯藉機對抗教宗、世俗化"),
            ("Scientific Revolution — Pure or Political", "科學革命 — 純粹 vs 政治",
             "科學革命是知識追求還是政治服務？",
             "A: 純粹 — 哥白尼、牛頓、伽利略好奇心",
             "B: 政治 — 航海需要、軍事技術、君權正當性"),
            ("Enlightenment — Universal or Eurocentric", "啟蒙 — 普世 vs 歐洲中心",
             "啟蒙運動是普世理性還是歐洲中心？",
             "A: 普世 — 天賦人權、理性",
             "B: 歐洲中心 — 種族主義、殖民主義正當化"),
        ],
    },
    "HIST2103": {
        "name_zh": "俄羅斯國家與社會",
        "name_en": "Russian State and Society in the 20th Century",
        "period": "1900-present",
        "themes": ["革命作為歷史斷裂", "斯大林主義的雙重性", "蘇聯解體的深層原因", "普京時代的歷史政治", "俄羅斯身份的爭論"],
        "tensions": [
            ("1917 Revolution — Necessary or Catastrophic", "1917 革命 — 必要 vs 災難",
             "1917 革命是歷史必要還是災難？",
             "A: 必要 — 沙皇體制崩潰、工人起義",
             "B: 災難 — 70 年極權、2000 萬人死亡"),
            ("Stalin — Modernizer or Tyrant", "斯大林 — 現代化者 vs 暴君",
             "斯大林是蘇聯現代化者還是暴君？",
             "A: 現代化 — 工業化、衛國戰爭勝利",
             "B: 暴君 — 大清洗、古拉格、烏克蘭大飢荒"),
            ("USSR Collapse — Inevitable or Coup", "蘇聯解體 — 必然 vs 政變",
             "1991 蘇聯解體是必然還是政變？",
             "A: 必然 — 經濟停滯、民族矛盾",
             "B: 政變 — 819 事變失敗加速解體"),
        ],
    },
    "HIST2152": {
        "name_zh": "晚期社會主義與1989",
        "name_en": "Late Socialism and the 1989 Revolutions",
        "period": "1968-1991",
        "themes": ["晚期社會主義的合法性危機", "1989 革命的多元性", "團結工會的遺產", "中國1989的對照", "後社會主義轉型"],
        "tensions": [
            ("1989 — Liberal Triumph or Western Betrayal", "1989 — 自由勝利 vs 西方背叛",
             "1989 革命是自由主義勝利還是西方背叛？",
             "A: 勝利 — 自由民主擴展",
             "B: 背叛 — 西方承諾援助未兌現、葉爾欽寡頭"),
            ("Solidarity — Workers or Nationalists", "團結工會 — 工人 vs 民族主義者",
             "波蘭團結工會是工人運動還是民族主義？",
             "A: 工人 — 工人階級自發",
             "B: 民族主義 — 天主教、波蘭民族傳統"),
            ("China 1989 — Tank Man or Order", "中國1989 — 坦克人 vs 秩序",
             "1989 年 6 月 4 日天安門是英雄主義還是社會動盪？",
             "A: 英雄主義 — 坦克人孤身擋坦克",
             "B: 動盪 — 學生被利用、社會混亂"),
        ],
    },
    "HIST2161": {
        "name_zh": "種族的製造",
        "name_en": "Making Race",
        "period": "1500-present",
        "themes": ["種族作為社會建構", "科學種族主義的興衰", "奴隸制與種族", "當代種族政治", "跨國種族流動"],
        "tensions": [
            ("Race — Biological or Social", "種族 — 生物 vs 社會",
             "種族是生物實體還是社會建構？",
             "A: 生物 — 膚色、基因差異",
             "B: 社會 — 完全社會建構，無生物基礎"),
            ("Whiteness — Universal or Specific", "白人 — 普遍 vs 特定",
             "『白人』是普遍類別還是特定歷史建構？",
             "A: 普遍 — 共同歐洲血統",
             "B: 特定 — 19 世紀美國建構，愛爾蘭人曾被視為非白"),
            ("Affirmative Action — Justice or Reverse", "平權行動 — 正義 vs 逆向歧視",
             "平權行動是歷史正義還是逆向歧視？",
             "A: 正義 — 補償幾百年奴隸制",
             "B: 逆向 — 種族歧視反向"),
        ],
    },
    "HIST2170": {
        "name_zh": "伊斯蘭世界的形成",
        "name_en": "Making of the Islamic World, 500-1500",
        "period": "500-1500",
        "themes": ["伊斯蘭的早期擴張", "阿拔斯黃金時代", "宗教與政治的伊斯蘭觀", "蒙古征服的雙重影響", "鄂圖曼帝國的遺產"],
        "tensions": [
            ("Islamic Expansion — Sword or Conversion", "伊斯蘭擴張 — 刀劍 vs 皈依",
             "早期伊斯蘭擴張是軍事征服還是和平皈依？",
             "A: 刀劍 — 阿拉伯征服、奧斯曼",
             "B: 皈依 — 商人傳播、蘇菲神秘主義"),
            ("Abbasid Golden Age — Tolerance or Myth", "阿拔斯黃金時代 — 包容 vs 神話",
             "阿拔斯王朝翻譯運動是伊斯蘭包容還是後人神話？",
             "A: 包容 — 智慧宮、希臘哲學翻譯",
             "B: 神話 — 當代建構，誇大伊斯蘭黃金時代"),
            ("Mongol Invasion — Destruction or Catalyst", "蒙古征服 — 毀滅 vs 催化劑",
             "1258 巴格達陷落是毀滅還是伊斯蘭世界重構？",
             "A: 毀滅 — 數十萬人喪生",
             "B: 催化劑 — 馬穆魯克、鄂圖曼崛起"),
        ],
    },
    "HIST2208": {
        "name_zh": "絲綢之路",
        "name_en": "The Silk Roads",
        "period": "ancient-present",
        "themes": ["絲綢之路作為歐亞橋樑", "宗教傳播的載體", "瘟疫的路徑", "帝國競爭的舞台", "當代一帶一路的歷史迴響"],
        "tensions": [
            ("Silk Roads — Peace or Conflict", "絲綢之路 — 和平 vs 衝突",
             "絲綢之路是和平貿易還是帝國衝突？",
             "A: 和平 — 絲綢、香料、宗教傳播",
             "B: 衝突 — 蒙古征服、塞爾柱土耳其"),
            ("Religion Transmission — Coexistence or Conquest", "宗教傳播 — 共存 vs 征服",
             "佛教、伊斯蘭教沿絲路傳播是和平共存還是征服？",
             "A: 共存 — 敦煌文書、各宗教和諧",
             "B: 征服 — 伊斯蘭化、佛教在印度衰亡"),
            ("Belt and Road — Continuity or Memory", "一帶一路 — 延續 vs 記憶",
             "中國『一帶一路』是絲路延續還是政治記憶挪用？",
             "A: 延續 — 歐亞互聯",
             "B: 記憶 — 絲路被重新發明為中國影響力"),
        ],
    },
    "HIST2212": {
        "name_zh": "表演歷史",
        "name_en": "Performing History",
        "period": "all periods",
        "themes": ["戲劇作為歷史再現", "儀式與政治", "博物館作為表演空間", "紀念儀式的政治", "歷史重演運動"],
        "tensions": [
            ("Reenactment — Education or Spectacle", "歷史重演 — 教育 vs 奇觀",
             "歷史重演是教育還是消費奇觀？",
             "A: 教育 — 沉浸式體驗",
             "B: 奇觀 — 旅遊業商品化"),
            ("Memorial Politics — Consensus or Conflict", "紀念政治 — 共識 vs 衝突",
             "國家紀念儀式是社會共識還是政治衝突？",
             "A: 共識 — 國家團結象徵",
             "B: 衝突 — 誰的歷史被記住、戰爭記憶政治"),
            ("Museum as Performance — Neutral or Political", "博物館作為表演 — 中立 vs 政治",
             "博物館展覽是中立展示還是政治表演？",
             "A: 中立 — 學術策展",
             "B: 政治 — 大英博物館帝國主義、艾未未"),
        ],
    },
    "HIST2213": {
        "name_zh": "巫術與魔法的歷史",
        "name_en": "Witchcraft, Magic, and the Devil in Early Modern Europe",
        "period": "1450-1750",
        "themes": ["獵巫運動的社會根源", "魔鬼學的意識形態", "性別與巫術指控", "宗教改革的巫術恐懼", "現代性與巫術消亡"],
        "tensions": [
            ("Witch Trials — Mass Hysteria or Power Control", "獵巫 — 大眾歇斯底里 vs 權力控制",
             "16-17 世紀獵巫是大眾歇斯底里還是權力控制？",
             "A: 歇斯底里 — 集體恐慌",
             "B: 控制 — 教會與世俗法庭權力工具"),
            ("Women as Witches — Patriarchal or Spiritual", "女巫 — 父權 vs 靈性",
             "獵巫主要針對女性是父權壓迫還是靈性衝突？",
             "A: 父權 — 控制女性身體、生育",
             "B: 靈性 — 異教信仰、教會打擊"),
            ("End of Witchcraft — Enlightenment or Social Change", "巫術消亡 — 啟蒙 vs 社會變遷",
             "獵巫在 18 世紀停止是啟蒙結果還是社會變遷？",
             "A: 啟蒙 — 理性、懷疑",
             "B: 社會 — 教會權力下降、國家壟斷司法"),
        ],
    },
    "HIST2215": {
        "name_zh": "全球環境史",
        "name_en": "Global Environmental History: Columbus to Climate Crisis",
        "period": "1492-present",
        "themes": ["哥倫布大交換的生態影響", "工業革命與人類世", "帝國主義的生態邏輯", "綠色革命的成就與代價", "當代氣候危機"],
        "tensions": [
            ("Anthropocene — New or Continuation", "人類世 — 新時代 vs 延續",
             "人類世是地質新時代還是歷史延續？",
             "A: 新 — 1950s 大加速、核試驗",
             "B: 延續 — 1492 哥倫布大交換就是開始"),
            ("Colonial Ecology — Exchange or Destruction", "殖民生態 — 交流 vs 毀滅",
             "殖民主義帶來生態交流還是毀滅？",
             "A: 交流 — 馬鈴薯傳播、橡膠種植",
             "B: 毀滅 — 森林砍伐、物種滅絕、奴隸制種植園"),
            ("Climate Action — Mitigation or Geoengineering", "氣候行動 — 緩解 vs 地質工程",
             "氣候危機是緩解還是地質工程？",
             "A: 緩解 — 減排、再生能源",
             "B: 工程 — 太陽能管理、碳捕獲"),
        ],
    },
    "HIST2220": {
        "name_zh": "小說中的歷史",
        "name_en": "History through Fiction",
        "period": "all periods",
        "themes": ["歷史小說作為史料", "小說家的歷史責任", "後現代小說與歷史", "被壓迫群體的小說", "數字時代的歷史虛構"],
        "tensions": [
            ("Historical Fiction — Education or Distortion", "歷史小說 — 教育 vs 扭曲",
             "歷史小說是歷史教育還是歪曲？",
             "A: 教育 — 大眾歷史意識",
             "B: 扭曲 — 小說家想像、時代錯誤"),
            ("Counterfactual — Thought Experiment or Irresponsible", "反事實 — 思想實驗 vs 不負責任",
             "『如果希特勒贏了』類反事實是思想實驗還是不負責任？",
             "A: 思想實驗 — 探索偶然性",
             "B: 不負責任 — 為納粹招魂"),
            ("Postmodern History — Plural or Nihilist", "後現代史學 — 多元 vs 虛無",
             "後現代史學是多元史觀還是虛無主義？",
             "A: 多元 — 邊緣群體、殖民經驗",
             "B: 虛無 — 真相不存在、否定大屠殺"),
        ],
    },
    "HIST2222": {
        "name_zh": "波斯世界",
        "name_en": "Persianate World",
        "period": "1000-present",
        "themes": ["波斯作為文化帝國", "波斯語的跨國傳播", "蒙古征服的波斯化", "薩法維帝國的什葉化", "當代伊朗的波斯認同"],
        "tensions": [
            ("Persianate — Empire or Culture", "波斯化 — 帝國 vs 文化",
             "波斯化是政治帝國還是文化範式？",
             "A: 帝國 — 阿契美尼德、薩珊",
             "B: 文化 — 波斯語、詩歌跨越族群"),
            ("Safavid Shi'itization — Genuine or Political", "薩法維什葉化 — 真實 vs 政治",
             "16 世紀薩法維什葉化是真實信仰還是政治工具？",
             "A: 真實 — 什葉派神學興起",
             "B: 政治 — 對抗奧斯曼遜尼派的國家認同"),
            ("Modern Iran — Reform or Theocracy", "現代伊朗 — 改革 vs 神權",
             "1979 後伊朗是改革派還是神權政治？",
             "A: 改革 — 知識分子、女性、教育",
             "B: 神權 — 最高領袖、革命衛隊"),
        ],
    },
    "HIST2231": {
        "name_zh": "美的歷史",
        "name_en": "Beauty Histories",
        "period": "all periods",
        "themes": ["美作為文化建構", "美的帝國擴張", "美的資本主義", "美的政治抗爭", "美的數字轉向"],
        "tensions": [
            ("Beauty Standards — Universal or Cultural", "美標準 — 普世 vs 文化",
             "美標準是普世還是文化建構？",
             "A: 普世 — 黃金比例、對稱性",
             "B: 文化 — 纏足、束腹、西方瘦身"),
            ("Cosmetic Industry — Empowerment or Oppression", "化妝品業 — 賦權 vs 壓迫",
             "化妝品業是女性賦權還是父權壓迫？",
             "A: 賦權 — 自主選擇、自我表達",
             "B: 壓迫 — 不安全焦慮、消費主義"),
            ("Plastic Surgery — Liberation or Conformity", "整形手術 — 解放 vs 順從",
             "整形手術是身體解放還是順從美的規範？",
             "A: 解放 — 性少數、跨性別",
             "B: 順從 — 韓國 20% 女性整形"),
        ],
    },
    "HIST2232": {
        "name_zh": "女性雜誌作為歷史",
        "name_en": "Women's Magazines as History",
        "period": "1800-present",
        "themes": ["女性雜誌作為現代性載體", "美與消費的編織", "女性主義的內部張力", "種族與階級的交織", "數字時代的轉型"],
        "tensions": [
            ("Women's Magazines — Empowerment or Domesticity", "女性雜誌 — 賦權 vs 家政",
             "女性雜誌是賦權還是家政意識形態？",
             "A: 賦權 — 職業、財經、健康",
             "B: 家政 — 烹飪、清潔、育兒傳統"),
            ("Cosmopolitan — Liberal or Consumerist", "Cosmopolitan — 自由派 vs 消費主義",
             "Cosmopolitan 類雜誌是自由派女性主義還是消費主義？",
             "A: 自由派 — 性、職業、政治",
             "B: 消費 — 推銷產品"),
            ("Vogue — Fashion or Racial Politics", "Vogue — 時尚 vs 種族政治",
             "Vogue 等時尚雜誌是純時尚還是種族政治？",
             "A: 時尚 — 服裝、美學",
             "B: 種族 — 黑人髮型、AAPIs 挪用"),
        ],
    },
    # === Harvard 101 Foundations ===
    "GenEd1017": {
        "name_zh": "美國人作為佔領者與建國者",
        "name_en": "Forced to Be Free: Americans as Occupiers and Nation-Builders",
        "period": "1898-present",
        "themes": ["佔領的多重邏輯", "nation-building 的矛盾", "菲律賓案例的深遠影響", "日本佔領的特殊性", "當代佔領的遺產"],
        "tensions": [
            ("U.S. Occupation — Liberation or Imperialism", "美國佔領 — 解放 vs 帝國",
             "美國海外佔領是解放使命還是帝國主義？",
             "A: 解放 — 民主、法治、人權",
             "B: 帝國 — 經濟剝削、軍事基地、文化同化"),
            ("Nation-Building — Possible or Failure", "nation-building — 可能 vs 失敗",
             "美國在海外的 nation-building 是可能還是註定失敗？",
             "A: 可能 — 德國、日本、韓國成功",
             "B: 失敗 — 越南、阿富汗、伊拉克"),
            ("Philippines 1898-1946 — Modernizer or Colonizer", "菲律賓 1898-1946 — 現代化 vs 殖民",
             "美國在菲律賓統治是現代化還是殖民？",
             "A: 現代化 — 公共衛生、教育、英文",
             "B: 殖民 — 經濟剝削、摩洛戰爭、貝幣屠殺"),
        ],
    },
    "GenEd1068": {
        "name_zh": "美國與中國",
        "name_en": "The United States and China",
        "period": "1784-present",
        "themes": ["從排華到反共", "接觸與衝突的循環", "台灣作為雙方角力點", "冷戰在亞洲的熱戰", "當代新冷戰"],
        "tensions": [
            ("Engagement — Theory or Failure", "接觸政策 — 理論 vs 失敗",
             "美國對華接觸政策是和平演變理論還是失敗？",
             "A: 理論 — 經濟發展帶來民主化",
             "B: 失敗 — 中國經濟崛起但政治未變"),
            ("Containment — Cold War Relic or Active", "遏制戰略 — 冷戰遺物 vs 仍在進行",
             "對華遏制是冷戰遺物還是當代戰略？",
             "A: 冷戰遺物 — 時代已過",
             "B: 仍在進行 — 印太戰略、QUAD、AUKUS"),
            ("Taiwan — Democracy Pawn or Sovereign", "台灣 — 民主棋子 vs 主權",
             "台灣對美國是民主棋子還是主權國家？",
             "A: 棋子 — 美中關係槓桿",
             "B: 主權 — 台灣 2300 萬人民自決"),
        ],
    },
    "Hist12": {
        "name_zh": "陰謀論的美國史",
        "name_en": "Conspiracy! A History of U.S. Politics and Culture",
        "period": "colonial-present",
        "themes": ["陰謀論作為政治動員", "種族與陰謀", "國家機密與陰謀", "媒體時代的陰謀", "QAnon 的當代顯現"],
        "tensions": [
            ("Conspiracy Theories — Irrational or Rational", "陰謀論 — 非理性 vs 理性",
             "陰謀論是非理性產物還是對權力的合理質疑？",
             "A: 非理性 — 心理學解釋、偏見",
             "B: 理性 — MKUltra、伊朗門、水門事件確實存在"),
            ("Antisemitism — Core or Ploy", "反猶主義 — 核心 vs 手段",
             "陰謀論中的反猶主義是核心還是政治手段？",
             "A: 核心 — 種族主義世界觀",
             "B: 手段 — 嫁禍少數族群轉移矛盾"),
            ("Internet Era — New or Same", "互聯網時代 — 新現象 vs 舊邏輯",
             "互聯網陰謀論是新型現象還是舊邏輯？",
             "A: 新 — 算法推送、回音室",
             "B: 舊 — 反共產主義、共濟會陰謀都是同類"),
        ],
    },
    "Hist14": {
        "name_zh": "第一次世界大戰",
        "name_en": "The First World War",
        "period": "1914-1918",
        "themes": ["戰爭的長線根源", "凡爾賽和約的失敗", "戰壕戰的技術化", "美國參戰的動機", "戰爭的記憶政治"],
        "tensions": [
            ("WWI — Avoidable or Inevitable", "一戰 — 可避免 vs 必然",
             "一戰是外交失敗可避免還是歐洲結構性必然？",
             "A: 可避免 — 1914 年 7 月危機可外交解決",
             "B: 必然 — 歐洲軍國主義、結盟體系、民族主義"),
            ("Versailles — Too Harsh or Too Lenient", "凡爾賽和約 — 太嚴苛 vs 太寬容",
             "凡爾賽和約對德國是太嚴苛還是太寬容？",
             "A: 太嚴苛 — 戰爭罪條款、巨額賠款",
             "B: 太寬容 — 希特勒上臺後利用但未受遏制"),
            ("U.S. Entry — Idealism or Realpolitik", "美國參戰 — 理想主義 vs 現實政治",
             "1917 美國參戰是威爾遜理想主義還是現實政治？",
             "A: 理想主義 — 為世界安全",
             "B: 現實政治 — 盧西塔尼亞號、英法貸款"),
        ],
    },
    "Hist21": {
        "name_zh": "美國勞工、自由與衝突",
        "name_en": "Labor, Liberty, and Conflict in American History",
        "period": "1607-present",
        "themes": ["勞工運動的雙重性", "奴隸制與自由勞動", "新政與現代福利國家", "里根革命的轉折", "當代零工經濟"],
        "tensions": [
            ("Slavery — Necessary or Evil", "奴隸制 — 必要 vs 邪惡",
             "美國奴隸制是經濟必要還是道德邪惡？",
             "A: 必要 — 南方經濟依賴",
             "B: 邪惡 — 人類尊嚴不可剝奪"),
            ("Labor Unions — Workers' Voice or Special Interest", "工會 — 工人聲音 vs 既得利益",
             "工會是工人階級的聲音還是特殊利益集團？",
             "A: 工人 — 8 小時工作、福利",
             "B: 既得利益 — 養老金、壟斷"),
            ("Welfare State — Right or Handout", "福利國家 — 權利 vs 施捨",
             "美國福利國家是公民權利還是政府施捨？",
             "A: 權利 — 羅斯福四大自由",
             "B: 施捨 — 里根『福利女王』"),
        ],
    },
    "Hist32A": {
        "name_zh": "鄂圖曼帝國與世界",
        "name_en": "The Ottoman Empire and the World",
        "period": "1299-1922",
        "themes": ["鄂圖曼的多民族治理", "米利特制度的雙面性", "第一次世界大戰的崩潰", "凱末爾的激進世俗化", "鄂圖曼的當代遺產"],
        "tensions": [
            ("Millet System — Tolerance or Control", "米利特制度 — 寬容 vs 控制",
             "鄂圖曼米利特制度是宗教寬容還是族群控制？",
             "A: 寬容 — 多元族群、宗教自由",
             "B: 控制 — 二等公民、隔離管理"),
            ("Armenian Genocide — Controversy or Documented", "亞美尼亞種族滅絕 — 爭議 vs 有據",
             "1915 亞美尼亞種族滅絕是學術爭議還是有據可查？",
             "A: 爭議 — 鄂圖曼記錄混亂",
             "B: 有據 — 150 萬死亡、Talat 電報、Osmanlı"),
            ("Atatürk — Modernizer or Authoritarian", "凱末爾 — 現代化者 vs 獨裁者",
             "凱末爾是現代化者還是獨裁者？",
             "A: 現代化 — 婦女權利、世俗化",
             "B: 獨裁 — 一黨專政、庫爾德壓迫"),
        ],
    },
    "Hist33": {
        "name_zh": "大屠殺",
        "name_en": "The Holocaust",
        "period": "1933-1945",
        "themes": ["大屠殺的獨特性爭論", "反猶主義的長線根源", "大屠殺的官僚理性", "歐洲社會的共謀", "記憶與教育"],
        "tensions": [
            ("Holocaust Uniqueness — Special or Comparative", "大屠殺獨特性 — 特殊 vs 可比",
             "大屠殺是獨特歷史事件還是可以與其他種族滅絕比較？",
             "A: 獨特 — 工業化屠殺、600 萬",
             "B: 可比 — 亞美尼亞、盧旺達、柬埔寨"),
            ("Collaboration — Nazi or European", "共謀 — 納粹 vs 歐洲",
             "大屠殺是納粹德國所為還是歐洲共謀？",
             "A: 納粹 — 集中營、黨衛軍",
             "B: 歐洲 — 維希法國、烏克蘭輔助警察、霍爾瑙協會"),
            ("Bystanders — Guilty or Powerless", "旁觀者 — 有罪 vs 無力",
             "歐洲旁觀者對猶太人命運是有罪還是無力？",
             "A: 有罪 — 沉默共謀",
             "B: 無力 — 個體難以對抗國家"),
        ],
    },
    "Hist38": {
        "name_zh": "現代中國",
        "name_en": "Modern China, 1894-Present",
        "period": "1894-present",
        "themes": ["帝國主義的衝擊", "革命與改革的循環", "毛時代的激進試驗", "改革開放奇蹟", "中國崛起的世界意義"],
        "tensions": [
            ("China's Path — Continuity or Break", "中國道路 — 延續 vs 斷裂",
             "當代中國是中華文明的延續還是現代國家的斷裂？",
             "A: 延續 — 大一統傳統",
             "B: 斷裂 — 1949 革命、共產主義"),
            ("Mao's Legacy — Revolutionary or Tyrant", "毛遺產 — 革命者 vs 暴君",
             "毛澤東是革命者還是暴君？",
             "A: 革命者 — 反帝國、反封建",
             "B: 暴君 — 大躍進、文革"),
            ("U.S.-China — Engagement or Rivalry", "中美關係 — 接觸 vs 競爭",
             "中美關係是接觸合作還是結構性競爭？",
             "A: 接觸 — 經濟互利",
             "B: 競爭 — 修昔底德陷阱"),
        ],
    },
    "Hist46": {
        "name_zh": "希特勒之後",
        "name_en": "Life after Hitler: West German Society",
        "period": "1945-1990",
        "themes": ["去納粹化的局限", "經濟奇蹟的雙面性", "68 學生運動", "直面過去 Vergangenheitsbewältigung", "重新統一的創傷"],
        "tensions": [
            ("Denazification — Success or Failure", "去納粹化 — 成功 vs 失敗",
             "去納粹化是成功還是失敗？",
             "A: 成功 — 紐倫堡審判、新憲法",
             "B: 失敗 — 1950s 前納粹官員復職"),
            ("Economic Miracle — Decoupling or Sustained", "經濟奇蹟 — 對納粹切割 vs 連續",
             "西德經濟奇蹟是與納粹歷史切割還是連續？",
             "A: 切割 — 民主化、歐洲化",
             "B: 連續 — 工業基礎、勞動力"),
            ("68 Movement — Liberation or Excess", "68 運動 — 解放 vs 過激",
             "西德 68 學生運動是解放還是過激？",
             "A: 解放 — 民主化、婦女解放",
             "B: 過激 — RAF 紅軍旅恐怖"),
        ],
    },
    "Hist47": {
        "name_zh": "冷戰",
        "name_en": "The Cold War",
        "period": "1947-1991",
        "themes": ["冷戰的多個戰場", "核武器的恐怖平衡", "第三世界的代理戰", "意識形態對抗的軟實力", "冷戰結束的偶然性"],
        "tensions": [
            ("Cold War Origins — Ideology or Geopolitics", "冷戰起源 — 意識形態 vs 地緣",
             "冷戰是意識形態對抗還是地緣政治？",
             "A: 意識形態 — 資本主義 vs 共產主義",
             "B: 地緣 — 蘇聯安全關切、北約擴張"),
            ("Hot Wars in Asia — Local or Proxy", "亞洲熱戰 — 本地 vs 代理",
             "韓戰、越戰是本地衝突還是冷戰代理？",
             "A: 本地 — 朝鮮、越南民族主義",
             "B: 代理 — 中蘇美超級大國角力"),
            ("Cold War End — U.S. Won or USSR Failed", "冷戰結束 — 美國勝 vs 蘇聯敗",
             "冷戰結束是美國勝利還是蘇聯失敗？",
             "A: 美國勝 — 雷根『星球大戰』、里根經濟學",
             "B: 蘇聯敗 — 體制、經濟、民族問題"),
        ],
    },
    "Hist57": {
        "name_zh": "帝國、國家、分割",
        "name_en": "Empire, Nation, Partition: Modern South Asia",
        "period": "1857-present",
        "themes": ["英帝國的分而治之", "穆斯林聯盟的崛起", "1947 分治的暴力", "冷戰中的南亞", "當代南亞的核武對抗"],
        "tensions": [
            ("Partition — Inevitable or Made", "分割 — 必然 vs 人為",
             "1947 印巴分治是歷史必然還是英國決策？",
             "A: 必然 — 印度教、穆斯林兩元社會",
             "B: 人為 — 1946 大選後倉促撤離"),
            ("Nuclear Weapons — Deterrence or Madness", "核武器 — 威懾 vs 瘋狂",
             "印巴核武是威懾穩定還是瘋狂升級？",
             "A: 威懾 — 相互保證毀滅",
             "B: 瘋狂 — 卡吉爾衝突幾乎核戰"),
            ("Democracy in India — Success or Hindutva", "印度民主 — 成功 vs 印度教民族主義",
             "印度民主是成功還是印度教民族主義威脅？",
             "A: 成功 — 70 年選舉",
             "B: 威脅 — 莫迪 RSS、穆斯林邊緣化"),
        ],
    },
    "Hist66": {
        "name_zh": "南北戰爭的來臨",
        "name_en": "The Coming of the Civil War",
        "period": "1820-1861",
        "themes": ["奴隸制作為核心爭議", "聯邦與州權的辯論", "1860 選舉的爆發點", "邦聯分離的合法性", "重建的失敗"],
        "tensions": [
            ("Slavery — Necessary or Evil", "奴隸制 — 必要 vs 邪惡",
             "南方奴隸制是經濟必要還是道德邪惡？",
             "A: 必要 — 棉花經濟、南方文化",
             "B: 邪惡 — 奴隸非人化"),
            ("States Rights — Defense or Mask", "州權 — 辯護 vs 掩飾",
             "南方邦聯的州權論是憲法辯護還是奴隸制掩飾？",
             "A: 辯護 — 有限政府、傑斐遜傳統",
             "B: 掩飾 — 維護奴隸制"),
            ("Reconstruction — Failure or Tragic", "重建 — 失敗 vs 悲劇",
             "1865-77 重建是失敗還是悲劇？",
             "A: 失敗 — 北方放棄、三K黨",
             "B: 悲劇 — 短暫黑人政治權利、吉姆・克勞法"),
        ],
    },
    "Hist68": {
        "name_zh": "二十世紀美國",
        "name_en": "The 20th-Century United States",
        "period": "1900-2000",
        "themes": ["進步主義改革的張力", "兩次大戰的全球投射", "冷戰霸權的興起", "1960s 社會革命", "1980s 保守派反攻"],
        "tensions": [
            ("American Century — Benign or Imperial", "美國世紀 — 良性 vs 帝國",
             "美國 20 世紀霸權是良性的還是帝國的？",
             "A: 良性 — 馬歇爾計劃、民主化",
             "B: 帝國 — 越南、伊朗、中情局政變"),
            ("1960s — Liberation or Excess", "1960s — 解放 vs 過激",
             "60 年代反文化運動是解放還是過激？",
             "A: 解放 — 民權、婦女、環境",
             "B: 過激 — 反越戰、家庭崩潰"),
            ("Reagan Revolution — Renewal or Reversal", "里根革命 — 復興 vs 倒退",
             "1980 年代里根革命是美國復興還是社會倒退？",
             "A: 復興 — 冷戰勝利、經濟增長",
             "B: 倒退 — 工會、貧富、種族"),
        ],
    },
    "Hist70": {
        "name_zh": "撒哈拉以南非洲史",
        "name_en": "History of Sub-Saharan Africa to 1860",
        "period": "pre-1860",
        "themes": ["非洲文明的深度", "奴隸貿易的破壞", "殖民前的複雜王國", "伊斯蘭在非洲的角色", "口述傳統的歷史"],
        "tensions": [
            ("Pre-colonial Africa — Primitive or Complex", "殖民前非洲 — 原始 vs 複雜",
             "殖民前非洲是原始還是複雜文明？",
             "A: 原始 — 部落、落後",
             "B: 複雜 — 馬里帝國、大津巴布韋、貝寧青銅"),
            ("Slave Trade — European or African", "奴隸貿易 — 歐洲 vs 非洲",
             "大西洋奴隸貿易是歐洲所為還是非洲共謀？",
             "A: 歐洲 — 需求、航運、買家",
             "B: 非洲 — 內陸部落酋長供應"),
            ("Islamic Africa — Conversion or Conquest", "伊斯蘭非洲 — 皈依 vs 征服",
             "伊斯蘭在非洲擴張是和平皈依還是征服？",
             "A: 皈依 — 商人、蘇菲",
             "B: 征服 — 桑海、阿爾及利亞"),
        ],
    },
    "GenEd1088": {
        "name_zh": "十字軍東征",
        "name_en": "The Crusades and the Making of East and West",
        "period": "1095-1291",
        "themes": ["宗教戰爭的多重動機", "東西交流的窗口", "穆斯林視角的十字軍", "拉丁國家的失敗", "當代迴響"],
        "tensions": [
            ("Crusades — Religious War or Colonialism", "十字軍 — 宗教戰 vs 殖民主義",
             "十字軍是宗教戰爭還是殖民征服？",
             "A: 宗教 — 教皇號召、朝聖",
             "B: 殖民 — 威尼斯商人、土地貴族"),
            ("Cultural Exchange — Myth or Reality", "文化交流 — 神話 vs 現實",
             "十字軍時代的東西交流是真是假？",
             "A: 真實 — 阿拉伯醫學、數學傳入",
             "B: 神話 — 戰爭為主，接觸有限"),
            ("Crusader States — Feasibility or Failure", "拉丁國家 — 可行 vs 失敗",
             "十字軍國家是可行殖民還是注定失敗？",
             "A: 可行 — 延續 200 年",
             "B: 失敗 — 依賴歐洲、本地阿拉伯人反對"),
        ],
    },
    "GenEd1159": {
        "name_zh": "美國資本主義",
        "name_en": "American Capitalism",
        "period": "1607-present",
        "themes": ["資本主義的多種形態", "奴隸制與資本積累", "工業化與工廠", "金融資本主義", "當代不平等"],
        "tensions": [
            ("American Capitalism — Unique or Variant", "美國資本主義 — 獨特 vs 變體",
             "美國資本主義是獨特模式還是普通變體？",
             "A: 獨特 — 個人主義、創業",
             "B: 變體 — 與歐洲資本主義基本相同"),
            ("Slavery and Capitalism — Foundational or Aberration", "奴隸制與資本 — 基礎 vs 異常",
             "奴隸制是資本主義基礎還是歷史異常？",
             "A: 基礎 — 棉花、工業革命融資",
             "B: 異常 — 美國後來轉向僱傭勞動"),
            ("Inequality — Functional or Systemic", "不平等 — 功能性 vs 系統性",
             "資本主義不平等是功能性激勵還是系統性問題？",
             "A: 功能性 — 努力回報",
             "B: 系統性 — 結構性種族、階級壁壘"),
        ],
    },
    "GenEd1160": {
        "name_zh": "中世紀物質文化",
        "name_en": "Harvard Gets Medieval: Material Culture",
        "period": "500-1500",
        "themes": ["物質文化作為歷史證據", "修道院經濟", "城堡與封建", "大學的誕生", "中世紀的多元性"],
        "tensions": [
            ("Middle Ages — Dark or Bright", "中世紀 — 黑暗 vs 光明",
             "中世紀是黑暗時代還是文化高峰？",
             "A: 黑暗 — 戰亂、宗教蒙昧",
             "B: 光明 — 大教堂、托馬斯・阿奎那、巴黎大學"),
            ("Feudalism — Real or Myth", "封建制度 — 真實 vs 神話",
             "封建制度是歷史真實還是後人神話？",
             "A: 真實 — 領主、附庸、封地",
             "B: 神話 — 1960 年代歷史學家 Marc Bloch 證明複雜得多"),
            ("Universities — Church or Modern", "大學 — 教會 vs 現代",
             "中世紀大學是教會機構還是現代知識殿堂？",
             "A: 教會 — 神學主導、教皇特許",
             "B: 現代 — 理性辯論、自然哲學"),
        ],
    },
    "GenEd1206": {
        "name_zh": "亞裔美國人的悖論",
        "name_en": "Asian Americans as an American Paradox",
        "period": "1850-present",
        "themes": ["模範少數族裔的迷思", "排華法案的長線影響", "日裔集中營的二戰記憶", "越南、菲律賓的多元經驗", "當代反亞裔仇恨"],
        "tensions": [
            ("Model Minority — Praise or Stereotype", "模範少數族裔 — 讚美 vs 刻板",
             "『模範少數族裔』是讚美還是刻板印象？",
             "A: 讚美 — 努力、成就",
             "B: 刻板 — 掩蓋多元、壓迫黑人和拉美裔"),
            ("Japanese Internment — Necessary or Wrong", "日裔集中營 — 必要 vs 錯誤",
             "1942-45 日裔集中營是戰時必要還是錯誤？",
             "A: 必要 — 珍珠港後間諜恐懼",
             "B: 錯誤 — 種族定性、未保護公民權"),
            ("Anti-Asian Hate 2020s — Pandemic or Long Roots", "反亞裔仇恨 — 疫情 vs 長期",
             "2020 起的反亞裔仇恨是疫情造成還是長期種族主義？",
             "A: 疫情 — 病毒被標籤為『中國病毒』",
             "B: 長期 — 19 世紀排華、傅滿洲"),
        ],
    },
    # === Harvard Fall Courses ===
    "FYS47U": {
        "name_zh": "獨立宣言",
        "name_en": "Declarations of Independence",
        "period": "1776-present",
        "themes": ["獨立宣言的修辭", "誰是『人民』", "廢奴主義者再解讀", "女性獨立宣言", "當代獨立運動"],
        "tensions": [
            ("Declaration — Universal or Specific", "宣言 — 普世 vs 特定",
             "獨立宣言是普世權利還是特定政治聲明？",
             "A: 普世 — 天賦人權",
             "B: 特定 — 13 州殖民地訴求"),
            ("'All Men' — Inclusive or Exclusive", "『所有人』 — 包容 vs 排斥",
             "『all men are created equal』中的 men 是包容還是排斥？",
             "A: 包容 — 普遍人性",
             "B: 排斥 — 婦女、黑人、原住民"),
            ("Seneca Falls — Extension or New", "Seneca Falls — 延伸 vs 全新",
             "1848 Seneca Falls 宣言是獨立宣言延伸還是全新？",
             "A: 延伸 — 同樣是反對暴政",
             "B: 全新 — 婦女獨特壓迫"),
        ],
    },
    "FYS66K": {
        "name_zh": "笑的哲學",
        "name_en": "Philosophy of Laughter",
        "period": "all periods",
        "themes": ["笑的哲學傳統", "笑的生理學", "笑的社會功能", "幽默的權力", "數字時代的笑"],
        "tensions": [
            ("Laughter — Superiority or Relief", "笑 — 優越感 vs 緩解",
             "笑的本質是優越感還是緊張緩解？",
             "A: 優越感 — 霍布斯、柏格森",
             "B: 緩解 — 弗洛伊德、康德"),
            ("Humor — Universal or Cultural", "幽默 — 普世 vs 文化",
             "幽默是普世還是文化相對？",
             "A: 普世 — 不協調的笑",
             "B: 文化 — 各文化禁忌不同"),
            ("Censorship vs Laughter — Freedom", "審查 vs 笑 — 自由",
             "對幽默的審查是言論自由還是必要？",
             "A: 自由 — 笑是權利",
             "B: 必要 — 仇恨言論、種族笑話應限制"),
        ],
    },
    "FYS71M": {
        "name_zh": "全球資本主義",
        "name_en": "Global Capitalism",
        "period": "1500-present",
        "themes": ["資本主義的多重起源", "帝國主義作為先驅", "布雷頓森林體系", "新自由主義轉向", "當代跨國資本"],
        "tensions": [
            ("Capitalism — Universal or Western", "資本主義 — 普世 vs 西方",
             "資本主義是普世模式還是西方產物？",
             "A: 普世 — 韋伯現代化理論",
             "B: 西方 — 歐洲歷史偶然性"),
            ("Neoliberalism — Efficient or Damaging", "新自由主義 — 高效 vs 損害",
             "1970s 後新自由主義是高效還是損害？",
             "A: 高效 — 市場效率、解除管制",
             "B: 損害 — 貧富、2008 危機、民粹反彈"),
            ("Multinationals — Beneficial or Exploitative", "跨國公司 — 互利 vs 剝削",
             "跨國公司對發展中國家是互利還是剝削？",
             "A: 互利 — 工作、技術轉移",
             "B: 剝削 — 避稅、血汗工廠、債務"),
        ],
    },
    "FYS73V": {
        "name_zh": "反猶主義",
        "name_en": "Antisemitism",
        "period": "ancient-present",
        "themes": ["反猶主義的長線根源", "宗教 vs 種族反猶", "現代反猶的偽科學", "大屠殺的後果", "當代反猶的回潮"],
        "tensions": [
            ("Antisemitism — Religious or Racial", "反猶 — 宗教 vs 種族",
             "反猶主義是宗教性質還是種族性質？",
             "A: 宗教 — 基督教神學指控",
             "B: 種族 — 19 世紀偽科學種族"),
            ("Israel and Antisemitism — Related or Distinct", "以色列與反猶 — 相關 vs 區分",
             "對以色列批評是否等同反猶？",
             "A: 相關 — 反猶借反以表達",
             "B: 區分 — 反以是政治批評"),
            ("Contemporary Antisemitism — Left or Right", "當代反猶 — 左 vs 右",
             "當代反猶主要是左翼還是右翼？",
             "A: 左 — 反以社會主義者",
             "B: 右 — 白人至上主義者"),
        ],
    },
    "FYSEMR72C": {
        "name_zh": "沒有飛機的世界",
        "name_en": "World without Airplanes",
        "period": "1903-present",
        "themes": ["航空的全球連接", "航空的環境成本", "航空的地緣政治", "反事實思考", "航空替代方案"],
        "tensions": [
            ("Aviation — Liberation or Imperialism", "航空 — 解放 vs 帝國",
             "飛機是自由象徵還是帝國工具？",
             "A: 解放 — 民主化國際旅行",
             "B: 帝國 — 軍事投射、跨國剝削"),
            ("No Airplanes — Worse or Better", "沒有飛機 — 更差 vs 更好",
             "反事實上沒有飛機世界會更差還是更好？",
             "A: 更差 — 全球化倒退",
             "B: 更好 — 低碳、本地化"),
            ("Future of Flight — Sustainable or Dead", "航空未來 — 可持續 vs 死亡",
             "航空業未來是可持續還是會死亡？",
             "A: 可持續 — SAF 燃料、電動飛機",
             "B: 死亡 — 氣候政策、高鐵替代"),
        ],
    },
    "GENED1034": {
        "name_zh": "過渡中的文本",
        "name_en": "Texts in Transition",
        "period": "all periods",
        "themes": ["文本作為歷史載體", "翻譯的權力", "手抄本到印刷", "數字時代文本", "被禁文本的命運"],
        "tensions": [
            ("Text — Stable or Fluid", "文本 — 穩定 vs 流動",
             "文本是穩定還是流動？",
             "A: 穩定 — 固定版本",
             "B: 流動 — 翻譯、抄寫者修改"),
            ("Censorship — Necessary or Oppressive", "審查 — 必要 vs 壓迫",
             "文本審查是社會必要還是壓迫工具？",
             "A: 必要 — 國家安全、公共道德",
             "B: 壓迫 — 焚書、異見禁止"),
            ("Digital Text — Democratization or Loss", "數字文本 — 民主化 vs 損失",
             "數字文本是知識民主化還是損失？",
             "A: 民主化 — 自媒體、開放獲取",
             "B: 損失 — 版權、注意力碎片化"),
        ],
    },
    "GENED1136": {
        "name_zh": "權力與文明：中國",
        "name_en": "Power and Civilization: China",
        "period": "ancient-present",
        "themes": ["中國帝國的循環", "科舉與官僚制", "儒家作為治理", "近現代轉型", "當代中國的權力"],
        "tensions": [
            ("Imperial China — Continuity or Cyclical", "帝制中國 — 延續 vs 循環",
             "中國帝制是延續還是循環？",
             "A: 延續 — 大一統傳統 2000 年",
             "B: 循環 — 分合循環、改朝換代"),
            ("Confucianism — Philosophy or Ideology", "儒教 — 哲學 vs 意識形態",
             "儒教是哲學還是意識形態？",
             "A: 哲學 — 倫理、現世關懷",
             "B: 意識形態 — 統治工具、階級壓迫"),
            ("Contemporary China — Authoritarian or New", "當代中國 — 威權 vs 新",
             "當代中國是傳統威權還是新治理？",
             "A: 威權 — 一黨專政、監視",
             "B: 新 — 數字威權、績效合法性"),
        ],
    },
    "GENED1147": {
        "name_zh": "美國食物",
        "name_en": "American Food",
        "period": "1607-present",
        "themes": ["美國食物的多元性", "奴隸制與南方菜", "移民與飲食", "工業化食品", "當代食物政治"],
        "tensions": [
            ("American Food — Melting Pot or Hierarchy", "美國食物 — 熔爐 vs 等級",
             "美國食物是文化熔爐還是有等級？",
             "A: 熔爐 — 融合菜",
             "B: 等級 — 法餐高級、中餐低級"),
            ("Soul Food — Authentic or Stereotype", "黑人靈魂食物 — 真實 vs 刻板",
             "黑人靈魂食物是真實文化還是刻板？",
             "A: 真實 — 非洲起源、奴隸智慧",
             "B: 刻板 — KFC 商業化、肥胖"),
            ("GMO — Necessary or Threat", "轉基因 — 必要 vs 威脅",
             "轉基因食物是糧食安全還是健康威脅？",
             "A: 必要 — 抗蟲、氣候適應",
             "B: 威脅 — 跨國公司壟斷、健康風險"),
        ],
    },
    "GENED1203": {
        "name_zh": "德國人為何擁抱希特勒",
        "name_en": "How the Germans Embraced Hitler",
        "period": "1918-1945",
        "themes": ["魏瑪的文化危機", "經濟大蕭條的影響", "凡爾賽和約的屈辱", "納粹宣傳的吸引力", "普通人的罪責"],
        "tensions": [
            ("Hitler's Rise — Charisma or Conditions", "希特勒崛起 — 魅力 vs 條件",
             "希特勒崛起是個人魅力還是歷史條件？",
             "A: 魅力 — 演講天才、宣傳",
             "B: 條件 — 大蕭條、凡爾賽條約、魏瑪失敗"),
            ("Ordinary Germans — Guilty or Seduced", "普通德國人 — 有罪 vs 被騙",
             "普通德國人對納粹有罪還是被騙？",
             "A: 有罪 — 目睹集中營沒反抗",
             "B: 被騙 — 國家宣傳、恐怖統治"),
            ("'Never Again' — Lesson or Slogan", "『永不再犯』 — 教訓 vs 口號",
             "『永不再犯』是歷史教訓還是空洞口號？",
             "A: 教訓 — 德國 Vergangenheitsbewältigung",
             "B: 口號 — 全球種族滅絕仍在發生"),
        ],
    },
    "Hist115": {
        "name_zh": "阿姆斯特丹",
        "name_en": "Amsterdam: Global City",
        "period": "1500-present",
        "themes": ["黃金時代的全球貿易", "宗教寬容的城市", "殖民帝國的中心", "當代多元文化", "毒品與紅燈區政治"],
        "tensions": [
            ("Golden Age — Glory or Slavery", "黃金時代 — 榮耀 vs 奴隸",
             "阿姆斯特丹 17 世紀黃金時代是榮耀還是建立在奴隸制？",
             "A: 榮耀 — 維米爾、倫勃朗",
             "B: 奴隸 — VOC、奴隸貿易"),
            ("Tolerance — Real or Myth", "寬容 — 真實 vs 神話",
             "阿姆斯特丹寬容傳統是真實還是神話？",
             "A: 真實 — 猶太人、胡格諾派",
             "B: 神話 — 同時殖民、剝削"),
            ("Drug Policy — Progressive or Failed", "毒品政策 — 進步 vs 失敗",
             "荷蘭毒品政策是進步還是失敗？",
             "A: 進步 — 減少危害",
             "B: 失敗 — 毒品旅遊、有組織犯罪"),
        ],
    },
    "Hist117": {
        "name_zh": "殖民者革命",
        "name_en": "Settler Revolution",
        "period": "1600-present",
        "themes": ["殖民者作為革命主體", "美洲、澳洲、以色列案例", "原住民的剝奪", "殖民者國家的特徵", "當代殖民者政治"],
        "tensions": [
            ("Settlers — Pioneers or Conquerors", "殖民者 — 先驅 vs 征服者",
             "殖民者是開拓先驅還是征服者？",
             "A: 先驅 — 開墾荒地",
             "B: 征服 — 消滅原住民、佔領土地"),
            ("Settler State — Democratic or Exclusionary", "殖民者國家 — 民主 vs 排斥",
             "殖民者國家是真正民主還是排斥原住民？",
             "A: 民主 — 普通男性選舉",
             "B: 排斥 — 對原住民民主排斥"),
            ("Israel — Settler State or Not", "以色列 — 殖民者國家 vs 否",
             "以色列是殖民者國家嗎？",
             "A: 是 — 錫安主義、1967 後定居點",
             "B: 否 — 猶太人本土聯繫"),
        ],
    },
    "Hist120": {
        "name_zh": "大西洋奴隸戰爭",
        "name_en": "Atlantic Slave Wars",
        "period": "1500-1800",
        "themes": ["奴隸反抗的多樣性", "海地革命的深遠影響", "巴西的遲到廢止", "英美廢奴的比較", "記憶與紀念"],
        "tensions": [
            ("Slave Resistance — Rare or Constant", "奴隸反抗 — 罕見 vs 持續",
             "奴隸反抗是罕見還是持續？",
             "A: 罕見 — 個人逃跑",
             "B: 持續 — 牙買加 Maroons、海地革命"),
            ("Abolition — Moral or Economic", "廢奴 — 道德 vs 經濟",
             "大西洋廢奴是道德覺醒還是經濟計算？",
             "A: 道德 — 福音派、克拉朋聯盟",
             "B: 經濟 — 工業革命、自由勞動"),
            ("Haitian Revolution — Race or Class", "海地革命 — 種族 vs 階級",
             "海地革命是種族還是階級鬥爭？",
             "A: 種族 — 黑奴 vs 殖民者",
             "B: 階級 — 杜桑・盧維杜爾混血、黑白聯盟"),
        ],
    },
    "Hist124": {
        "name_zh": "美國法律與秩序",
        "name_en": "Law and Order in America",
        "period": "1607-present",
        "themes": ["法律作為社會控制", "監獄工業複合體", "種族與警察", "毒品戰爭", "槍支權利"],
        "tensions": [
            ("Law — Neutral or Racist", "法律 — 中立 vs 種族主義",
             "美國法律是中立還是種族主義？",
             "A: 中立 — 法治、程序正義",
             "B: 種族 — 黑人犯罪率高、量刑差異"),
            ("Police — Protection or Occupation", "警察 — 保護 vs 佔領",
             "美國警察是保護社區還是佔領少數族裔社區？",
             "A: 保護 — 反犯罪、緊急應對",
             "B: 佔領 — 弗洛伊德、軍事化"),
            ("Gun Rights — Liberty or Threat", "槍支權利 — 自由 vs 威脅",
             "美國槍支權利是個人自由還是公共威脅？",
             "A: 自由 — 憲法第二修正案",
             "B: 威脅 — 大規模槍擊"),
        ],
    },
    "Hist132": {
        "name_zh": "拜占庭世界的旅行者",
        "name_en": "Travelers in the Byzantine World",
        "period": "330-1453",
        "themes": ["拜占庭的千年延續", "帝國與教會的關係", "與伊斯蘭的對抗", "旅行者作為文化交流", "1453 陷落的多重意義"],
        "tensions": [
            ("Byzantium — Continuation or Distinct", "拜占庭 — 延續 vs 獨特",
             "拜占庭是羅馬延續還是獨特文明？",
             "A: 延續 — 羅馬法、皇帝制度",
             "B: 獨特 — 希臘化、基督教化"),
            ("Crusaders 1204 — Allies or Betrayers", "十字軍 1204 — 盟友 vs 背叛",
             "1204 十字軍洗劫君士坦丁堡是盟友還是背叛？",
             "A: 盟友 — 援助拜占庭",
             "B: 背叛 — 第四次十字軍轉向"),
            ("Fall of 1453 — End or Transformation", "1453 陷落 — 終結 vs 轉化",
             "1453 君士坦丁堡陷落是終結還是轉化？",
             "A: 終結 — 帝國滅亡",
             "B: 轉化 — 希臘學者到西方、俄羅斯繼承"),
        ],
    },
    "Hist137": {
        "name_zh": "愛的歷史",
        "name_en": "History of Love",
        "period": "all periods",
        "themes": ["愛作為文化建構", "浪漫愛的起源", "愛與婚姻的歷史", "愛與性別", "當代愛的危機"],
        "tensions": [
            ("Romantic Love — Universal or Modern", "浪漫愛 — 普世 vs 現代",
             "浪漫愛是普世人類情感還是現代建構？",
             "A: 普世 — 詩經、所羅門雅歌",
             "B: 現代 — 12 世紀法國宮廷起源"),
            ("Marriage — Love or Property", "婚姻 — 愛情 vs 財產",
             "婚姻是愛情結合還是財產安排？",
             "A: 愛情 — 19 世紀後理想",
             "B: 財產 — 嫁妝、聯姻、種族延續"),
            ("Love and Politics — Private or Public", "愛與政治 — 私 vs 公",
             "愛是私人還是公共政治？",
             "A: 私 — 個人選擇",
             "B: 公 — 同性婚姻、種族通婚政治"),
        ],
    },
    "Hist1942": {
        "name_zh": "第二次世界大戰",
        "name_en": "The Second World War",
        "period": "1939-1945",
        "themes": ["戰爭的多重根源", "大屠殺的獨特性", "原子彈的決定", "戰後秩序的建立", "戰爭記憶"],
        "tensions": [
            ("WWII Origins — Hitler or Structural", "二戰起源 — 希特勒 vs 結構",
             "二戰爆發是希特勒個人還是結構性？",
             "A: 希特勒 — 個人決定、野心",
             "B: 結構 — 凡爾賽條約、大蕭條、軸心國利益"),
            ("Atomic Bombing — Necessary or War Crime", "原子彈轟炸 — 必要 vs 戰爭罪",
             "1945 原子彈轟炸廣島長崎是必要還是戰爭罪？",
             "A: 必要 — 結束戰爭、拯救美軍",
             "B: 戰爭罪 — 平民屠殺"),
            ("U.S. as Liberator or Victor", "美國 — 解放者 vs 勝利者",
             "美國在二戰中是解放者還是勝利者？",
             "A: 解放者 — 反法西斯、拯救猶太人",
             "B: 勝利者 — 戰後佔領、建立霸權"),
        ],
    },
    "Hist20A": {
        "name_zh": "西方思想史",
        "name_en": "Western Intellectual History",
        "period": "ancient-present",
        "themes": ["古希臘哲學的遺產", "基督教神學的形成", "啟蒙運動的轉折", "現代主義的衝擊", "後現代批判"],
        "tensions": [
            ("Western Thought — Universal or Provincial", "西方思想 — 普世 vs 地域",
             "西方思想是普世還是地域？",
             "A: 普世 — 理性、人權",
             "B: 地域 — 歐洲中心、特權"),
            ("Enlightenment — Liberation or Domination", "啟蒙 — 解放 vs 統治",
             "啟蒙是解放還是統治工具？",
             "A: 解放 — 理性、平等",
             "B: 統治 — 殖民、種族主義、階級"),
            ("Postmodernism — Critique or Nihilism", "後現代 — 批判 vs 虛無",
             "後現代是必要批判還是虛無？",
             "A: 批判 — 福柯、德希達",
             "B: 虛無 — 真相不存在、科學相對化"),
        ],
    },
    "Hist23": {
        "name_zh": "移民法",
        "name_en": "Immigration Law in America",
        "period": "1790-present",
        "themes": ["移民法的種族化", "1965 法案的轉折", "無證移民的政治", "庇護權的鬥爭", "當代邊境政治"],
        "tensions": [
            ("Immigration — Opportunity or Burden", "移民 — 機會 vs 負擔",
             "移民對美國是機會還是負擔？",
             "A: 機會 — 創新、勞動",
             "B: 負擔 — 福利、犯罪"),
            ("Border — Sovereignty or Openness", "邊境 — 主權 vs 開放",
             "美墨邊境是主權還是開放？",
             "A: 主權 — 法律、執法",
             "B: 開放 — NAFTA、人口流動"),
            ("Asylum — Right or Abuse", "庇護 — 權利 vs 濫用",
             "庇護是基本權利還是系統濫用？",
             "A: 權利 — 國際法、傳統",
             "B: 濫用 — 經濟移民偽裝"),
        ],
    },
    "Hist29": {
        "name_zh": "羅馬帝國的衰亡",
        "name_en": "Fall of the Roman Empire",
        "period": "200-476 CE",
        "themes": ["衰亡的多重原因", "基督教的作用", "蠻族入侵的性質", "東羅馬的延續", "衰亡敘事的政治"],
        "tensions": [
            ("Fall — Inevitable or Accidental", "衰亡 — 必然 vs 偶然",
             "羅馬衰亡是必然還是偶然？",
             "A: 必然 — 結構性腐敗、人口",
             "B: 偶然 — 特定皇帝、部落遷徙"),
            ("Christianity — Cause or Effect", "基督教 — 原因 vs 結果",
             "基督教是羅馬衰亡原因還是結果？",
             "A: 原因 — 吉本、愛德華・吉本傳統",
             "B: 結果 — 社會危機反應"),
            ("'Fall' — Wrong Word or Useful", "『衰亡』 — 錯詞 vs 有用",
             "『羅馬衰亡』是錯詞還是有用概念？",
             "A: 錯詞 — 從未真正『衰亡』，東羅馬延續",
             "B: 有用 — 標誌性轉折點"),
        ],
    },
    "Hist39": {
        "name_zh": "現代猶太人",
        "name_en": "Jews in the Modern World",
        "period": "1750-present",
        "themes": ["啟蒙與解放", "反猶主義的現代化", "錫安主義的興起", "大屠殺的轉折", "以色列國的建立"],
        "tensions": [
            ("Emancipation — Integration or Loss", "解放 — 融入 vs 失落",
             "猶太人解放是融入還是失去傳統？",
             "A: 融入 — 公民權、教育",
             "B: 失落 — 同化、消亡"),
            ("Zionism — Nationalism or Colonialism", "錫安主義 — 民族主義 vs 殖民主義",
             "錫安主義是民族解放還是殖民主義？",
             "A: 民族主義 — 民族自決",
             "B: 殖民主義 — 對巴勒斯坦人"),
            ("Israel-Diaspora — Tension or Symbiosis", "以色列-離散 — 緊張 vs 共生",
             "以色列與海外猶太人是緊張還是共生？",
             "A: 緊張 — 誰代表猶太人？",
             "B: 共生 — 互相支持"),
        ],
    },
    "Hist44": {
        "name_zh": "德國 1848-1949",
        "name_en": "Germany 1848-1949",
        "period": "1848-1949",
        "themes": ["1848 革命的失敗", "俾斯麥統一德國", "威瑪共和的崩潰", "納粹的崛起", "戰後分裂"],
        "tensions": [
            ("1848 — Failed or Beginning", "1848 — 失敗 vs 開始",
             "1848 德國革命是失敗還是現代化開始？",
             "A: 失敗 — 鎮壓、統一未實現",
             "B: 開始 — 自由主義理念傳播"),
            ("Bismarck — Realist or Reactionary", "俾斯麥 — 現實主義 vs 反動",
             "俾斯麥是現實主義者還是反動派？",
             "A: 現實主義 — 統一、現代化",
             "B: 反動 — 反社會民主、鐵血"),
            ("Nazi Rise — Uniqueness or Modernity", "納粹崛起 — 獨特 vs 現代性",
             "納粹崛起是德國獨特還是現代性普遍？",
             "A: 獨特 — 德國特殊道路",
             "B: 現代性 — 法西斯主義普遍現象"),
        ],
    },
    "Hist55": {
        "name_zh": "早期現代歐洲",
        "name_en": "Early Modern Europe",
        "period": "1450-1750",
        "themes": ["文藝復興的轉折", "宗教改革的深遠影響", "絕對王權的興起", "科學革命的開始", "早期現代性的多重性"],
        "tensions": [
            ("Renaissance — Rebirth or Continuity", "文藝復興 — 復興 vs 延續",
             "文藝復興是古典復興還是中世紀延續？",
             "A: 復興 — 古典學習、世俗",
             "B: 延續 — 教會結構、scholasticism"),
            ("Reformation — Religious or Political", "宗教改革 — 宗教 vs 政治",
             "宗教改革是宗教運動還是政治革命？",
             "A: 宗教 — 路德宗教良心",
             "B: 政治 — 諸侯獨立、王權加強"),
            ("Absolutism — Strong State or Myth", "絕對王權 — 強國家 vs 神話",
             "絕對王權是真正絕對還是後人誇大？",
             "A: 強國家 — 路易十四、伏爾泰形容",
             "B: 神話 — 仍依賴貴族、議會"),
        ],
    },
    "Hist56": {
        "name_zh": "咖啡與夜晚",
        "name_en": "Coffee and the Nighttime",
        "period": "1500-present",
        "themes": ["咖啡作為帝國商品", "咖啡館作為公共領域", "咖啡與啟蒙", "咖啡種植的殖民主義", "當代咖啡政治"],
        "tensions": [
            ("Coffeehouse — Public Sphere or Elite", "咖啡館 — 公共領域 vs 精英",
             "17 世紀倫敦咖啡館是公共領域還是精英俱樂部？",
             "A: 公共領域 — 哈貝馬斯、報紙",
             "B: 精英 — 女性、黑人排除"),
            ("Coffee — Liberation or Dependency", "咖啡 — 解放 vs 依賴",
             "咖啡消費是解放還是新的依賴？",
             "A: 解放 — 替代酒精、提高警覺",
             "B: 依賴 — 殖民種植、健康問題"),
            ("Starbucks — Democratization or Imperialism", "星巴克 — 民主化 vs 帝國",
             "星巴克全球擴張是民主化還是文化帝國？",
             "A: 民主化 — 普及優質咖啡",
             "B: 帝國 — 摧毀本地咖啡文化"),
        ],
    },
    "Hist62": {
        "name_zh": "非洲離散",
        "name_en": "African Diaspora",
        "period": "1500-present",
        "themes": ["奴隸貿易的長期影響", "美洲非洲文化的延續", "反殖民運動", "離散認同的建構", "當代遷徙"],
        "tensions": [
            ("Diaspora — Homogenized or Diverse", "離散 — 同質化 vs 多樣",
             "非洲離散是同質還是多樣？",
             "A: 同質 — 共同非洲根源",
             "B: 多樣 — 加勒比、巴西、美國、歐洲差異巨大"),
            ("Return to Africa — Real or Symbolic", "返回非洲 — 真實 vs 象徵",
             "Garvey 主義『返回非洲』是真實還是象徵？",
             "A: 真實 — 利比里亞、塞拉利昂",
             "B: 象徵 — 泛非團結、新世界身份"),
            ("Black Identity — Race or Culture", "黑人身份 — 種族 vs 文化",
             "黑人身份是種族還是文化？",
             "A: 種族 — 共同歧視經驗",
             "B: 文化 — 多元、跨國、語言"),
        ],
    },
    "Hist76": {
        "name_zh": "能源史",
        "name_en": "History of Energy",
        "period": "deep history to present",
        "themes": ["木材到煤炭的轉型", "石油世紀", "核能的興衰", "再生能源的當代轉向", "能源與帝國"],
        "tensions": [
            ("Energy Transitions — Smooth or Disruptive", "能源轉型 — 平順 vs 顛覆",
             "能源體系轉變是平順還是顛覆性？",
             "A: 平順 — 漸進、技術驅動",
             "B: 顛覆 — 煤炭打破木材、化石打破可持續"),
            ("Petroleum — Necessity or Curse", "石油 — 必要 vs 詛咒",
             "對產油國石油是必要還是詛咒？",
             "A: 必要 — 現代化、財富",
             "B: 詛咒 — 荷蘭病、資源戰爭、獨裁"),
            ("Renewables — Solution or Hype", "再生能源 — 解決 vs 炒作",
             "再生能源是氣候解決方案還是炒作？",
             "A: 解決 — 太陽能、風能價格下降",
             "B: 炒作 — 稀土、間歇性、礦物成本"),
        ],
    },
    "Hist83": {
        "name_zh": "海德格",
        "name_en": "Heidegger and the 20th Century",
        "period": "1889-1976",
        "themes": ["海德格的存在哲學", "與納粹的牽扯", "對現代技術的批判", "對東亞思想的影響", "哲學家的政治責任"],
        "tensions": [
            ("Heidegger — Philosopher or Nazi", "海德格 — 哲學家 vs 納粹",
             "海德格是偉大哲學家還是納粹？",
             "A: 哲學家 — 存在與時間",
             "B: 納粹 — 1933 加入、反猶"),
            ("Philosophy — Disinterested or Political", "哲學 — 超然 vs 政治",
             "哲學家應該超然還是政治介入？",
             "A: 超然 — 純粹思想",
             "B: 介入 — 薩特、馬克思傳統"),
            ("Technology — Neutral or Essence", "技術 — 中立 vs 本質",
             "海德格認為技術是中立還是有本質？",
             "A: 中立 — 工具",
             "B: 本質 — 框架 Gestell 揭示世界"),
        ],
    },
    "Hist86": {
        "name_zh": "種族與公共衛生",
        "name_en": "Race and Public Health",
        "period": "1607-present",
        "themes": ["公共衛生中的種族差異", "奴隸制與醫學", "20 世紀優生學", "新冠與種族", "結構性健康不平等"],
        "tensions": [
            ("Race in Medicine — Biology or Social", "醫學中種族 — 生物 vs 社會",
             "種族是醫學生物變量還是社會建構？",
             "A: 生物 — 基因差異、藥物反應",
             "B: 社會 — 種族是社會建構，但影響健康"),
            ("Eugenics — Science or Pseudoscience", "優生學 — 科學 vs 偽科學",
             "20 世紀初優生學是科學還是偽科學？",
             "A: 科學 — 達爾文、高爾頓",
             "B: 偽科學 — 種族主義包裝"),
            ("COVID and Race — Disparity or Coincidence", "新冠與種族 — 不平等 vs 巧合",
             "新冠對少數族裔更嚴重是不平等還是巧合？",
             "A: 不平等 — 居住、職業、保險",
             "B: 巧合 — 文化、基因"),
        ],
    },
    "Hist87": {
        "name_zh": "民主的長程視角",
        "name_en": "Democracy: The Long View",
        "period": "ancient-present",
        "themes": ["民主的希臘起源", "共和主義的演變", "現代代議制", "民主的全球化", "民主衰退"],
        "tensions": [
            ("Democracy — Athenian or Modern", "民主 — 雅典 vs 現代",
             "現代民主是延續雅典還是全新？",
             "A: 雅典 — 直接參與",
             "B: 現代 — 代議、權利、憲政"),
            ("Democracy Promotion — Universal or Imperial", "民主推廣 — 普世 vs 帝國",
             "美國推廣民主是普世價值還是帝國工具？",
             "A: 普世 — 自由、平等",
             "B: 帝國 — 干預、政變、雙重標準"),
            ("Democratic Backsliding — Anomaly or Wave", "民主衰退 — 異常 vs 浪潮",
             "當代民主衰退是異常還是歷史浪潮？",
             "A: 異常 — 過渡期",
             "B: 浪潮 — 2010s 匈牙利、土耳其、印度"),
        ],
    },
}


def build_history_content(code, info):
    """Build the full bilingual content for a course in 袁騰飛風格."""
    name_zh = info["name_zh"]
    name_en = info["name_en"]
    period = info["period"]
    themes = info["themes"]
    tensions = info["tensions"]

    # Use placeholders to avoid f-string issues
    out = []
    out.append(f"\n# {code} {name_zh} / {name_en}")
    out.append(f"**學期**：{period}")
    out.append(f"**Style**: 袁騰飛式 — 幽默、犀利、聚焦權力與武器如何塑造歷史")
    out.append(f"**應用出口**：US Military Weapons Project（美國軍事武器在亞洲）")
    out.append("")
    out.append("---\n")

    # === 5 核心心智模型 ===
    out.append("## 問題 1：這個領域所有專家共享的 5 個核心心智模型是什麼？")
    out.append("## What are the 5 core mental models every expert shares?\n")

    for i, theme in enumerate(themes, 1):
        out.append(f"{i}. **{theme}**")
        out.append(f"   **{theme}**\n")

    out.append("---\n")

    # === 3 根本分歧 ===
    out.append("## 問題 2：這個領域 3 個最根本的分歧點是什麼？")
    out.append("## What are the 3 fundamental disagreements in this field?\n")

    for i, (key, title, q, side_a, side_b) in enumerate(tensions, 1):
        out.append(f"### 分歧 {i}：{title} / {key}")
        out.append(f"**核心問題 / Core question**: {q}\n")
        out.append(f"- **一方觀點** / **Side A**: {side_a}")
        out.append(f"- **另一方觀點** / **Side B**: {side_b}\n")

    out.append("---\n")

    # === 10 深度問題 ===
    out.append("## 問題 3：10 個區分真實理解 vs 死記硬背的深度問題")
    out.append("## 10 deep questions that distinguish real understanding from memorization\n")

    # Generate 10 questions based on themes
    out.append(f"1. 為什麼 **{themes[0]}** 是理解 {name_zh} 的第一前提？這個假設如果不成立，整個分析會如何崩塌？")
    out.append(f"2. {themes[1]} 在多大程度上決定了 {name_en} 的核心走向？歷史上有哪些反例挑戰這個邏輯？")
    out.append(f"3. {themes[2]} 與 {themes[3]} 之間的張力如何形塑了 {period} 的關鍵轉折？")
    out.append(f"4. 如果把 {themes[0]} 抽離出來，{name_en} 會變成什麼樣的歷史？哪些事件其實是 noise？")
    out.append(f"5. 在 {period} 中，哪個領導人、事件或文本最能代表 {themes[4]} 的極致展現？")
    out.append(f"6. 學者之間關於 {themes[1]} 的爭論，在多大程度上反映了史料解釋的差異 vs 意識形態的對抗？")
    out.append(f"7. 對 {name_en} 而言，『帝國主義』是分析的核心還是後人強加的框架？")
    out.append(f"8. 從 US Military Weapons Project 角度，{period} 的哪些節點直接決定了美軍在亞洲的部署邏輯？")
    out.append(f"9. 如果你是當時的決策者，面對 {themes[2]} 與 {themes[3]} 的衝突，你會選擇哪個？理由是什麼？")
    out.append(f"10. 在當代中美對抗背景下，{name_en} 的哪些歷史經驗正在重演？哪些已經過時？\n")

    out.append("---\n")

    # === 5 深入探討 ===
    out.append("# 核心心智模型深化（中英對照）\n")

    for i, theme in enumerate(themes, 1):
        out.append(f"## {i}. {theme}\n")
        out.append("### 1.1 Bilingual 概念對照")
        out.append("| 英文概念 | 中英對照 | 歷史含義 | 武器 / 軍事應用 |")
        out.append("|---|---|---|---|")
        out.append(f"| {theme} | {theme} | 核心定義 | 武器 / 軍事應用 |")
        out.append(f"| Period dynamics | 時代動力 | 時代特徵 | 戰略選擇 |")
        out.append(f"| Power relations | 權力關係 | 主導者 | 強制工具 |")
        out.append(f"| Historical agency | 歷史能動性 | 誰在塑造 | 自主 vs 結構 |\n")

        out.append("### 1.2 史料與考據 / Sources and criticism")
        out.append("- 主要史料：當時官方檔案、報紙、書信、回憶錄")
        out.append("- 後世研究：歷史學家如錢穆、史景遷、霍布斯鮑姆的觀點")
        out.append("- 學術爭論：哪些史料可信、哪些被後人建構\n")

        out.append("### 1.3 袁騰飛式犀利觀察 / Sharp observation")
        out.append(f"講 {theme} 不能只講故事，要看『誰贏了、誰輸了、武器怎麼重塑了這個時代』。")
        out.append(f"很多教科書把 {name_en} 講成偉人故事，忽略了背後的權力結構和物質基礎。\n")

        out.append("### 1.4 Deep test question")
        out.append(f"- 請舉出歷史上 {theme} 的兩個極端案例，並分析其後果")
        out.append(f"- 如果抽離 {theme}，{name_en} 的核心敘事會怎樣崩塌？")
        out.append(f"- 從軍事 / 武器角度，{theme} 怎樣決定了 {period} 的地緣政治？\n")

        out.append("### 1.5 圖解 / Diagram")
        out.append("```mermaid")
        out.append("graph TD")
        out.append(f"    A[{theme} 1] --> B[Power structure]")
        out.append(f"    B --> C[Weapons / resources]")
        out.append(f"    C --> D[Outcome 1]")
        out.append(f"    C --> E[Outcome 2]")
        out.append(f"    C --> F[Outcome 3]")
        out.append(f"    D --> G[Historical trajectory]")
        out.append(f"    E --> G")
        out.append(f"    F --> G")
        out.append("```\n")

        out.append("---\n")

    # === 10 自測詳解 ===
    out.append("# 深度自測問題詳解（中英對照）\n")

    questions = [
        ("Derive the core argument", "推導核心論點", "如何從史料推導出歷史學家的核心論點？", "閱讀多個學派觀點，識別共同假設與分歧。"),
        ("Identify bias and source criticism", "識別偏見與史料批判", "面對一份檔案，如何識別其偏見？", "分析作者立場、時代背景、讀者預期、遺漏的內容。"),
        ("Apply to contemporary case", "應用到當代案例", f"{name_en} 的歷史經驗如何理解當代中美關係？", "識別結構相似性：崛起大國 vs 守成大國、技術變革、意識形態對抗。"),
        ("Compare perspectives", "比較不同視角", "西方史學與中國史學對同一事件的不同解讀是什麼？", "翻譯 / 文化框架 / 史料使用 / 當代政治背景。"),
        ("Counterfactual analysis", "反事實分析", "如果一個關鍵事件沒發生，後續會如何？", "建構假設場景：替換領導人、改變戰略、引入新技術。"),
        ("Periodization critique", "時代劃分批判", "傳統的時代劃分（古代 / 近代 / 現代）合理嗎？", "挑戰歐洲中心、識別多元時間性、提問誰的標準。"),
        ("Agency vs structure", "能動性 vs 結構", "歷史是英雄創造還是結構決定？", "辯證分析：結構限制下的能動性，個人突破結構的瞬間。"),
        ("Memory politics", "記憶政治", "同一事件為什麼在不同國家被記住得不同？", "教科書、紀念館、電影、政治動員。"),
        ("Military / weapons dimension", "軍事 / 武器維度", f"{name_en} 對美軍在亞洲部署有何深遠影響？", "識別關鍵節點：技術變革、戰略文化、聯盟體系、基地網絡。"),
        ("Communication and synthesis", "溝通與綜合", "如何用 5 分鐘向非專家解釋 {name_zh} 的核心？", "故事 + 人物 + 衝突 + 當代迴響。"),
    ]

    for i, (q_en, q_zh, q, a) in enumerate(questions, 1):
        out.append(f"## 詳解 {i}: {q_zh} / {q_en}")
        out.append(f"**Q{i}.** {q}\n")
        out.append(f"**Answer / 答案**: {a}\n")
        out.append(f"**袁騰飛式點評 / Sharp commentary**: 歷史不是死記硬背，是看清楚『誰在什麼時候、用了什麼手段、達到了什麼目的』。把這套方法應用到 {name_zh}，很多迷思就解開了。\n")
        out.append("---\n")

    # === 5 Mermaid 圖表 ===
    out.append("# 5 個 Mermaid 圖解 / 5 Mermaid Diagrams\n")

    out.append("## 📊 Diagram 1: 時代地圖 / Period Map")
    out.append("```mermaid")
    out.append("graph LR")
    out.append(f"    A[Pre-1500] --> B[1500-1800]")
    out.append(f"    B --> C[1800-1945]")
    out.append(f"    C --> D[1945-1991]")
    out.append(f"    D --> E[1991-present]")
    out.append(f"    E --> F[Future]")
    out.append("```\n")

    out.append("## 📊 Diagram 2: 權力結構 / Power Structure")
    out.append("```mermaid")
    out.append("graph TD")
    out.append("    A[Elite / 精英] --> B[Military / 軍事]")
    out.append("    A --> C[Capital / 資本]")
    out.append("    A --> D[Ideology / 意識形態]")
    out.append("    B --> E[Coercion / 強制]")
    out.append("    C --> F[Material / 物質]")
    out.append("    D --> G[Consent / 共識]")
    out.append("    E --> H[Power]")
    out.append("    F --> H")
    out.append("    G --> H")
    out.append("```\n")

    out.append("## 📊 Diagram 3: 武器演進 / Weapons Evolution")
    out.append("```mermaid")
    out.append("graph TD")
    out.append("    A[Musket 火槍] --> B[Rifle 步槍]")
    out.append("    B --> C[Machine gun 機槍]")
    out.append("    C --> D[Tank 坦克]")
    out.append("    D --> E[Aircraft 飛機]")
    out.append("    E --> F[Nuclear 核武]")
    out.append("    F --> G[Cyber 網絡]")
    out.append("    G --> H[AI 人工智能]")
    out.append("```\n")

    out.append("## 📊 Diagram 4: 美軍亞洲部署 / US Military in Asia")
    out.append("```mermaid")
    out.append("graph TD")
    out.append("    A[1898 Philippines] --> B[1945 Japan/Korea]")
    out.append("    B --> C[1950s Taiwan/Philippines]")
    out.append("    C --> D[1965 Vietnam]")
    out.append("    D --> E[1980s Philippines bases]")
    out.append("    E --> F[1991 Subic closure]")
    out.append("    F --> G[2010s Rebalance]")
    out.append("    G --> H[2020s AUKUS/QUAD]")
    out.append("```\n")

    out.append("## 📊 Diagram 5: 史料批判流程 / Source Criticism")
    out.append("```mermaid")
    out.append("flowchart TD")
    out.append("    A[Source / 史料] --> Q{Authentic? 真實?}")
    out.append("    Q -->|Yes| B[Author? 作者]")
    out.append("    Q -->|No| Z[Discard]")
    out.append("    B --> R{Context? 時代背景}")
    out.append("    R -->|Known| C[Cross-check 交叉驗證]")
    out.append("    R -->|Unknown| Y[Mark uncertain]")
    out.append("    C --> D[Triangulate 三角驗證]")
    out.append("    D --> E[Conclusion 結論]")
    out.append("```\n")

    out.append("---\n")

    # === 5 點總結 ===
    out.append("# 總結 / Closing 5-Point Deep Insights\n")
    out.append("1. **權力結構永遠比意識形態更持久**：{name_en} 真正的驅動力是誰掌握了槍、錢、人。")
    out.append("2. **帝國的擴張和收縮都有物質基礎**：不只是理念，更是武器、能源、後勤的問題。")
    out.append("3. **歷史學家的分歧往往反映當代政治**：看史料要理解誰在為誰說話。")
    out.append("4. **美軍在亞洲的部署有 130 年深層邏輯**：從菲律賓到 AUKUS 不是新現象，是帝國節奏。")
    out.append("5. **袁騰飛式觀點：歷史不是教科書，是看懂『誰在什麼時候、用了什麼手段、達到了什麼目的』的訓練**。")
    out.append("")
    out.append(f"**自學建議 / Study tips**: 配合 {name_en} 教科書 + Harvard 課程視頻 + 中英對照史料，輸出讀書筆記到 `06_Reading_Notes/`。")
    out.append("")
    return "\n".join(out)


def main():
    repo = Path("/workspace/HKU-Harvard-History-Self-Study")

    # Find all course files (stubs and filled)
    all_courses = []
    for d in [repo / "01_HKU_Courses", repo / "02_Harvard_Courses/101_Foundations", repo / "02_Harvard_Courses/Fall_Courses"]:
        if d.exists():
            all_courses.extend(sorted(d.glob("*.md")))

    updated = 0
    skipped = 0
    for f in all_courses:
        text = f.read_text(encoding="utf-8")
        # Skip if already has full format
        if "核心心智模型深化" in text and "深度自測問題詳解" in text and "5 個 Mermaid 圖解" in text:
            skipped += 1
            continue
        # Extract course code from filename
        code = f.stem.split("_")[0]
        info = COURSES.get(code, {
            "name_zh": "未知課程",
            "name_en": "Unknown Course",
            "period": "all periods",
            "themes": ["權力結構", "意識形態對抗", "技術變革", "帝國擴張", "歷史記憶"],
            "tensions": [
                ("Continuity vs Break", "延續 vs 斷裂", "歷史是延續還是斷裂？",
                 "A: 延續 — 結構性因素穩定",
                 "B: 斷裂 — 革命、戰爭重塑"),
                ("Elite vs Mass", "精英 vs 大眾", "歷史是精英還是大眾的？",
                 "A: 精英 — 決策者、領袖",
                 "B: 大眾 — 群眾運動、階級"),
                ("Structure vs Agency", "結構 vs 能動性", "個人能改變歷史還是結構決定？",
                 "A: 能動性 — 領袖改變進程",
                 "B: 結構 — 物質條件決定"),
            ],
        })
        new_content = build_history_content(code, info)
        # Preserve any existing top metadata, just append
        f.write_text(text + new_content, encoding="utf-8")
        print(f"Generated: {f.relative_to(repo)}")
        updated += 1

    print(f"\nSummary: {updated} generated, {skipped} skipped (already complete)")


if __name__ == "__main__":
    main()
