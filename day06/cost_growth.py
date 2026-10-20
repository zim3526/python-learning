# 演示：多轮对话的成本是怎么膨胀的
# 运行：py cost_growth.py

AVG_TOKENS_PER_MSG = 50          # 假设每句话 50 tokens
INPUT_PRICE = 1.0 / 1_000_000    # 输入 1 元/百万 tokens

print("=" * 70)
print("多轮对话的成本增长（假设每句话 50 tokens）")
print("=" * 70)
print(f"{'轮次':>4} | {'本轮发送条数':>12} | {'本轮输入tokens':>14} | {'本轮费用(元)':>12} | {'累计tokens':>11}")
print("-" * 70)

total_tokens = 0
for round_num in range(1, 21):
    msg_count = 2 * round_num                       # 第 N 轮发 2N 条
    input_tokens = msg_count * AVG_TOKENS_PER_MSG
    cost = input_tokens * INPUT_PRICE
    total_tokens += input_tokens

    if round_num <= 10 or round_num % 5 == 0:
        print(f"{round_num:>4} | {msg_count:>12} | {input_tokens:>14} | {cost:>12.6f} | {total_tokens:>11}")

print("-" * 70)
print()
print("关键观察：")
print("  1. 第 1 轮输入 100 tokens，第 20 轮输入 2000 tokens —— 贵了 20 倍")
print("  2. 累计发送量按平方增长：N 轮总共发送 N(N+1) 条消息的量")
print("  3. 第 20 轮时，你只问了一句 50 tokens 的话，却要发送 2000 tokens")
print()
print("=" * 70)
print("对比：如果每轮只发【最近 3 轮】历史")
print("=" * 70)

total_tokens_limited = 0
for round_num in range(1, 21):
    msg_count = 1 + 2 * 3                            # system + 最近3轮的6条
    input_tokens = msg_count * AVG_TOKENS_PER_MSG
    total_tokens_limited += input_tokens
    if round_num == 20:
        print(f"  第 20 轮：发送 {msg_count} 条 = {input_tokens} tokens（不再增长）")

print()
print(f"  20 轮累计（全量历史）: {total_tokens:>6} tokens")
print(f"  20 轮累计（只留3轮）: {total_tokens_limited:>6} tokens")
print(f"  节省比例: {100 - total_tokens_limited / total_tokens * 100:.1f}%")

