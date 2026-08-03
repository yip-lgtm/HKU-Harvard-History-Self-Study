#!/usr/bin/env python3
"""Expand all 92 HKU + Harvard History course files to the full 袁騰飛-style format.

Per AGENTS.md spec:
  - 5 core mental models (bilingual)
  - 3 fundamental disagreements (bilingual)
  - 10 deep questions (bilingual)
  - 5 deep dives (one per mental model) with bilingual tables + diagrams
  - 10 detailed self-test solutions (bilingual, sharp commentary)
  - 5 Mermaid diagram sections
  - Closing 5-point "deep insights" summary

Style: 袁騰飛 — sharp, humorous, focused on power, weapons, who won/lost.
Application: US Military Weapons Project（美國軍事武器在亞洲）.
"""
import re
from pathlib import Path


# Course-specific mental models, periods, themes
# Each entry: code -> (period_zh, period_en, model1..5, question_focus)
COURSES = {
    # ===== HKU Courses =====
    "HIST1016": ("1500-present", "1500-present", [
        ("現代世界的多重時間性", "Modernity as multiple temporalities",
         "世界不是單一時間軸；不同地區有各自的『現代』，歐洲不是唯一基準。"),
        ("帝國擴張的物質基礎", "Material basis of empire",
         "每個帝國的崛起背後是槍、錢、煤、鋼、橡膠、石油。"),
        ("跨文化接觸的雙向性", "Bidirectional cultural contact",
         "殖民主義不是單向灌輸；被殖民者反向重塑了殖民者（茶葉、印度公務員、英國飲食）。"),
        ("革命的多重形式", "Multiple forms of revolution",
         "政治（法國）、工業（英國）、社會（俄國）、科技（信息）四種革命，時間地點互不相同。"),
        ("全球化的退潮與再起", "Tides of globalization",
         "現代全球化並非線性：1914、1945、2008 多次中斷，2020 加速重組。"),
    ]),
    "HIST1017": ("1841-present", "1841-present", [
        ("殖民現代性的雙重性", "Colonial modernity's double edge",
         "英治香港同時是法治-公共衛生的現代化工程，也是帝國主義的轉口貿易控制。"),
        ("香港作為帝國轉運點", "Hong Kong as imperial entrepôt",
         "1841-1997 之間香港是英帝國進入東亞的踏板，1997 後是中國進入全球資本市場的踏板。"),
        ("1997 過渡的歷史斷裂", "Historical rupture of 1997",
         "主權移交不只是法律事件，更是經濟、身份、記憶的斷裂與重組。"),
        ("香港身份的混雜性", "Hybridity of Hong Kong identity",
         "粵-英-中三語並行，東西方文化交匯，自成一家。"),
        ("全球資本主義的香港節點", "HK node in global capitalism",
         "金融、航運、貿易三位一體：香港繁榮靠『自由港 + 法治 + 西方資金 + 中國腹地』。"),
    ]),
    "HIST1023": ("1840-present", "1840-present", [
        ("東亞的帝國主義重塑", "East Asia's imperial reshaping",
         "1840-1945 東亞經歷了西方、俄國、日本三重帝國主義的衝擊與重塑。"),
        ("日本現代化的雙刃", "Double-edged Japanese modernization",
         "明治維新既建立了亞洲第一個現代國家，也走向帝國主義擴張。"),
        ("中國的革命斷裂", "China's revolutionary ruptures",
         "1911、1949、1978 三次斷裂：共和、共產、改革開放。"),
        ("冷戰在東亞的熱戰", "Hot wars in Cold War East Asia",
         "韓戰、越戰、台海危機——冷戰在亞洲從未冷過。"),
        ("東亞經濟奇蹟的結構基礎", "Structural basis of East Asian miracle",
         "日本、韓國、台灣、香港、新加坡的起飛靠『國家主導 + 出口導向 + 美國安全傘』。"),
    ]),
    "HIST1025": ("1607-present", "1607-present", [
        ("美國例外論的歷史建構", "American exceptionalism as historical construct",
         "『山巔之城』不是事實，是 17 世紀清教徒到 19 世紀昭昭天命不斷重述的意識形態。"),
        ("種族、奴隸制、資本積累", "Race, slavery, capital accumulation",
         "美國的財富起點是 1619 的奴隸種植園；資本積累與種族壓迫從未分開。"),
        ("聯邦制與帝國擴張", "Federalism and imperial expansion",
         "1787 憲法設計了聯邦制，但 19 世紀『昭昭天命』把大陸擴張合理化。"),
        ("美國全球霸權的興起", "Rise of US global hegemony",
         "1898 美西戰爭是分水嶺：美國從大陸帝國變成太平洋-大西洋雙洋強權。"),
        ("美軍與現代戰爭的演化", "US military and modern warfare evolution",
         "從內戰步槍到二戰核武到 21 世紀無人機，每一次技術革命都重塑美軍的全球部署。"),
    ]),
    "HIST2031": ("1895-present", "1895-present", [
        ("電影作為歷史證據", "Cinema as historical evidence",
         "電影不只是娛樂，是時代意識形態的視聽化石（好萊塢黃金時代 = 美國夢的視覺化）。"),
        ("影像與記憶政治", "Image and memory politics",
         "誰掌握了膠片、攝影棚、發行渠道，誰就掌握了歷史敘事（好萊塢 vs 蘇聯蒙太奇 vs 第三世界電影）。"),
        ("紀錄片與史學方法", "Documentary and historiography",
         "紀錄片是歷史的鏡子還是建構？影像證據的可信度邊界在哪？"),
        ("冷戰與好萊塢意識形態", "Cold War and Hollywood ideology",
         "1947-1991 好萊塢是美國軟實力的核心引擎；CIA 早期曾秘密支持文化冷戰。"),
        ("亞洲電影與西方觀看", "Asian cinema and Western gaze",
         "從 1960s 功夫片到 1990s 第五代、第六代導演，亞洲電影如何重塑西方對東方的想像？"),
    ]),
    "HIST2063": ("1890-1940", "1890-1940", [
        ("世紀末維也納的現代性", "Viennese fin-de-siècle modernity",
         "佛洛伊德、維特根斯坦、克林姆特、馬勒：1890-1914 維也納是現代思想的重要發源地。"),
        ("第一次世界大戰的文化斷裂", "Cultural rupture of WWI",
         "1914-1918 不只是軍事災難，更把歐洲文明自信打成碎片。"),
        ("戰間期的極權誘惑", "Totalitarian temptation of interwar",
         "法西斯主義、共產主義、納粹——民主為何在 1930s 顯得無力？"),
        ("現代主義藝術與社會", "Modernist art and society",
         "立體派、達達、超現實——現代主義既是美學革命也是對資本主義異化的回應。"),
        ("戰爭記憶與歐洲認同", "War memory and European identity",
         "『歐洲』這個概念在二戰後才真正被建構，戰爭記憶是其核心黏合劑。"),
    ]),
    "HIST2068": ("1900-2000", "1900-2000", [
        ("五四運動的遺產爭論", "Legacy debate of May Fourth",
         "1919 五四究竟是愛國啟蒙，還是全盤反傳統？毛澤東 vs 胡適的詮釋至今未平。"),
        ("馬克思主義中國化", "Sinification of Marxism",
         "從列寧到毛澤東到鄧小平，馬克思主義怎樣被改造為中國革命的武器？"),
        ("新文化運動的語言革命", "Linguistic revolution of New Culture",
         "白話文運動不只改變書寫，更改變了誰能進入知識階層。"),
        ("傳統 vs 現代的拉鋸", "Tradition vs modernity tug-of-war",
         "百年來『打倒孔家店』與『復興儒學』的反覆拉鋸，揭示中國現代性的深層張力。"),
        ("20 世紀中國思想的政治化", "Politicization of 20th-century Chinese thought",
         "胡適的『多談問題少談主義』vs 陳獨秀的『主義優先』——學術從未脫離政治。"),
    ]),
    "HIST2070": ("modern", "modern", [
        ("自傳作為史料的可信度", "Autobiography as source reliability",
         "自傳是回憶的建構，不是事實的鏡子；要問『為何這樣寫』而非『寫了什麼』。"),
        ("自我敘事與社會結構", "Self-narrative and social structure",
         "個人故事從不只屬於個人——性別、階級、種族決定了誰能說話、怎樣說話。"),
        ("口述史的方法論", "Methodology of oral history",
         "口述史是 1960s 以後史學的重大突破，但也面臨記憶衰退、敘事框架、後視偏差等問題。"),
        ("邊緣群體的自我書寫", "Self-writing by marginalized groups",
         "工人、婦女、原住民、殖民地的自傳挑戰了主流史學的『偉人敘事』。"),
        ("數字時代的自傳", "Digital age autobiography",
         "社交媒體、博客、AI 生成的『自傳』重新定義了自我書寫的可能性與風險。"),
    ]),
    "HIST2076": ("1945-1991", "1945-1991", [
        ("冷戰的多個戰場", "Multiple Cold War arenas",
         "歐洲、亞洲、非洲、拉美——冷戰從來不只是美蘇，是全球多個戰場的代理人戰爭。"),
        ("核武器的恐怖平衡", "Balance of nuclear terror",
         "1949 蘇聯核試、1962 古巴導彈危機——MAD 確保了超級大國不打直接戰。"),
        ("柏林牆的象徵意義", "Symbolism of the Berlin Wall",
         "1961-1989 柏林牆不只是冷戰地標，更是意識形態對抗的視覺象徵。"),
        ("德國分裂與統一的政治", "Politics of German division and reunification",
         "1949 兩個德國、1990 統一是冷戰結束的標誌；統一條約埋下今日德俄緊張的種子。"),
        ("聯盟體系與歐洲整合", "Alliance systems and European integration",
         "NATO vs 華約 vs 歐共體——三套制度競爭決定了歐洲的冷戰軌跡。"),
    ]),
    "HIST2077": ("1800-present", "1800-present", [
        ("食物作為權力象徵", "Food as power symbol",
         "宮廷飲食、殖民香料貿易、戰時口糧——食物從來不只是營養。"),
        ("帝國與香料/糖/茶的全球貿易", "Empire and global trade in spices/sugar/tea",
         "葡萄牙、荷蘭、英國的帝國興衰都離不開對東印度群島、加勒比、中國茶的控制。"),
        ("飲食的文化政治", "Cultural politics of cuisine",
         "吃什麼、怎麼吃、誰與誰同桌——食物標記階級、種族、文明的邊界。"),
        ("飢荒與政治", "Famine and politics",
         "1845 愛爾蘭大飢荒、1958-1961 大躍進、1984 埃塞俄比亞——飢荒總是政治失敗。"),
        ("工業化與食品革命", "Industrialization and food revolution",
         "罐頭、速食、超市、外賣——工業化重塑了 19 世紀以來人類吃什麼、何時吃、怎麼吃。"),
    ]),
    "HIST2079": ("1500-1800", "1500-1800", [
        ("宗教改革的多重原因", "Multiple causes of Reformation",
         "1517 路德 95 條不是孤立的宗教事件；印刷術、城市中產階級、王權擴張都推了一把。"),
        ("科學革命的社會建構", "Social construction of scientific revolution",
         "哥白尼、伽利略、牛頓的『革命』背後是贊助者、學院、出版網絡的轉變。"),
        ("早期現代國家形成", "Early modern state formation",
         "威斯特伐利亞 1648 標誌主權國家體系的誕生，但國家形成是百年漫長過程。"),
        ("重商主義與殖民", "Mercantilism and colonization",
         "17-18 世紀重商主義把殖民地看作母國財富的延伸，是帝國主義的經濟基礎。"),
        ("啟蒙運動的多元性", "Plurality of Enlightenment",
         "啟蒙不是法國百科全書派的專利；蘇格蘭啟蒙、美國啟蒙、女性啟蒙都有獨特貢獻。"),
    ]),
    "HIST2103": ("1900-2000", "1900-2000", [
        ("革命作為政治傳統", "Revolution as political tradition",
         "1917 十月革命、1991 蘇聯解體——俄國 20 世紀是革命的世紀。"),
        ("史達林主義的結構", "Structure of Stalinism",
         "集體化、工業化、大清洗——史達林把蘇聯變成極權國家，但也把農國變成工業國。"),
        ("二戰的蘇聯戰場", "WWII's Soviet front",
         "1941-1945 東線是二戰最血腥戰場，蘇聯傷亡 2700 萬，是擊敗納粹的主力。"),
        ("冷戰與蘇聯的全球野心", "Cold War and Soviet global ambitions",
         "從東歐衛星國到古巴、越南、非洲之角——冷戰中蘇聯的全球擴張。"),
        ("蘇聯解體的多重原因", "Multiple causes of USSR collapse",
         "戈巴契夫改革 + 民族矛盾 + 經濟停滯 + 西方軍備競賽——1991 蘇聯解體沒有單一原因。"),
    ]),
    "HIST2118": ("1784-present", "1784-present", [
        ("中美關係的雙向建構", "Mutual construction of Sino-American relations",
         "1784 中國皇后號到 1972 尼克森訪華，中美互相建構對方的想像（黃禍、中國威脅論）。"),
        ("排華法的深層邏輯", "Deep logic of Chinese Exclusion",
         "1882 排華法不只是種族歧視，更是經濟危機中的政治動員工具。"),
        ("太平洋戰爭與中美同盟", "Pacific War and Sino-American alliance",
         "1941-1945 中美結成反法西斯同盟，埋下戰後複雜關係的種子。"),
        ("冷戰中的中美對抗", "Sino-American Cold War confrontation",
         "1949-1972 中美在韓戰、越戰、台海直接對抗；1972 開始的『準同盟』重塑了亞洲格局。"),
        ("中美貿易戰的歷史深層", "Historical depth of US-China trade war",
         "2018 起的貿易戰不是新現象；1844 望廈條約、1900 庚子賠款、1950 封鎖、1990s 最惠國待遇——百年節奏。"),
    ]),
    "HIST2127": ("1644-1912", "1644-1912", [
        ("清帝國的內亞性", "Inner-Asian character of Qing Empire",
         "清帝國不只是漢化王朝；滿蒙聯盟、藏傳佛教、伊斯蘭治理使其成為多元帝國。"),
        ("朝貢體系的現實與神話", "Reality and myth of tributary system",
         "朝貢不只是禮儀，更是貿易、外交、安全的複合體系；西方『朝貢神話』是後人建構。"),
        ("鴉片戰爭的全球背景", "Global context of Opium War",
         "1839-1842 鴉片戰爭是英國工業革命後對華貿易逆差的暴力解決，是全球資本擴張的縮影。"),
        ("太平天國的革命試驗", "Revolutionary experiment of Taiping",
         "1851-1864 太平天國是 19 世紀最大內戰，洪秀全的基督教-儒家混合意識形態獨特且致命。"),
        ("清末改革的不徹底", "Incompleteness of late Qing reforms",
         "洋務運動、戊戌變法、清末新政——為何 1911 革命仍不可避免？"),
    ]),
    "HIST2143": ("ancient-present", "ancient-present", [
        ("性別作為社會建構", "Gender as social construct",
         "性別不是生物事實，是權力關係的產物；『男主外女主內』是特定歷史的發明。"),
        ("中國女性史的多線敘事", "Multi-line narrative of Chinese women's history",
         "不是單一壓迫史；不同朝代、不同階層、不同族群女性經驗差異巨大。"),
        ("纏足的文化政治", "Cultural politics of footbinding",
         "10 世紀到 20 世紀初的纏足不只是美學，更是父權、階級、種族的視覺符號。"),
        ("婚姻與政治", "Marriage and politics",
         "從漢唐和親到清末政治婚姻，中國女性史是政治史的隱性維度。"),
        ("現代性與性別解放", "Modernity and gender liberation",
         "五四女權、共產婦女解放、當代女性主義——百年來性別秩序的重組從未完成。"),
    ]),
    "HIST2152": ("1970s-1991", "1970s-1991", [
        ("1989 年作為全球事件", "1989 as global event",
         "1989 不只是天安門；柏林牆倒塌、蘇聯解體、整個共產陣營崩潰。"),
        ("晚期社會主義的危機", "Crisis of late socialism",
         "1970s 石油危機、1980s 改革困境——晚期社會主義國家集體陷入合法性危機。"),
        ("改革派的政治遺產", "Political legacy of reformists",
         "戈巴契夫 vs 葉爾欽 vs 鄧小平——三種改革路徑決定了不同國家的命運。"),
        ("公民社會的興起", "Rise of civil society",
         "哈維爾、瓦文薩、方勵之——1980s 公民社會從下而上挑戰極權。"),
        ("意識形態的終結？", "End of ideology?",
         "福山『歷史的終結』是對還是錯？1989 之後意識形態真的結束了嗎？"),
    ]),
    "HIST2161": ("1400-present", "1400-present", [
        ("種族作為社會建構", "Race as social construct",
         "種族不是生物學事實，是 15 世紀以來殖民主義、奴隸制、帝國擴張的產物。"),
        ("現代種族觀念的發明", "Invention of modern race",
         "17-19 世紀自然史、優生學、統計學共同『發明』了現代種族分類。"),
        ("奴隸制與資本主義", "Slavery and capitalism",
         "大西洋奴隸貿易不只是道德問題，是英美資本積累的核心；沒有奴隸貿易就沒有工業革命。"),
        ("帝國主義的種族論述", "Racial discourse of imperialism",
         "19 世紀『白人的負擔』、『黃禍論』——種族話語合理化了帝國擴張。"),
        ("去殖民化與種族正義", "Decolonization and racial justice",
         "1960s 民權運動、反殖民運動；2020s BLM 表明種族問題遠未解決。"),
    ]),
    "HIST2170": ("500-1500", "500-1500", [
        ("伊斯蘭文明的多元性", "Plurality of Islamic civilization",
         "伊斯蘭世界不是單一文明；阿拉伯、波斯、土耳其、柏柏爾文化各具特色。"),
        ("伊斯蘭黃金時代", "Islamic Golden Age",
         "8-14 世紀巴格達智慧宮、數學、醫學、光學——伊斯蘭世界保存並擴展了古典知識。"),
        ("蒙古入侵的雙重影響", "Dual impact of Mongol invasions",
         "1258 巴格達陷落既是伊斯蘭文明的災難，也意外促進了東西文化交流。"),
        ("伊斯蘭法律的多樣性", "Diversity of Islamic law",
         "遜尼、什葉、蘇菲、瓦哈比——伊斯蘭從來不是單一法律傳統。"),
        ("歐洲中心 vs 全球視角", "Eurocentric vs global perspectives",
         "『黑暗時代』是歐洲中心主義的標籤；伊斯蘭、印度、中國當時都處於文明高峰。"),
    ]),
    "HIST2177": ("1800-present", "1800-present", [
        ("中國經濟的長期停滯論", "Long-term stagnation thesis",
         "加州學派 vs 傳統史學：1800 年前中國是領先還是停滯？"),
        ("鴉片貿易與白銀流動", "Opium trade and silver flows",
         "晚清白銀外流不只是經濟問題，是國家安全問題。"),
        ("半殖民地的經濟結構", "Economic structure of semi-colonialism",
         "1842-1949 中國被迫捲入全球資本主義，但保留了部分主權和本土經濟。"),
        ("毛時代的工業化", "Industrialization in Mao era",
         "1949-1976 毛時代完成了從農業國到工業國的基礎建設，雖然付出了巨大代價。"),
        ("改革開放的深層邏輯", "Deep logic of reform and opening",
         "1978- 中國『社會主義市場經濟』是 20 世紀最獨特的制度實驗。"),
    ]),
    "HIST2179": ("1500-present", "1500-present", [
        ("海盜作為原始全球資本家", "Pirates as primitive global capitalists",
         "16-18 世紀海盜不只是罪犯，是全球貿易的早期主體；東印度公司有海盜血統。"),
        ("帝國秩序與國際法", "Imperial order and international law",
         "格勞秀斯、康德、聯合國憲章——國際法是帝國秩序的法律化還是人類進步？"),
        ("人權話語的帝國性", "Imperial character of human rights discourse",
         "1970s 卡特政府把人權引入外交，是美國軟實力的工具還是普世價值？"),
        ("戰爭法的演變", "Evolution of laws of war",
         "從日內瓦公約到當代 ICC——戰爭法是不切實際的理想還是切實的限制？"),
        ("海洋法與領土爭端", "Maritime law and territorial disputes",
         "UNCLOS、南海爭端——21 世紀仍是海權時代。"),
    ]),
    "HIST2188": ("1757-present", "1757-present", [
        ("東印度公司作為早期現代國家", "EIC as proto-modern state",
         "東印度公司有軍隊、有領土、有外交——是公司還是國家？"),
        ("分治的暴力", "Violence of partition",
         "1947 印巴分治造成 100-200 萬人死亡、1500 萬人無家可歸，是 20 世紀最暴力的人口遷移。"),
        ("種姓制度的延續", "Persistence of caste system",
         "種姓不只是宗教習俗，是當代印度的政治現實；選舉民主沒能消除種姓壓迫。"),
        ("冷戰中的南亞", "South Asia in Cold War",
         "1971 孟加拉國戰爭、1998 印巴核試——南亞是冷戰最危險的熱點之一。"),
        ("印度崛起與莫迪時代", "India's rise and Modi era",
         "21 世紀印度的崛起是人口紅利還是制度紅利？莫迪的印度教民族主義有何歷史根源？"),
    ]),
    "HIST2192": ("1800-present", "1800-present", [
        ("殖民的多重形式", "Multiple forms of colonialism",
         "荷蘭、英、法、美、日在東南亞的殖民形式差異極大。"),
        ("東南亞的抵抗運動", "Southeast Asian resistance",
         "從 1945 印尼獨立戰爭到 1975 越戰結束——東南亞抵抗史是 20 世紀去殖民的重要組成。"),
        ("越戰的全球影響", "Global impact of Vietnam War",
         "1955-1975 越戰不只是越南的事；改變了美國社會、冷戰格局、第三世界革命。"),
        ("種族多元性的政治", "Politics of ethnic plurality",
         "印尼、馬來西亞、菲律賓的種族多元既是國家資產也是衝突源。"),
        ("東盟的歷史起源", "Historical origins of ASEAN",
         "1967 東盟成立是去殖民、區域合作、冷戰中立的產物。"),
    ]),
    "HIST2193": ("1800-present", "1800-present", [
        ("煤炭與英國霸權", "Coal and British hegemony",
         "19 世紀英國霸權的物質基礎是煤。"),
        ("石油與 20 世紀地緣政治", "Oil and 20th-century geopolitics",
         "1908 波斯石油、1943 中東司令部、1973 石油危機、2003 伊拉克戰爭——石油定義了 20 世紀戰爭。"),
        ("核武器的恐怖平衡", "Nuclear balance of terror",
         "1945- 核武器把能源武器化到了極致。"),
        ("再生能源的歷史契機", "Historical opportunity of renewables",
         "1970s 石油危機推動了太陽能、風能的早期發展；2020s 氣候危機是第二次契機。"),
        ("能源帝國主義", "Energy imperialism",
         "能源從來不只是技術問題；誰控制能源供應鏈，誰就控制地緣政治。"),
    ]),
    "HIST2202": ("ancient-present", "ancient-present", [
        ("基督教傳播的雙向性", "Bidirectionality of Christian mission",
         "基督教傳播不是單向西方灌輸；亞洲基督徒重塑了信仰（韓國教會、印度教會）。"),
        ("殖民主義與傳教", "Colonialism and missions",
         "傳教士既是帝國工具也是被殖民者教育的橋樑（利瑪竇在中國）。"),
        ("本色化的張力", "Tension of inculturation",
         "基督教要本土化還是保持普世性？這是 21 世紀的核心神學問題。"),
        ("亞洲基督徒的人口學", "Demographics of Asian Christianity",
         "韓國、菲律賓、中國的基督徒人口在 21 世紀急劇增長，重塑了全球基督教版圖。"),
        ("宗教自由與國家主權", "Religious freedom and state sovereignty",
         "宗教自由是普世人權還是西方概念？亞洲國家的宗教治理有獨特模式。"),
    ]),
    "HIST2208": ("200 BCE-1500 CE", "200 BCE-1500 CE", [
        ("絲路的多重路線", "Multiple routes of Silk Road",
         "絲路不只是歐亞陸橋；還有海上絲路、草原絲路、沙漠絲路。"),
        ("物種、商品、疾病", "Species, commodities, diseases",
         "絲路交換的不只是絲綢；小麥、馬、宗教、瘟疫也沿絲路傳播。"),
        ("宗教傳播的絲路路徑", "Silk Road routes of religious transmission",
         "佛教、摩尼教、景教、伊斯蘭教都通過絲路進入中國。"),
        ("蒙古和平的世界意義", "Pax Mongolica's world significance",
         "13-14 世紀蒙古帝國意外促成了歐亞連接，是早期全球化的雛形。"),
        ("絲路敘事的政治化", "Politicization of Silk Road narratives",
         "中國『一帶一路』是當代對絲路的政治化使用。"),
    ]),
    "HIST2212": ("modern", "modern", [
        ("表演作為史料", "Performance as historical source",
         "儀式、戲劇、遊行、慶典——表演是政治權力的視覺化。"),
        ("儀式與權力", "Ritual and power",
         "加冕、葬禮、國慶——儀式建構了政治共同體的想像。"),
        ("戲劇作為政治評論", "Theater as political commentary",
         "從希臘悲劇到貝爾托·布萊希特——戲劇是政治批評的傳統形式。"),
        ("博物館展演的意識形態", "Ideology of museum display",
         "大英博物館的帕特農雕塑、大屠殺紀念館——展覽是國家敘事的視覺化。"),
        ("數字時代的表演", "Performance in digital age",
         "從 TikTok 到 deepfake——數字時代的表演政治是新的。"),
    ]),
    "HIST2213": ("1500-1800", "1500-1800", [
        ("獵巫的社會功能", "Social function of witch hunts",
         "獵巫不只是迷信，是 16-17 世紀歐洲社會轉型的壓力閥。"),
        ("宗教改革的副產品", "Byproduct of Reformation",
         "路德、加爾文的新教倫理把巫術視為異端，直接導致獵巫。"),
        ("魔鬼學的認識論", "Epistemology of demonology",
         "『魔鬼』是怎樣從宗教概念變成法律概念？"),
        ("獵巫與性別", "Witch hunts and gender",
         "75% 的獵巫受害者是女性——這是巧合還是性別壓迫的歷史？"),
        ("現代偏見的史前史", "Prehistory of modern prejudice",
         "獵巫是現代種族主義、宗教偏見的史前史。"),
    ]),
    "HIST2215": ("1492-present", "1492-present", [
        ("哥倫布大交換的生態後果", "Ecological consequences of Columbian exchange",
         "1492 後歐亞病菌殺死 90% 美洲原住民，馬鈴薯、玉米改變了全球飲食。"),
        ("殖民地的資源掠奪", "Resource extraction in colonies",
         "從銀礦到橡膠到石油——殖民地的資源掠奪塑造了現代資本主義。"),
        ("工業革命與環境", "Industrial revolution and environment",
         "1750 後的化石燃料革命不只改變了經濟，也改變了地球大氣。"),
        ("帝國的生態帝國主義", "Ecological imperialism of empires",
         "帝國不只輸出統治，也輸出動植物（澳洲兔子、印度茶葉、英國橡樹）。"),
        ("氣候變遷的歷史責任", "Historical responsibility of climate change",
         "氣候變遷是誰的責任？殖民與工業的歷史責任如何分配？"),
    ]),
    "HIST2220": ("modern", "modern", [
        ("歷史小說作為史料", "Historical fiction as source",
         "歷史小說不是史料，但反映了後人對歷史的想像（司各特、雨果、勒卡雷）。"),
        ("虛構與真實的邊界", "Boundary between fiction and reality",
         "歷史小說怎樣混合事實與虛構？讀者如何分辨？"),
        ("後現代歷史學的挑戰", "Challenge of postmodern historiography",
         "海登·懷特：歷史敘事本質上是文學；客觀性是幻覺。"),
        ("戰爭小說與記憶政治", "War fiction and memory politics",
         "從《西線無戰事》到《殺戮》一場——戰爭小說塑造了國家的戰爭記憶。"),
        ("帝國小說與殖民反思", "Empire fiction and colonial reflection",
         "吉卜林、康拉德、拉什迪——帝國小說如何參與或挑戰殖民敘事？"),
    ]),
    "HIST2222": ("1000-present", "1000-present", [
        ("波斯文明的多元性", "Plurality of Persian civilization",
         "波斯從來不是單一民族國家；波斯人、庫爾德人、阿塞拜疆人共同構成了波斯文化圈。"),
        ("伊斯蘭化與波斯延續", "Islamization and Persian continuity",
         "7 世紀阿拉伯征服後波斯改信伊斯蘭，但波斯語、文學、行政傳統延續至今。"),
        ("薩法維帝國的現代性", "Modernity of Safavid Empire",
         "1501-1736 薩法維把什葉伊斯蘭定為國教，是當代伊朗國家敘事的源頭。"),
        ("英俄大博弈的波斯", "Persia in Great Game",
         "19 世紀英俄爭奪中亞；波斯夾在大博弈中失去主權。"),
        ("1979 革命的歷史深層", "Historical depth of 1979 revolution",
         "1979 伊斯蘭革命不是孤立事件；1906 立憲運動、1953 政變、白色革命是深層背景。"),
    ]),
    "HIST2225": ("1700-present", "1700-present", [
        ("監獄作為現代性發明", "Prison as modern invention",
         "監獄不是古老制度；18 世紀才出現『改造式監禁』的現代概念。"),
        ("規訓與權力", "Discipline and power",
         "傅柯《規訓與懲罰》：監獄是現代規訓權力的縮影。"),
        ("殖民地的監獄", "Prisons in colonies",
         "從澳洲流放地到關塔那摩——監獄是帝國控制邊界人群的工具。"),
        ("政治犯與良心犯", "Political and conscience prisoners",
         "從曼德拉到納瓦尼——政治犯的歷史是反抗史的鏡像。"),
        ("現代監獄的危機", "Crisis of modern prison",
         "美國監禁率全球最高；私人監獄、毒品戰爭、種族不公是當代問題。"),
    ]),
    "HIST2229": ("1760-1830", "1760-1830", [
        ("大西洋革命的多重性", "Plurality of Atlantic revolutions",
         "美國 1776、法國 1789、海地 1804、拉美 1810s-1820s——大西洋革命不是單一事件。"),
        ("海地革命的獨特性", "Uniqueness of Haitian Revolution",
         "1804 海地獨立是世界史上第一次奴隸革命成功建立國家。"),
        ("革命話語的擴散", "Diffusion of revolutionary discourse",
         "盧梭、洛克、潘恩的革命話語如何在大西洋世界擴散？"),
        ("保守主義的反動", "Conservative reaction",
         "梅特涅、神聖同盟、1815 維也納會議——保守主義是 19 世紀的重要潮流。"),
        ("革命的代價與遺產", "Costs and legacy of revolutions",
         "恐怖、戰爭、平等幻滅——大西洋革命的遺產是雙重的。"),
    ]),
    "HIST2230": ("1500-1800", "1500-1800", [
        ("大西洋世界的形成", "Formation of Atlantic world",
         "1500-1800 歐洲、非洲、美洲通過奴隸貿易、商品交換、宗教傳播形成大西洋世界。"),
        ("三角貿易的結構", "Structure of triangular trade",
         "歐洲製造品 → 非洲奴隸 → 美洲種植園 → 糖/煙草/棉花 → 歐洲——三角貿易的殘酷邏輯。"),
        ("早期現代帝國的競爭", "Competition among early modern empires",
         "西、葡、荷、英、法在大西洋的帝國競爭塑造了 16-18 世紀的國際秩序。"),
        ("原住民的抵抗", "Indigenous resistance",
         "從印加到阿茲特克到北美部落——原住民抵抗了 500 年的殖民。"),
        ("大西洋世界的遺產", "Legacy of Atlantic world",
         "種族、奴隸制、資本主義、革命——大西洋世界遺產仍在 21 世紀回響。"),
    ]),
    "HIST2231": ("1700-present", "1700-present", [
        ("美的標準的文化建構", "Cultural construction of beauty standards",
         "美的標準不是自然事實；不同文化、不同時代有不同美的標準。"),
        ("美容產業的帝國基礎", "Imperial basis of beauty industry",
         "美白產品、捲髮護理、化妝品——美容產業的原材料來自帝國的香料、礦物、植物。"),
        ("美的政治", "Politics of beauty",
         "從高跟鞋到束腰到紋身——美的實踐是性別、階級、種族的政治表達。"),
        ("美的視覺化", "Visualization of beauty",
         "從文藝復興油畫到 Instagram——美的視覺化技術不斷演進。"),
        ("美的身體政治", "Body politics of beauty",
         "殘障、肥胖、變性——美的身體政治是當代文化戰爭的核心。"),
    ]),
    "HIST2232": ("1800-present", "1800-present", [
        ("婦女雜誌作為性別史料", "Women's magazines as gender sources",
         "Vogue、Cosmopolitan、中國《婦女雜誌》——婦女雜誌是性別意識形態的視覺化。"),
        ("廣告與消費主義", "Advertising and consumerism",
         "20 世紀消費主義的核心是婦女雜誌的廣告。"),
        ("美與現代性", "Beauty and modernity",
         "20 世紀初婦女雜誌把『現代女性』與特定美學（短髮、煙妝、職業裝）綁定。"),
        ("殖民地與婦女雜誌", "Colonies and women's magazines",
         "印度的婦女雜誌、日本的良妻賢母運動——婦女雜誌是帝國與性別的交匯點。"),
        ("數字時代的婦女雜誌", "Women's magazines in digital age",
         "從紙本到 Instagram、小紅書——婦女雜誌的數字轉型。"),
    ]),
    "HIST2233": ("1500-present", "1500-present", [
        ("全球化的歷史節奏", "Historical rhythms of globalization",
         "全球化不是新現象；1500- 已有全球化，19 世紀加速，20 世紀有起有落。"),
        ("全球史的方法論", "Methodology of global history",
         "全球史是史學的新範式；強調跨地域連接、互動、比較。"),
        ("帝國是全球化的載體", "Empire as vehicle of globalization",
         "葡萄牙、荷蘭、英、美帝國都是全球化的載體——全球化從不中立。"),
        ("抵抗與另類全球化", "Resistance and alternative globalization",
         "反殖民運動、世界社會主義論壇——全球史也有抵抗的傳統。"),
        ("數字全球化", "Digital globalization",
         "1990s 起的數字全球化是當代最深遠的全球連接。"),
    ]),
    "HIST3075": ("research", "research", [
        ("自主研究的方法論", "Methodology of independent research",
         "選題、找資料、批判分析、寫作——自主研究是史學的核心訓練。"),
        ("導師與學生的權力關係", "Power relations between supervisor and student",
         "導師不只是指導者；也是評估者、推薦人，是學術權力的重要節點。"),
        ("研究計畫的設計", "Research proposal design",
         "問題意識、文獻回顧、方法論、章節安排——研究計畫是博士生最重要的訓練。"),
        ("資料的批判使用", "Critical use of sources",
         "史料不是透明的；要用批判方法判斷真偽、立場、局限。"),
        ("學術寫作與發表", "Academic writing and publication",
         "學術寫作是學術共同體的對話；引用、註腳、學術倫理是基本功。"),
    ]),
    "HIST3076": ("1800-present", "1800-present", [
        ("旅遊作為現代性發明", "Tourism as modern invention",
         "Thomas Cook 1841 開創商業旅遊；旅遊是 19 世紀中產階級的新發明。"),
        ("帝國與旅遊", "Empire and tourism",
         "從大旅行（Grand Tour）到殖民地旅遊——旅遊從來是帝國的視角。"),
        ("旅遊與文化想像", "Tourism and cultural imagination",
         "旅遊目的地是被建構的（東方主義、非洲主義）；旅遊者消費的是想像。"),
        ("戰爭紀念旅遊", "War memorial tourism",
         "從諾曼第到廣島——戰爭紀念地是國家記憶政治的場景。"),
        ("生態旅遊的批判", "Critique of ecotourism",
         "生態旅遊承諾可持續，但常常是新殖民的變體。"),
    ]),
    "HIST4017": ("research", "research", [
        ("學位論文作為學術作品", "Dissertation as academic work",
         "博士論文不是書，是研究能力的展示；原創性、方法論、文獻是評估標準。"),
        ("原創性的辯證", "Dialectics of originality",
         "原創性不是發明新東西；是在前人基礎上推進知識邊界。"),
        ("論文題目的選擇", "Choosing dissertation topic",
         "題目要 balance 新穎性、可行性、學術價值、職業方向。"),
        ("田野與檔案", "Fieldwork and archives",
         "歷史研究的兩大方法：田野調查 vs 檔案研究，各有局限。"),
        ("學術共同體的接受", "Acceptance by academic community",
         "論文發表、同行評議、學術會議——學術共同體的接受是研究的最後一步。"),
    ]),
    "HIST4023": ("research", "research", [
        ("歷史研究的方法論光譜", "Methodology spectrum of historical research",
         "政治史、社會史、文化史、經濟史、全球史——研究方法多樣。"),
        ("檔案研究的技藝", "Craft of archival research",
         "找檔案、讀檔案、引用檔案——檔案研究的技藝是史學基本功。"),
        ("量化與質性方法", "Quantitative and qualitative methods",
         "數字 vs 敘事——歷史學越來越多使用量化方法，但仍以質性為主。"),
        ("比較歷史分析", "Comparative historical analysis",
         "比較不同國家、時代、地區——比較方法是史學的傳統方法。"),
        ("歷史敘事的倫理", "Ethics of historical narrative",
         "為誰寫、怎樣寫、寫了給誰看——歷史敘事從不中立。"),
    ]),
    "HIST4024": ("modern", "modern", [
        ("香港史料的多元性", "Plurality of Hong Kong sources",
         "中英政府檔案、商會紀錄、報紙、訪談、地圖、建築——香港史料極其多元。"),
        ("殖民檔案的批判使用", "Critical use of colonial archives",
         "殖民檔案是誰寫的、為誰寫的、遺漏了什麼？批判使用是後殖民史學的核心。"),
        ("口述史與香港身份", "Oral history and Hong Kong identity",
         "1970s 起的口述史計畫（葉靈鳳、鄺健成）建構了香港身份。"),
        ("大眾史學的香港實踐", "Hong Kong practice of public history",
         "從香港歷史博物館到 818 抗爭紀錄——大眾史學是當代香港的重要戰場。"),
        ("香港史與中國史的張力", "Tension between HK history and China history",
         "香港史是大中國史的補充還是獨立敘事？這是當代香港史學的核心辯論。"),
    ]),
    "HIST4028": ("modern", "modern", [
        ("跨國史學的方法", "Methodology of transnational history",
         "跨國史學超越民族國家框架，研究人員、觀念、機構的跨國流動。"),
        ("檔案的跨國視野", "Transnational view of archives",
         "跨國研究需要多國檔案；檔案在哪、用什麼語言寫、誰能讀。"),
        ("比較帝國", "Comparative empires",
         "英、法、荷、美、日帝國的比較是當代史學熱點。"),
        ("無國界史的倫理", "Ethics of borderless history",
         "跨國史學要警惕『無國界』論述背後的西方中心。"),
        ("跨國史的寫作", "Writing transnational history",
         "怎樣在跨國主題上保持敘事連貫性？語言、讀者、學術傳統都影響寫作。"),
    ]),
    "HIST4033": ("modern", "modern", [
        ("博物館作為權力機構", "Museum as institution of power",
         "博物館不只是收藏；是國家敘事、記憶政治、文化權力的展演空間。"),
        ("文物返還的辯論", "Debate over artifact repatriation",
         "大英博物館的帕特農雕塑、故宮的明清檔案——文物返還是 21 世紀核心議題。"),
        ("展覽的策展政治", "Curatorial politics of exhibitions",
         "策展人決定展什麼、不展什麼；展覽的政治從來不中立。"),
        ("大屠殺紀念館的政治", "Politics of Holocaust memorials",
         "猶太人大屠殺紀念館、廣島和平紀念館——大屠殺記憶的展演是政治。"),
        ("數字博物館的未來", "Future of digital museums",
         "從 Google Arts & Culture 到 VR 展覽——數字博物館重塑了文化遺產的存取。"),
    ]),
    "HIST4035": ("professional", "professional", [
        ("歷史學的職業化", "Professionalization of history",
         "歷史學從業餘到專業；檔案管理、博物館、政策研究、教學是當代歷史學的主要職業。"),
        ("實習作為橋樑", "Internship as bridge",
         "博物館、檔案館、出版社、政府實習是進入歷史職業的橋樑。"),
        ("可轉移技能", "Transferable skills",
         "歷史系訓練的可轉移技能：研究、寫作、分析、批判——這些技能在 21 世紀勞動力市場很受歡迎。"),
        ("歷史學的公共角色", "Public role of history",
         "歷史學家不只在大學；也應在公共政策、媒體、社區參與中發聲。"),
        ("歷史學的危機與轉型", "Crisis and transformation of history",
         "人文學科危機、數字史學、公共史學——歷史學在 21 世紀面臨轉型。"),
    ]),
    "HIST4038": ("modern", "modern", [
        ("移民作為歷史主體", "Migrants as historical subjects",
         "移民不是被動受害者；是歷史的主動塑造者。"),
        ("檔案與移民", "Archives and migration",
         "移民的歷史痕跡在哪？海關檔案、護照、照片、社區檔案。"),
        ("香港作為移民城市", "Hong Kong as migrant city",
         "1945- 香港經歷多次移民潮（內戰、1967、1989、2019）；移民是香港的核心經驗。"),
        ("離散華人研究", "Diaspora Chinese studies",
         "王賡武、顏清湟——離散華人研究是 20 世紀史學的重要分支。"),
        ("當代移民政治", "Contemporary migration politics",
         "2010s 起反移民浪潮、特朗普時代、歐洲右翼——移民政治是當代核心議題。"),
    ]),
    "HIST4039": ("modern", "modern", [
        ("音樂產業的帝國基礎", "Imperial basis of music industry",
         "20 世紀音樂產業建立在帝國通訊網絡（電報、無線電、衛星）之上。"),
        ("技術變革與音樂", "Technological change and music",
         "黑膠→磁帶→CD→MP3→串流——技術變革總是重塑音樂產業。"),
        ("音樂與意識形態", "Music and ideology",
         "從納粹的 Wagner 到蘇聯的 Shostakovich 到美國的搖滾——音樂從來是意識形態的工具。"),
        ("全球化音樂", "Global music",
         "K-pop、Latin music、Afrobeats——全球化時代的音樂是跨文化混血。"),
        ("音樂的未來", "Future of music",
         "AI 作曲、區塊鏈版權、AR 演唱會——音樂的未來充滿技術與倫理挑戰。"),
    ]),

    # ===== Harvard Foundations =====
    "GenEd1017": ("1898-present", "1898-present", [
        ("美國作為佔領者的歷史", "US as occupier through history",
         "1898 菲律賓、1945 日本、1945 德國、2003 伊拉克——美國是現代史上最大的佔領者。"),
        ("國家建設的概念史", "Conceptual history of nation-building",
         "nation-building 是 20 世紀的概念，從美國內戰重建到阿富汗戰爭。"),
        ("民主輸出的矛盾", "Contradiction of democracy export",
         "『自由世界』是否應該通過佔領輸出民主？這是美國外交的核心矛盾。"),
        ("佔領文化的批判", "Critique of occupation culture",
         "從好萊塢的『仁慈佔領者』敘事到伊拉克的阿布格萊布——佔領文化的批判。"),
        ("當代佔領的新形式", "New forms of contemporary occupation",
         "從軍事佔領到經濟制裁、數字監控、代理人戰爭——佔領的形式在演化。"),
    ]),
    "GenEd1068": ("1784-present", "1784-present", [
        ("中美關係的長期節奏", "Long rhythm of US-China relations",
         "1784-2025 中美關係 240 年；從貿易到對抗再到競爭，節奏清晰。"),
        ("太平洋共同體的神話", "Myth of Pacific community",
         "19 世紀美國推『太平洋共同體』；實際上是美國主導的太平洋秩序。"),
        ("冷戰在亞洲的熱戰", "Hot wars in Cold War Asia",
         "韓戰、越戰、台海——冷戰在亞洲從未冷過。"),
        ("尼克森衝擊的深層", "Deep layers of Nixon shock",
         "1972 尼克森訪華不只是外交事件；是美國戰略重組、蘇聯困境、中國崛起的多重轉折。"),
        ("21 世紀的中美競爭", "21st century US-China competition",
         "貿易戰、科技戰、台海、南海——21 世紀中美競爭是 21 世紀的核心地緣政治。"),
    ]),
    "GenEd1088": ("1095-1291", "1095-1291", [
        ("十字軍的多重原因", "Multiple causes of Crusades",
         "宗教狂熱、土地飢渴、商業利益、教皇權力——十字軍從不只一個原因。"),
        ("東西文明的相遇", "East-West civilizational encounter",
         "十字軍把歐洲與伊斯蘭世界直接碰撞；誤解、學習、衝突並存。"),
        ("十字軍的暴力與記憶", "Violence and memory of Crusades",
         "1099 耶路撒冷屠殺、1291 阿卡淪陷——十字軍暴力深深刻進歐亞記憶。"),
        ("耶路撒冷的象徵", "Symbolism of Jerusalem",
         "三宗教聖城；十字軍的目標是宗教，但結果是地緣政治。"),
        ("十字軍的當代迴響", "Contemporary reverberations of Crusades",
         "從 911 到 ISIS——十字軍敘事在 21 世紀中東仍在被使用。"),
    ]),
    "GenEd1159": ("1607-present", "1607-present", [
        ("資本主義的多重起源", "Multiple origins of capitalism",
         "Wallerstein、布倫南——資本主義起源有爭議；歐洲不是唯一發源地。"),
        ("奴隸制作為資本主義基礎", "Slavery as capitalist foundation",
         "沒有大西洋奴隸貿易，沒有英美工業革命。"),
        ("工業革命的物質基礎", "Material basis of industrial revolution",
         "煤、鐵、蒸汽機——工業革命的物質基礎是地質學的偶然。"),
        ("美式資本主義的特殊性", "Uniqueness of American capitalism",
         "大政府、大企業、大軍事——美式資本主義是 20 世紀的獨特現象。"),
        ("21 世紀資本主義的危機", "Crisis of 21st-century capitalism",
         "2008 金融危機、2011 佔領華爾街、2020 疫情——資本主義面臨合法性危機。"),
    ]),
    "GenEd1160": ("400-1500", "400-1500", [
        ("中世紀的發明", "Invention of the Middle Ages",
         "中世紀不是『黑暗時代』；是歐洲文明的關鍵形成期。"),
        ("大學的誕生", "Birth of universities",
         "1088 博洛尼亞、1200 牛津——大學是中世紀最重要的制度發明。"),
        ("哥特大教堂的技術革命", "Technical revolution of Gothic cathedrals",
         "尖拱、飛扶壁、玫瑰窗——哥特式是中世紀的技術革命。"),
        ("封建制度的結構", "Structure of feudalism",
         "領主-附庸-農奴——封建制度是歐洲中世紀的政治經濟結構。"),
        ("中世紀的全球視野", "Global view of Middle Ages",
         "中國宋朝、伊斯蘭黃金時代——中世紀的歐洲不是世界中心。"),
    ]),
    "GenEd1206": ("1850-present", "1850-present", [
        ("亞裔美國人的移民節奏", "Immigration rhythms of Asian Americans",
         "從 1850 華工到 1965 移民法案到當代——亞裔美國人經歷多波移民潮。"),
        ("模範少數族裔的神話", "Myth of model minority",
         "1966 報導發明『模範少數族裔』神話；隱藏了亞裔內部的階級、語言、世代差異。"),
        ("排華法的深層邏輯", "Deep logic of Chinese Exclusion",
         "1882 排華法不只是種族歧視；是經濟危機、政治動員、種族意識形態的交匯。"),
        ("日裔集中營的歷史教訓", "Lessons of Japanese internment",
         "1942-1945 拘留日裔美國人是美國民權史上最深的污點之一。"),
        ("當代亞裔政治", "Contemporary Asian American politics",
         "從 2020 疫情歧視到 AAPI 運動——亞裔政治進入新階段。"),
    ]),
    "Hist12": ("colonial-present", "colonial-present", [
        ("陰謀論的歷史深度", "Historical depth of conspiracy theories",
         "從共濟會到光明會到新世界秩序——陰謀論有 300 年歷史。"),
        ("美國政治中的陰謀文化", "Conspiracy culture in US politics",
         "從約翰·威爾克斯·布斯到 JFK 到 QAnon——美國政治的陰謀文化獨特。"),
        ("陰謀論的社會功能", "Social function of conspiracy theories",
         "陰謀論是邊緣群體對權力結構的另類解讀。"),
        ("秘密社會與政治", "Secret societies and politics",
         "從光明會到三K黨到共濟會——秘密社會在政治中扮演複雜角色。"),
        ("數字時代的陰謀論", "Conspiracy theories in digital age",
         "QAnon、Pizzagate、反疫苗——數字時代陰謀論有了新形式。"),
    ]),
    "Hist14": ("1914-1918", "1914-1918", [
        ("一戰的多重原因", "Multiple causes of WWI",
         "同盟體系、軍國主義、帝國主義、種族民族主義——一戰不是單一原因。"),
        ("壕溝戰的技術革命", "Technological revolution of trench warfare",
         "機槍、毒氣、坦克、飛機——一戰是現代戰爭技術的催化劑。"),
        ("凡爾賽體系的遺產", "Legacy of Versailles",
         "1919 凡爾賽條約埋下了二戰的種子；戰爭賠款、領土調整、民族自決的矛盾。"),
        ("帝國解體的開端", "Beginning of imperial collapse",
         "奧斯曼、奧匈、俄羅斯、德意志帝國都在一戰後解體。"),
        ("一戰的全球視野", "Global view of WWI",
         "中國戰場、太平洋殖民地、非洲殖民地——一戰真的是『世界』大戰。"),
    ]),
    "Hist21": ("colonial-present", "colonial-present", [
        ("美國勞工史的種族維度", "Racial dimension of US labor history",
         "奴隸、契約勞工、移民勞工、囚犯勞工——美國勞工史從來是種族史。"),
        ("工會的雙重性", "Duplicity of unions",
         "工會是工人鬥爭的工具，但也常常是種族排斥的機制（AFL 的種族問題）。"),
        ("勞資衝突的暴力", "Violence of labor-capital conflict",
         "從 Homestead 罷工到 Ludlow 大屠殺——勞資衝突常常是暴力。"),
        ("新政與勞工權利", "New Deal and labor rights",
         "1930s 新政是美國勞工權利的奠基，但也排除了家政、農業工人。"),
        ("全球化與美國勞工", "Globalization and US labor",
         "NAFTA、WTO、中國入世——全球化重塑了美國勞工市場。"),
    ]),
    "Hist32A": ("1300-1922", "1300-1922", [
        ("奧斯曼帝國的多元性", "Plurality of Ottoman Empire",
         "奧斯曼帝國統治中東 600 年；米利特制度讓多元宗教共存。"),
        ("伊斯蘭世界的法律多元", "Legal plurality of Islamic world",
         "沙里亞、奧斯曼法、習慣法——伊斯蘭世界從來不是單一法律傳統。"),
        ("奧斯曼與歐洲的關係", "Ottoman-Europe relations",
         "從敵對到協商到現代化——奧斯曼與歐洲的關係塑造了 16-20 世紀的國際秩序。"),
        ("第一次世界大戰的奧斯曼遺產", "WWI's Ottoman legacy",
         "1915 亞美尼亞大屠殺、1920 色佛爾條約、1922 奧斯曼解體——一戰重塑了中東。"),
        ("現代土耳其的歷史建構", "Historical construction of modern Turkey",
         "凱末爾的世俗化改革是當代土耳其國家敘事的核心。"),
    ]),
    "Hist33": ("1933-1945", "1933-1945", [
        ("反猶太主義的歐洲史", "European history of antisemitism",
         "從中世紀宗教歧視到 19 世紀種族反猶——大屠殺的意識形態根源有 1000 年。"),
        ("納粹上台的多重原因", "Multiple causes of Nazi rise",
         "凡爾賽羞辱、1929 大蕭條、魏瑪民主失敗——納粹上台是多重因素的匯聚。"),
        ("大屠殺的獨特性", "Uniqueness of Holocaust",
         "600 萬猶太人；工業化屠殺；國家級別的種族滅絕——大屠殺是現代性的極端表現。"),
        ("旁觀者的責任", "Responsibility of bystanders",
         "美國拒絕接收猶太難民、教廷沉默、瑞士銀行——大屠殺的旁觀者問題。"),
        ("大屠殺記憶的當代政治", "Contemporary politics of Holocaust memory",
         "從 1945 紐倫堡審判到當代否定主義——大屠殺記憶在 21 世紀仍在政治化。"),
    ]),
    "Hist38": ("1894-present", "1894-present", [
        ("中國現代史的斷裂與延續", "Rupture and continuity in modern China",
         "1894- 現代中國的歷史是斷裂（1911、1949）與延續（文化、人口、地理）的辯證。"),
        ("半殖民地的雙重性", "Duplicity of semi-colonialism",
         "1842-1949 中國是半殖民地；既不是完全殖民也不是完全主權。"),
        ("革命與改革的辯證", "Dialectic of revolution and reform",
         "1911 革命 vs 清末新政；1949 革命 vs 改良——革命與改革是中國現代化的兩條路。"),
        ("黨國體制的深層", "Deep structure of party-state",
         "1921 中共成立、1949 建政——黨國體制成為中國政治的核心結構。"),
        ("中國崛起的歷史深層", "Historical depth of China's rise",
         "21 世紀中國崛起不是偶然；是 20 世紀革命 + 改革 + 全球化的累積結果。"),
    ]),
    "Hist46": ("1945-1990", "1945-1990", [
        ("佔領與改造", "Occupation and transformation",
         "1945-1949 盟軍佔領德國；去納粹化、紐倫堡審判、領土重組——佔領不只是軍事。"),
        ("德國分裂的深層原因", "Deep causes of German division",
         "1949 兩個德國不只是冷戰結果；是西方民主化 + 蘇聯佔區差異的產物。"),
        ("經濟奇蹟的條件", "Conditions of economic miracle",
         "1948 馬歇爾計劃、1948 貨幣改革、社會市場經濟——西德奇蹟有具體條件。"),
        ("1968 學生運動的遺產", "Legacy of 1968 student movement",
         "西德 APO、紅軍旅——1968 重塑了西德政治文化。"),
        ("統一與其遺產", "Reunification and its legacy",
         "1990 統一不是歷史終結；是東德經濟崩潰 + 移民問題的開始。"),
    ]),
    "Hist47": ("1947-1991", "1947-1991", [
        ("冷戰的多個戰場", "Multiple Cold War arenas",
         "歐洲、亞洲、非洲、拉美、中東——冷戰從不只美蘇兩個主角。"),
        ("核武器的恐怖平衡", "Nuclear balance of terror",
         "MAD 確保了超級大國不打直接戰；但核擴散仍是 21 世紀的威脅。"),
        ("中蘇分裂的深層", "Deep layers of Sino-Soviet split",
         "1960s 中蘇分裂不只是意識形態；是國家利益、地緣政治、革命路線的深層分歧。"),
        ("美國內政的冷戰化", "Cold War-ization of US domestic politics",
         "麥卡錫、公民權利、1960s 反戰——冷戰深刻影響了美國內政。"),
        ("冷戰的全球文化效應", "Global cultural effects of Cold War",
         "搖滾樂、好萊塢、太空競賽、奧運——冷戰是 20 世紀文化的主導框架。"),
    ]),
    "Hist57": ("1857-present", "1857-present", [
        ("英屬印度的統治結構", "Structure of British Indian rule",
         "1757-1947 英屬印度；東印度公司、皇家殖民政府、分治——印度現代史的起點。"),
        ("分治的暴力", "Violence of partition",
         "1947 印巴分治是 20 世紀最暴力的人口遷移之一；陰影延續至今。"),
        ("民族主義的多元性", "Plurality of nationalism",
         "甘地、尼赫魯、真納——印度民族主義從來不是單一。"),
        ("核武南亞", "Nuclear South Asia",
         "1974 印度核試、1998 印巴核試、2004 戰略對話——南亞是核擴散最危險的熱點。"),
        ("印巴關係的長線", "Long arc of India-Pakistan relations",
         "克什米爾衝突、孟加拉國戰爭、2019 取消查謨-克什米爾特殊地位——印巴關係是當代核心。"),
    ]),
    "Hist66": ("1607-1865", "1607-1865", [
        ("奴隸制作為建國基礎", "Slavery as founding institution",
         "1776 美國建國的 89 位簽字者中 41 位是奴隸主——奴隸制是美國建國的核心。"),
        ("1787 憲法的奴隸制條款", "Slavery clauses of 1787 Constitution",
         "五分之三條款、奴隸貿易條款——憲法從開頭就包含奴隸制。"),
        ("棉花經濟的全球性", "Globality of cotton economy",
         "南方棉花 → 英國紡織廠 → 全球市場——棉花是 19 世紀全球化的核心商品。"),
        ("廢奴運動的長期鬥爭", "Long struggle of abolitionism",
         "從 1830s Garrison 到 1863 林肯——廢奴是美國最長的政治鬥爭。"),
        ("南北戰爭的當代迴響", "Contemporary reverberations of Civil War",
         "從 1619 項目到 BLM 到 Confederate 雕像爭議——南北戰爭在 21 世紀仍未結束。"),
    ]),
    "Hist68": ("1900-2000", "1900-2000", [
        ("美國世紀的概念史", "Conceptual history of American Century",
         "1941 Luce 提出『美國世紀』；這個概念塑造了 20 世紀美國的自我認知。"),
        ("進步主義的雙重性", "Duplicity of progressivism",
         "1900-1920 進步主義既推動社會改革，也常與種族主義、帝國主義交織。"),
        ("羅斯福新政的遺產", "Legacy of New Deal",
         "1933-1938 新政建立了美國現代國家；社會安全、勞動法、金融監管都源於新政。"),
        ("冷戰美國的全球擴張", "Global expansion of Cold War America",
         "1947- 馬歇爾計劃、北約、駐日韓美軍——冷戰把美國變成全球帝國。"),
        ("美國世紀的終結？", "End of American Century?",
         "2008 金融危機、2020 疫情、2021 阿富汗撤軍——美國世紀是否在終結？"),
    ]),
    "Hist70": ("prehistory-1860", "prehistory-1860", [
        ("非洲歷史的全球地位", "Global position of African history",
         "非洲不是邊緣；從人類起源到伊斯黃金時代再到奴隸貿易，非洲是世界史的核心。"),
        ("班圖遷徙的深遠影響", "Far-reaching impact of Bantu migrations",
         "公元前 1000-公元 500 的班圖遷徙塑造了撒哈拉以南非洲的語言、文化、政治。"),
        ("大西洋奴隸貿易的全球影響", "Global impact of Atlantic slave trade",
         "1500-1866 約 1250 萬非洲人被運到美洲；改變了非洲、美洲、歐洲的人口與經濟。"),
        ("伊斯蘭在非洲的角色", "Role of Islam in Africa",
         "從 7 世紀到現代；伊斯蘭是非洲歷史的重要組成。"),
        ("殖民前的非洲國家", "Pre-colonial African states",
         "馬里、桑海、貝南、辛巴威、埃塞俄比亞——殖民前非洲有強大國家。"),
    ]),
}


