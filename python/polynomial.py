import re
import math
import numpy as np
from fractions import Fraction


def fix_signs(expr):
    expr = expr.replace("--", "+")
    expr = expr.replace("+-", "-")
    expr = expr.replace("-+", "-")
    return expr


def format_fraction_or_decimal(x):
    frac = Fraction(x).limit_denominator(1000)
    if abs(float(frac) - x) < 1e-10:
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"
    else:
        return f"{x:.8f}"


def format_complex_number(real, imag):
    def fmt(x):
        if abs(x - int(x)) < 1e-10:
            return str(int(x))
        else:
            return f"{x:.8f}"

    sign = "+" if imag >= 0 else "-"
    return f"{fmt(real)} {sign} {fmt(abs(imag))}i"


def format_factor_root(root):
    frac = Fraction(root).limit_denominator(1000)
    if abs(float(frac) - root) < 1e-10:
        val = (
            frac.numerator
            if frac.denominator == 1
            else f"{frac.numerator}/{frac.denominator}"
        )
    else:
        val = f"{root:.8f}"
    if abs(root) < 1e-10:
        return "x"
    elif root < 0:
        return f"(x+{val.lstrip('-')})"
    else:
        return f"(x-{val})"


class PolynomialRootFinder:
    def __init__(self):
        self.coefficients = []
        self.degree = 0
        self.steps = []

    def parse_polynomial(self, equation_str):
        equation_str = equation_str.replace(" ", "").lower()
        if "=0" in equation_str:
            equation_str = equation_str.split("=0")[0]
        elif "= 0" in equation_str:
            equation_str = equation_str.split("= 0")[0]
        max_degree = 0
        terms = re.findall(r"([+-]?\d*\.?\d*)x\^?(\d*)", equation_str)
        for coef, deg in terms:
            if deg == "":
                deg = "1"
            if deg != "":
                max_degree = max(max_degree, int(deg))
        self.degree = max_degree
        self.coefficients = [0] * (self.degree + 1)
        constant_match = re.search(r"([+-]?\d+)(?!.*x)", equation_str)
        if constant_match:
            self.coefficients[0] = float(constant_match.group(1))
        for coef, deg in terms:
            if coef in ["", "+"]:
                coef_val = 1.0
            elif coef == "-":
                coef_val = -1.0
            else:
                coef_val = float(coef) if coef else 1.0
            if deg == "":
                deg_val = 1
            else:
                deg_val = int(deg)
            self.coefficients[deg_val] = coef_val
        print(f"[-] Polynomial degree: {self.degree}")

    def evaluate_poly(self, x):
        result = 0
        for i, coef in enumerate(self.coefficients):
            result += coef * (x**i)
        return result

    def find_all_roots_complex(self):
        if not self.coefficients:
            return []
        coeffs_array = self.coefficients[::-1]
        try:
            all_roots = np.roots(coeffs_array)
            return sorted(all_roots, key=lambda x: (x.real, x.imag))
        except Exception as e:
            print(f"[!] Error finding roots: {e}")
            return []

    def find_rational_roots(self):
        if not self.coefficients:
            return []
        constant = self.coefficients[0]
        leading = self.coefficients[self.degree]
        factors_constant = set()
        constant_int = int(abs(constant))
        for i in range(1, constant_int + 1):
            if constant_int % i == 0:
                factors_constant.add(i)
                factors_constant.add(-i)
        factors_leading = set()
        leading_int = int(abs(leading))
        for i in range(1, leading_int + 1):
            if leading_int % i == 0:
                factors_leading.add(i)
                factors_leading.add(-i)
        possible_roots = set()
        for p in factors_constant:
            for q in factors_leading:
                if q != 0:
                    frac = Fraction(p, q)
                    possible_roots.add(frac)
        rational_roots = []
        tolerance = 1e-10
        sorted_roots = sorted(
            possible_roots, key=lambda x: (abs(x.denominator), abs(x.numerator), x)
        )
        for root in sorted_roots:
            value = self.evaluate_poly(float(root))
            if abs(value) < tolerance:
                rational_roots.append(root)
        return rational_roots

    def polynomial_division(self, coefficients, root):
        n = len(coefficients) - 1
        quotient = [0] * n
        remainder = coefficients[n]
        for i in range(n - 1, -1, -1):
            quotient[i] = remainder
            remainder = coefficients[i] + remainder * root
        return quotient

    def format_polynomial_simple(self, coeffs):
        terms = []
        for i in range(len(coeffs) - 1, -1, -1):
            coef = coeffs[i]
            if abs(coef) > 1e-10:
                if i == 0:
                    terms.append(f"{coef:g}")
                elif i == 1:
                    terms.append(f"{coef:g}x")
                else:
                    terms.append(f"{coef:g}x{i}")
        if not terms:
            return "0"
        result = terms[0]
        for term in terms[1:]:
            if term.startswith("-"):
                result += term
            else:
                result += "+" + term
        return result

    def format_polynomial(self, coeffs):
        terms = []
        for i in range(len(coeffs) - 1, -1, -1):
            coef = coeffs[i]
            if abs(coef) > 1e-10:
                if i == 0:
                    term = f"{coef:+g}"
                elif i == 1:
                    term = f"{coef:+g}x"
                else:
                    term = f"{coef:+g}x^{i}"
                if not terms and term.startswith("+"):
                    term = term[1:]
                terms.append(term)
        if not terms:
            return "0"
        return " ".join(terms)

    def float_to_fraction(self, x, max_denominator=1000):
        try:
            frac = Fraction(x).limit_denominator(max_denominator)
            if abs(float(frac) - x) < 1e-10:
                return frac
            else:
                return None
        except:
            return None

    def format_root_display(self, root):
        if abs(root.imag) < 1e-10:
            real_part = root.real
            frac = self.float_to_fraction(real_part)
            if frac and frac.denominator != 1:
                return f"{frac.numerator}/{frac.denominator}"
            elif frac:
                return f"{frac.numerator}"
            else:
                return f"{real_part:.8f}"
        else:
            return format_complex_number(root.real, root.imag)

    def show_factorization_step(self, coefficients, root):
        n = len(coefficients) - 1
        root_value = float(root)
        factor_str = format_factor_root(root_value)
        terms = []
        current_coeff = coefficients[n]
        for i in range(n - 1, -1, -1):
            term_coeff = current_coeff
            if abs(term_coeff) > 1e-10:
                factor_term = format_factor_root(root_value)
                if i == 0:
                    terms.append(f"{abs(term_coeff):g}{factor_term}")
                elif i == 1:
                    terms.append(f"{abs(term_coeff):g}x{factor_term}")
                else:
                    terms.append(f"{abs(term_coeff):g}x{i}{factor_term}")
            current_coeff = coefficients[i] + current_coeff * root_value
        result = terms[0]
        for i in range(1, len(terms)):
            if terms[i].startswith("-"):
                result += terms[i]
            else:
                result += "+" + terms[i]
        result = fix_signs(result)
        quotient_coeffs = self.polynomial_division(coefficients, root_value)
        quotient_str = self.format_polynomial_simple(quotient_coeffs)
        quotient_str = fix_signs(quotient_str)
        print(f"> {result}=0")
        print(f"> {factor_str}({quotient_str})=0")

    def factor_polynomial_step_by_step(self, coefficients, depth=0):
        if len(coefficients) <= 1:
            return []
        poly_str = self.format_polynomial(coefficients)
        print(f"\n[{depth + 1}] Solving {poly_str} = 0")
        if len(coefficients) == 2:
            root = -coefficients[0] / coefficients[1]
            frac = self.float_to_fraction(root)
            if frac:
                print(
                    f"[+] Linear equation: x = {frac.numerator}/{frac.denominator}"
                    if frac.denominator != 1
                    else f"Linear equation: x = {frac.numerator}"
                )
            else:
                print(f"[+] Linear equation: x = {root:.8f}")
            return [root]
        elif len(coefficients) == 3:
            a, b, c = coefficients[2], coefficients[1], coefficients[0]
            discriminant = b**2 - 4 * a * c
            if discriminant >= 0:
                root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                frac1 = self.float_to_fraction(root1)
                frac2 = self.float_to_fraction(root2)
                if frac1 and frac2:
                    print(
                        f"[+] Quadratic roots: x = {frac1.numerator}/{frac1.denominator}, {frac2.numerator}/{frac2.denominator}"
                    )
                else:
                    print(f"[+] Quadratic roots: x = {root1:.8f}, {root2:.8f}")
                return [root1, root2]
            else:
                real_part = -b / (2 * a)
                imag_part = math.sqrt(-discriminant) / (2 * a)
                root1 = complex(real_part, imag_part)
                root2 = complex(real_part, -imag_part)
                print(
                    f"[+] Complex roots: x = {format_complex_number(real_part, imag_part)}"
                )
                print(
                    f"[+] Complex roots: x = {format_complex_number(real_part, -imag_part)}"
                )
                return [root1, root2]
        temp_poly = PolynomialRootFinder()
        temp_poly.coefficients = coefficients
        temp_poly.degree = len(coefficients) - 1
        rational_roots = temp_poly.find_rational_roots()
        if rational_roots:
            integer_roots = [r for r in rational_roots if r.denominator == 1]
            fraction_roots = [r for r in rational_roots if r.denominator != 1]
            if integer_roots:
                root = integer_roots[0]
            else:
                root = fraction_roots[0]
            root_value = float(root)
            root_str = (
                f"{root.numerator}/{root.denominator}"
                if root.denominator != 1
                else f"{root.numerator}"
            )
            print(f"[+] Found rational root: x = {root_str}")
            print(f"[-] Using Factor Theorem: f({root_str}) = 0")
            self.show_factorization_step(coefficients, root_value)
            quotient_coeffs = self.polynomial_division(coefficients, root_value)
            self.steps.append(
                {
                    "original": coefficients.copy(),
                    "root": root,
                    "quotient": quotient_coeffs.copy(),
                    "depth": depth,
                }
            )
            remaining_roots = self.factor_polynomial_step_by_step(
                quotient_coeffs, depth + 1
            )
            return [root_value] + remaining_roots
        else:
            print(f"[!] No rational roots found. Finding all roots numerically...")
            all_roots = temp_poly.find_all_roots_complex()
            real_roots = [r for r in all_roots if abs(r.imag) < 1e-10]
            complex_roots = [r for r in all_roots if abs(r.imag) >= 1e-10]
            real_roots_sorted = sorted(real_roots, key=lambda x: x.real)
            complex_pairs = []
            used_indices = set()
            for i, root in enumerate(complex_roots):
                if i in used_indices:
                    continue
                for j, other_root in enumerate(complex_roots[i + 1 :], i + 1):
                    if (
                        j not in used_indices
                        and abs(root.real - other_root.real) < 1e-10
                        and abs(root.imag + other_root.imag) < 1e-10
                    ):
                        complex_pairs.append((root, other_root))
                        used_indices.add(i)
                        used_indices.add(j)
                        break
            if real_roots_sorted:
                real_strs = []
                for r in real_roots_sorted:
                    frac = self.float_to_fraction(r.real)
                    if frac:
                        real_strs.append(self.format_root_display(r))
                    else:
                        real_strs.append(f"{r.real:.8f}")
                print(f"[+] Real roots: {', '.join(real_strs)}")
            if complex_pairs:
                for root1, root2 in complex_pairs:
                    print(
                        f"[+] Complex conjugate pair: {format_complex_number(root1.real, root1.imag)}"
                    )
                    print(
                        f"[+] Complex conjugate pair: {format_complex_number(root2.real, root2.imag)}"
                    )
            return real_roots_sorted + complex_roots

    def find_all_roots(self, equation_str):
        print("=" * 60)
        print(f"[-] Solving: {equation_str}")
        print("=" * 60)
        self.parse_polynomial(equation_str)
        self.steps = []
        all_roots = self.find_all_roots_complex()
        real_roots = [r for r in all_roots if abs(r.imag) < 1e-10]
        complex_roots = [r for r in all_roots if abs(r.imag) >= 1e-10]
        real_roots_sorted = sorted(real_roots, key=lambda x: x.real)
        print(f"\n[-] ALL ROOTS:")
        print("-" * 40)
        root_num = 1
        for root in real_roots_sorted:
            frac = self.float_to_fraction(root.real)
            if frac and frac.denominator != 1:
                print(f"[+] Root {root_num}: x = {frac.numerator}/{frac.denominator}")
            elif frac:
                print(f"[+] Root {root_num}: x = {frac.numerator}")
            else:
                print(f"[+] Root {root_num}: x = {root.real:.8f}")
            root_num += 1
        used_indices = set()
        for i, root in enumerate(complex_roots):
            if i in used_indices:
                continue
            conjugate_found = False
            for j, other_root in enumerate(complex_roots[i + 1 :], i + 1):
                if (
                    j not in used_indices
                    and abs(root.real - other_root.real) < 1e-10
                    and abs(root.imag + other_root.imag) < 1e-10
                ):
                    print(
                        f"[+] Root {root_num}: x = {format_complex_number(root.real, root.imag)}"
                    )
                    root_num += 1
                    print(
                        f"[+] Root {root_num}: x = {format_complex_number(root.real, -root.imag)}"
                    )
                    root_num += 1
                    used_indices.add(i)
                    used_indices.add(j)
                    conjugate_found = True
                    break
            if not conjugate_found:
                print(
                    f"[+] Root {root_num}: x = {format_complex_number(root.real, root.imag)}"
                )
                root_num += 1
        return all_roots


def main():
    finder = PolynomialRootFinder()
    print("POLYNOMIAL ROOT FINDER")
    print("Enter polynomial equations in the format:")
    print("Example: 8x^5 - 26x^4 - 163x^3 - 295x^2 - 232x - 42 = 0")
    print("=" * 60)
    while True:
        equation_str = input("\nEnter equation (or 'quit'): ").strip()
        if equation_str.lower() in ["quit", "exit", "q"]:
            break
        if not equation_str:
            continue
        try:
            roots = finder.find_all_roots(equation_str)
            real_count = sum(1 for root in roots if abs(root.imag) < 1e-10)
            complex_count = len(roots) - real_count
            print(f"\nSUMMARY: {real_count} real roots, {complex_count} complex roots")
            response = input("\nShow step-by-step? (yes/no): ").strip().lower()
            if response in ["yes", "y"]:
                print("\n" + "=" * 60)
                finder.steps = []
                final_roots = finder.factor_polynomial_step_by_step(finder.coefficients)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
