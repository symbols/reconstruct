"""
Hyper Text Transfer Protocol (TCP/IP protocol stack)

Construct is not meant for text manipulation, and is probably not the right
tool for the job, but I wanted to demonstrate how this could be done using
the provided `text` module.
"""
from reconstruct import *
from reconstruct.text import *


class HttpParamDictAdapter(Adapter):
    """turns the sequence of params into a dict"""
    def _encode(self, obj, context):
        return [Container(name = k, value = v) for k, v in obj.iteritems()]
    def _decode(self, obj, context):
        return dict((o.name, o.value) for o in obj)


lineterm = Literal("\r\n")
space = Whitespace()

# http parameter: 'name: value\r\n'
http_param = Struct("params",
    StringUpto("name", ":\r\n"),
    Literal(":"),
    space,
    StringUpto("value", "\r"),
    lineterm,
)

http_params = HttpParamDictAdapter(
    OptionalGreedyRange(http_param)
)

# request: command and params
http_request = Struct("request",
    StringUpto("command", " "),
    space,
    StringUpto("url", " "),
    space,
    Literal("HTTP/"),
    StringUpto("version", "\r"),
    lineterm,
    http_params,
    lineterm,
)

# reply: header (answer and params) and data
http_reply = Struct("reply",
    Literal("HTTP/"),
    StringUpto("version", " "),
    space,
    DecNumber("code"),
    space,
    StringUpto("text", "\r"),
    lineterm,
    http_params,
    lineterm,
    HexDumpAdapter(
        Field("data", lambda ctx: int(ctx["params"]["Content-length"]))
    ),
)

# session: request followed reply
http_session = Struct("session",
    http_request,
    http_reply,
)


