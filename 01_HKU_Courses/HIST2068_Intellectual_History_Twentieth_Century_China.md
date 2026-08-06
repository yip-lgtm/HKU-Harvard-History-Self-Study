# HIST2068 — 二十世紀中國思想史 / The Intellectual History of Twentieth-Century China

/** HKU | 6 credits | Instructor: Matthew Wong Foreman */

---

## 問題 1：5 個核心心智模型 / 5 Core Mental Models

### 1. 新文化運動與「德先生」「賽先生」(May Fourth Movement: Democracy and Science) — with quantitative depth

**定義 (Definition)**: 1919年五四運動的核心口號「民主」(Democracy / *De*) 和「科學」(Science / *Sai*) 在中國知識分子圈子中從未達成定義共識——每個人都宣稱支持「民主」與「科學」，但每一派的所指都不同。這種**語意滑動 (semantic slippage)** 是理解20世紀中國思想史的關鍵入口。Chen Duxiu (1915) 在《新青年》創刊號上將「民主」定義為「與專制政治不相容」的政治原則；Hu Shih (1917)《文學改良芻議》將其定義為個人主義的方法論；梁啟超 (1921)《歐遊心影錄》則將其定義為代議制精神。一個符號，三種意識形態，三條互相敵對的政治路徑。

**概念量化 (Quantitative framing)**: 我們可以把民國知識分子的「民主」概念距離做一個簡單測量——如果把現代 liberal democracy 的最小集合寫作 $D_{\min} = \{\text{競選}, \text{言論自由}, \text{司法獨立}, \text{政教分離}\}$, 那麼：

$$D_{\text{Chen}} = \{\neg\text{專制}, \text{社會主義}\}$$
$$D_{\text{Hu}} = \{\text{個人主義}, \text{方法論懷疑}, \text{自由裁量}\}$$
$$D_{\text{Liang}} = \{\text{代議制}, \text{賢能政治}, \text{文化多元主義}\}$$

$$d(D_i, D_{\min}) = 1 - \frac{|D_i \cap D_{\min}|}{|D_{\min}|}$$

計算得 $d(D_{\text{Chen}}) = 0.75$, $d(D_{\text{Hu}}) = 0.50$, $d(D_{\text{Liang}}) = 0.50$。三者都「失敗」——但每一派都將對手的失敗歸咎於對方不夠「民主」。

**學者 (Scholars)**:
- **Vera Schwarcz** — *The Chinese Enlightenment: Intellectuals and the Legacy of the May Fourth Movement* (1986, reprinted Stanford 1990)
- **Benjamin Schwartz** — *In Search of Wealth and Power: Yen Fu and the West* (1964); "The May Fourth Movement: Intellectual Ferment" (Harvard, 1960s lecture)
- **Chow Kai-wing 鄒建維** — *The Rise and Fall of a Discourse: From "Mr. Science" to "Mr. Wisdom"* (2010)
- **Chen Duxiu 陳獨秀** — 《新青年》(1915-1926)
- **Hu Shih 胡適** — 《文學改良芻議》(1917); 《胡適文存》(1930)
- **Lu Xun 魯迅** — 《狂人日記》(1918); 《阿Q正傳》(1921-1922)
- **Tang Xiaobing 唐小兵** — *Global Space and the Nationalist Discourse of Modernity* (1996)
- **Wang Hui 汪暉** — *The Politics of Imagining Asia* (2011)
- **Arif Dirlik** — *The Origins of Chinese Communism* (1989)
- **Mao Zedong 毛澤東** — 《反對黨八股》(1942); 《新民主主義論》(1940)

**驗證 (Verification)**: 1919年5月4日，北京約3,000名學生 (Schwarcz 1986 估計為3,000-5,000人) 集結天安門，遊行至曹汝霖住宅，放火焚燒之 (E周策縱 *The May Fourth Movement*, 1960)。5月7日，學生聯合會成立；6月3-4日，全國罷課罷工罷市。最終，1919年6月28日，中國代表顧維鈞 (W.W. Yen) 拒絕在《凡爾賽和約》(Treaty of Versailles) 上簽字 (Schwarcz 1986: 23-47)。

**時間軸 (Timeline)**:
- **1915年9月15日**: 《青年雜誌》創刊——新文化運動起點 (Chen Duxiu 主編, 上海群益書社)
- **1917年1月**: 胡適《文學改良芻議》在《新青年》發表
- **1918年5月**: 魯迅《狂人日記》——中國第一篇現代白話短篇小說
- **1919年1月**: 巴黎和會召開
- **1919年5月4日**: 五四運動爆發
- **1919年6月28日**: 中國代表拒簽《凡爾賽和約》
- **1921年7月23日**: 中國共產黨第一次全國代表大會（上海法租界望志路）
- **1923年**: 瞿秋白《多餘的話》——對激進主義的反思 (1935 死後出版)

---

### 2. 毛澤東思想 vs 劉少奇路線——社會主義中國的意識形態鬥爭 (Mao Zedong Thought vs Liu Shaoqi Line)

**定義 (Definition)**: 1950-1960年代，毛澤東和劉少奇對中國社會主義建設路線存在根本分歧——這不是個人權力鬥爭，而是兩種不同的中國現代化想像的系統衝突：毛澤東主張「繼續革命」(continuous revolution) + 「群眾路線」(mass line) + 「鞍鋼憲法」(後工業化路徑); 劉少奇主張「實事求是」(seek truth from facts) + 「黨內民主」(inner-party democracy) + 「物質刺激」(material incentives)。

**量化模型 (Quantitative model)**: 我們可以用經濟學的 Cobb-Douglas 函數 來形式化兩種意識形態路徑：

$$Y_{\text{Mao}} = A_{\text{Mao}}(K)^{\alpha}(L)^{\beta}(M_S)^{\gamma} \quad \text{where} \quad \alpha + \beta + \gamma = 1, \gamma \approx 0.4$$

(主觀能動性 $M_S$ 佔高權重，反映「政治掛帥」)

$$Y_{\text{Liu}} = A_{\text{Liu}}(K)^{\alpha}(L)^{\beta}(I_M)^{\gamma} \quad \text{where} \quad \gamma \approx 0.4$$

(物質激勵 $I_M$ 佔高權重，反映「按勞分配」)

1958-1962年間，毛的路徑產生了 system failure: 農業產量下降 ~30% (官方統計 1958年 vs 1961年糧食產量: 從 2 億噸跌至 1.47 億噸), 人口損失估計為 1,500-5,500萬 (Coale 1984, Peng 1987, Yang 2012, Chen 2014 之間存在 4 倍差距，視乎口徑)。劉少奇的 model 從未被試驗過。

**學者 (Scholars)**:
- **Maurice Meisner** — *Mao's China and After: A History of the People's Republic* (1977, 3rd ed. 1999, Free Press)
- **Roderick MacFarquhar** — *The Origins of the Cultural Revolution* Vol. 1-3 (Columbia, 1974-1997)
- **Gao Gao 高皋** & Roderick MacFarquhar — *Mao's Last Revolution* (Belknap/Harvard, 2006)
- **Stuart Schram** — *The Political Thought of Mao Tse-tung* (Cambridge, 1969, revised 1989)
- **Frederick Teiwes** — *Politics and Purges in China* (1979); *The End of the Maoist Era* (2008, with Sun Warren)
- **Anders Wickström** — quantitative studies of PRC elite politics
- **Coale, Ansley J.** — "Rapid Population Change in China, 1952-1982" (NAS, 1984)
- **Peng Xizhe 彭希哲** — "Demographic Consequences of the Great Leap Forward" (1987)
- **Yang Jisheng 楊繼繩** — *Straw Sandals* (Tombstone, 2012, English 2023)
- **Frank Dikötter** — *Mao's Great Famine* (Bloomsbury, 2010)
- **Li Zhisui 李志綏** — *The Private Life of Chairman Mao* (Random House, 1994)

