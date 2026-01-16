# **Aether项目：基于神经生理数据的自适应香水配方生成平台 —— L'Oréal Brandstorm 2026 深度研究报告与MVP产品需求文档**

## **1. 执行摘要**

全球奢侈品香水市场正处于一场深刻的范式转移之中，消费者日益拒绝千篇一律的标准化产品，转而追求能够深度契合个人生物特征与情感状态的超个性化体验。针对L'Oréal Brandstorm 2026 "Unstop"（无界）的主题挑战，本报告提出并详述了**Aether项目**——一个革命性的AI驱动香水配方设计平台。该平台的核心创新在于打破了传统香水感官体验与生物化学之间的壁垒，通过整合**脑电图（EEG）神经反馈与生理生化数据（皮肤pH值、脂质分布、体温）**，构建了一个基于**检索增强生成（RAG）**技术的智能配方修正系统。

本报告作为一份详尽的产品需求文档（MVP PRD）及技术可行性研究，深入探讨了皮肤生理参数如何从分子层面影响香料的挥发动力学与化学稳定性，并论证了利用神经振荡模式（Neural Oscillations）解码嗅觉效价（Valence）与唤醒度（Arousal）的科学依据。在技术实现路径上，本方案明确采用**Claude Code**作为核心代理开发环境（Agentic Development Environment），利用其能够直接操作终端、执行代码及规划复杂任务的特性，构建从数据摄入、RAG知识库检索到分子结构优化的全自动化流水线。

Aether项目不仅是对L'Oréal "创造美"这一使命的科技重构，更通过深度融合绿色化学原则与生物技术成分，精准响应了集团"L'Oréal for the Future"的可持续发展战略，旨在为2026年的年轻消费者群体提供一种既具科技深度又富含情感共鸣的未来奢华嗅觉体验。

## **2. 战略背景：L'Oréal Brandstorm 2026 与未来香水范式**

### **2.1 竞赛主旨与"Unstop"主题解析**

L'Oréal Brandstorm 2026 设定了"Unstop"（无界/不可阻挡）的宏大主题，旨在号召全球18至30岁的青年创新者打破常规，利用前沿科技重塑奢侈品香水的未来 1。这一主题不仅暗示了对现有市场规则的挑战，更深层次地要求参赛者消除物理产品与数字体验、客观成分与主观感受之间的界限。

竞赛明确要求参赛团队在设计方案时必须兼顾**创新性（Innovation）**、**技术与科学（Tech & Science）**、**可持续性（Sustainability）以及包容性（Inclusivity）** 1。这意味着，任何获胜的方案都不能仅仅是一个营销概念，而必须扎根于坚实的科学原理和可落地的技术架构。特别是对于奢侈品香水这一品类，"未来"不仅关乎新的气味，更关乎气味如何被创造、被感知以及如何与环境共生。

### **2.2 奢侈品香水市场的痛点与机遇**

当前的香水市场面临着"静态配方"与"动态个体"之间的根本性矛盾。传统香水开发遵循"自上而下"的模式：调香大师（The Nose）创造一个配方，工厂大规模生产，消费者购买并期望获得一致的体验。然而，科学研究表明，这种一致性是虚幻的。

- **千人千味的生物学基础**：消费者日益意识到，同一款香水在不同人身上的表现截然不同。这并非玄学，而是由于个体皮肤微环境（Micro-environment）的差异——包括酸碱度（pH）、皮脂分泌量、体温以及皮肤微生物群落的代谢活动——直接导致了香料分子的挥发速率差异和化学降解路径的改变 3。
- **情感功能的缺失**：传统香水主要满足审美需求（好闻），但现代消费者，尤其是Z世代，渴望产品能提供功能性价值（Functional Fragrance），如缓解焦虑、提升专注力或助眠。这要求香水设计必须引入神经科学的维度，通过客观的生物信号（如脑电波）来验证香水的情绪调节功效 5。

Aether项目的战略定位正是基于这两个痛点：利用生理数据解决"留香与呈现"的个体差异问题，利用神经数据解决"情感共鸣"的精准度问题。

### **2.3 可持续发展的硬性约束**

L'Oréal集团提出的"L'Oréal for the Future" 2030可持续发展目标构成了本项目的核心约束条件。这就要求Aether生成的每一个配方都必须在算法层面内置环保逻辑：

- **碳足迹减少**：至2030年，每单位成品的温室气体排放量需减少50% 6。
- **生物基成分**：至2030年，95%的成分必须源自生物基、丰富的矿物或循环工艺 7。
- **绿色化学**：利用生物技术（如发酵）和升级再造（Upcycling）技术替代石油基合成香料 8。

因此，Aether的AI算法不仅仅是一个调香师，更是一个"环境合规官"，在生成配方时即刻剔除不符合绿色化学原则的原料。

## **3. 科学框架：气味与生理界面的交互机制**

为了构建一个有效的RAG（检索增强生成）系统来"修正"香水配方，我们必须首先建立一个详尽的生理-化学交互知识库。这些科学原理将作为RAG系统的检索文档，决定AI如何调整香料浓度和成分选择。