def build_course_content(code, period_zh, period_en, models):
    """Build full course file content for a course given its metadata."""
    m1, m2, m3, m4, m5 = models
    return f"""# {code}
**{m1[1].split(':')[0] if ':' in m1[1] else m1[1]}**

**學期 / Period**: {period_zh} / {period_en}
**Style**: 袁騰飛式 — 幽默、犀利、聚焦權力與武器如何塑造歷史
**應用出口**：US Military Weapons Project（美國軍事武器在亞洲）

---

## 問題 1：這個領域所有專家共享的 5 個核心心智模型是什麼？
## What are the 5 core mental models every expert shares?

1. **{m1[0]}**  
   {m1[1]}.  
   {m1[2]}

2. **{m2[0]}**  
   {m2[1]}.  
   {m2[2]}

3. **{m3[0]}**  
   {m3[1]}.  
   {m3[2]}

4. **{m4[0]}**  
   {m4[1]}.  
   {m4[2]}

5. **{m5[0]}**  
   {m5[1]}.  
   {m5[2]}

---

## 問題 2：這個領域 3 個最根本的分歧點是什麼？
## What are the 3 fundamental disagreements in this field?

### 分歧 1 / Disagreement 1
**核心問題 / Core question**: {m1[0]} 究竟是現代化引擎還是意識形態的遮羞布？

- **一方觀點 / Side A**: A 派認為 {m1[0]} 是推動 {m1[1].lower()} 的真實動力，要用其邏輯去理解。
- **另一方觀點 / Side B**: B 派認為 {m1[0]} 只是後人建構的敘事，掩蓋了背後的權力鬥爭與武器物質基礎。

### 分歧 2 / Disagreement 2
**核心問題 / Core question**: {m2[0]} 的深層邏輯是普世還是特定？

- **一方觀點 / Side A**: A 派強調 {m2[0]} 的普世性——這是任何現代社會都會經歷的結構性過程。
- **另一方觀點 / Side B**: B 派堅持 {m2[0]} 是特定時代、特定地區的產物，不能簡單套用到其他時空。

### 分歧 3 / Disagreement 3
**核心問題 / Core question**: {m3[0]} vs {m4[0]} — 哪個才是解釋這段歷史的主導框架？

- **一方觀點 / Side A**: A 派主張 {m3[0]} 是主導框架，{m4[0]} 是次要或衍生現象。
- **另一方觀點 / Side B**: B 派堅持 {m4[0]} 才是深層結構，{m3[0]} 只是表面上的事件流。

---

## 問題 3：10 個區分真實理解 vs 死記硬背的深度問題
## 10 deep questions that distinguish real understanding from memorization

1. 為什麼 **{m1[0]}** 是理解這段歷史的第一前提？這個假設如果不成立，整個分析會如何崩塌？
2. **{m2[0]}** 在多大程度上決定了這段歷史的核心走向？歷史上有哪些反例挑戰這個邏輯？
3. **{m3[0]}** 與 **{m4[0]}** 之間的張力如何形塑了 {period_zh} 的關鍵轉折？
4. 如果把 **{m5[0]}** 抽離出來，這段歷史會變成什麼樣的故事？哪些事件其實是 noise？
5. 在這段時期中，哪個領導人、事件或文本最能代表 **{m1[0]}** 的極致展現？
6. 學者之間關於 **{m2[0]}** 的爭論，在多大程度上反映了史料解釋的差異 vs 意識形態的對抗？
7. 對這段歷史而言，『帝國主義』是分析的核心還是後人強加的框架？
8. 從 US Military Weapons Project 角度，{period_zh} 的哪些節點直接決定了美軍在亞洲的部署邏輯？
9. 如果你是當時的決策者，面對 **{m3[0]}** 與 **{m4[0]}** 的衝突，你會選擇哪個？理由是什麼？
10. 在當代中美對抗背景下，{period_zh} 的哪些歷史經驗正在重演？哪些已經過時？

---

# 核心心智模型深化（中英對照）

## 1. {m1[0]} / {m1[1]}

### 1.1 Bilingual 概念對照
| 英文概念 | 中英對照 | 歷史含義 | 武器 / 軍事應用 |
|---|---|---|---|
| {m1[0]} | {m1[0]} | 核心定義：{m1[2]} | 軍備競賽、戰略部署 |
| Period dynamics | 時代動力 | {period_zh} 特徵 | 戰略選擇 |
| Power relations | 權力關係 | 帝國 vs 殖民 | 強制工具 |
| Historical agency | 歷史能動性 | 領導人 vs 結構 | 自主決策 |
| Material basis | 物質基礎 | 武器、資金、技術 | 戰鬥力 |

### 1.2 史料與考據 / Sources and criticism
- **主要史料**：當時官方檔案、外交文書、報紙、書信、回憶錄
- **後世研究**：歷史學家如錢穆、史景遷、霍布斯鮑姆、Philip Kuhn、Pinker 的觀點
- **學術爭論**：哪些史料可信、哪些被後人建構、哪些需要去殖民化重讀

### 1.3 袁騰飛式犀利觀察 / Sharp observation
講 {m1[0]} 不能只講故事，要看『誰贏了、誰輸了、武器怎麼重塑了這個時代』。
很多教科書把 {m1[1].lower()} 講成偉人故事，忽略了背後的權力結構和物質基礎。
真正的史學家會問：哪個國家掌握了最新的武器？哪條貿易路線被誰控制？誰的軍費佔 GDP 最高？

### 1.4 Deep test question
- 請舉出歷史上 {m1[0]} 的兩個極端案例，並分析其後果
- 如果抽離 {m1[0]}，這段歷史的核心敘事會怎樣崩塌？
- 從軍事 / 武器角度，{m1[0]} 怎樣決定了 {period_zh} 的地緣政治？

### 1.5 圖解 / Diagram
```mermaid
graph TD
    A[{m1[0]} 1] --> B[Power structure]
    B --> C[Weapons / resources]
    C --> D[Outcome 1]
    C --> E[Outcome 2]
    C --> F[Outcome 3]
    D --> G[Historical trajectory]
    E --> G
    F --> G
```

---

## 2. {m2[0]} / {m2[1]}

### 2.1 Bilingual 概念對照
| 英文概念 | 中英對照 | 歷史含義 | 武器 / 軍事應用 |
|---|---|---|---|
| {m2[0]} | {m2[0]} | 核心定義：{m2[2]} | 地緣政治影響 |
| Imperial reach | 帝國觸角 | 控制範圍 | 海軍、基地 |
| Comparative power | 對比實力 | 帝國 vs 對手 | 武器代差 |
| Strategic culture | 戰略文化 | 怎樣打仗 | 軍事傳統 |
| Economic base | 經濟基礎 | 財稅、貿易 | 軍費開支 |

### 2.2 史料與考據
- **檔案**：海軍部、國務院、軍部解密檔案
- **二手研究**：外交史、軍事史、帝國史學派的對話
- **爭論**：修昔底德陷阱、現實主義 vs 自由主義的解釋

### 2.3 袁騰飛式犀利觀察
講 {m2[0]} 要看槍、錢、人三件套。
帝國從來不是靠理念擴張的；是靠加農炮、打開市場、駐軍維持。
讀帝國史要跟着錢走，錢到哪裡，帝國就到哪裡。

### 2.4 Deep test question
- {m2[0]} 的兩個極端案例是什麼？結果如何？
- 抽離 {m2[0]} 後，這段歷史會怎樣被重寫？
- 在 {period_zh} 中，{m2[0]} 怎樣決定了戰略選擇？

### 2.5 圖解
```mermaid
graph TD
    A[{m2[0]}] --> B[Material base]
    B --> C[Military capability]
    C --> D[Strategic outcome]
    D --> E[Imperial expansion]
    D --> F[Resistance]
    E --> G[New order]
    F --> G
```

---

## 3. {m3[0]} / {m3[1]}

### 3.1 Bilingual 概念對照
| 英文概念 | 中英對照 | 歷史含義 | 武器 / 軍事應用 |
|---|---|---|---|
| {m3[0]} | {m3[0]} | 核心定義：{m3[2]} | 內部 / 外部衝突 |
| Revolution | 革命 | 結構性轉變 | 內戰、解放戰爭 |
| Counter-revolution | 反革命 | 保守反擊 | 鎮壓、清洗 |
| Ideology | 意識形態 | 動員工具 | 政治宣傳 |
| Mobilization | 動員 | 群眾、軍隊 | 兵源、後勤 |

### 3.2 史料與考據
- **檔案**：黨派文件、宣言、秘密警察檔案
- **後世研究**：革命史學派、社會史學派、後殖民批評
- **爭論**：革命的必然性 vs 偶然性、領導人 vs 群眾

### 3.3 袁騰飛式犀利觀察
講 {m3[0]} 要看哪個階級贏了、哪個階級輸了。
革命從來不是請客吃飯；是把舊秩序的屍體埋下去，新秩序才能站起來。
教科書喜歡講理念；真正的史學家要算誰的槍多、誰的錢多、誰的盟友多。

### 3.4 Deep test question
- {m3[0]} 的深層動力是意識形態還是物質利益？
- 在 {period_zh} 中，{m3[0]} 的關鍵轉折點是什麼？
- 如果抽離 {m3[0]}，這段歷史會怎樣改寫？

### 3.5 圖解
```mermaid
graph TD
    A[Old order] --> B[Crisis]
    B --> C[Revolutionary moment]
    C --> D[Force 1]
    C --> E[Force 2]
    C --> F[Force 3]
    D --> G[New order]
    E --> G
    F --> G
```

---

## 4. {m4[0]} / {m4[1]}

### 4.1 Bilingual 概念對照
| 英文概念 | 中英對照 | 歷史含義 | 武器 / 軍事應用 |
|---|---|---|---|
| {m4[0]} | {m4[0]} | 核心定義：{m4[2]} | 國家安全、軍備 |
| Security dilemma | 安全困境 | 增強軍備反而更不安全 | 軍備競賽 |
| Alliance system | 聯盟體系 | 集體安全 | 北約、華約 |
| Deterrence | 威懾 | 不戰而屈人之兵 | 核武、導彈 |
| Balance of power | 權力平衡 | 均勢外交 | 結盟、調停 |

### 4.2 史料與考據
- **檔案**：軍事情報、決策備忘、外交密電
- **後世研究**：現實主義、攻勢現實主義、防禦現實主義的辯論
- **爭論**：結構現實主義 vs 建構主義 vs 自由主義

### 4.3 袁騰飛式犀利觀察
講 {m4[0]} 要明白：國家之間沒有永遠的朋友，只有永遠的利益。
最會算的戰略家能預判對手的下一步。
讀國際關係史要數每個國家的坦克、飛彈、核彈頭；這些數字比任何宣言都實在。

### 4.4 Deep test question
- 在 {period_zh} 中，{m4[0]} 怎樣決定了國際格局？
- 哪些歷史事件證明 {m4[0]} 失效？哪些證明其有效？
- 從 US Military Weapons Project 角度，{m4[0]} 怎樣形塑了美軍亞洲部署？

### 4.5 圖解
```mermaid
graph TD
    A[State A] --> B[Build arms]
    B --> C[State B reacts]
    C --> D[State A reacts]
    D --> E[Arms race]
    E --> F{Détente?}
    F -->|Yes| G[Negotiation]
    F -->|No| H[Conflict]
```

---

## 5. {m5[0]} / {m5[1]}

### 5.1 Bilingual 概念對照
| 英文概念 | 中英對照 | 歷史含義 | 武器 / 軍事應用 |
|---|---|---|---|
| {m5[0]} | {m5[0]} | 核心定義：{m5[2]} | 治理、抵抗 |
| Memory politics | 記憶政治 | 誰記得、怎樣記得 | 紀念館、教科書 |
| Historiography | 史學方法 | 怎樣寫歷史 | 學術機構、出版 |
| Public history | 公共史學 | 對公眾講歷史 | 博物館、媒體 |
| Counter-memory | 反記憶 | 邊緣群體的歷史 | 另類敘事 |

### 5.2 史料與考據
- **檔案**：教學大綱、教科書、紀念館檔案
- **後世研究**：Hayden White 後現代史學、Michel Foucault 知識考古學
- **爭論**：客觀性是否可能、敘事 vs 分析、業餘 vs 專業

### 5.3 袁騰飛式犀利觀察
講 {m5[0]} 要看：誰掌握了歷史的書寫權，誰就掌握了未來。
歷史從來不是中立的教科書；每個時代的史學都是當代政治的延伸。
袁老師曰：教科書是統治者的工具；批判閱讀才是史學家的修養。

### 5.4 Deep test question
- {m5[0]} 怎樣形塑了當代我們對 {period_zh} 的理解？
- 哪些歷史敘事被後人建構、哪些有堅實證據？
- 從 US Military Weapons Project 角度，{m5[0]} 怎樣影響美軍史學？

### 5.5 圖解
```mermaid
graph TD
    A[Power] --> B[Write history]
    B --> C[School textbooks]
    C --> D[Public memory]
    D --> E[Identity]
    E --> F[Legitimacy]
```

---

# 深度自測問題詳解（中英對照）

## 詳解 1: 推導核心論點 / Derive the core argument
**Q1.** 如何從史料推導出歷史學家的核心論點？

**Answer / 答案**: 閱讀多個學派觀點，識別共同假設與分歧。比較 1980s vs 2020s 學術研究，識別時代變遷對史學的影響。批判性閱讀 5-10 篇核心文獻，找出重複出現的議題。

**袁騰飛式點評 / Sharp commentary**: 歷史不是死記硬背，是看清楚『誰在什麼時候、用了什麼手段、達到了什麼目的』。把這套方法應用到 {period_zh}，很多迷思就解開了。

**工程 / 戰略應用 / Engineering implication**: 對 US Military Weapons Project 而言，這個方法幫助識別美軍亞洲部署的深層邏輯——不是『保護盟友』，而是『維持前沿部署、控制海上通道、圍堵對手』。

---

## 詳解 2: 識別偏見與史料批判 / Identify bias and source criticism
**Q2.** 面對一份檔案，如何識別其偏見？

**Answer / 答案**: 分析作者立場、時代背景、讀者預期、遺漏的內容。問：誰寫的、為誰寫、什麼時候寫、為什麼寫。對比多份檔案，識別沉默與缺席。

**袁騰飛式點評 / Sharp commentary**: 史料批判的基本功：把同一件事找 5 個來源的記錄對比，誰的版本在場、誰的缺席，立刻清楚。
黨派檔案 vs 外交檔案 vs 私人書信——三個視角，故事就立體了。

**工程 / 戰略應用**: 對美軍研究而言，DARPA 報告、國防部解密檔案、退役軍官回憶錄——三類材料要交叉讀，才不會被一方敘事帶偏。

---

## 詳解 3: 應用到當代案例 / Apply to contemporary case
**Q3.** {period_zh} 的歷史經驗如何理解當代中美關係？

**Answer / 答案**: 識別結構相似性：崛起大國 vs 守成大國、技術變革、意識形態對抗、地緣政治競爭。Thucydides 陷阱、權力轉移理論、修昔底德 2.0 是相關分析框架。

**袁騰飛式點評 / Sharp commentary**: 歷史不是命運；但歷史告訴我們，當崛起大國的 GDP 達到守成大國 60% 以上，衝突概率飆升。當代中美正是這個結構。

**工程 / 戰略應用**: 對美軍亞太部署而言，2014 以來的『重返亞太』、AUKUS、QUAD 都是 19 世紀末『大博弈』的 21 世紀重演。

---

## 詳解 4: 比較不同視角 / Compare perspectives
**Q4.** 西方史學與中國史學對同一事件的不同解讀是什麼？

**Answer / 答案**: 翻譯 / 文化框架 / 史料使用 / 當代政治背景。中華人民共和國 vs 中華民國 vs 美國 vs 日本史學對 1937-1945 的解讀截然不同。

**袁騰飛式點評 / Sharp commentary**: 看史學要看『為誰服務』。教科書的差異背後是當代國家的政治需要。
史學沒有純客觀；但史學家可以做到誠實——把所有證據攤開，結論讓讀者自己判。

**工程 / 戰略應用**: 對美軍研究而言，要看美國官方史學 + 對手國家史學 + 第三方史學，三方對照才見全貌。

---

## 詳解 5: 反事實分析 / Counterfactual analysis
**Q5.** 如果一個關鍵事件沒發生，後續會如何？

**Answer / 答案**: 建構假設場景：替換領導人、改變戰略、引入新技術。例如：如果 1949 國民黨贏了國共內戰，當代東亞格局會怎樣？

**袁騰飛式點評 / Sharp commentary**: 反事實是史學的實驗室。把關鍵變量抽離，看後續如何崩塌。
真正的史學家敢做反事實；平庸的史學家只會按時間順序抄。

**工程 / 戰略應用**: 對美軍戰略規劃而言，反事實分析是標準工具：模擬對手決策、評估替代方案。

---

## 詳解 6: 時代劃分批判 / Periodization critique
**Q6.** 傳統的時代劃分（古代 / 近代 / 現代）合理嗎？

**Answer / 答案**: 挑戰歐洲中心、識別多元時間性、提問誰的標準。『古代』在哪個地區？中國的『近代』是 1840？日本是 1868？韓國是 1910？

**袁騰飛式點評 / Sharp commentary**: 時代劃分是史學家的權力——誰有能力定義時代邊界，誰就掌握了歷史的解釋權。
警惕西方中心史學：拿歐洲的『古代 / 近代 / 現代』套到中國、非洲、拉美，一定格格不入。

**工程 / 戰略應用**: 對美軍戰略而言，時代劃分是規劃的起點：定義『當前戰略環境』才能推導未來 5-20 年的部署。

---

## 詳解 7: 能動性 vs 結構 / Agency vs structure
**Q7.** 歷史是英雄創造還是結構決定？

**Answer / 答案**: 辯證分析：結構限制下的能動性，個人突破結構的瞬間。邱吉爾、列寧、毛澤東、鄧小平——這些人改變了歷史，但他們的行動空間受結構限制。

**袁騰飛式點評 / Sharp commentary**: 把歷史完全歸結為結構決定論是懶人的做法；把歷史完全歸結為英雄史是宣傳的做法。
史學家要看：什麼條件下英雄能改變歷史？什麼條件下結構決定一切？

**工程 / 戰策應用**: 對美軍決策而言，領導人個性能在短期改變戰略，但結構（地理位置、經濟實力、人口）決定長期走向。

---

## 詳解 8: 記憶政治 / Memory politics
**Q8.** 同一事件為什麼在不同國家被記住得不同？

**Answer / 答案**: 教科書、紀念館、電影、政治動員。廣島 vs 長崎、南京大屠殺的不同記憶、靖國神社問題——記憶是政治工具。

**袁騰飛式點評 / Sharp commentary**: 歷史是死的，記憶是活的；誰控制了記憶的生產，誰就控制了未來。
一個國家選擇記住什麼、不記住什麼，比事件本身更重要。

**工程 / 戰策應用**: 對美軍公共外交而言，越戰紀念館、阿富汗戰爭記憶、伊拉克戰爭反思——美國如何記憶戰爭直接影響未來兵力部署。

---

## 詳解 9: 軍事 / 武器維度 / Military / weapons dimension
**Q9.** 這段歷史對美軍在亞洲部署有何深遠影響？

**Answer / 答案**: 識別關鍵節點：技術變革（黑火藥到核武）、戰略文化（陸軍 vs 海軍）、聯盟體系（美日、美韓、美菲、美澳）、基地網絡（橫須賀、沖繩、關島、迪戈加西亞）。

**袁騰飛式點評 / Sharp commentary**: 教科書講理念，戰略家看地圖；地圖上每一個基地背後都是 100 年的政治交易。
1898 菲律賓 → 1945 日本 → 1950 韓戰 → 1965 越戰 → 2020 AUKUS：130 年的亞洲部署有深層邏輯。

**工程 / 戰策應用**: 對 US Military Weapons Project 而言，這個歷史維度決定了當代美軍前沿部署的合理性——為什麼關島？為什麼橫須賀？為什麼新加坡？

---

## 詳解 10: 溝通與綜合 / Communication and synthesis
**Q10.** 如何用 5 分鐘向非專家解釋這段歷史的核心？

**Answer / 答案**: 故事 + 人物 + 衝突 + 當代迴響。一個關鍵事件、一個關鍵人物、一個關鍵衝突、一個當代共鳴。

**袁騰飛式點評 / Sharp commentary**: 史學家的本事是『把複雜的東西講簡單，把簡單的東西講透徹』。
能用 5 分鐘講清楚一段歷史的人，才真正懂那段歷史；講不清楚的，是因為他自己也沒懂。

**工程 / 戰策應用**: 對美軍決策簡報而言，5 分鐘簡報是基本功：背景、問題、方案、風險、建議。

---

# 5 個 Mermaid 圖解 / 5 Mermaid Diagrams

## 📊 Diagram 1: 時代地圖 / Period Map
```mermaid
graph LR
    A[Pre-{period_zh.split('-')[0]}] --> B[{period_zh}]
    B --> C[Modern era]
    C --> D[21st century]
    D --> E[Future]
```

## 📊 Diagram 2: 權力結構 / Power Structure
```mermaid
graph TD
    A[Elite / 精英] --> B[Military / 軍事]
    A --> C[Capital / 資本]
    A --> D[Ideology / 意識形態]
    B --> E[Coercion / 強制]
    C --> F[Material / 物質]
    D --> G[Consent / 共識]
    E --> H[Power]
    F --> H
    G --> H
```

## 📊 Diagram 3: 武器演進 / Weapons Evolution
```mermaid
graph TD
    A[Musket 火槍] --> B[Rifle 步槍]
    B --> C[Machine gun 機槍]
    C --> D[Tank 坦克]
    D --> E[Aircraft 飛機]
    E --> F[Nuclear 核武]
    F --> G[Cyber 網絡]
    G --> H[AI 人工智能]
```

## 📊 Diagram 4: 美軍亞洲部署 / US Military in Asia
```mermaid
graph TD
    A[1898 Philippines] --> B[1945 Japan/Korea]
    B --> C[1950s Taiwan/Philippines]
    C --> D[1965 Vietnam]
    D --> E[1980s Philippines bases]
    E --> F[1991 Subic closure]
    F --> G[2010s Rebalance]
    G --> H[2020s AUKUS/QUAD]
```

## 📊 Diagram 5: 史料批判流程 / Source Criticism
```mermaid
flowchart TD
    A[Source / 史料] --> Q{{"Authentic? 真實?"}}
    Q -->|Yes| B[Author? 作者]
    Q -->|No| Z[Discard]
    B --> R{{"Context? 時代背景"}}
    R -->|Known| C[Cross-check 交叉驗證]
    R -->|Unknown| Y[Mark uncertain]
    C --> D[Triangulate 三角驗證]
    D --> E[Conclusion 結論]
```

---

# 總結 / Closing 5-Point Deep Insights

1. **權力結構永遠比意識形態更持久**：這段歷史的驅動力是誰掌握了槍、錢、人；不是宣言、不是理念。
2. **帝國的擴張和收縮都有物質基礎**：不只是理念，更是武器、能源、後勤的問題。
3. **歷史學家的分歧往往反映當代政治**：看史料要理解誰在為誰說話；學派之爭背後是時代之爭。
4. **美軍在亞洲的部署有 130 年深層邏輯**：從菲律賓到 AUKUS 不是新現象，是帝國節奏的當代延續。
5. **袁騰飛式觀點：歷史不是教科書，是看懂『誰在什麼時候、用了什麼手段、達到了什麼目的』的訓練**。

**自學建議 / Study tips**: 配合本課核心教科書 + Harvard 課程視頻 + 中英對照史料，輸出讀書筆記到 `06_Reading_Notes/`。
**Application**: 所有內容最終應用於 US Military Weapons Project——識別 {period_zh} 中美軍亞洲部署的歷史深層邏輯。
"""


def main():
    repo_root = Path("/workspace/HKU-Harvard-History-Self-Study")
    course_dirs = [
        repo_root / "01_HKU_Courses",
        repo_root / "02_Harvard_Courses" / "101_Foundations",
        repo_root / "02_Harvard_Courses" / "Fall_Courses",
    ]
    updated = 0
    skipped = 0
    for course_dir in course_dirs:
        if not course_dir.exists():
            print(f"Skip missing: {course_dir}")
            continue
        for f in sorted(course_dir.glob("*.md")):
            # Extract course code from filename
            stem = f.stem
            # Try to find a course code
            code = None
            for c in COURSES:
                if c in stem:
                    code = c
                    break
            if not code:
                print(f"No course data: {f.name}")
                skipped += 1
                continue
            period_zh, period_en, models = COURSES[code]
            new_content = build_course_content(code, period_zh, period_en, models)
            f.write_text(new_content, encoding="utf-8")
            print(f"Updated: {f.relative_to(repo_root)}")
            updated += 1
    print(f"\nSummary: {updated} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
