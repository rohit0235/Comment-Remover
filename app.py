from flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def remove_comments(code: str, language: str) -> str:
    if language == "python":
        import io, tokenize
        result = []
        g = tokenize.generate_tokens(io.StringIO(code).readline)
        for toknum, tokval, *_ in g:
            if toknum != tokenize.COMMENT:
                result.append(tokval)
        return ''.join(result)
    elif language in ["c", "cpp", "java", "javascript"]:
        pattern = r"(//.*?$)|(/\*.*?\*/)"
        return re.sub(pattern, "", code, flags=re.DOTALL | re.MULTILINE)
    else:
        return code


@app.route("/remove-comments", methods=["POST"])
def remove_comments_api():
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "python")
    cleaned = remove_comments(code, language)
    return jsonify({"cleaned_code": cleaned})

if __name__ == "__main__":
    app.run(debug=True)