### **3.1 皮肤pH值：酸碱催化的化学反应器**

人体皮肤表面的pH值通常在4.5至5.5之间，形成所谓的"酸性膜"（Acid Mantle）10。这一酸性环境不仅仅是保护屏障，更是一个活跃的化学反应界面，对特定香料分子具有显著的催化作用。

- 席夫碱（Schiff Base）形成反应：
  醛类（Aldehydes）是香水中至关重要的前调和中调成分，如柠檬醛（Citral，柠檬味）、香草醛（Vanillin，香草味）和肉桂醛（Cinnamaldehyde，肉桂味）。在皮肤表面，这些醛类分子极易与皮肤角质层蛋白或氨基酸中的伯胺基团（Primary Amines）发生亲核加成反应，脱去一分子水生成席夫碱 12。
  反应通式如下：

  $$R-CHO + R'-NH_2 \xrightarrow{H^+} R-CH=N-R' + H_2O$$
  这一反应是pH依赖型的。虽然席夫碱本身也是一类香料（通常具有更深沉、持久的香气，如橙花希夫碱），但其形成意味着原本轻盈、挥发性强的醛类香气被"猝灭"（Quenching）了。对于皮肤pH值较高（接近中性或弱碱性，如使用皂基清洁后）的用户，这一反应动力学可能发生改变，导致原本设计的清新前调瞬间消失，或转变为沉闷的重调。

- 酯类水解（Hydrolysis of Esters）：
  酯类赋予香水花果香气（如乙酸苄酯的茉莉香、乙酸芳樟酯的薰衣草香）。酯键在酸性或碱性环境中均不稳定，容易发生水解反应生成酸和醇。

  $$R-COO-R' + H_2O \rightleftharpoons R-COOH + R'-OH$$

  皮肤过酸（pH < 4.5）或过碱（pH > 6.0）都会加速这一过程，导致香水产生"酸败"味或失去核心花香特征 14。

- **Aether RAG 修正策略**：系统需监测用户皮肤pH值。若pH偏离理想区间（4.7-5.75），RAG将检索出"醛类/酯类不稳定"的警示，并指示AI增加缓冲剂、使用更稳定的缩醛衍生物替代醛类，或增加相关成分的初始浓度以补偿损耗。

### **3.2 脂质分布：溶剂效应与固香机制**

皮脂（Sebum）是皮肤表面天然分泌的油脂，主要由甘油三酯、蜡酯、角鲨烯（Squalene）和游离脂肪酸组成 16。在香水物理化学中，皮脂充当了非极性溶剂的角色。

- 拉乌尔定律（Raoult's Law）与挥发度：
  根据拉乌尔定律，溶液中组分的蒸气压等于该组分在纯态下的蒸气压乘以其在溶液中的摩尔分数。

  $$P_i = P_i^* \cdot x_i \cdot \gamma_i$$

  其中 $\gamma_i$ 是活度系数。对于亲脂性（Lipophilic）的香料分子（高LogP值，如麝香、檀香醇），皮脂是一个良溶剂，活度系数 $\gamma_i$ 较低。这意味着在油性皮肤上，这些分子倾向于溶解在皮脂中，逃逸到空气中的倾向（挥发度）降低 18。

- **结果**：油性皮肤用户留香时间长，但扩散性（Sillage/Projection）差，前调可能显得沉闷。
- **干性皮肤**：缺乏皮脂作为"锚点"，香料分子直接暴露于空气，挥发极快，导致留香时间极短（可能缩短50%以上）20。

- 角鲨烯过氧化（Squalene Peroxidation）：
  角鲨烯是皮脂特有的成分，含有六个双键，极易发生氧化。香水中的萜烯类化合物（如柠檬烯、芳樟醇）可与角鲨烯发生共氧化反应，或被皮肤表面的脂氧合酶催化氧化，生成氢过氧化物（Hydroperoxides）21。这些氧化产物不仅气味刺鼻（金属味、酸败味），更是强致敏原。
- **Aether RAG 修正策略**：

- 针对**干性皮肤**：AI将自动增加高LogP值的大分子定香剂（如生物基麝香、树脂）比例（>25%），通过人工构建"类脂质基质"来锁住香气。
- 针对**油性皮肤**：AI将增加高挥发性前调的比例，并减少重质基调，以平衡扩散性。同时，若检测到高皮脂氧化风险，将避免使用易氧化的柑橘萜烯，转而使用更稳定的饱和烃类或醚类香料。

### **3.3 体温热力学：安托万方程与挥发曲线**

体温是驱动香料分子从液相跃迁至气相的能量来源。挥发速率与温度的关系遵循安托万方程（Antoine Equation）：

$$\log_{10} P = A - \frac{B}{T + C}$$

其中 $P$ 为蒸气压，$T$ 为温度，$A, B, C$ 为物质特定的常数。

