#!/usr/bin/env python3

import yaml
import os
from jinja2 import Template

policy_template = Template("""
{% for policy in data %}
- **FROM {{policy["from_zone"]}} TO {{policy["to_zone"]}}**
  - **Description:** {{policy["description"]}}
{% for term in policy["terms"] %}
  - **Term:**
    - **Source:** {{ ", ".join(term["source_addresses"]) }}
    - **Destination:** {{ ", ".join(term["destination_addresses"]) }}
    - **Port:** {{ ", ".join(term["destination_addresses"]) }}
    - **Protocol:** {{ ", ".join(term["destination_addresses"]) }}
{% endfor %}

{% endfor %}
""", trim_blocks=True, lstrip_blocks=True)

request_template = Template("""{% set request = data["request"] %}
- Firewall Request
  - **Contact Information**
    - **Name:** {{request['requestor']['name']}}
    - **Phone:** {{request['requestor']['phone']}}
    - **EMail:** {{request['requestor']['email']}}
  - **Policy Information**
""", trim_blocks=True, lstrip_blocks=True)

addresses_template = Template("""| Region| Site | Subnet | Zone |
| :---: | :---: | :---: | :---: |
{% for prefix in data["prefixes"] %}
    {% for subnet in prefix['subnets'] %}
|{{prefix['region']}}|{{prefix['site']}}|{{subnet['subnet']}}|{{subnet['zone']}}|
    {% endfor %}
{% endfor %}
""", trim_blocks=True, lstrip_blocks=True)

TAG_PREFIX="<!-- TAG_"
TAG_START="_START -->"
TAG_END="_END -->"

def render_template(filename, tmpl):
    data = None
    with open(filename) as file:
        data = yaml.load(file, yaml.SafeLoader) 
    return tmpl.render(data=data)

def render(tag):
    if tag.startswith("TABLE_IPADDRESSES"):
        return render_template("config/network.yaml", addresses_template)
    if tag.startswith("REQUEST_"):
        return render_template(f"requests/{tag[len('REQUEST_'):]}.yaml", request_template)
    if tag.startswith("POLICY_"):
        return render_template(f"policies/{tag[len('POLICY_'):]}.yaml", policy_template)

    # prevent an unhandled tag from blowing things up
    return ""

def main():
    line_num = 0
    with open("README.md") as input:
        with open(".README.md", "w") as output:
            inblock = False
            block_end = ""
            for line in input.readlines():
                line_num += 1
                line = line.strip()
                if inblock and line == block_end:
                    inblock = False

                if line.startswith(TAG_PREFIX) and line.endswith(TAG_START):
                    inblock = True
                    tag = line[len(TAG_PREFIX):-len(TAG_START)]
                    block_end = f"{TAG_PREFIX}{tag}{TAG_END}"
                    content = render(tag)
                    output.write(line + "\n")
                    output.write(content)
                    if not content.endswith("\n"):
                        output.write("\n")

                if inblock:
                    continue

                output.write(line+"\n")
            os.rename(".README.md", "README.md")

if __name__ == "__main__":
    main()