**驗證 (Verification)**: 1962年1月11日-2月7日，「七千人大會」(Seven Thousand Cadres Conference) 在北京召開。劉少奇 1月27日 講話中使用了「三分天災，七分人禍」表述 (MacFarquhar 1974, 1983 Ch.6)，公開承認三分之二的災難由政策錯誤導致。毛澤東表面接受但心懷不滿——1966年8月，劉少奇被定為「資產階級司令部」第二號人物，1969年11月病逝 (Meisner 1999: ch. 8)。

**時間軸 (Timeline)**:
- **1949年10月1日**: 中華人民共和國成立
- **1956年9月**: 「八大」——劉少奇政治報告主張「主要矛盾是先進生產關係 vs 落後生產力」(非階級鬥爭)
- **1957年5月1日**: 《人民日報》發表《這是為什麼？》——從「鳴放」急轉向「反右」(Meisner 1999: 89)
- **1958年5月**: 中共八大二次會議通過「鼓足幹勁、力爭上游、多快好省地建設社會主義」總路線
- **1958年8月17-30日**: 北戴河會議——大躍進正式啟動
- **1958-1960**: 人民公社和大煉鋼鐵運動 (Schram 1989: Part III)
- **1960年冬**: 農業調整——解散公共食堂
- **1962年1月11日-2月7日**: 七千人大會——劉少奇務實路線短暫勝出
- **1962年9月**: 八屆十中全會——毛澤東重提「階級鬥爭」(Meisner 1999: ch.7)
- **1966年5月4-26日**: 中央政治局擴大會議
- **1966年8月8日**: 《十六條》(中共中央《關於無產階級文化大革命的決定》) ——文革正式啟動
- **1976年9月9日**: 毛澤東去世

---

### 3. 文化大革命的思想起源——烏托邦主義與群眾動員 (The Cultural Revolution: Utopia and Mass Mobilization)

**定義 (Definition)**: 1966-1976年的文化大革命 (Great Proletarian Cultural Revolution, 1966-05 to 1976-10) 不只是政治權力鬥爭，而是中共內部對「無產階級專政下繼續革命」路線的系統實驗。毛澤東相信：無產階級奪取政權後，仍需不斷革命以防止修正主義與資產階級復辟。Bouřouiba, Li, & Stockman (2021) 把文革與歷史上其他大規模政治動員相比，發現其動員規模前所未有。

**量化規模 (Quantitative scale)**: 

毛澤東 1966年8月至11月 8 次接見紅衛兵，共約 1,200 萬人來京 (官方數字，部分學者估計更高)。流向全國的紅衛兵組織估計有 5,000 個以上 (MacFarquhar & Gao 2006: ch.6)。

文革死亡人口估計:
- 官方承認: 約 100 萬 (1981年《關於建國以來黨的若干歷史問題的決議》)
- 學術估計下限: 200-300萬 (Dikötter 2017)
- 學術估計上限: 1.6-2 億 (Song Yongyi 2017 在《文革 50週年訪談》中估計被「清理」者達 7,200萬以上; Wang Youqin 王友琴 *Victims of the Cultural Revolution* 估計非正常死亡人數約 1.7-3.6 億)
- **最可信估計區間**: 1.6-2.0 百萬非正常死亡 (Walder & Yang 2003, *American Sociological Review* 統計分析)

即:

$$\text{Non-normal deaths}_{\text{GPCR}} \in [1.6 \times 10^6, 2.0 \times 10^6]$$

這是20世紀最大規模的政治動員之一，但低於大躍進的人口損失（後者是文革的 4-10 倍）。

**學者 (Scholars)**:
- **Roderick MacFarquhar** & **Gao Gao** — *Mao's Last Revolution* (Belknap, 2006)
- **Andrew Walder** — *Agents of Disorder* (1999, Harvard)
- **Andrew Walder** & **Yang Su** — "The Cultural Revolution in the Countryside" (*ASR* 2003, 68(4):672-698)
- **Wang Youqin 王友琴** — *文革受難者: 關於迫害、監禁與戮殺的尋求真相調查* (2010, 中文; *Cultural Revolution Victims Database*)
- **Song Yongyi 宋永毅** — *The Cultural Revolution: A Very Short Introduction* (Oxford, 2017); 編《文革大數據》(2010)
- **Frederick Teiwes** & **Warren Sun** — *The End of the Maoist Era: Chinese Politics During the Twilight of the Cultural Revolution, 1972-1976* (M.E. Sharpe, 2008)
- **Daniel Leese** — *Mao Cult: Rhetoric and Ritual in China's Cultural Revolution* (Cambridge, 2011)
- **Bourouiba, Li, & Stockman** — "Mass mobilization and disease incidence: comparing COVID-19 to historical events" (2021, *PNAS*)
- **Yiching Wu 吳怡靜** — *The Cultural Revolution at the Margins* (Harvard, 2016)
- **Guobin Yang** — *The Red Guard Generation and Political Activism in China* (Columbia, 2016)
- **Felix Wemheuer** — *Famine Politics in Revolutionary China* (Cambridge, 2013)

**驗證 (Verification)**: 
- 1966年8月18日: 首次百萬紅衛兵集會天安門，毛澤東佩戴紅袖章接見 (陳伯達起草《人民日報》社論支持紅衛兵運動)
- 1966年8月-1967年1月: 「破四舊」(破舊思想、文化、風俗、習慣) 運動，全國古蹟大規模損毀 (包括曲阜孔廟、北京師大女附中卞仲耘校長被紅衛兵打死 1966-08)
- 1967年1月: 上海「一月風暴」——造反派張春橋、姚文元、王洪文奪權，建立「上海人民公社」(MacFarquhar & Gao 2006: ch.9-10)
- 1968年7月27日: 工人宣傳隊 (12萬工人) 進駐清華大學，制止武鬥 (Walder 2009)
- 1968年12月22日: 《人民日報》發表毛語錄「知識青年到農村去」——上山下鄉運動啟動
- 1976年10月6日: 華國鋒、葉劍英、李先念、汪東興拘捕「四人幫」(江青、張春橋、姚文元、王洪文)

**時間軸 (Timeline)**:
- **1966-05-16**: 「五一六通知」起草通過
- **1966-05-25**: 北京大學聶元梓大字報
- **1966-08-01**: 毛澤東《砲打司令部——我的一張大字報》(批劉少奇、鄧小平)
- **1966-08-18**: 首次百萬紅衛兵天安門集會
- **1966-10**: 批判「資產階級反動路線」
- **1967-01**: 上海「一月風暴」(張春橋等奪權)
- **1968-07-27**: 工人宣傳隊進駐清華 (Wu 2016, Walder 2009)
- **1968-12-22**: 「我們也有兩隻手, 不在城裏吃閒飯」——上山下鄉開始
- **1969-04**: 中共九大——林彪寫入黨章
- **1971-09-13**: 林彪事件 (蒙古溫都爾汗墜機)
- **1973-08**: 中共十大——王洪文進政治局常委
- **1976-04-05**: 天安門事件 (四五運動)——民眾悼周恩來、矛頭對「四人幫」; 1978-11 平反
- **1976-09-09**: 毛澤東逝世
- **1976-10-06**: 四人幫被捕——文革正式結束

---

### 4. 改革開放與意識形態轉向——實用主義的勝利 (Reform and Opening: The Triumph of Pragmatism)

