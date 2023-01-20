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

    
    async getPosts() {
        this.loading = true;

        let response = await fetch("/api/posts", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ latest: 0 }),
        }).then((response) => response.json());

        if (response.status == "success") {
            let data = response.data;
            this.posts = data;
            this.innerHTML = `<div class="post-area w-full flex flex-col px-10 md:px-36 lg:px-80" id="post_section"> </div>`;
        }
        this.loading = false;
    }

    async connectedCallback() {
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

    like(){
        console.log("tes")
    }


    render() {
        if (!this.loading) {
            let uname = localStorage.getItem("uname")
            let self = this.getAttribute("self")

            let data = this.posts;
            let keys = Object.keys(data).reverse();
            let i;
            const options = {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: "numeric",
                minute: "numeric",
            };
            
            for (i in keys) {
                var post = data[keys[i]];
                let pid = keys[i];
                let content = linkify(post["content"]);
                let lc = post["lc"];
                let dlc = post["dlc"];
                let islike = post["islike"];
                let isdislike = post["isdislike"];
                let user = post["uname"];
                let date = post["datetime"];
                let d = new Date(`${date} UTC`);
                d = d.toLocaleString("en-us", options);

                if(self == "true" && uname != user){
                    continue;
                }

                this.children[0].innerHTML += ` <div class="post flex flex-col shadow-md w-full pb-2 mb-2 " id="${pid}">
        <div class="first-row flex flex-row w-full ">
            <div
                class="pfp-container min-w-[45px] min-h-[45px] pt-2 pr-4"
            >
                <img src="/images/${user}" alt="pfp" class="min-w-[45px] h-[45px] rounded-full" />
            </div>
            <div class="uname-date flex flex-col w-full">
                <div
                    class="username pt-3 flex flex-row w-full place-content-between"
                >
                    <a href="/u/${user}" class="hover:underline underline-offset-1 accent-black font-medium text-lg" >${user}</a>
                    <p class="pr-4 text-xs ">${d}</p>
                </div>
                <!-- <div class="username">
                    <p class="text-sm"></p>
                </div> -->
            </div>
        </div>
        <div class="content pl-14 pr-2 whitespace-pre-wrap text-lg">${content}</div>
        <div class="buttons-row flex flex-row">
            <div class="lc flex flex-row pl-14 pt-4">
                <span class="material-icons w-full h-4 hover:cursor-pointer" onclick="onBtnPress(${pid},this)">${
                    islike ? "thumb_up" : "thumb_up_off_alt"
                }</span>
                <p class="pl-2">${lc}</p>
            </div>
            <div class="dlc flex flex-row pl-4 pt-4">
                <span class="material-icons w-full h-4 hover:cursor-pointer" onclick="onBtnPress(${pid},this)">${
                    isdislike ? "thumb_down" : "thumb_down_off_alt"
                }</span>
                <p class="pl-2">${dlc}</p>
            </div>
        </div>
    </div>`;
            }
        }
    }
}

customElements.define("post-section", PostSection);
