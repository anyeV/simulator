__author__ = "anyeV"

import base64
from Crypto.Cipher import AES
import json
import hmac


def formatting_dict_to_str(dict_text):
    """
    处理dict原文,格式化输出字符串
    按照双方约定来格式化加密字符串
    """

    print("formatting_dict_to_str入参不是dict")
    return


def pkcs7padding(text):
    """
    明文使用PKCS7填充
    最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
    """
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    # tips：utf-8编码时，英文占1个byte，而中文占3个byte
    padding_size = length if (bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
    padding_text = chr(padding) * padding
    return text + padding_text


def pkcs5padding(text):
    """
    明文使用PKCS5填充
    """
    bs = AES.block_size
    text_length = len(text)
    amount_to_pad = bs - (text_length % bs)
    if amount_to_pad == 0:
        amount_to_pad = bs
    pad = chr(amount_to_pad)
    return text + pad * amount_to_pad


def pkcs5_7unpadding(text):
    """
    处理使用PKCS5或PKCS7填充过的数据
    """
    length = len(text)
    unpadding = ord(text[length - 1])
    return text[0:length - unpadding]


def encrypt(key, dict_content, iv):
    """
    AES加密
    模式cbc
    密钥key
    补码iv
    填充pkcs5
    """
    content = formatting_dict_to_str(dict_content)
    key_bytes = bytes(key, encoding='utf-8')
    iv_bytes = bytes(iv, encoding='utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    # 处理明文
    content_padding = pkcs5padding(content)
    # 加密
    encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    # 重新编码
    result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
    return result


def decrypt(key, content, iv):
    """
    AES解密
    密钥key
    补码iv
    模式cbc
    """
    key_bytes = bytes(key, encoding='utf-8')
    iv = bytes(iv, encoding='utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    # base64解码
    encrypt_bytes = base64.b64decode(content)
    # 解密
    decrypt_bytes = cipher.decrypt(encrypt_bytes)
    # 重新编码
    result = str(decrypt_bytes, encoding='utf-8')
    # 去除填充内容
    result = pkcs5_7unpadding(result)
    return result


def HMACMD5(data, key):
    h = hmac.new(bytes(key.encode(encoding='UTF-8')), msg=bytes(data.encode(encoding='UTF-8')))
    h_str = h.hexdigest()
    return h_str.upper()