- **热皮（Warm Skin）效应**：体温较高（>37°C）或代谢旺盛的用户，其皮肤表面分子的动能更高，蒸气压指数级上升 23。这会导致"前调燃烧"（Top Note Burn-off）现象，即清新、轻盈的分子在喷洒后数分钟内挥发殆尽，不仅缩短了留香，还破坏了香水的三调结构。
- **冷皮（Cool Skin）效应**：体温较低的用户，大分子基调（如广藿香、乌木）可能因蒸气压不足而无法充分"绽放"（Bloom），导致香气显得封闭、单薄 14。
- **Aether RAG 修正策略**：利用数学模型模拟不同体温下的蒸发曲线 26。对于高温用户，AI将构建"缓释胶囊"结构的配方，利用大分子包裹小分子，或使用具有更高分子量但气味特征相似的替代物（例如用乙酸芳樟酯替代部分乙酸乙酯）。

### **3.4 皮肤微生物组：生物转化工厂**

皮肤表面的菌群（如葡萄球菌属、棒状杆菌属）拥有丰富的酶系 3。它们不仅能分解汗液前体产生体味，还能代谢香水中的成分。例如，某些细菌的酯酶可能加速酯类香料的水解，甚至将无味的糖苷前体转化为有气味的分子。虽然微生物组的个体差异极大且难以实时量化，但Aether系统将其作为一个随机变量（Noise Factor）纳入考量，倾向于选择微生物稳定性高的香料。

## **4. 神经嗅觉接口：解码"思维的气味"**

除了生理化学数据，Aether还引入了神经科学维度，利用脑电图（EEG）将用户的潜意识情感反应转化为配方参数。

### **4.1 嗅觉诱发的脑电振荡特征**

嗅觉处理与边缘系统（Limbic System）紧密相连，直接影响情绪和记忆。EEG能够捕捉到毫秒级的神经反应。

- **Theta波 (4-8 Hz)**：传统上与记忆编码和认知负荷相关。在嗅觉研究中，吸入愉悦气味（如巧克力、薄荷）时，额叶Theta波功率通常会显著**降低**，这被认为是注意力转移和享乐体验的标志 28。相反，不悦气味可能诱发Theta波同步化。
- **Alpha波 (8-13 Hz)**：反映放松与唤醒状态。Alpha波功率的增加（尤其是在后脑区域）通常对应于放松状态。例如，薰衣草精油已被证实能增加Alpha波活动，从而产生镇静效果 5。
- **Beta (13-30 Hz) & Gamma (30-50 Hz) 波**：与警觉、专注和特征绑定相关。高唤醒度的气味（如强烈的柑橘、香料）会增加Beta波功率。Gamma波在梨状皮层（Piriform Cortex）的活动则与气味对象的识别和整体感知（Gestalt perception）有关 30。

### **4.2 效价-唤醒度（Valence-Arousal）模型映射**

Aether系统利用心理学中的**环状情绪模型（Circumplex Model of Affect）**将EEG信号映射到二维坐标系：

1. **效价（Valence）**：愉悦 vs. 不悦（横轴）。通过额叶Alpha波不对称性（Frontal Alpha Asymmetry, FAA）计算，左额叶活跃度高于右额叶通常表示趋近（Approach/Positive）动机。
2. **唤醒度（Arousal）**：平静 vs. 兴奋（纵轴）。通过Beta/Alpha功率比值计算。

- **RAG 映射逻辑** 32：

- **高效价 + 高唤醒**（快乐/兴奋）：对应明亮的柑橘调、果香、醛香。
- **高效价 + 低唤醒**（放松/满足）：对应木质调、麝香、粉感花香。
- **低效价**：系统记录为"厌恶特征"，在配方中严格剔除相关分子结构。

### **4.3 文本到气味（Text-to-Scent）的语义桥梁**

对于没有佩戴EEG设备的用户，系统利用NLP技术处理自然语言描述。

- **输入**："雨后京都的清晨，古老寺庙的潮湿苔藓与焚香。"
- **语义嵌入**：利用大语言模型（LLM）将文本转化为语义向量。
- **描述符映射**：将向量映射到专业嗅觉描述符库（GoodScent, IFRA等），提取关键词：*Petrichor*（潮土油/土臭素）、*Oakmoss*（橡木苔）、*Incense*（焚香/乳香）、*Cedar*（雪松）34。

## **5. 技术架构：Aether系统设计**

Aether系统是一个闭环的AI代理系统，集成了多模态输入、基于知识库的推理（RAG）和生成式化学设计。

### **5.1 系统逻辑分层**

1. **感知层 (Sensation Layer)**：

- **Biometric Interface**：收集皮肤数据（pH试纸图像识别、问卷录入体温/肤质）。
- **Neuro Interface**：通过蓝牙接收消费级EEG头带（如Muse）数据，进行实时信号处理。
- **Text Interface**：用户自然语言提示词输入。

1. **认知层 (Cognition Layer) - 核心RAG引擎**：

