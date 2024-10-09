import random
from lark import Lark


class CFG:
    def __init__(
        self,
        non_terminals=None,
        terminals=None,
        num_productions_range=(1, 3),
        production_length_range=(1, 3),
        terminal_probability=0.5,
    ):
        self.non_terminals = (
            non_terminals if non_terminals else ["S", "A", "B"]
        )  # 非终结符集合
        self.terminals = terminals if terminals else ["a", "b", "c"]  # 终结符集合
        self.productions = {}  # 产生式集合
        self.num_productions_range = num_productions_range
        self.production_length_range = production_length_range
        self.terminal_probability = terminal_probability

    def add_production(self, lhs, rhs):
        if lhs not in self.productions:
            self.productions[lhs] = []
        self.productions[lhs].append(rhs)

    def is_terminal(self, symbol):
        return symbol in self.terminals

    def generate_random_cfg(self):
        for nt in self.non_terminals:
            num_productions = random.randint(*self.num_productions_range)
            for _ in range(num_productions):
                rhs = []
                production_length = random.randint(*self.production_length_range)
                for _ in range(production_length):
                    if random.random() < self.terminal_probability:
                        rhs.append(random.choice(self.terminals))
                    else:
                        rhs.append(random.choice(self.non_terminals))
                self.add_production(nt, rhs)

    def can_terminate(self):
        T = set()
        for nt in self.non_terminals:
            productions = self.productions.get(nt, [])
            for rhs in productions:
                if all(self.is_terminal(s) for s in rhs):
                    T.add(nt)
                    break

        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                if nt not in T:
                    productions = self.productions.get(nt, [])
                    for rhs in productions:
                        if all(self.is_terminal(s) or s in T for s in rhs):
                            T.add(nt)
                            changed = True
                            break

        return all(nt in T for nt in self.non_terminals)

    def reachable_non_terminals(self):
        reachable = set()
        worklist = ["S"]

        while worklist:
            current_nt = worklist.pop()
            if current_nt in reachable:
                continue

            reachable.add(current_nt)
            productions = self.productions.get(current_nt, [])
            for rhs in productions:
                for symbol in rhs:
                    if symbol in self.non_terminals and symbol not in reachable:
                        worklist.append(symbol)

        return reachable

    def all_non_terminals_reachable(self):
        reachable_nts = self.reachable_non_terminals()
        return set(self.non_terminals) == reachable_nts

    def check_string_diversity(
        self, min_length=2, max_length=40, num_iterations=10, threshold=0.6
    ):
        generated_strings = set()
        total_generated = 0

        for _ in range(num_iterations):
            random_string = self.generate_string_within_length(min_length, max_length)
            generated_strings.add(random_string)
            total_generated += 1

        diversity_ratio = len(generated_strings) / total_generated
        print(f"生成的字符串总数: {total_generated}")
        print(f"唯一字符串的数量: {len(generated_strings)}")
        print(f"多样性比例: {diversity_ratio:.4f}")

        return diversity_ratio >= threshold

    def generate_terminating_cfg(self):
        attempt = 0
        while True:
            attempt += 1
            self.productions = {}  # 清空之前的产生式集合
            try:
                self.generate_random_cfg()
                if (
                    self.can_terminate()
                    and self.all_non_terminals_reachable()
                    and self.check_string_diversity()
                ):
                    print(f"在第 {attempt} 次尝试后生成了可接受的CFG。")
                    return
                else:
                    print(f"第 {attempt} 次生成的CFG未通过检查，重新生成。")
            except:
                print(f"第 {attempt} 次生成出现异常，重新生成。")

    def generate_string_from_cfg(
        self, symbol, min_length, max_length, current_length=0
    ):
        if current_length > max_length:
            return "", current_length

        if self.is_terminal(symbol):
            return symbol, current_length + 1

        productions = self.productions[symbol]
        suitable_productions = []
        for production in productions:
            min_possible_length = current_length
            for s in production:
                if self.is_terminal(s):
                    min_possible_length += 1
                else:
                    min_possible_length += 1

            if min_possible_length <= max_length:
                suitable_productions.append(production)

        if not suitable_productions:
            chosen_production = random.choice(productions)
        else:
            chosen_production = random.choice(suitable_productions)

        result = []
        for s in chosen_production:
            generated_str, current_length = self.generate_string_from_cfg(
                s, min_length, max_length, current_length
            )
            result.append(generated_str)

        return "".join(result), current_length

    def generate_string_within_length(self, min_length, max_length):
        while True:
            result, length = self.generate_string_from_cfg("S", min_length, max_length)
            if min_length <= length <= max_length:
                return result


    def cfg_to_lark(self):
        result = []
        result.append(
            f's: {" | ".join(" ".join(rhs) for rhs in self.productions["S"])}'
        )

        for non_terminal in self.non_terminals:
            if non_terminal == "S":
                continue
            productions = self.productions.get(non_terminal, [])
            rhs_options = [" ".join(rhs) for rhs in productions]
            rhs_str = " | ".join(rhs_options)
            result.append(f"{non_terminal.lower()}: {rhs_str}")

        lark_grammar = "\n".join(result)
        for terminal in self.terminals:
            lark_grammar = lark_grammar.replace(f" {terminal} ", f' "{terminal}" ')
            lark_grammar = lark_grammar.replace(f" {terminal}", f' "{terminal}"')
            lark_grammar = lark_grammar.replace(f"{terminal} ", f'"{terminal}" ')

        for non_terminal in self.non_terminals:
            lark_grammar = lark_grammar.replace(
                f"{non_terminal} ", f"{non_terminal.lower()} "
            )
            lark_grammar = lark_grammar.replace(
                f" {non_terminal}", f" {non_terminal.lower()}"
            )

        return lark_grammar
    
    def __str__(self):
        result = []
        for lhs, rhss in self.productions.items():
            rhs_str = " | ".join(" ".join(rhs) for rhs in rhss)
            result.append(f"{lhs} -> {rhs_str}")
        return "\n".join(result)


def test():
    cfg = CFG(
        non_terminals=["S", "A", "B", "C"],
        terminals=["x", "y", "z"],
        num_productions_range=(1, 5),
        production_length_range=(1, 5),
        terminal_probability=0.4,
    )
    cfg.generate_terminating_cfg()

    # 输出生成的CFG
    print(cfg)

    # 将CFG转换为Lark格式并打印
    lark_grammar = cfg.cfg_to_lark()
    print("\nLark Grammar:")
    print(lark_grammar)

    # 使用Lark解析生成的字符串
    parser = Lark(lark_grammar, start="s", parser="earley")
    random_string = cfg.generate_string_within_length(5, 30)
    print(f"\n生成的随机字符串: {random_string}")
    try:
        parse_tree = parser.parse(random_string)
        print("\n解析成功:\n", parse_tree)
    except Exception as e:
        print("\n解析失败:", e)


if __name__ == "__main__":
    test()
