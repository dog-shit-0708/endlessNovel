from pathlib import Path
from bfcl_eval import BFCLDataset, BFCLEvaluator
from agent import MyAgent


def main():
    # 1. 数据路径
    data_path = Path("temp_gorilla/berkeley-function-call-leaderboard/bfcl_eval/data")

    # 2. 加载数据
    dataset = BFCLDataset(str(data_path), category="simple_python")

    # 3. evaluator
    evaluator = BFCLEvaluator(dataset, category="simple_python")

    # 4. agent
    agent = MyAgent()

    # 5. 跑评测（先小样本）
    results = evaluator.evaluate(agent, max_samples=5)

    # 6. 输出结果
    print("\n===== BFCL RESULT =====")
    print("Accuracy:", results["overall_accuracy"])
    print("Correct:", results["correct_samples"], "/", results["total_samples"])


if __name__ == "__main__":
    main()