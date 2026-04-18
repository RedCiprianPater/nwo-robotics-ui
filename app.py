import gradio as gr
import httpx, os

GATEWAY = os.getenv("GATEWAY_URL", "https://nwo-robotics-api.onrender.com")

def get_platform_health():
    try:
        r = httpx.get(f"{GATEWAY}/v1/health", timeout=10)
        return r.json()
    except:
        return {"status": "unreachable"}

def register_agent(name, public_key):
    try:
        r = httpx.post(f"{GATEWAY}/v1/agents/register",
            json={"name": name, "public_key": public_key}, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def query_graph(node_type, limit):
    try:
        params = {"limit": int(limit)}
        if node_type: params["node_type"] = node_type
        r = httpx.get(f"{GATEWAY}/v1/graph/nodes", params=params, timeout=10)
        data = r.json()
        nodes = data.get("nodes", [])
        return f"Total: {data['total']}\n\n" + "\n".join(
            f"[{n['node_type']}] {n['title']} — {n['agent_did'][:30]}"
            for n in nodes
        )
    except Exception as e:
        return str(e)

with gr.Blocks(theme=gr.themes.Default(), title="NWO Robotics") as demo:
    gr.Markdown("# NWO Robotics Self-Assembly Economic Market")
    gr.Markdown("Autonomous robot-to-robot design, fabrication, and economic settlement.")

    with gr.Tab("Platform health"):
        health_btn = gr.Button("Check all layers")
        health_out = gr.JSON(label="Platform status")
        health_btn.click(get_platform_health, outputs=health_out)

    with gr.Tab("Register agent"):
        name_in = gr.Textbox(label="Agent name")
        key_in  = gr.Textbox(label="Public key (hex)")
        reg_btn = gr.Button("Register")
        reg_out = gr.JSON(label="Result")
        reg_btn.click(register_agent, inputs=[name_in, key_in], outputs=reg_out)

    with gr.Tab("Agent graph"):
        type_in  = gr.Textbox(label="Node type filter (optional)")
        limit_in = gr.Slider(5, 100, value=20, label="Limit")
        graph_btn = gr.Button("Query graph")
        graph_out = gr.Textbox(label="Nodes", lines=15)
        graph_btn.click(query_graph, inputs=[type_in, limit_in], outputs=graph_out)

    with gr.Tab("Market info"):
        gr.Markdown("""
**Contracts (Base Mainnet · Chain ID 8453)**

| Contract | Address |
|---|---|
| NWOIdentityRegistry | `0x78455AFd5E5088F8B5fecA0523291A75De1dAfF8` |
| NWOAccessController | `0x29d177bedaef29304eacdc63b2d0285c459a0f50` |
| NWOPaymentProcessor | `0x4afa4618bb992a073dbcfbddd6d1aebc3d5abd7c` |

**Credit rates**
- Earn: +1 part download · +2 skill run · +5 print job · +100 registration
- Spend: −10 design · −5 simulate · −3 slice · −1 skill run
- Settlement: 50 min credits → 0.0001 ETH/credit on Base
        """)

demo.launch()