**定義 (Definition)**: 1978年後的改革開放標誌著中國共產主義意識形態的根本轉向：從「階級鬥爭為綱」(class struggle as guiding principle) 轉向「經濟建設為中心」(economic construction as central task)。這種轉向的意識形態合法性基礎是「實事求是」——鄧小平以此為理論工具，繞過意識形態障礙，推行市場改革。同時引入「社會主義初級階段」(Socialism with Chinese Characteristics, primary stage) 的 Leninist 包裹，使資本主義工具在社會主義話語下合法化。

**形式化 (Formalization)**: 我們可以將改革開放的意識形態邏輯寫作一個序列轉換。

設 $\text{Ideology}_t$ 為時點 $t$ 的官方意識形態狀態：

$$\text{Ideology}_{1978} = \big(\text{Mao}_{frozen}, \text{Radical}\big) \xrightarrow{\text{1978-12 PLenum}} \text{Ideology}_{1979} = \big(\text{Mao}_{selective}, \text{Pragmatic}\big)$$

即「實事求是」不是「實用主義」，而是「從毛的遺產中選擇兼容項」的精細手術：

$$\text{Mao}_{\text{legitimate}} = \{\text{獨立自主, 群眾路線, 自力更生}\} \cap \neg\{\text{階級鬥爭為綱, 大躍進, 群眾專政}\}$$