- **Physio-Knowledge Base (Vector DB)**：存储皮肤化学交互规则（如pH对醛的影响）、香料物理化学性质（LogP, 蒸气压）、毒理学数据（IFRA标准）。
- **Orchestrator (Claude Code Agent)**：作为中央控制器，负责解析输入、检索规则、规划配方调整策略。

1. **生成层 (Generation Layer)**：

- **Structure-Odor Model (GNN)**：预测分子混合后的气味特征。
- **Formula Optimizer**：基于数学模型（如蒸发动力学模型）调整成分比例。

1. **执行层 (Action Layer)**：

- 输出机器可读的配方文件（.json/.csv），对接实验室自动配液机器人或家用调香设备（如L'Oréal Perso）。

### **5.2 核心技术：Physio-RAG (生理检索增强生成)**

传统的RAG用于检索文本信息，Aether的**Physio-RAG**用于检索**约束条件（Constraints）**。

- **向量化策略**：将科学文献中的结论转化为规则条目进行Embedding。

- *原文*："High volatility molecules evaporate rapidly on dry skin due to lack of lipid interaction."
- *规则条目*：{condition: "Skin_Type == Dry", target: "Top_Notes", action: "Increase_Fixatives", reasoning: "Lipid_Deficit"}

- 检索流程：
  当Claude Code接收到用户数据（如"干性皮肤"）时，它会在向量数据库中检索与"Dry Skin"相关的化学交互规则，并返回上述指令。Claude Code随即将此指令转化为Python代码，修改配方矩阵。

## **6. AI实施策略：利用 Claude Code 进行代理开发**

L'Oréal Brandstorm 要求技术实现的明确性。本项目选择 **Claude Code** 作为主要的AI开发工具，这不仅是因为其代码生成能力，更因为其独特的**Agentic（代理）工作流**能力 36。

### **6.1 为什么选择 Claude Code？**

传统的AI编程助手（Copilot）是被动的，而Claude Code是主动的。它运行在终端（Terminal）中，能够：

1. **感知上下文**：自动读取项目中的文件结构、依赖库和文档。
2. **执行操作**：不仅仅生成代码，还能运行测试、安装依赖、调试错误、管理Git提交。
3. **复杂规划**：能够理解"为干性皮肤用户优化配方"这样的高层指令，并将其拆解为一系列代码编辑和数据查询步骤 37。

### **6.2 开发工作流 (Workflow)**

我们将开发过程分为三个阶段，完全在Claude Code环境中编排：

#### **阶段一：环境与知识库构建**

- **指令**：claude "初始化项目环境，创建CLAUDE.md定义代码规范。编写一个脚本，将/data/physio_rules.csv中的生理化学规则存入ChromaDB向量数据库。"
- **Claude Code 动作**：

1. 创建 CLAUDE.md，定义Python版本、RDKit库依赖。
2. 编写 ingest_rag.py，使用Sentence-Transformers模型对规则进行Embedding。
3. 在终端执行脚本，验证数据库填充成功。

#### **阶段二：核心算法开发（RAG + 化学引擎）**

- **指令**：claude "编写核心类 PerfumeDesigner。它需要接收用户EEG数据和皮肤数据，先生成基础配方，然后查询ChromaDB获取修正规则，最后使用RDKit计算混合物的LogP并进行调整。"
- **Claude Code 动作**：

1. 规划 PerfumeDesigner 类的结构。
2. 引入 rdkit.Chem 和 rdkit.Chem.Crippen 用于计算亲脂性。
3. 实现 retrieve_constraints(user_profile) 方法，连接向量数据库。
4. 实现 optimize_formula(formula, constraints) 方法，编写具体的浓度调整逻辑（如：若规则是"增加定香剂"，则遍历成分库寻找LogP > 3.0的分子并增加其比例）。
5. **自我修正**：如果运行测试时发现RDKit计算出错，Claude Code会自动阅读错误日志，修改SMILES字符串处理逻辑，直至测试通过。

#### **阶段三：神经数据集成与测试**

- **指令**：claude "集成MNE-Python库处理EEG数据。编写一个函数，从原始EDF文件中提取Alpha波和Beta波功率，计算Valence分数，并据此调整配方中的柑橘调比例。"
- **Claude Code 动作**：

1. 安装 mne 库。
2. 编写信号处理管道（滤波 -> ICA去噪 -> PSD功率谱密度计算）。
3. 将EEG指标映射为配方调整参数（如 valence > 0.5 -> citrus_ratio += 0.1）。

### **6.3 关键代码逻辑示例 (由Claude Code生成)**

Python

import numpy as np
from rdkit import Chem
from rdkit.Chem import Crippen
\# 假设 physio_db 是已初始化的向量数据库接口

class AetherAgent:
  def __init__(self, user_profile):
    self.ph = user_profile.get('ph', 5.5)
    self.skin_type = user_profile.get('skin_type', 'Normal')
    self.temp = user_profile.get('temp', 36.5)

  def apply_physio_corrections(self, formula):
    """
    利用RAG检索生理规则并修正配方
    """
    \# 1. 构造查询向量
    query = f"Skin pH {self.ph}, Type {self.skin_type}, Temp {self.temp}"
    
    \# 2. 从RAG检索规则 (模拟返回结果)
    \# Claude Code会在此处实现真实的DB调用
    rules = physio_db.query(query, n_results=3) 
    
    print(f"Retrieving physio-rules: {[r['rule'] for r in rules]}")