if __name__ == "__main__":
    cap1 = (
    "474554202f636e6e2f2e656c656d656e742f696d672f312e352f6365696c696e672f6e"
    "61765f706970656c696e655f646b626c75652e67696620485454502f312e310d0a486f"
    "73743a20692e636e6e2e6e65740d0a557365722d4167656e743a204d6f7a696c6c612f"
    "352e30202857696e646f77733b20553b2057696e646f7773204e5420352e313b20656e"
    "2d55533b2072763a312e382e3129204765636b6f2f3230303631303130204669726566"
    "6f782f322e300d0a4163636570743a20696d6167652f706e672c2a2f2a3b713d302e35"
    "0d0a4163636570742d4c616e67756167653a20656e2d75732c656e3b713d302e350d0a"
    "4163636570742d456e636f64696e673a20677a69702c6465666c6174650d0a41636365"
    "70742d436861727365743a2049534f2d383835392d312c7574662d383b713d302e372c"
    "2a3b713d302e370d0a4b6565702d416c6976653a203330300d0a436f6e6e656374696f"
    "6e3a206b6565702d616c6976650d0a526566657265723a20687474703a2f2f7777772e"
    "636e6e2e636f6d2f0d0a0d0a485454502f312e3120323030204f4b0d0a446174653a20"
    "53756e2c2031302044656320323030362031373a34383a303120474d540d0a53657276"
    "65723a204170616368650d0a436f6e74656e742d747970653a20696d6167652f676966"
    "0d0a457461673a202266313232383761352d63642d3562312d30220d0a4c6173742d6d"
    "6f6469666965643a204d6f6e2c2032372046656220323030362032323a33393a303920"
    "474d540d0a436f6e74656e742d6c656e6774683a20313435370d0a4163636570742d72"
    "616e6765733a2062797465730d0a4b6565702d416c6976653a2074696d656f75743d35"
    "2c206d61783d313032340d0a436f6e6e656374696f6e3a204b6565702d416c6976650d"
    "0a0d0a47494638396148001600f7000037618d436a94ebf0f4cad5e1bccad93a638fd2"
    "dce639628e52769c97adc44c7299426a93dce3eb6182a5dee5ec5d7fa338628d466d95"
    "88a1bb3c65907b97b4d43f3ba7bacdd9e1eaa6b8cce6ebf1dc5a59cc1313718faed8e0"
    "e99fb3c8ced9e350759b6989aa6787a85e80a391a8c0ffffffbbc9d8b1c2d3e0e7eed1"
    "dae5c2cfdcd2dbe57c98b4e7ecf23b648f587ba098aec4859eb9e4e9ef3e67918aa3bc"
    "aebfd17793b1cfd9e4abbdcfbfcddbb3c3d44b71995a7da13f6791a5b8cccbd6e17491"
    "b051759cd535327390afc7d2dfb8c7d7b0c0d24e739a7693b19bb0c64f749ac3cfdd49"
    "6f97afc0d14f749b3d66916e8cacb167758ba3bdd84b4c476e96c8d4e0d84340406892"
    "597ca0d53331adbed0a3b7cb52779d6f8ead9eb2c87a96b3a6b9cc567a9f94aac294ab"
    "c24b70985a7ca1b5c5d5b9c8d7aabccfd94849819bb7acbdd0c5d1dedb5253486f9744"
    "6c95da4943ae3832b7464fc40e0e3d659096acc3546d93c63c42796b88dce4eb815b74"
    "d02d1e9db2c7dc4a4a89a1bbc2393cd8413e9aafc5d01d1eb7c6d6da4142d43837c542"
    "48d3dce6687897d3322a829cb8d93438b2c2d3cd2120c4d1dd95abc3d6dfe8ca0e0cd8"
    "4c45e1e7eeb6c5d5cdd7e2d93c3c6c8bab5f5a73b14c56c6282b5b6386cd2826cf2829"
    "d5dee73e638c9f788acf3626686683436790d02724d32f2f7f728cde6261dd6864df6d"
    "6bc0353ecc3537dd545499617387637a864a5e8e697fd437388ca5be90a7c085687e8f"
    "a6bfd31d1e48648ce26665476d96d93137cd100fcb4944587195c02e34cd1619d94342"
    "7d7a95da4141da4343d63930d73c3399677bc3d0ddd22a2ad01f22d42f2d6d7d9dd124"
    "1de14b516384a6c64c52a64b58ab49514969915b7ea2c3636a734a5daa5255d9454468"
    "87a9bb3439be3b39dc353ecf26245e7396bc444c585d806081a46283a6dd615dd74a46"
    "dd675dd74138c90909dbe2ea6d8cac834d6489a2bcb15a65c34851b8636d54789e5679"
    "9ec26e78ae5762c20000d0dae4955c68dde4ecc0676fe0e6ed87a0bb4a7098446b948c"
    "a4bd8f6980aa39317d98b5c50b0d21f90400000000002c00000000480016000008ff00"
    "01081c48b0a0c18308132a5c583000c38710234a04e070a2c58b122b62dcc8d1a0c68e"
    "20377ec4c802038290080f24b08070e4453627d0b8406950828f160f0eba9c38228311"
    "09340df2f0704f8c4e83b4b2d98a82e79fb703b77c455a06204e33816226e1100140e5"
    "191f024d267c43a18005270a17241830e8e8c051fcb88d2b044f8e3860b0be914aa5ea"
    "53bf6d02cd40da5206800d01fe189d2b500744c217022204729c10028d220edc0a74b5"
    "2a0dbb6a98a8c1d160281d2f0dd7e8595b24f086010c5c007c3921d0c11726002e0df8"
    "9153c18f79057a5ce8d10000901a066c00b8b2a40365292704680610cd8a103b02ed15"
    "db706a8ea45d539471ff222450460a3e0a00207104a08100272978e4d9c7020500062c"
    "b0a5d84124170a2e9e9c018e00fa7c90c4112d3c01803a5a48e71141d058b78940ed94"
    "f30b20b1109385206d6c204c792b78915e17678cd14208000c80c0000a3651830561c4"
    "20401766bcb1441004a447003e044c13c28c00f8b186830d1164ca1d6968f28a1e7f54"
    "10c53a1590f38c31c8e062496b068011847a2a0ce442154a54e20e0060e8e001191444"
    "e0c6070ba8a0440e5c994001013b70501c00d01149d047740493cc14c3e8c24a16adf4"
    "d2082a9d4893491b7d08a4c3058401a00803035de14018393803050a4c5ca0861bf920"
    "20c01b176061c01000d4034415304c100e0010c88e5204a50f16248a368984b2073388"
    "00008a3cf100d08d39a5084442065bb597c4401390108109631c820e0058acc0001a33"
    "c0b0c02364ccf20e005e1c01c10a17b001c00c6b5132dd450f64d0040d0909000e470f"
    "78e0402deb5ef4c1315a1470d0016a2cc09104438e70101520bd00c4044119844d0c08"
    "71d0f0c40c7549f1c506895102c61c53d1051125941010003b").decode("hex")
    x = http_session.parse(cap1)
    print x
    #print x.request.url
    #print x.request.params["Referer"]
    #print x.reply.params["Server"]
    #print "-" * 80
    #print x