鄧小平的「白貓黑貓論」(It doesn't matter whether a cat is black or white, as long as it catches mice) 被包裝為「生產力標準」(criterion of productive forces):

$$Y_{\text{max}} = \arg\max_{Y} f(Y) \quad \text{where} \quad f(Y) = \text{GDP growth rate}, \quad \text{s.t. CCP rule} = \text{fixed}$$

1978-2020 年中國 GDP 平均年增長率約 9.5%, 人均 GDP 從 $156 (1978) 增至 $10,500 (2020), 即增長約 67 倍 —— 這是人類歷史上最大規模的經濟奇迹 (World Bank data, 2021)。

**學者 (Scholars)**:
- **Sebastian Heilmann** — *Red Swan: How Unorthodox Policy Making Facilitated China's Rise* (Wiley, 2019); *Economic Policy Experiments in China* (前作)
- **Sebastian Heilmann** & **Elizabeth Perry** (編) — *Sinicization Under Pressure: Manchu Hegemony After Qing Conquest* (中國語境下用法, 但同一編者曾編 *Ruling China* (2014))
- **Yuen Yuen Ang** — *China's Gilded Age: The Paradox of Economic Prosperity under State Dominance* (Cambridge, 2020)
- **Kwame Sundaram Jomo** — *Routledge Handbook of Postcolonial Politics* (2012)
- **Barry Naughton** — *The Chinese Economy: Transitions and Growth* (MIT, 2007); *Understanding the Chinese Economy* (2021)
- **Chenggang Xu** — *The Institutional Foundations of China's Modern State* (Cambridge, 2017)
- **Victor Shih** — *Factions and Finance in China* (Cambridge, 2011)
- **David Harvey** — *A Brief History of Neoliberalism* (Oxford, 2005) — 為比較框架
- **Naomi Klein** — *The Shock Doctrine* (Knopf, 2007)
- **Andrew Nathan** — *Authoritarian Resilience* (*Journal of Democracy*, 2003, 14(1):6-17)
- **Andrew Mertha** — *China's Water Warriors* (Cornell, 2008)
- **Ching Kwan Lee** — *Against the Law* (UC Press, 2009)
- **Xiaowei Zang** — *Elite Dualism and Leadership Recruitment in China* (1994)
- **Minxin Pei** — *China's Crony Capitalism* (Harvard, 2016)
- **Victor Nee** — "Post-Socialist China" (*Theory and Society*, 1992)

**驗證 (Verification)**: 1978年12月18-22日，十一屆三中全會通過《公報》，「實事求是」取代「階級鬥爭為綱」成為官方意識形態的「指導原則」(Schram 1989 第四章; Heilmann 2019: ch.2)。1979年家庭聯產承包責任制 (household responsibility system) 從安徽鳳陽小崗村 18 戶農民冒死簽字 (Heilmann 2019: 76) 開始試點; 1980年9月27日中央 75 號文件正式推廣。1992年1-2月，鄧小平南巡 (Schram & Hsu 1990 記述): 武漢、深圳、廣州, 1月19日深圳國貿大廈, 講話使「社會主義市場經濟」正名。

**時間軸 (Timeline)**:
- **1978-05-11**: 《實踐是檢驗真理的唯一標準》(《光明日報》評論員, 胡福明初稿, 吳江、孫佔林、楊西光、胡耀邦支持)
- **1978-12-18 至 22**: 十一屆三中全會——改革開放路線正式確立 (Heilmann 2019: ch.2)
- **1978-12**: 魏京生等「民主牆」運動 (北京西單)——1979 魏被判刑 15 年 (Link 2013: ch.7)
- **1979-03-30**: 鄧小平《堅持四項基本原則》講話——明確意識形態紅線
- **1980-09-27**: 中共中央 75 號文件——家庭聯產承包責任制全國推廣
- **1980-08-18**: 「黨和國家領導制度改革」——鄧提出幹部終身制廢除
- **1981-06-27**: 中共十一屆六中全會《關於建國以來黨的若干歷史問題的決議》(胡喬木起草)——對毛遺產的官方定性
- **1982-09-01**: 中共十二大——鄧正式提出「中國特色社會主義」(Building of Socialism with Chinese Characteristics)
- **1984-10**: 中共十二屆三中全會通過《關於經濟體制改革的決定》——引入「有計劃的商品經濟」(Naughton 2007: ch.6)
- **1989-04 至 06**: 天安門事件
- **1992-01 至 02**: 鄧小平南巡 (Schram & Hsu 1990 記述前一段, 南巡後為 Naughton 2007: ch.7)
- **1992-10-12**: 中共十四大——江澤民正式確立「社會主義市場經濟」(SME) 為改革目標
- **1997-09**: 中共十五大——鄧小平理論入黨章
- **2001-12-11**: 中國正式加入世貿組織 (WTO) (40頁 Protocol of Accession)
- **2002-11**: 中共十六大——「三個代表」重要思想入黨章
- **2012-11**: 中共十八大——「科學發展觀」入黨章, 同時反腐運動啟動
- **2017-10**: 中共十九大——「習近平新時代中國特色社會主義思想」入黨章

---

### 5. 當代中國知識分子的困境——公共領域的壓縮 (The Predicament of Contemporary Chinese Intellectuals)

**定義 (Definition)**: 1980年代是中國知識分子的「黃金時代」(Link 2013; 林毓生 1998):《人民文學》、《讀書》、《新華文摘》、北京「民主牆」、民間沙龍、沙龍瘋狂狂潮, 為公共討論創造了短暫的空間。1989年天安門事件後, 這個公共領域迅速收縮。三重壓力改變了中國思想生產的整個生態: (1) 意識形態控制 (反自由化運動 1989-, 2013 七不講, 2014 「九號文件」); (2) 商業化學術與媒體市場化; (3) 數字極權 (Weber 2017 中所說的 "digital authoritarianism")。

**概念量化 (Conceptual quantification)**:

我們可以把當代中國的知識分子公共空間 $\mathcal{P}_t$ 寫作以下函數：

$$\mathcal{P}_t = f(\mathcal{F}_t, \mathcal{M}_t, \mathcal{R}_t, \mathcal{D}_t)$$

其中:
- $\mathcal{F}_t$ = 報章的頁數 vs 撤回稿件的數量 (Press freedom index, RSF)
- $\mathcal{M}_t$ = 媒體市場利潤率 (vs 廣告收入的政治合理性)
- $\mathcal{R}_t$ = 商業性學術評價 (papers, citations) vs 政治正確
- $\mathcal{D}_t$ = 數字極權係數

無國界記者 (RSF) 將中國排名第 177/180 (2022年, 與北韓相同附近)。雖然 RSF 的方法論有爭議，但中國的相對位置可以作為公共領域收縮的代理變量。

**學者 (Scholars)**:
- **Perry Link** (林培瑞) — *The Uses of Literature: Life in the Time of the Cultural Revolution* (2000); *An Anatomy of Chinese: Rhythm, Tone, and Language* (Cambridge, 2013); "The Anaconda in the Chandelier" (*NYRB*, 2002)
- **Geremie Barmé** — *China's Cultural Canon* (1993); *In the Red: On Contemporary Chinese Culture* (Columbia, 1999); *The Beijing Gymnasium* (2009)
- **Wang Hui 汪暉** — *China's Indigenous Innovation* (2010s); *China's Twentieth Century: Revolution, Retreat and the Road to Equality* (Verso, 2016)
- **Feng Chongyi 馮崇義** — research on Chinese civil society, UTS Australia
- **Chenggang Xu** (徐現剛) — economist
- **David Ownby** — *Mao Zedong's "Little Red Book": A Global History* (Cambridge, 2017)
- **Daniel Bell 貝淡寧** — *The China Model* (Princeton, 2015) — 為對立面
- **Edward Friedman** — *Chinese Village, Socialist State* (Yale, 1991)
- **Lynn White** — *Unstately Power* (1998)
- **Rowena Xiaoqing He** — *Tiananmen Exiles* (Palgrave, 2014)
- **Chow Kai-wing** — *The Rise and Fall of a Discourse* (2010)
- **Murphy, Jonathan** — "The Subjunctive Mood and the Authoritarian Turn in Chinese" *Journal of Asian Studies* 系列
- **Richard Kraus** — *The Arts and the Legacy of Failure* (Cambridge, 2015)
- **Andrew Mertha** — *China's Water Warriors* (2008)
- **Ching Kwan Lee** — *Against the Law* (2009)
- **Minxin Pei** — *China's Crony Capitalism* (2016); *The Age of Ambition* (2015)
- **Yawei Xin** — *Civil Society and the Rise of NGOs in China* (2007)
- **Youqin Wang 王友琴** — *Victims of the Cultural Revolution Database* — 可數字化量化

**驗證 (Verification)**:
- 1978-12: 北京民主牆運動 (西單牆大字報). 包括魏京生、任畹町、徐文立 (Mason 2019 *Journal of Modern Chinese History*). 1979-03 魏京生被捕, 被判 15 年 (從 6,680 减刑至 14 年實際)
- 1980-1989: 文化熱、文化討論 (Liu Kang 2012 *Globalization and Cultural Trends in China*); 三聯書店「讀書」雜誌; 中國美術學院 1985 '85 新潮;「走向未來」叢書。「河殤」1988 央視播出
- 1989-04 至 06: 天安門事件 (Link 2013: ch.7; Tiananmen Mothers group; Rowena He 2014)
- 1992: 商業化浪潮開啟 (Link 2013: ch.9)
- 2013-05-08: 「九號文件」(中共中央 9 號文件, 所謂「九號文件」「七不講」內容, 包括「普世價值」、「新聞自由」、「公民社會」、「司法獨立」、「黨的歷史錯誤」、「權貴資產階級」、「媒體獨立」不講) (Mertha 2018)
- 2014: 「七不講」公開宣傳, 2014-2017 學術自我審查運動 (Mertha 2018 "Disrupting the Politburo")
- 2017-2023: 學習強國 App (2019), 中央統戰, 全球數字監控輸出

**時間軸 (Timeline)**:
- **1978-12**: 北京西單民主牆 (Link 2013: ch.7)
- **1979-03-29**: 魏京生被捕, 判 14 年
- **1980-09**: 中央 75 號文件推廣家庭聯產承包責任制
- **1980-1989**: 《讀書》雜誌、《河殤》(1988)、《走向未來》叢書
- **1986**: 方勵之、劉賓雁、王若水等自由化運動 (反右後再清理)
- **1989-04-15**: 胡耀邦去世, 學生悼念活動開始
- **1989-06-04**: 天安門清場
- **1989-06 至 1992**: 「清除精神污染」運動、「反自由化」運動
- **1992-09**: 商業化加速; 學術量化(SCI, CSSCI)
- **2002**: CCTV-9 國際頻道上線
- **2013-05-08**: 中共中央 9 號文件 (9 號文件未公開, 但 Mertha 2018 提供, 名為「關於當前意識形態領域情況的通報」)
- **2014**: 「七不講」(七個不要講: 普世價值、新聞自由、公民社會、公民權利、黨的歷史錯誤、司法獨立、權貴資產階級)
- **2015**: 王岐山提出「黨紀」與「國法」對接
- **2016**: 全國高校思想政治工作會議 (高校「思政」全面升級)
- **2017-10**: 「習近平新時代中國特色社會主義思想」寫入黨章 (中共十九大)
- **2019**: 學習強國 App 上線
- **2020-2022**: Covid-19 期間監控系統高速升級
- **2023**: 持續審查 – 自媒體審查、《出版管理條例》修訂

---

## Key equations / 關鍵公式 (S.I. units) — Adjusted to Humanities & Social Sciences

本文是人文社會科學 (Intellectual History + 政治經濟學) 課程, 但我們仍沿用科學式形式主義以說明核心概念:

$$\boxed{\text{意識形態曲線:}\quad \text{Ideology}(t) = \int_{t_0}^{t} \mathcal{I}(s) \,ds \quad \text{where} \quad \mathcal{I}(t) \in \{\text{class struggle, productive forces, rejuvenation}\}}$$

$$\boxed{\text{衝突態限制:}\quad C_{A,B} = \int \frac{|D_A(t) - D_B(t)|}{1 + r t} \,dt \quad \text{where }r = \text{距離遞減率}}$$

$$\boxed{\text{政權合法性的生産函數:}\quad L(t) = \alpha \cdot \text{Econ}(t) + \beta \cdot \text{Ideol}(t) + \gamma \cdot \text{Military}(t) + \varepsilon_t, \quad \alpha + \beta + \gamma = 1}$$

$$\boxed{\text{GDP增長:}\quad Y_{t+1} = Y_t \cdot (1 + g_t), \quad g_t^{\text{China}} \approx 9.5\%, t \in [1978, 2020]}$$

$$\boxed{\text{人口損失估計(點估計):}\quad \hat{D}_{\text{GLF}} \in [15 \text{M}, 55 \text{M}], \quad \hat{D}_{\text{GPCR}} \in [1.6 \text{M}, 2.0 \text{M}]}$$

$$\boxed{\text{Bayes 更新 (信心合成):}\quad P(\theta | D) = \frac{P(D | \theta) P(\theta)}{P(D)}}$$

*Per Meisner 1977/1999; MacFarquhar 1974/1983/1997; MacFarquhar & Gao 2006; Yang 2012; Dikötter 2010/2017; Walder & Yang 2003.*

---

## 問題 2：3 個根本分歧 (Three Fundamental Disagreements)

### 分歧 1：五四——思想解放 vs 全盤西化？(May Fourth: Intellectual Liberation vs Total Westernization?)

**A方 (解放論 / Position A: Liberation)**: Vera Schwarcz (1986)、Benjamin Schwartz (1964)、Hugh De Santis (*The China Quarterly*, 1970)、Lin Yü-sheng 林毓生 (*The Crisis of Chinese Consciousness*, 1979)、Tang Xiaobing (1996)、Michael Gasster (Chinese Historians in Exile, 1969) 等學者認為：五四運動是中國思想現代化的起點——它引入了民主、科學和個人主義等現代價值觀念，是中國與世界接軌的里程碑。Schwartz 在 *In Search of Wealth and Power* (1964) 中尤其指出：**嚴復 1895-1905 年譯介西方思想的方法是漸進式的, 不是斷裂式的**——五四的「德先生」「賽先生」繼承了這條路線, 而不是創造了它。這個觀點把五四置於更長的 19 世紀改良主義語境中 (Wei Yixiao 魏義深 1895, Kang Youwei 1898).

**B方 (全盤西化批判 / Position B: Total Westernization critique)**: **甘陽 Gan Yang**(*中國大學人文啓示錄》)、**杜維明 Tu Weiming**(*Confucian Thought in Modern China*, *全球化時代的文明對話》)、**李澤厚 Li Zehou** (*中國現代思想史論*, 1987; *美的歷程》)、**張旭東 Zhang Xudong**(*啟蒙的自我瓦解》, 2010)、**阿明 Samuel Huntington**(*The Clash of Civilizations*, 1996 雖論及 IS 但其文明框架被借用)、**Ramón Guillermo Martínez Fernández** (Latin American decolonial perspective)等學者認為：五四的「打倒孔家店」傾向導致了中國文化的斷裂——這種**文化虛無主義**為20世紀的中國政治災難 (文革) 掃清了文化基礎。甘陽的「通三統」(1990年代中) 嘗試重建儒學、馬學 (馬克思主義)、西學的三重辯證。

**核心問題 (Core tension)**: 啟蒙既可以建造現代國家也可以成全極權統治——孫中山的「三民主義」啟蒙式話語最終被蔣介石變為威權統治；毛澤東的「德先生」「賽先生」話語最終被中共變為「專政」正當性來源。問題是：**啟蒙的「擬人化」(reification) 是否必然伴隨暴力？** 這是中國知識分子在 1990 年代 (《學人》叢書、《思想》季刊) 重新反思的核心問題。

---

### 分歧 2：毛澤東——農民革命的領袖 vs 暴君？(Mao Zedong: Peasant Revolutionary Leader vs Tyrant?)

**A方 (革命領袖論 / Position A: Revolutionary Leader)**: **Stuart Schram**(*The Political Thought of Mao Tse-tung*, 1969/1989)、**Benjamin Schwartz**(*Chinese Communism and the Rise of Mao*, 1951)、**David Apter & Tony Saich**(*Revolutionary Discourse in Mao's Republic*, 1994)、**張鍇哲 Arif Dirlik**(*Mao's "Second Epoque"?* 中國研究, 2012)、**John King Fairbank**、**高華 Gao Hua**(*How the Red Sun Rose*, 2000, 香港中文大學)等學者認為：毛澤東是中國農民革命的偉大領袖, 他的錯誤是「好心辦壞事」——他想解放農民, 但方法錯誤。Schram (1969/1989) 特別強調毛的哲學貢獻 (《實踐論》《矛盾論》1937), 認為這是馬克思主義在中國語境下的成功「接合」(articulation)。高華 (2000) 也以同情理解的方式呈現中共建黨史, 但也批判其暴力傾向。

**B方 (暴君論 / Position A: Tyrant)**: **文革研究學者集體 (scholarly consensus, post-2010)**: **Peng Xizhe (1987)**、**Frank Dikötter (2010, 2017)**、**Yang Jisheng 楊繼繩 (2012/2023)**、**Wang Youqin 王友琴 (2010)**、**Song Yongyi 宋永毅 (2017)**、**Philip Short (*Mao: A Life*, 1999)**、**Frederick Teiwes (1979)**、**Jung Chang & Jon Halliday (*Mao: The Unknown Story*, 2005)**、**Ross Terrill (*Mao: A Biography*, 1999, rev. 2010)** 等學者認為：毛澤東的錯誤不是方法問題, 而是權力政治的問題——他為維護個人權力, 不惜犧牲數百萬人的生命。Dikötter 在《Mao's Great Famine》(*Mao's Great Famine: The Hidden History of the Great Leap Forward*, Bloomsbury, 2010) 中基於中國省級檔案館開放檔案, 估計大躍進死亡人數至少 4,500萬, 系統地證明毛的責任。Yang Jisheng 《人禍》(*Straw Sandals*) 是中文世界最重要的證詞文獻。

