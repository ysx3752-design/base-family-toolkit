import base64
import base58
import base91

# ==================== Base92 纯内置实现 ====================
# ==================== Base92 纯内置实现（修复版） ====================
class Base92:
    base92_chars = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~"'''
    
    @staticmethod
    def encode(data):
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            if not data:                # 空字节 → 空字符串
                return ''
            num = int.from_bytes(data, 'big')
            # 如果数据非空但整数为0（即全零字节），至少编码为一个字符
            if num == 0:
                return Base92.base92_chars[0]
            encoded = []
            while num > 0:
                num, rem = divmod(num, 92)
                encoded.append(Base92.base92_chars[rem])
            return ''.join(reversed(encoded))
        except:
            return "[!] Base92 编码失败"

    @staticmethod
    def decode(encoded):
        try:
            if not encoded:
                return ''
            num = 0
            for c in encoded:
                idx = Base92.base92_chars.find(c)
                if idx == -1:
                    # 遇到非法字符时返回错误提示，避免数据出错
                    return f"[!] Base92 解码失败：发现非法字符 '{c}'"
                num = num * 92 + idx
            if num == 0:
                # 对应编码时全零字节，返回一个零字节
                return '\x00'
            # 计算所需字节长度，转换回原文
            byte_len = (num.bit_length() + 7) // 8
            data = num.to_bytes(byte_len, 'big')
            return data.decode('utf-8')
        except:
            return "[!] Base92 解码失败"

# ==================== Base100 (标准 AdamNiederer 规范) ====================
def convert_base100_encode(text):
    try:
        data = text.encode('utf-8')
        encoded = []
        for byte_val in data:
            codepoint = 0x1F3F7 + byte_val
            encoded.append(chr(codepoint))
        return ''.join(encoded)
    except Exception:
        return "[!] Base100 编码失败"

def convert_base100_decode(text):
    try:
        if not text:
            return ''
        bytes_list = []
        for emoji_char in text:
            codepoint = ord(emoji_char)
            if 0x1F3F7 <= codepoint <= 0x1F4F6:
                bytes_list.append(codepoint - 0x1F3F7)
            else:
                return f"[!] Base100 解码失败：发现非法Emoji字符 '{emoji_char}' (U+{codepoint:04X})"
        return bytes(bytes_list).decode('utf-8', errors='replace')
    except Exception:
        return "[!] Base100 解码失败"

# ==================== 其他 Base 编解码 ====================
def convert_base16_decode(text):
    try:
        return base64.b16decode(text.strip().upper()).decode('utf-8')
    except Exception:
        return "[!] Base16 解码失败"

def convert_base16_encode(text):
    try:
        return base64.b16encode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[!] Base16 编码失败"

def convert_base32_decode(text):
    try:
        return base64.b32decode(text.strip().upper()).decode('utf-8')
    except Exception:
        return "[!] Base32 解码失败"

def convert_base32_encode(text):
    try:
        return base64.b32encode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[!] Base32 编码失败"

def convert_base58_decode(text):
    try:
        return base58.b58decode(text.strip()).decode('utf-8')
    except Exception:
        return "[!] Base58 解码失败"

def convert_base58_encode(text):
    try:
        return base58.b58encode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[!] Base58 编码失败"

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def convert_base62_encode(text):
    try:
        data = text.encode('utf-8')
        num = int.from_bytes(data, byteorder='big')
        if num == 0: return BASE62_ALPHABET[0]
        res = []
        while num > 0:
            num, rem = divmod(num, 62)
            res.append(BASE62_ALPHABET[rem])
        return ''.join(reversed(res))
    except Exception:
        return "[!] Base62 编码失败"

def convert_base62_decode(text):
    try:
        num = 0
        for c in text.strip():
            num = num * 62 + BASE62_ALPHABET.index(c)
        byte_len = (num.bit_length() + 7) // 8
        return num.to_bytes(byte_len, byteorder='big').decode('utf-8')
    except Exception:
        return "[!] Base62 解码失败"

def convert_base64_decode(text):
    try:
        return base64.b64decode(text.strip()).decode('utf-8')
    except Exception:
        return "[!] Base64 解码失败"

def convert_base64_encode(text):
    try:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[!] Base64 编码失败"

def convert_base85_decode(text):
    try:
        return base64.b85decode(text.strip()).decode('utf-8')
    except Exception:
        return "[!] Base85 解码失败"

def convert_base85_encode(text):
    try:
        return base64.b85encode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[!] Base85 编码失败"

def convert_base91_decode(text):
    try:
        return base91.decode(text.strip()).decode('utf-8')
    except Exception:
        return "[!] Base91 解码失败"

def convert_base91_encode(text):
    try:
        return base91.encode(text.encode('utf-8'))
    except Exception:
        return "[!] Base91 编码失败"

def convert_base92_decode(text):
    return Base92.decode(text.strip())

def convert_base92_encode(text):
    return Base92.encode(text)

# ==================== 选项列表 ====================
def get_all_options():
    return [
        ("Base16 解密", convert_base16_decode),
        ("Base16 加密", convert_base16_encode),
        ("Base32 解密", convert_base32_decode),
        ("Base32 加密", convert_base32_encode),
        ("Base58 解密", convert_base58_decode),
        ("Base58 加密", convert_base58_encode),
        ("Base62 解密", convert_base62_decode),
        ("Base62 加密", convert_base62_encode),
        ("Base64 解密", convert_base64_decode),
        ("Base64 加密", convert_base64_encode),
        ("Base85 解密", convert_base85_decode),
        ("Base85 加密", convert_base85_encode),
        ("Base91 解密", convert_base91_decode),
        ("Base91 加密", convert_base91_encode),
        ("Base92 解密", convert_base92_decode),
        ("Base92 加密", convert_base92_encode),
        ("Base100 解密", convert_base100_decode),
        ("Base100 加密", convert_base100_encode),
    ]