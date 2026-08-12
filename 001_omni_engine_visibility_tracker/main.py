"""Omni-Engine Visibility & Attribution Intelligence Tracker
Developed by HSINI MOHAMED | Python 3.12+ | CustomTkinter"""
import asyncio, threading, os, json, sys
from datetime import datetime
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core import (C, PROVIDERS, Attribution, SearchResult,
                  AttributionExtractor, SemanticEngine,
                  ProviderEngine, export_jsonld, export_pdf)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def _btn(parent, text, cmd, color=None, h=38, **kw):
    c = color or C["cyan_dark"]
    return ctk.CTkButton(parent, text=text, command=cmd, height=h,
        fg_color=c, hover_color=C["sel"], text_color=C["cyan"],
        border_color=C["cyan"], border_width=1, font=("Consolas",11,"bold"),
        corner_radius=6, **kw)

def _label(parent, text, size=10, color=None, bold=False, **kw):
    w = "bold" if bold else "normal"
    return ctk.CTkLabel(parent, text=text, font=("Consolas",size,w),
        text_color=color or C["text2"], **kw)

def _entry(parent, ph="", show="", **kw):
    return ctk.CTkEntry(parent, placeholder_text=ph, show=show,
        fg_color=C["bg2"], border_color=C["border"], border_width=1,
        text_color=C["text"], font=("Consolas",11), height=36, **kw)

def _frame(parent, color=None, **kw):
    return ctk.CTkFrame(parent, fg_color=color or C["bg2"], **kw)


class OmniApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("[O] OMNI-ENGINE VISIBILITY TRACKER | HSINI PREMIUM")
        self.geometry("1560x920"); self.minsize(1100,650)
        self.configure(fg_color=C["bg0"])
        self.results: list[SearchResult] = []
        self.running = False
        self.pvars = {k: ctk.BooleanVar(value=True) for k in PROVIDERS}
        self.api_keys = {
            "gemini":     os.environ.get("GEMINI_API_KEY",""),
            "perplexity": os.environ.get("PERPLEXITY_API_KEY",""),
            "openai":     os.environ.get("OPENAI_API_KEY",""),
        }
        self.extractor = AttributionExtractor()
        self.engine    = ProviderEngine(self.api_keys, log_fn=self._log)
        threading.Thread(target=self._init_semantic, daemon=True).start()
        self._build(); self._tick()

    def _init_semantic(self):
        ok = SemanticEngine.load()
        self.after(0, lambda: self._log(
            "[OK] Sentence-Transformers ready" if ok else
            "[!] Install sentence-transformers for semantic scoring"))

    # -- Build UI -------------------------------------------------------------
    def _build(self):
        self._topbar()
        body = _frame(self, C["bg0"])
        body.pack(fill="both", expand=True)
        self._sidebar(body)
        self._content(body)

    def _topbar(self):
        bar = _frame(self, C["bg1"], corner_radius=0, height=60)
        bar.pack(fill="x"); bar.pack_propagate(False)
        _label(bar,"[O]",28,C["cyan"],True).pack(side="left",padx=(20,6),pady=8)
        tf = _frame(bar, C["bg1"]); tf.pack(side="left")
        _label(tf,"OMNI-ENGINE",13,C["text"],True).pack(anchor="w")
        _label(tf,"VISIBILITY & ATTRIBUTION INTELLIGENCE",9,C["text2"]).pack(anchor="w")
        self.clock_lbl = _label(bar,"",11,C["cyan"])
        self.clock_lbl.pack(side="right",padx=24)
        self.stat_lbl = _label(bar,"* Initializing…",10,C["text2"])
        self.stat_lbl.pack(side="right",padx=20)

    def _sidebar(self, parent):
        sb = _frame(parent, C["bg1"], width=310, corner_radius=0)
        sb.pack(side="left", fill="y"); sb.pack_propagate(False)
        sc = ctk.CTkScrollableFrame(sb, fg_color="transparent")
        sc.pack(fill="both", expand=True, padx=14, pady=14)

        # Query
        self._sec(sc,"[O] QUERY ENGINE")
        self.qbox = ctk.CTkTextbox(sc, height=90, fg_color=C["bg2"],
            border_color=C["border"], border_width=1, font=("Consolas",12),
            text_color=C["text"], corner_radius=8)
        self.qbox.pack(fill="x", pady=(4,10))
        self.qbox.insert("0.0","Type your search query…")
        self.qbox.bind("<FocusIn>", lambda e: (
            self.qbox.delete("0.0","end")
            if self.qbox.get("0.0","end").strip()=="Type your search query…" else None))

        # Providers
        self._sec(sc,"[O] PROVIDERS")
        self.pframes = {}
        for k, cfg in PROVIDERS.items():
            f = _frame(sc, C["bg2"], corner_radius=6)
            f.pack(fill="x", pady=3)
            ctk.CTkSwitch(f, text=cfg["label"], variable=self.pvars[k],
                onvalue=True, offvalue=False, font=("Consolas",11),
                text_color=cfg["color"], progress_color=cfg["color"],
                button_color=cfg["color"]).pack(side="left", padx=10, pady=6)
            self.pframes[k] = f

        # API Keys
        self._sec(sc,"[O] API KEYS")
        self.key_entries = {}
        for label, key in [("Gemini","gemini"),("Perplexity","perplexity"),("OpenAI","openai")]:
            _label(sc, label, 9).pack(anchor="w", pady=(4,0))
            e = _entry(sc, "sk-…", "*")
            e.pack(fill="x", pady=(2,6))
            if self.api_keys.get(key): e.insert(0, self.api_keys[key])
            e.bind("<FocusOut>", lambda ev, k=key, w=e: self.api_keys.update({k: w.get()}))
            self.key_entries[key] = e

        # Settings
        self._sec(sc,"[O] SETTINGS")
        _label(sc,"Semantic Threshold",9).pack(anchor="w")
        self.thresh = ctk.CTkSlider(sc, from_=0, to=1, number_of_steps=20,
            progress_color=C["cyan"], button_color=C["cyan"])
        self.thresh.set(0.3); self.thresh.pack(fill="x", pady=(2,10))
        _label(sc,"Max attributions / provider",9).pack(anchor="w")
        self.max_e = _entry(sc,"20"); self.max_e.pack(fill="x",pady=(2,12))
        self.max_e.insert(0,"20")

        # Buttons
        self.run_btn = _btn(sc,"[O]  EXECUTE SCAN", self._run, h=50)
        self.run_btn.pack(fill="x", pady=(6,4))
        self.stop_btn = _btn(sc,"STOP  ABORT", self._stop, C["bg0"], h=34)
        self.stop_btn.configure(text_color=C["red"], border_color=C["red"],
                                hover_color="#1a0808", state="disabled")
        self.stop_btn.pack(fill="x", pady=4)

        # Export
        self._sec(sc,"[O] EXPORT")
        _btn(sc,"SAVE  JSON-LD Export",  self._exp_json, C["bg2"], h=34).pack(fill="x",pady=3)
        _btn(sc,"SAVE  PDF Executive Summary", self._exp_pdf, C["bg2"], h=34).pack(fill="x",pady=3)

        _label(sc,"* Developed by HSINI MOHAMED",9,C["muted"]).pack(pady=(24,4),anchor="w")

    def _content(self, parent):
        main = _frame(parent, C["bg0"])
        main.pack(side="right", fill="both", expand=True, padx=14, pady=14)

        self.pbar = ctk.CTkProgressBar(main, height=3, corner_radius=0,
            fg_color=C["bg2"], progress_color=C["cyan"])
        self.pbar.pack(fill="x"); self.pbar.set(0)

        self.tabs = ctk.CTkTabview(main, fg_color=C["bg1"],
            segmented_button_fg_color=C["bg2"],
            segmented_button_selected_color=C["cyan_dark"],
            segmented_button_unselected_color=C["bg2"],
            text_color=C["cyan"], corner_radius=8)
        self.tabs.pack(fill="both", expand=True, pady=(10,0))
        for t in ["* Dashboard","* Sunburst","* Attribution Log",
                  "* Responses","* System Log"]:
            self.tabs.add(t)

        self._tab_dashboard()
        self._tab_sunburst()
        self._tab_attribution()
        self._tab_responses()
        self._tab_syslog()

    # -- Tabs -----------------------------------------------------------------
    def _tab_dashboard(self):
        t = self.tabs.tab("* Dashboard")
        krow = _frame(t, C["bg0"]); krow.pack(fill="x", pady=(8,14))
        self.kpis = {}
        for i,(k,lbl,val) in enumerate([
            ("providers","PROVIDERS","0"),("attrs","ATTRIBUTIONS","0"),
            ("domains","UNIQUE DOMAINS","0"),("score","AVG SEMANTIC","0.00")]):
            f = _frame(krow, C["bg2"], corner_radius=10)
            f.grid(row=0, column=i, padx=6, pady=0, sticky="nsew")
            krow.grid_columnconfigure(i, weight=1)
            _label(f, lbl, 8, C["text2"]).pack(pady=(12,2))
            v = _label(f, val, 30, C["cyan"], True)
            v.pack(pady=(0,12))
            self.kpis[k] = v

        # Domain frequency table
        _label(t,"* TOP DOMAINS BY MENTION",10,C["cyan"],True).pack(anchor="w",pady=(0,4))
        cols=("Domain","Mentions","Provider","Semantic")
        self.dom_table = ctk.CTkScrollableFrame(t, fg_color=C["bg2"], height=300, corner_radius=8)
        self.dom_table.pack(fill="both", expand=True)
        for i,c in enumerate(cols):
            _label(self.dom_table, c, 9, C["text2"], True).grid(row=0,column=i,padx=12,pady=6,sticky="w")
        self.dom_rows = []

    def _tab_sunburst(self):
        t = self.tabs.tab("* Sunburst")
        self.sunburst_frame = t
        _label(t,"Sunburst chart renders after a scan. Requires plotly + kaleido.",
               10, C["text2"]).pack(expand=True)
        self.sunburst_lbl = None

    def _tab_attribution(self):
        t = self.tabs.tab("* Attribution Log")
        hdr = _frame(t, C["bg2"], corner_radius=6, height=36)
        hdr.pack(fill="x", pady=(0,6)); hdr.pack_propagate(False)
        for i,(col,w) in enumerate([("#",30),("Provider",90),("Domain",160),
                                    ("Title",260),("Author",130),("Mentions",70)]):
            _label(hdr, col, 9, C["text2"], True).grid(row=0,column=i,padx=8,pady=8,sticky="w")
            hdr.grid_columnconfigure(i, minsize=w)
        self.attr_log = ctk.CTkScrollableFrame(t, fg_color=C["bg1"], corner_radius=6)
        self.attr_log.pack(fill="both", expand=True)
        self.attr_rows = []

    def _tab_responses(self):
        t = self.tabs.tab("* Responses")
        self.resp_tabs = ctk.CTkTabview(t, fg_color=C["bg2"],
            segmented_button_fg_color=C["bg1"],
            segmented_button_selected_color=C["cyan_dark"],
            text_color=C["cyan"])
        self.resp_tabs.pack(fill="both", expand=True)
        self.resp_boxes = {}
        for p in PROVIDERS:
            self.resp_tabs.add(PROVIDERS[p]["label"])
            box = ctk.CTkTextbox(self.resp_tabs.tab(PROVIDERS[p]["label"]),
                fg_color=C["bg1"], text_color=C["text"], font=("Consolas",11),
                wrap="word", state="disabled")
            box.pack(fill="both", expand=True, padx=6, pady=6)
            self.resp_boxes[p] = box

    def _tab_syslog(self):
        t = self.tabs.tab("* System Log")
        self.syslog = ctk.CTkTextbox(t, fg_color=C["bg1"], text_color=C["text2"],
            font=("Consolas",10), wrap="word", state="disabled")
        self.syslog.pack(fill="both", expand=True)

    # -- Logic -----------------------------------------------------------------
    def _run(self):
        q = self.qbox.get("0.0","end").strip()
        if not q or q=="Type your search query…":
            messagebox.showwarning("No Query","Please enter a search query."); return
        selected = [k for k,v in self.pvars.items() if v.get()]
        if not selected:
            messagebox.showwarning("No Provider","Enable at least one provider."); return
        self.running = True
        self.results.clear()
        self.run_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.pbar.set(0)
        self._log(f">> Scan started: {q}")
        threading.Thread(target=self._scan_thread, args=(q, selected), daemon=True).start()

    def _stop(self):
        self.running = False
        self._log("STOP Scan aborted by user.")
        self._reset_btns()

    def _scan_thread(self, query: str, selected: list):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._scan_async(query, selected))
        loop.close()

    async def _scan_async(self, query: str, selected: list):
        total = len(selected); done = 0
        limit = int(self.max_e.get() or 20)
        tasks = {p: asyncio.create_task(self.engine.query(p, query)) for p in selected}
        for p, task in tasks.items():
            if not self.running: break
            self.after(0, lambda p=p: self._log(f"* Querying {p.upper()}…"))
            try:
                res = await task
                text = res.get("text","")
                status = res.get("status","demo")
                attrs = self.extractor.extract(text, p, limit)
                score = SemanticEngine.score(query, text)
                sr = SearchResult(provider=p, query=query, response_text=text,
                                  attributions=attrs, semantic_score=score, status=status)
                self.results.append(sr)
                done += 1
                self.after(0, lambda p=p, s=score, n=len(attrs), st=status:
                    self._log(f"[OK] {p.upper()} | score={s:.2f} | {n} attributions | {st}"))
                self.after(0, lambda r=sr: self._update_resp(r))
                self.after(0, lambda v=done/total: self.pbar.set(v))
            except Exception as e:
                self.after(0, lambda p=p, e=e: self._log(f"[ERR] {p.upper()} error: {e}"))
        self.after(0, self._finalize)

    def _finalize(self):
        self.running = False
        self._reset_btns()
        self.pbar.set(1)
        self._update_dashboard()
        self._update_attr_log()
        self._render_sunburst()
        self._log(f"[OK] Scan complete. {len(self.results)} providers · "
                  f"{sum(len(r.attributions) for r in self.results)} attributions")

    def _reset_btns(self):
        self.run_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def _update_resp(self, r: SearchResult):
        box = self.resp_boxes.get(r.provider)
        if not box: return
        box.configure(state="normal")
        box.delete("0.0","end")
        box.insert("0.0", f"[{r.status.upper()}] Score: {r.semantic_score:.2f} | "
                           f"{len(r.attributions)} attributions\n{'-'*60}\n{r.response_text}")
        box.configure(state="disabled")

    def _update_dashboard(self):
        all_a = [a for r in self.results for a in r.attributions]
        domains = {a.domain for a in all_a}
        avg_s = sum(r.semantic_score for r in self.results)/max(len(self.results),1)
        self.kpis["providers"].configure(text=str(len(self.results)))
        self.kpis["attrs"].configure(text=str(len(all_a)))
        self.kpis["domains"].configure(text=str(len(domains)))
        self.kpis["score"].configure(text=f"{avg_s:.2f}")
        # Domain table
        for w in self.dom_rows: w.destroy()
        self.dom_rows.clear()
        from collections import Counter
        top = Counter({a.domain: a.mention_count for a in all_a}).most_common(20)
        for row,(dom,cnt) in enumerate(top,1):
            prov = next((a.provider for a in all_a if a.domain==dom),"—")
            scr  = next((r.semantic_score for r in self.results if r.provider==prov), 0)
            for col,val in enumerate([dom, str(cnt), prov.upper(), f"{scr:.2f}"]):
                lbl = _label(self.dom_table, val, 9, C["text"])
                lbl.grid(row=row, column=col, padx=12, pady=4, sticky="w")
                self.dom_rows.append(lbl)

    def _update_attr_log(self):
        for w in self.attr_rows: w.destroy()
        self.attr_rows.clear()
        all_a = [(r.provider, a) for r in self.results for a in r.attributions]
        for i,(prov,a) in enumerate(all_a,1):
            bg = C["bg2"] if i%2==0 else C["bg1"]
            row_f = _frame(self.attr_log, bg, corner_radius=4, height=32)
            row_f.pack(fill="x", pady=1)
            for col,val in enumerate([str(i), prov.upper(), a.domain[:24],
                                       a.title[:40], a.author[:22], str(a.mention_count)]):
                color = PROVIDERS.get(prov,{}).get("color", C["text2"]) if col==1 else C["text"]
                _label(row_f, val, 9, color).grid(row=0, column=col, padx=8, pady=6, sticky="w")
            self.attr_rows.append(row_f)

    def _render_sunburst(self):
        try:
            import plotly.graph_objects as go
            import tempfile, webbrowser
            all_a = [a for r in self.results for a in r.attributions]
            if not all_a: return
            ids,labels,parents,vals = ["root"],["All Attributions"],[""],[ len(all_a)]
            for r in self.results:
                ids.append(r.provider); labels.append(r.provider.upper())
                parents.append("root"); vals.append(len(r.attributions))
                for a in r.attributions:
                    uid = f"{r.provider}:{a.domain}"
                    if uid not in ids:
                        ids.append(uid); labels.append(a.domain[:20])
                        parents.append(r.provider); vals.append(a.mention_count or 1)
            fig = go.Figure(go.Sunburst(ids=ids, labels=labels, parents=parents, values=vals,
                branchvalues="total",
                marker=dict(colors=[C["cyan"],C["purple"],C["emerald"]]*50,
                            line=dict(color=C["bg0"], width=1)),
                textfont=dict(family="Consolas", color=C["text"])))
            fig.update_layout(paper_bgcolor=C["bg1"], plot_bgcolor=C["bg0"],
                font=dict(color=C["text"], family="Consolas"),
                margin=dict(t=20,b=10,l=10,r=10),
                title=dict(text="Visibility Sunburst — Attribution Distribution",
                           font=dict(color=C["cyan"],size=13)))
            tmp = tempfile.mktemp(suffix=".html")
            fig.write_html(tmp)
            webbrowser.open(tmp)
            self._log("* Sunburst chart opened in browser.")
        except ImportError:
            self._log("[!] Install plotly to render sunburst charts.")
        except Exception as e:
            self._log(f"[!] Sunburst error: {e}")

    # -- Export ----------------------------------------------------------------
    def _exp_json(self):
        if not self.results: messagebox.showinfo("No Data","Run a scan first."); return
        p = filedialog.asksaveasfilename(defaultextension=".json",
            filetypes=[("JSON-LD","*.json")],
            initialfile=f"omni_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
        if p:
            ok = export_jsonld(self.results, p)
            (messagebox.showinfo if ok else messagebox.showerror)(
                "Export","Saved: " + p if ok else "Export failed.")

    def _exp_pdf(self):
        if not self.results: messagebox.showinfo("No Data","Run a scan first."); return
        p = filedialog.asksaveasfilename(defaultextension=".pdf",
            filetypes=[("PDF","*.pdf")],
            initialfile=f"omni_exec_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        if p:
            ok = export_pdf(self.results, p)
            (messagebox.showinfo if ok else messagebox.showerror)(
                "Export","Saved: " + p if ok else "Export failed (install reportlab).")

    # -- Helpers ---------------------------------------------------------------
    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}\n"
        self.syslog.configure(state="normal")
        self.syslog.insert("end", line)
        self.syslog.see("end")
        self.syslog.configure(state="disabled")
        self.stat_lbl.configure(text=msg[:60])

    def _sec(self, parent, text: str):
        f = _frame(parent, C["bg0"], height=28, corner_radius=0)
        f.pack(fill="x", pady=(10,4))
        _label(f, text, 9, C["cyan"], True).pack(side="left", padx=0)

    def _tick(self):
        self.clock_lbl.configure(text=datetime.now().strftime("* %H:%M:%S"))
        self.after(1000, self._tick)


if __name__ == "__main__":
    app = OmniApp()
    app.mainloop()