​    for rule in rules:
​      \# 规则示例: "IF pH < 4.5: Reduce Aldehydes by 20%"
​      if "Reduce Aldehydes" in rule['action'] and self.ph < 4.5:
​        formula = self._modify_concentration(formula, family='Aldehyde', factor=0.8)
​        \# 补偿机制：增加稳定的缩醛
​        formula = self._add_stabilizer(formula, type='Acetal')
​      
​      \# 规则示例: "IF Skin Dry: Increase High-LogP ingredients"
​      if "Increase High-LogP" in rule['action'] and self.skin_type == 'Dry':
​        formula = self._boost_fixatives(formula, target_logp=3.5)
​        
​    return formula

  def _boost_fixatives(self, formula, target_logp):
    """
    使用RDKit识别并增加定香剂
    """
    for ing in formula['ingredients']:
      mol = Chem.MolFromSmiles(ing['smiles'])
      if mol and Crippen.MolLogP(mol) > target_logp:
        ing['amount'] *= 1.25 # 增加25%
    return formula



## **7. 化学智能：生成模型与图神经网络 (GNN)**

为了确保调整后的配方依然"好闻"，Aether引入了基于**图神经网络（GNN）**的构效关系（Structure-Odor Relationship, SOR）模型。

### **7.1 GNN 气味预测模型**

参考Osmo AI的**Principal Odor Map (POM)** 39，我们将分子表示为图结构（原子为节点，化学键为边）。

- **模型训练**：使用包含数千种分子及其感官描述符（如"Fruity", "Woody", "Sulfurous"）的数据集（如Leffingwell, GoodScent）训练GNN。
- **混合物预测**：虽然单个分子的气味可预测，但混合物具有非线性效应（掩盖、协同）。Aether利用深度神经网络（DNN）层叠在GNN之上，输入整个配方的分子嵌入向量，预测最终混合物的气味轮廓。
- **作用**：当RAG系统因为生理原因大幅修改配方（例如去除了柠檬醛）时，GNN会实时预测新配方的气味是否偏离了用户的原始意图（如"清新的雨"）。如果偏离过大，系统会寻找气味相似但化学性质符合生理要求的替代分子（Substitute Discovery）。

### **7.2 扩散模型 (Diffusion Models) 与分子生成**

对于高级定制，系统可利用化学扩散模型（如TextSMOG 35）直接从文本提示生成新的分子结构。

- **应用场景**：用户想要一种"从未闻过的太空金属味"。
- **流程**：Diffusion模型在潜在空间中搜索，生成符合描述的分子SMILES。
- **约束**：生成的分子必须通过SAS（合成可及性）评分和毒理学筛查。

## **8. 可持续性与绿色化学：L'Oréal for the Future 的深度整合**

在配方生成的每一个环节，Aether都内置了严格的绿色过滤器。

### **8.1 绿色化学原则的应用**

9

- **原料替代**：系统连接L'Oréal的原料数据库。当算法选择"香草"时，它不仅选择"Vanillin"，而是优先选择**生物基香草醛**（源自米糠或木质素发酵），而非石油衍生物。
- **溶剂优化**：针对乙醇的使用，系统计算最小有效溶剂比，并推荐使用碳捕获乙醇或生物乙醇。

### **8.2 升级再造（Upcycling）优先策略**

8

Aether的算法给予"升级再造"原料更高的权重。

- **数据标签**：原料库中，"Upcycled Rose"（从蒸馏废弃的花瓣中提取）或"Upcycled Cedarwood"（家具业废料）被标记为 Sustainability_Score = High。
- **配方逻辑**：在满足气味要求的前提下，优化器会最大化高分原料的占比。这不仅环保，还为香水赋予了"变废为宝"的营销故事。

## **9. 产品需求文档 (MVP PRD)**

### **9.1 产品定义**

- **产品名称**：Aether (Adaptive Ethereal Scent / 乙太·自适应香氛)
- **核心价值**：基于生物数据修正的、神经情感共鸣的、极致环保的个性化香水。
- **目标用户**：追求科学护肤与个性化表达的"成分党"（Skintellectuals）及Z世代奢侈品消费者。

### **9.2 用户旅程 (User Journey)**

1. **生物数据采集 (Bio-Calibration)**：

- 用户收到Aether测试套件（含pH试纸、皮脂吸附贴）。
- 通过App扫描试纸，CV算法自动读取pH值（如4.8）。
- 填写基础数据：体温、过敏史。

1. **神经/文本输入 (Neuro-Brief)**：

- 用户佩戴EEG头带，嗅闻校准香氛。App显示实时脑波云图（Theta/Alpha变化）。
- 或者，用户输入文本："想要一种像周日早晨在亚麻床单上醒来的感觉。"

