# Use modified eve docs for projects

## Setting UP
1. create a function to return the blueprint
```python
def edinet_docs():
    blueprints = [edinet_methods.edinet_methods] # list with blueprints containing extra methods
    eve_docs = Blueprint('eve_docs', __name__, template_folder='templates') #blueprint

    # set the different routes as desired, modify the templates as required
    @eve_docs.route('/')
    def index():
        cfg = get_cfg(blueprints)
        return render_template('index.html', cfg=cfg)

    @eve_docs.route('/v1/docs')
    def indexv1():
        cfg = get_cfg(blueprints)
        return render_template('indexv1.html', cfg=cfg)

    @eve_docs.route('/v1/spec.json')
    def spec():
        cfg = get_cfg(blueprints)
        return jsonify(cfg)

    return eve_docs
```
2. add the methods for each version and an index version
3. copy and paste the templates in the same folder where the blueprint is and modify it if you like
4. add the general documentation in the general_doc.html file for each version.