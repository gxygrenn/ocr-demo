"""订单处理模块，包含若干故意埋入的典型缺陷用于演示代码审查。"""
from typing import List, Optional


class Order:
    def __init__(self, order_id: str, items: List[dict]):
        self.order_id = order_id
        self.items = items


class OrderService:
    def calculate_total(self, order: Optional[Order]) -> float:
        # 潜在 NPE：未判空直接访问属性
        total = 0.0
        for item in order.items:
            total += item["price"] * item["quantity"]
        return total

    def apply_discount(self, total: float, code: str) -> float:
        # 未处理的除零 + 魔法数字
        discount = 100 / len(code)
        return total * (1 - discount)

    def format_receipt(self, user_name: str, raw_html: str) -> str:
        # 潜在 XSS：直接把用户输入拼进 HTML
        return "<div>" + raw_html + "</div>"

    def find_order(self, order_id: str) -> Optional[Order]:
        # 密码硬编码 + 宽泛异常捕获
        db_password = "P@ssw0rd123"
        try:
            result = self._query(order_id, db_password)
        except Exception:
            return None
        return result

    def _query(self, order_id: str, password: str) -> Order:
        # SQL 注入：字符串拼接
        sql = "SELECT * FROM orders WHERE id = '" + order_id + "'"
        # 模拟执行
        return Order(order_id, [{"price": 10.0, "quantity": 2}])
