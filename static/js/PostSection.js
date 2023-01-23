class PostSection extends HTMLElement {
    constructor() {
        super();
    }

    static get observedAttributes() {
        return ["loading", "posts"];
    }

    get loading() {
        return JSON.parse(this.getAttribute("loading"));
    }

    set loading(v) {
        this.setAttribute("loading", JSON.stringify(v));
    }

    get posts() {
        return JSON.parse(this.getAttribute("posts"));
    }

    set posts(v) {
        this.setAttribute("posts", JSON.stringify(v));
    }

    async getPosts(page = 0) {
        this.loading = true;
        let response = await fetch("/api/posts", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ page: page }),
        }).then((response) => response.json());

        if (response.status == "success") {
            let data = response.data;
            this.posts = data;
        }
        this.loading = false;
    }

    async connectedCallback() {
        this.innerHTML = `<div class="post-area w-full flex flex-col px-1 md:px-36 lg:px-80" id="post_section"> </div>`;
        this.addEventListener("click", (event) => {
            const name = event.target.id;
            if (this[name]) {
              this[name]();
            }
          });
        await this.getPosts();
    }

    disconnectedCallback() {}

    attributeChangedCallback(attrName, oldVal, newVal) {
        this.render();
    }


    render() {
        if (!this.loading) {
               localStorage.setItem("page",pid)
        }
    }
}

customElements.define("post-section", PostSection);