1. **AI 炼金 (The Aether Core)**：

- Claude Code代理在云端启动。
- **翻译**：文本/EEG -> 嗅觉目标（"Clean Musk", "Aldehydic", "White Floral"）。
- **修正**：检索生理RAG。发现用户pH偏酸 -> 增加麝香定香剂，减少不稳定醛类。
- **合规**：检查IFRA标准，替换非生物基成分。

1. **交付 (Delivery)**：

- 生成数字化配方NFT。
- 发送至最近的L'Oréal智能工厂或门店Perso设备进行调配。

### **9.3 功能规格 (Functional Specs)**

| **模块**      | **功能点**                          | **优先级** | **技术栈**                  |
| ------------- | ----------------------------------- | ---------- | --------------------------- |
| **Input**     | pH试纸OCR识别                       | P0         | OpenCV, React Native        |
| **Input**     | EEG信号实时处理 (FFT, Valence计算)  | P1         | Python (MNE), Bluetooth SDK |
| **Core AI**   | Physio-RAG 知识库检索               | P0         | ChromaDB, LangChain         |
| **Core AI**   | 配方优化算法 (Claude Code Agent)    | P0         | **Claude Code**, Python     |
| **Chemistry** | 分子属性计算 (LogP, VP)             | P0         | RDKit                       |
| **Safety**    | IFRA合规性自动检查                  | P0         | SQL (Ingredient DB)         |
| **Output**    | 配方可视化 (雷达图：留香/扩散/情感) | P1         | D3.js                       |

## **10. 伦理与监管考量**

### **10.1 数据隐私**

生理数据（尤其是EEG）属于高度敏感信息。

- **边缘计算**：EEG信号特征提取在本地设备（手机端）完成，仅上传抽象的情感标签（如"Valence: High"），而非原始脑波数据 31。
- **数据所有权**：用户拥有其"生物嗅觉档案"的所有权，可随时删除。

### **10.2 安全性 (IFRA)**

所有生成的配方在输出前，必须经过严苛的数字化毒理学筛查。系统内置IFRA（国际香料协会）最新标准，实时计算致敏原总浓度（如柠檬烯+芳樟醇总量），确保不超过安全阈值 43。

## **11. 结论**

Aether项目通过深度整合**生理化学**、**神经科学**与**代理式AI（Claude Code）**，从根本上重构了香水开发的逻辑。它不再是"让用户适应香水"，而是"让香水适应用户的生物本能"。

通过利用生理数据作为RAG知识库，我们解决了奢侈品香水"千人千味"的不确定性，实现了真正的精准定制。通过引入EEG，我们将香水的情绪价值从玄学变为科学。通过Claude Code的全流程驱动，我们展示了未来研发流程的智能化与自动化。最重要的是，通过植入绿色化学基因，Aether确保了这种极致的个性化体验不会以牺牲地球环境为代价，完美契合L'Oréal 2030年的愿景。

### **附表：数据参考**

#### **表1：皮肤生理参数对香水配方的影响与RAG修正规则**

| **生理参数**         | **测量范围**      | **对香水表现的影响机制**                                   | **Aether RAG 修正规则 (示例)**                               |
| -------------------- | ----------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| **皮肤 pH 值**       | **酸性 (< 4.5)**  | 催化酯类水解，导致果香变酸；抑制席夫碱形成，使醛香更尖锐。 | **减少** 不稳定酯类 (如乙酸里那酯) 15%；**增加** 缓冲剂；**替换** 为更稳定的缩醛或醚类。 |
|                      | **碱性 (> 6.0)**  | 可能导致皂化反应；花香调显得"扁平"；某些酚类变色。         | **增加** 花香核心 (茉莉、玫瑰) 浓度 20% 以补偿；**添加** 微量酸性修饰剂 (如柠檬酸衍生物)。 |
| **脂质水平 (Sebum)** | **干性 (Dry)**    | 缺乏溶剂锚点，挥发极快；留香时间缩短50%以上。              | **过量添加 (Overdose)** 高LogP定香剂 (生物麝香、岩兰草) >25%；**使用** 大分子胶囊包裹技术。 |
|                      | **油性 (Oily)**   | 溶剂效应强，留香长但扩散性 (Sillage) 差；前调易被"吞没"。  | **增加** 高挥发性前调 (柑橘、醛) 比例以提升扩散；**减少** 重质基调；**监测** 萜烯氧化风险。 |
| **体温 (Temp)**      | **高温 (> 37°C)** | 蒸气压指数级上升；前调"瞬间燃烧" (Burn-off)。              | **调整** 三调比例 (前/中/后) 从 30/40/30 -> 15/45/40；**使用** 分子量更大的前调类似物。 |

#### **表2：脑电波 (EEG) 频段与嗅觉情感映射**