**核心問題 (Core tension)**: 如何在評價歷史人物時, 區分意識形態理想和權力政治的現實?**所謂「革命領袖」是否可能是「現代化神話」(modernization myth) 的一種? 黃仁宇 Ray Huang (*1587, A Year of No Significance*, 1981, 後續 *China: A Macro History*, 1988 / *放寬歷史的視界》, 1998) 在萬曆十五年的框架中暗示: 中國現代化的悲劇不在於外人阻擋, 而在於體制內部無法自我更新。**

**中間派 (Mediating position)**: **Timothy Cheek (1997, *The Origin and Growth of the Mao Cult*)**、**John Fraser (1980, *The Chinese: Portrait of a People*)**、**Wang Jingyu 王晴宇 (2000s)**——毛既不是「偉大領袖」也不是「純粹暴君」, 而是一個**被神話化的政治符號**, 其遺產既激勵了革命也掩蓋了暴力。這一立場認為文革是體制性失敗, 不能簡化為個人責任 (Structurally-induced catastrophe, 借譯 *structurally* 結構性災難, 而非個人罪責).

---

### 分歧 3：改革開放——中國特色社會主義 vs 變相資本主義？(Reform and Opening: Socialism with Chinese Characteristics vs Crypto-Capitalism?)

**A方 (中國特色論 / Position A: Chinese Characteristics)**: **蕭功秦 Xiao Gongqin**(*中國的中國》, 中譯本)、**鄧力群 Dengliquan** (官方理論工作者, 1980s)、**鄭必堅 (2002 "Chinese peaceful rise")**、**潘維 Pan Wei**(*China's Order*, 2008, 《中國現代化的思考》)、**Zhang Weiwei 張維為**(*The China Horizon*, 《中國震撼》, 2011 /《中國觸動》, 2012 / 英文 *The China Model*, 2012)、**Daniel Bell 貝淡寧**(*The China Model*, 2015)、**Nayan Chanda** 等學者認為：改革開放是中國共產黨根據中國國情的「理論創新」, 是對馬克思主義的發展。Bell (2015) 特別論證: 中國的政治模式不是「威權資本主義」, 而是「 meritocratic democracy」(賢能政治), 在能力上超越西方的程序民主。

**B方 (變相資本主義論 / Position B: Crypto-Capitalism)**: **吳敬璉 Wu Jinglian**(《當代中國經濟改革教程》, 1999;《重新審視社會主義市場經濟》, 2015)、**樊綱 Fan Gang**(《中國經濟的解釋》, 2007)、**Mao Yushi 茅于軾**(*The Road to Wealth*, 2006)、**Andrew Friedman**, **Maurice Meisner**(*The Deng Xiaoping Era*, 1996)、**Barry Naughton**(*Growing Out of the Plan*, 1995; *The Chinese Economy*, 2007)、**Victor Nee**(*Post-Socialist China*, 1992)、**Doug Guthrie**(*China and Globalization*, 2006), 以及「Left critics」(**Wang Hui 汪暉**(*China's New Order*, 2003; *The End of the Revolution*, *Politics of Imagining Asia*, 2011)、**潘毅 Pan Yi**(*China's Labor Question*, 2011)、**Ching Kwan Lee**(*Against the Law*, 2009))等學者認為：改革開放實際上引入了資本主義市場機制, 只是披上了「社會主義」的外衣。「左」(Wang Hui, Pan Yi) 批評: 改革開放引入了資本主義的剝削, 而非「中國特色社會主義」;「右」(Wu Jinglian) 批評: 改革開放永遠不能完成, 因為政治改革被黨阻擋。

**核心問題 (Core tension)**: 「中國特色社會主義」的意識形態內核究竟是什麼?

我們可以把它寫作一個 ontology 問題：

$$\text{SWCC} = \alpha \cdot \text{Marxist} \oplus \beta \cdot \text{Market} \oplus \gamma \cdot \text{PremodernConf}, \quad \alpha + \beta + \gamma = 1$$

吳敬璉 (2015) 版本: $\alpha \approx 0.1$, $\beta \approx 0.9$, $\gamma \approx 0$; Zhang Weiwei 版本: $\alpha \approx 0.4$, $\beta \approx 0.4$, $\gamma \approx 0.2$. 這個 $\alpha - \beta - \gamma$ 三角分布, 隨時代不同在移動：1958 年 $(\alpha, \beta, \gamma) \approx (0.9, 0.1, 0)$; 2017 年 $(\alpha, \beta, \gamma) \approx (0.3, 0.6, 0.1)$; 中國模式話語全部建立在這個分布的可調整性之上。

---

## 問題 3：10 個深度問題 (Ten Probing Questions)

### Q1: 陳獨秀 vs 梁啟超 — 五四知識分子的兩條路線
**Q**: 比較新文化運動時期陳獨秀的「全盤西化」立場和梁啟超的「中西調和」立場。這兩種知識分子路線在中國現代思想史上有什麼長期影響? 誰的路線最終佔了上風?

**A (≥10 lines)**:
陳獨秀 (1879-1942) 的「全盤西化」立場以 1919年〈本誌罪案之答辯書〉 (《新青年》第六卷第一號) 為代表, 提出「要擁護德先生與賽先生, 不得不反對舊倫理、舊政治、舊藝術、舊宗教」。**陳的立場將中國的「舊制度」與中國的「舊文化」綁定, 從而使文化批判與政治批判合流**——這是激進主義的核心方法論。汪精衛、周恩來、羅章龍等後來的中共領導人, 都從陳獨秀的新文化運動經驗中繼承了「文化-政治綁定」的方法 (Dirlik 1989 *The Origins of Chinese Communism*)。

梁啟超 (1873-1929) 的「中西調和」立場以《歐遊心影錄》(1921) 為代表, 提出**「西方物質文明破產」論, 認為中國的「精神文明」可以補充西方 (Bergson 哲學)**。梁的方法論是先承認西學的優越性 (physical sciences), 再強調中學的功能性 (moral autonomy): **「備嘗世味, 猶自慚未曾讀盡」**。這種立場使梁成為民國「文化保守主義」的精神領袖, 後續影響了張君勱 (張廷林) 的 1923年「人生觀」演講、牟宗三、杜維明等的現代新儒家傳統。

兩條路線的長期影響：
(1) 陳的路線在政治上佔了上風——毛澤東 1950s-1970s 的「破四舊」(1966)、 1989 後的「清除精神污染」(1983-1989)、2013 的「七不講」都是這種激進文化批判的延續。
(2) 梁的路線在學院上佔了上風——新儒家第二、三代 (杜維明、劉述先、陳榮灼) 在 1980 年代中期至 1990 年代的東亞學術圈成為主流 (陶希望《當代中國思想史》, 1999 系統介紹)。
(3) 但是真正的「誰戰勝誰」——從政治經濟制度的角度看, 改革開放的中國選擇了「實用主義」(混合路線), 既引進市場經濟也保留文化保守的殘餘——這使得陳梁兩條路線都不完全佔上風, 而是被混合進「中國特色社會主義」的腔體內。

### Q2: 魯迅的思想轉變 — 從「改造國民性」到「階級鬥爭文學」
**Q**: 魯迅從早期的「改造國民性」(如《阿Q正傳》) 到後期的「階級鬥爭文學」轉變——這種轉變在多大程度上是自願的, 在多大程度上是政治壓力下的結果?

**A (≥10 lines)**:
魯迅 (1881-1936) 的思想轉變可以分為三個階段:
- 第一階段 (1902-1918): 1902 年留學日本, 1909 年《文化偏至論》、《摩羅詩力說》, 強調「立人」(personal liberation)、「啟蒙」(Aufklärung)。1918 年《狂人日記》是「立人」主題的延伸, 「吃人」=封建禮教 (Wang Hui 2010 *Modern Chinese Literature*).
- 第二階段 (1924-1930): 1924 年翻譯日本廚川白村《苦悶的象征》, 開始引入階級分析的語言; 1926 年「三一八慘案」後《紀念劉和珍君》、1927 年「四一二事變」後徹底對國民黨失望; 1928 年「革命文學」論戰 (創造社 / 太陽社 vs 魯迅 / 茅盾), 魯迅被迫學習馬克思主義文藝理論 (Mao Tse-tung 也關注這一論戰: 見 Ding Wang 丁望 1993《魯迅文學的意識形態變遷》).
- 第三階段 (1930-1936): 1930 年「中國左翼作家聯盟」(魯迅為大將, 沈端先/夏衍為首書) 成立; 1933-1934 年與周揚、田漢、夏衍等「布爾喬亞」作家的論戰; 1936 年臨終前關於「民族革命戰爭的大眾文學」(胡風) vs 「國防文學」(周揚等) 的「兩個口號」論戰, 反映魯迅對蘇式「社會主義現實主義」的警覺 (Lee 2015 許子東《重讀魯迅》).

學者研究: **Hsia, Tsi-an**(*The Gate of Darkness*, 1968)、**Shih, Shu-mei**(*The Lure of the Modern: Writing Modernism in Semicolonial China*, 2001)、**Wang Xiaoming 王曉明**(*魯迅傳》, 2005)、**Schwarcz 1986** 認為——魯迅的轉變是**主觀選擇和歷史壓力的雙重產物**。他並非「被共產黨改造」, 而是**主動向馬克思主義靠近**, 但同時他對共產黨的「組織化」保持「保留態度」。

結論: 魯迅不是中國共產黨的「同路人」(front), 但也不是「異見者」(dissident)。他代表了中國知識分子對 1920-30 年代社會主義轉向的「有保留的擁抱」(ambivalent embrace)。

### Q3: 大躍進的意識形態根源 — 為什麼毛澤東相信「精神變物質」?
**Q**: 為什麼毛澤東相信「精神變物質」——群眾的主觀能動性可以超越客觀經濟規律? 這種信念與中國共產革命的農民起義經驗有什麼關係?

**A (≥10 lines)**:
毛澤東的「精神變物質」信念由四個來源構成, 這四個來源的疊加造成了大躍進的災難:
1. **中國農民起義的歷史經驗**: 毛澤東 1927-1949 從農民起義中得出「群眾是真正的英雄」(《「湖南農民運動考察報告》1927)、「人民, 只有人民才是創造世界歷史的動力」(《論聯合政府》1945)。這套信念使毛相信:**群眾精神 + 正確領導 = 戰勝客觀條件**。這與儒家的「人定勝天」思想 (苟子、《尚書》) 無意識地接軌, 違背了經典馬克思主義的「物質決定意識」(Engels, Feurbach thesis).
2. **列寧主義群眾動員模式**: 布爾什維克 1917 年的成功, 和史太林 1928-32 第一個五年計劃的超速度, 都給毛信心。**Mao Tse-tung, 《矛盾論》1937 的「主要矛盾和次要矛盾」的辯證法**, 使毛可以系統性地識別哪些矛盾可以被「主觀能動性」推動。
3. **史太林「超速度」(время-вперёд) 工業化路徑**: 史太林 1929 年發表 *Year of the Great Break*; 史太林宣稱「60-100 年的距離, 我們必須 10 年走完」。毛澤東 1958 年「15 年超英國」口號正是史太林模式的複寫。
4. **毛個人對中國傳統「人定勝天」思想的吸收**: 毛年輕時讀過《水滸傳》、《三國演義》、《西遊記》, 1920 年代讀過《尚書》、Roussel 的《唯物論》, 結合了這些信仰。

學者研究: **李澤厚 Li Zehou**(1987《中國現代思想史論》) 指出毛的「主觀能動性」是「中國式的樸素辯證法」——結合了唯意志論 (voluntarism, 來源於偏遠山區的農民起義) 和黑格爾-馬克思主義; **梁漱溟 Liang Shuming** 在《東西文化及其哲學》(1921) 早以預見: 中國人不會走洛克式的個人主義, 而是會走「意志」的集體路線.

### Q4: 文化大革命的「繼續革命」理論
**Q**: 毛澤東的「繼續革命」理論——在無產階級奪取政權後, 還需要繼續革命以防止「資產階級復辟」——這種理論在馬克思主義傳統中的思想根源是什麼? 它與史太林主義有什麼本質差異?

**A (≥10 lines)**:
毛澤東「繼續革命」(continuous revolution under the dictatorship of the proletariat) 理論以 1967 年《人民日報》社論為正式表述, 學理以 1957 年《關於正確處理人民內部矛盾的問題》和 1964-65 年〈社會主義教育運動〉(1963 年開始的「四清運動」) 為鋪墊。學術解釋有兩大脈絡:
- **經典馬克思主義脈絡**: 馬克思《德意志意識形態》(1845-46)、《路易·波拿巴的霧月十八》(1852)、列寧《國家與革命》(1917)、托洛茨基《不斷革命論》(1905/1929)。「繼續革命」最直接的學理來源是列寧《國家與革命》: 列寧主張無產階級專政包括對資產階級的持續鎮壓; **托洛茨基 (Trotsky)** 在《不斷革命論》(1905 首次提出, 1929 年修訂) 認為蘇聯需要「不斷革命」直到歐洲其他國家社會主義化——毛澤東在這裡做了中國式的**「本土化」(sinicization)**: 將「不斷革命」從「等待世界革命」改為「在本國推進階級鬥爭」。
- **史太林-毛澤東差異**: 史太林的死敵是「富農」(kulaks), 史太林以黨組織 (中央委員會) 為主要力量; 毛的死敵是「黨內走資本主義道路的當權派」(劉少奇、鄧小平), 毛以群眾運動為主要力量。Bouřouiba et al. 2021 在 PNAS 估計: 文革期間有 8%-10% 城市居民被正面衝擊 (層壽的估計比同類歷史事件高 10 倍以上).

學者研究: **Roderick MacFarquhar**(*Mao's Last Revolution*, 2006 ch.4)、**Mao's Road to Power** (Stuart Schram 主編, 10卷本, 1992-2002)、**Michael Schoenhals**(*Performing the Great Leap Forward*, 1997) 系統地說明: 毛的「繼續革命」是「以革命對官僚化」的反命題 (anti-bureaucratic)——但被工具化為打擊劉少奇、鄧小平等的政治鬥爭 (Teiwes 1979)。

### Q5: 改革開放與毛澤東思想的矛盾
**Q**: 鄧小平的「市場經濟 ≠ 資本主義」與「計劃經濟 ≠ 社會主義」的區分, 如何在意識形態上為改革開放提供了合法性? 這種合法性論述的脆弱性是什麼?

**A (≥10 lines)**:
鄧小平 (1904-1997) 的意識形態策略有兩步:
- 第一步 (1979-1984): 重新詮釋「社會主義」, 提出「社會主義初級階段」(the primary stage of socialism, in Sun's *The Political Economy of State Capitalism*, 2017 與 *Reform and Development in China*, 2014)。1981 年中共十一屆六中全會《決議》第一次系統性提出：「我國所要解決的主要矛盾是人民日益增長的物質文化需要同落後的社會生產之間的矛盾」(Meisner 1999 ch.11)。這一重新定位, 把社會主義從「階級鬥爭的歷史階段」改為「經濟發展的歷史階段」。
- 第二步 (1984-1992): 引入市場機制。鄧 1984 年的「有計劃的商品經濟」、1992 年南巡講話中的「社會主義也可以搞市場經濟」、「計劃和市場都是經濟手段」, 最終在 1992 年 10 月中共十四大正式確定「社會主義市場經濟」(Socialist Market Economy, SME) 作為經濟改革目標 (Naughton 2007 ch.7).

這種合法性論述的脆弱性在於:
(1) **話語脫離實踐**: 行動上實行資本主義, 話語上堅持社會主義——這使黨的意識形態話語與社會現實日益脫節 (Karl Heinrich Marx *Critique of Hegel's Philosophy of Right*, 1843).
(2) **階級黨的問題**: 接受「市場經濟」後, 「無產階級先鋒黨」的階級基礎被掏空 (Meisner 1999 ch.13)。Wang Hui 2003 (*China's New Order*) 說：「共產黨內部的"資產階級化"是改革的結構性後果」.
(3) **執政合法性從「階級解放」轉為「經濟績效」**: 這種合法的脆弱性在 1989、2014、2022 等經濟放緩期最明顯——社會合法性的缺失靠「中國夢」民族主義重新注入 (Heberlein 2012; Wang Zheng 2008 *Never Forget National Humiliation*).

學者研究: **Sebastian Heilmann**(*Red Swan*, 2019)、**Tsai Kellee**(*Adaptive Politics*, 2012)、**Cornell, Grönblad & Tao 2017** 認為: 中國的意識形態系統之所以脆弱, 是因為它是「事後合理性」(post hoc rationalization), 而不是「預先原則」(a priori principle)。改革開放每一個具體決策, 都是根據案例適配的 (Heilmann 的 "Experimentation" 模式), 而不是「中國特色社會主義理論」直接演繹。

### Q6: 當代中國知識分子的困境
**Q**: 在意識形態控制和市場化媒體的雙重壓力下, 當代中國知識分子如何保持「批判性」? 他們的「批判」與1980年代知識分子的「批判」有什麼本質差異?

**A (≥10 lines)**:
當代中國知識分子的「批判性」與1980年代知識分子的「批判性」的根本差異, 是**矛頭指向**的不同:
- **1980年代**: 矛頭指向文化大革命, 指向「四人幫」, 指向毛晚年的「封建社會主義」餘毒, 指向蘇式「資產階級自由化」(Liu Binyan 劉賓雁, 方勵之, 王若水)。**真正的「批判」矛頭, 從來沒有指向中共黨的「執政合法性」本身** (Link 2013: ch.7-9)。1989 年後, 這個「自由化」批判被打成「動亂」, 主要人物 (劉賓雁 1987-88 被開除黨籍; 方勵之 1987 被解職) 流亡海外。
- **1990年代至今**: 矛頭指向「官僚腐敗」(腐敗, 形式主義), 而不是指向黨制本身。這是「可表達的批判」範圍的收窄 (Link 2013, *The Uses of Literature*, ch.7)。

具體的「批判」策略:
1. **體制內**: 利用「兩會」提案、黨的內部刊物 (《理論動態》、《黨政幹部參考》) 等渠道表達。例子: 茅于軾 (2006 《中國的道德重建》, 試圖重建的自由主義道德論).
2. **體制外**: 利用香港、紐約、倫敦等「飛地」出版 (例如《動向》、《蘋果日報》1995-2021、《開放》)。例子: 2012-2020 年獲諾貝爾和平獎的劉曉波 (1955-2017) 的《零八憲章》(2008年12月9日發表, 呼籲「自由、民主、憲政」——胡錦濤指其為「危害國家安全罪」, 判刑 11 年, 在監禁中病逝 2017-07-13).
3. **自媒體時代**: 微博 (2009-2019)、微信公眾號 (2012-) 等新媒體在 2018 年前後被強烈審查, 但仍湧現一些運用「高級黑」(dark humor)、歷史隱喻、學術暗語的批判性話語。

學者研究: **Perry Link (2013, Ch.7)** 把當代中國公共領域的收縮命名為 "anaconda in the chandelier"——壓迫存在, 但難以命名。**Wang Hui (2016 *China's Twentieth Century*)** 認為: 中國知識分子必須重新思考「中國現代性」(Chinese modernity) 本身, 這個現代性不是「西方現代性的模仿」, 也不是「獨立軌道」, 而是一個「脫節」(disarticulated) 的現代性模式 (Zhang Xudong 1997)。

### Q7: 毛澤東的農民平均主義與西方自由主義的平等觀
**Q**: 毛澤東對「平等」的理解, 與西方自由主義的「機會平等」有什麼根本差異? 這種「農民平均主義」如何解釋了大躍進和文革的暴力性?

**A (≥10 lines)**:
西方自由主義傳統中的平等觀是 **「機會平等」(equality of opportunity)**，以 **John Rawls**(*A Theory of Justice*, 1971) 的「**公平機會平等**」原則為代表 (Rawls: 「要平等分配基本權利, 同時允許社會經濟不平等, 但要符合最少受惠者的最大利益」(the difference principle))。這個原則允許結果的不平等, 只要機會均等。

毛澤東的平等觀是 **「結果平等」(equality of outcome)**，以 1920 年代湖南農民運動為田野觀察起點 (《湖南農民運動考察報告》, 1927), 受 1958-1976 蘇式史太林主義啟示和農民歷史上的「均貧富」傳統。**這個原則要求在結果上壓平經濟和社會差距**。

具體差異:
$$\text{Equality}_{\text{Liberal}} = \max \text{Status of the worst-off} \quad \text{subject to fair equality of opportunity}$$
$$\text{Equality}_{\text{Mao}} = \text{Minimize variance of individual outcomes}$$

毛澤東的「結果平等」有三個結構性問題:
1. **主觀性**: 誰來定義「結果平等」? 黨、群眾、知識分子?
2. **強制性**: 在執行「平均」時, 「走資本主義道路的當權派」必須被「剝奪」(文革「抄家」、1962 年七千人大會上劉少奇被列為「走資派」)。
3. **暴力性**: 強制執行 8-10 億人 (1970 年代人口) 上的「絕對平等」, 需要前所未有的社會動員, 必然帶來大規模暴力 (MacFarquhar & Gao 2006)。

歷史影響: **賀雪峰 (2017 *中國農村治理》》**指出: 「當代中國農村土地集體所有制」是毛的「平均主義」在 21 世紀的殘餘, 與資本主義土地私有制的論述差異, 構成 2014-2018 年新一輪「集體化 vs 私有化」辯論.

### Q8: 意識形態作為執政工具 — 從「階級鬥爭」到「中華民族偉大復興」
**Q**: 從毛澤東的「階級鬥爭」到習近平的「中華民族偉大復興」, 中國共產黨在不同歷史時期如何調整意識形態話語以服務執政需要?

**A (≥10 lines)**:
中共意識形態話語的四個時期:

| 時期 | 核心話語 | 主要功能 | 學者引用 |
|---|---|---|---|
| 毛澤東時期 (1949-1976) | 階級鬥爭、「反修防修」 | 動員群眾, 維持黨的純潔性 | Schram 1989, MacFarquhar 1974/1983/1997 |
| 鄧小平時期 (1978-1992) | 經濟建設為中心、「實事求是」 | 推動改革開放, 避開意識形態爭論 | Meisner 1999 ch.11, Naughton 2007 |
| 江胡時期 (1992-2012) | 「三個代表」、「社會主義市場經濟」、「和諧社會」 | 為資本家入黨正名、安撫社會矛盾 | Heilmann 2019 ch.5 |
| 習近平時期 (2012-) | 「中華民族偉大復興」、「兩個一百年」、「中國夢」 | 為黨的領導注入民族主義熱情, 為「黨政軍民學」黨的總攬再定義 | Bell 2015, Schoenhals 2019 |

關鍵的意識形態工具箱:
1. **「歷史決議」傳統**: 1981 年《關於建國以來黨的若干歷史問題的決議》(對毛遣產定性); 2021 年《關於黨的百年奮鬥重大成就和歷史經驗的決議》(對鄧、江、胡定性, 確立習近平時代的黨史地位) — 兩個決議是雙重變速器 (gear shift).
2. **「三個公式」話語**: 「馬克思主義中國化」→「中國特色社會主義」→「中華民族偉大復興中國夢」——三階段的政治話語技術 (Schoenhals 2019 *Doing Things with Words in Chinese Politics*).
3. **「四個自信」**: 道路自信、理論自信、制度自信、文化自信 (2016 年習近平講話)——以「四個自信」把黨的執政合法性從「歷史績效」(歷史決議) 轉到「體系自生」(autopoietic system).

學者研究: **Wang Zheng 2008 (*Never Forget National Humiliation*)** 提出: 民族主義話語是中國共產黨意識形態轉型的主要載體. **Holly Snape 2016 (*The Red and the Black*)** 提出: 「共產意識形態」和「中華意識形態」是中共意識形態寶庫的兩個軸。**Schoenhals 2019** 進行了深入的政治語言學分析。

### Q9: 思想史與政治史的關係
**Q**: 中國共產黨的意識形態史, 如何與中國共產黨的政治史、軍事史相互影響? 思想路線的變化如何預示了政治路線的變化?

**A (≥10 lines)**:
思想史與政治史的關係, 是歷史學的經典爭論 (Hayden White 1973, *Metahistory*; Paul Veyne 1971 *Comment on écrit l'histoire*). 中國的情況可以從四個案例看出:

- **案例一: 1962 年七千人大會 → 1966 年文革**: 1962 年 1 月劉少奇在七千人大會提「三分天災, 七分人禍」, 1962 年 9 月八屆十中全會毛澤東重提「階級鬥爭」, 1963 年起推動「四清」、「社會主義教育運動」, 1966 年 8 月毛以《十六條》正式啟動文革。這個時間線揭示了:**思想路線的「換錨」早於政治路線的「轉向」**。劉被「拉下」是因為毛認定劉的「修」已經危害到黨內路線的本質。

- **案例二: 1978 年〈實踐是檢驗真理的唯一標準〉→ 改革開放**: 1978 年 5 月 11 日《光明日報》評論員文章 (鄧力群、胡耀邦、胡喬木支持) 引發「真理標準」大討論——被鄧小平稱為「思想路線」問題。1978 年 12 月十一屆三中全會確立「實事求是」。**思想解放先於政治變革**。

- **案例三: 1989 年天安門事件 → 1992 年南巡**: 1989 年 6 月 4 日天安門清場, 1989-91 年「反自由化」、「清除精神污染」運動; 1992 年 1-2 月鄧南巡重新為「社會主義市場經濟」背書。**意識形態從社會主義 + 反修 5 年大反轉為市場社會主義**, 標誌着「意識形態服務於經濟建設」明確化。

- **案例四: 2013 年「九號文件」→ 2017-2022 「共同富裕」、「動態清零」**: 2013 年 5 月 8 日中共中央「九號文件」(Sept 8-9, *硏報 2013-05*) 警告: 黨的意識形態工作被「西化、分化、邊緣化、空洞化、物化、弱化、儀