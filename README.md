# Docs

### Client
*class* speechsim.**Client**(path=None)

**Parameters**
- **path** - Filepath to where the speech data will be stored. Defaults to "data.json" if none
<br>
<br>
<br>
<br>
**add_to_data**(messages)

Adds to the speech data based on given messages

**Parameters**
- **messages** (List[str], str) - Message(s) to add
<br>
<br>
<br>
<br>
**create_message()**

Creates a message based on current speech data

**Returns**

The generated message