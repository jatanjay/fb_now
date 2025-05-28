# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import base64


def dict_from_payload(base64_input: str, fport: int = None):
    """ Decodes a base64-encoded binary payload into JSON.
            Parameters 
            ----------
            base64_input : str
                Base64-encoded binary payload
            fport: int
                FPort as provided in the metadata. Please note the fport is optional and can have value "None", if not provided by the LNS or invoking function. 

                If  fport is None and binary decoder can not proceed because of that, it should should raise an exception.

            Returns
            -------
            JSON object with key/value pairs of decoded attributes

        """

    # Used the Dragino JS Decoder as reference
    # https://www.dragino.com/downloads/downloads/LoRa_End_Node/LLMS01/Decoder/LLMS01_Datacake_Decode_V1.0.0.js
    decoded = base64.b64decode(base64_input)

    battery_value = (((decoded[0] << 8) + decoded[1]) / 1000) # /Battery,units:V
    temperature1 = (((decoded[2] << 8) + decoded[3]) / 10)
    adc = (((decoded[4] << 8) + decoded[5]) / 1000)
    istatus = "L"
    if (decoded[6] & 0x02):
        istatus = "H"
    temperature2 = (((decoded[7] <<24>>16) + decoded[8]) / 10)
    temperature3 = (((decoded[9] <<24>>16) + decoded[10]) / 10)

    result = {
        "battery_value": battery_value,
        "adc": adc,
        "istatus": istatus,
        "temperature1": temperature1,
        "temperature2":  temperature2,
        "temperature3":  temperature3,
    }
    return result