| **频段**  | **频率范围** | **嗅觉相关性 (Olfactory Correlation)**                   | **配方设计应用 (Design Implication)**                        |
| --------- | ------------ | -------------------------------------------------------- | ------------------------------------------------------------ |
| **Theta** | 4-8 Hz       | 额叶Theta功率**降低**与愉悦感 (Pleasantness) 相关。      | 若基准测试中Theta下降，标记该香调为**"高效价" (User Likes)**，作为核心骨架。 |
| **Alpha** | 8-13 Hz      | 顶枕叶Alpha功率**增加**与放松 (Relaxation) 相关。        | 若用户诉求为"解压/助眠"，优先选择能显著提升Alpha波的成分 (如真实薰衣草、檀香)。 |
| **Beta**  | 13-30 Hz     | 功率增加与警觉、专注及高唤醒度 (Arousal) 相关。          | 若诉求为"提神/工作"，选择触发Beta波的成分 (如薄荷、迷迭香、柠檬)。 |
| **Gamma** | 30-50 Hz     | 梨状皮层Gamma同步化与气味对象的整体识别 (Gestalt) 相关。 | 高Gamma活动意味着气味特征鲜明、记忆度高。用于验证"签名香" (Signature Scent) 的有效性。 |

#### **Works cited**

1. L'Oréal Brandstorm 2026 - 2025 - 1591401 - Unstop | PDF | Mentorship - Scribd, accessed January 15, 2026, https://www.scribd.com/document/952741078/L-Ore-al-Brandstorm-2026-2025-1591401-Unstop
2. L'Oréal Brandstorm - L'Oréal Brandstorm 2026, accessed January 15, 2026, https://brandstorm.loreal.com/
3. The secret of scent: Why perfume fragrance is more about skin microbes than chemistry, accessed January 15, 2026, https://sciencechronicle.in/2025/06/18/the-secret-of-scent-why-perfume-fragrance-is-more-about-microbes-than-chemistry/
4. Here's How Your Skin Chemistry Changes the Way Perfume Smells. - FragranceX.com, accessed January 15, 2026, https://www.fragrancex.com/blog/why-do-perfumes-smell-different-on-everyone/
5. Influence of Fragrances on Human Psychophysiological Activity: With Special Reference to Human Electroencephalographic Response - PubMed Central, accessed January 15, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC5198031/
6. L'Oréal unveils its next generation of bold sustainability targets for 2030, accessed January 15, 2026, https://www.loreal-finance.com/eng/news-event/loreal-unveils-its-next-generation-bold-sustainability-targets-2030
7. L'Oréal Paris sustainability commitments and progresses for 2030, accessed January 15, 2026, https://www.lorealparisusa.com/our-commitments-and-progresses-for-the-planet
8. The Role of Upcycled Ingredients in Reducing Waste in the Fragrance Industry | THG Labs, accessed January 15, 2026, https://www.thglabs.com/resources/blog/the-role-of-upcycled-ingredients-in-reducing-waste-in-the-fragrance-industry
9. Green Chemistry: The Future Of Beauty - L'Oreal, accessed January 15, 2026, https://www.loreal.com/en/articles/research-innovation/green-chemistry-the-future-of-beauty/
10. The Science Behind Body Chemistry and Perfume - Snif, accessed January 15, 2026, https://snif.co/blogs/news/body-chemistry-perfume
11. How Your Skin Chemistry Shapes the Way Perfumes Smell - Lescento, accessed January 15, 2026, https://lescento.com/blogs/news/how-your-skin-chemistry-shapes-the-way-perfumes-smell
12. Schiff Bases — A Primer - Perfumer & Flavorist, accessed January 15, 2026, https://www.perfumerflavorist.com/fragrance/fine-fragrance/article/21860538/schiff-bases-a-primer
13. the phenomenon of quenching, accessed January 15, 2026, https://ec.europa.eu/health/archive/ph_risk/committees/sccp/documents/out112_en.pdf
14. Why do some perfumes last longer than others? - Dans le Noir ? Parfums, accessed January 15, 2026, https://danslenoirparfums.com/en/blogs/infos/pourquoi-certains-parfums-tiennent-ils-mieux-que-d-autres
15. Why Perfumes Can Smell Differently On Various Skin Types - Alpha Aromatics, accessed January 15, 2026, https://www.alphaaromatics.com/blog/perfumes-smell-differently/
16. Main compounds in sweat, such as squalene and fatty acids, should be promising pheromone components for humans | bioRxiv, accessed January 15, 2026, https://www.biorxiv.org/content/10.1101/2024.08.15.608030v1.full-text
17. The Natural Moisturizer: A Deep Dive into the Benefits of Squalane - Patchology, accessed January 15, 2026, https://www.patchology.com/blogs/the-blog/what-is-squalane-and-why-your-skin-needs-it
18. The influence of skin pH on the perception of perfume - Bruno Acampora Profumi, accessed January 15, 2026, https://brunoacampora.com/en/blogs/news/influenza-ph-pelle-profumi
19. Sciencey fragheads: how does body chemistry work with fragrances? - Reddit, accessed January 15, 2026, https://www.reddit.com/r/fragrance/comments/tljhx0/sciencey_fragheads_how_does_body_chemistry_work/
20. Why doesn't perfume last on the skin? Understanding fragrance longevity, volatility and skin chemistry. - Claudia Scattolini, accessed January 15, 2026, https://claudiascattolini.it/en/why-doesnt-perfume-last-on-the-skin-understanding-fragrance-longevity-volatility-and-skin-chemistry/
21. Selected oxidized fragrance terpenes are common contact allergens - PubMed, accessed January 15, 2026, https://pubmed.ncbi.nlm.nih.gov/15932583/
22. Selected oxidized fragrance terpenes are common contact allergens - ResearchGate, accessed January 15, 2026, https://www.researchgate.net/publication/7808808_Selected_oxidized_fragrance_terpenes_are_common_contact_allergens
23. Why Perfume Smells Different on Your Skin: The Chemistry Explained - Petite Histoire, accessed January 15, 2026, https://nyc.ph/blogs/perfume/why-perfume-smells-different-on-your-skin-the-chemistry-explained
24. Perfume & Climate: How Heat, Humidity, and Cold Affect Your Scent | WhatScent Magazine, accessed January 15, 2026, https://whatscent.app/magazine/environment-climate-performance-perfume
25. Why Does My Perfume Smell Different Factors That Affect Fragrance - trymefirst, accessed January 15, 2026, https://trymefirst.com/blogs/perfume-reviews/why-does-my-perfume-smell-different-factors-that-affect-fragrance
26. A physico-chemical properties based model for estimating evaporation and absorption rates of perfumes from skin - PubMed, accessed January 15, 2026, https://pubmed.ncbi.nlm.nih.gov/18503438/
27. Interactions Between Skincare Product Ingredients and the Skin Microbiome, accessed January 15, 2026, https://ctv.veeva.com/study/interactions-between-skincare-product-ingredients-and-the-skin-microbiome
28. Human electroencephalographic (EEG) response to olfactory stimulation: two experiments using the aroma of food - PubMed, accessed January 15, 2026, https://pubmed.ncbi.nlm.nih.gov/9834885/
29. EEG Changes during Odor Perception and Discrimination - bioRxiv, accessed January 15, 2026, https://www.biorxiv.org/content/10.1101/2022.12.12.520035v1.full-text
30. The human olfactory bulb communicates perceived odor valence to the piriform cortex in the gamma band and receives a refined representation back in the beta band, accessed January 15, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC11501019/
31. Cortical network and connectivity underlying hedonic olfactory perception - UNIPI, accessed January 15, 2026, https://arpi.unipi.it/retrieve/e0d6c931-efba-fcf8-e053-d805fe0aa794/Callara_2021_J._Neural_Eng._18_056050.pdf
32. The Valence–Arousal Model: A Simple Map to Understand Complex Human Emotions, accessed January 15, 2026, https://imentiv.ai/blog/the-valencearousal-model-a-simple-map-to-understand-complex-human-emotions/
33. The Relation Between Valence and Arousal in Subjective Odor Experience - UU Research Portal, accessed January 15, 2026, https://research-portal.uu.nl/files/78704417/The_Relation_Between_Valence_and_Arousal_in_Subjective_Odor_Experience2020Chemosensory_Perception.pdf
34. Generative AI masters the art of scent creation - Science Tokyo, accessed January 15, 2026, https://www.isct.ac.jp/en/news/0vw7079vqnao
35. Text-guided small molecule generation via diffusion model - PMC - NIH, accessed January 15, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC11700631/
36. Claude Code overview - Claude Code Docs, accessed January 15, 2026, https://code.claude.com/docs/en/overview
37. Claude Code: Best practices for agentic coding - Anthropic, accessed January 15, 2026, https://www.anthropic.com/engineering/claude-code-best-practices
38. Introducing advanced tool use on the Claude Developer Platform - Anthropic, accessed January 15, 2026, https://www.anthropic.com/engineering/advanced-tool-use
39. A Principal Odor Map Unifies Diverse Tasks in Olfactory Perception - PMC - NIH, accessed January 15, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC11898014/
40. Deep Learning for Odor Prediction on Aroma-Chemical Blends | ACS Omega, accessed January 15, 2026, https://pubs.acs.org/doi/10.1021/acsomega.4c07078
41. Green Sciences at the Heart of the Cosmetic Transition for L'Oréal for the Future, accessed January 15, 2026, https://www.loreal.com/en/articles/science-and-technology/green-sciences-noveal/
42. From leftovers to luxury: Pioneering upcycling in fragrances - Givaudan, accessed January 15, 2026, https://www.givaudan.com/fragrance-beauty/pioneering-upcycling-in-fragrances
43. 3. How can fragrance substance become skin allergens? - European Commission, accessed January 15, 2026, https://ec.europa.eu/health/scientific_committees/opinions_layman/perfume-allergies/en/l-3/3-becoming-allergens.htm
44. Mathematical model for predicting the percutaneous absorption of perfume raw materials - CDC Stacks, accessed January 15, 2026, https://stacks.cdc.gov/view/cdc/192015