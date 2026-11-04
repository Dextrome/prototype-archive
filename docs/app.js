"use strict";
(() => {
const projects=window.PROJECTS||[];
const $=s=>document.querySelector(s);
const grid=$("#project-grid"), search=$("#search"), dialog=$("#project-dialog"), imageDialog=$("#image-dialog");
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
let filter="All", active=null, photoIndex=0, lastFocus=null, closing=false;
const filmShort=g=>g.video?.kind==="staged"?"STAGED CONCEPT":g.video?.kind==="reel"?"CONCEPT REEL":"GAMEPLAY";
function render(){
 const term=search.value.trim().toLowerCase();
 const list=projects.filter(g=>(filter==="All"||g.category===filter)&&(!term||[g.title,g.genre,g.pitch,g.description,...g.loop].join(" ").toLowerCase().includes(term)));
 grid.innerHTML=list.map(g=>`<article class="project-card"><button class="card-image" data-open="${esc(g.id)}" aria-label="Explore ${esc(g.title)}"><img src="${esc(g.images[0].src)}" alt="${esc(g.images[0].caption)}" loading="lazy" width="640" height="400"><span class="image-wash"></span><span class="card-number">NO. ${String(projects.indexOf(g)+1).padStart(2,"0")}</span><span class="film-type"><span class="play-symbol" aria-hidden="true">▶</span>${filmShort(g)}</span></button><div class="card-meta"><span class="genre">${esc(g.genre)}</span><span class="stage">${esc(g.stage)}</span></div><h3>${esc(g.title)}</h3><p class="card-pitch">${esc(g.pitch)}</p><div class="card-bottom"><span>${esc(g.players)}</span><button class="explore-button" data-open="${esc(g.id)}" aria-label="Open ${esc(g.title)}">Explore project <span aria-hidden="true">↗</span></button></div></article>`).join("");
 $("#results-count").textContent=`${list.length} ${list.length===1?"project":"projects"}${filter!=="All"?" / "+filter.toLowerCase():" in the archive"}${term?" matching “"+search.value.trim()+"”":""}`;
 $("#empty").hidden=list.length!==0;
}
function openProject(id,play=false,writeHash=true){
 const g=projects.find(x=>x.id===id); if(!g)return;
 const already=dialog.open;
 if(!already)lastFocus=document.activeElement;
 const oldVideo=dialog.querySelector("video");if(oldVideo)oldVideo.pause();
 active=g;photoIndex=0;
 $("#project-detail").innerHTML=`<div class="detail-heading"><div><div class="eyebrow">${esc(g.stage.toUpperCase())} / ${esc(g.genre.toUpperCase())}</div><h2 id="detail-title">${esc(g.title)}</h2><p>${esc(g.pitch)}</p></div><button class="share-button" id="share-project">Copy project link ↗</button></div><section class="detail-film" aria-label="${esc(g.video.label)}"><div class="video-wrap"><video id="detail-video" controls playsinline preload="none" poster="${esc(g.images[0].src)}" aria-label="${esc(g.video.label+': '+g.title)}"><source src="${esc(g.video.src)}" type="video/mp4">Your browser cannot play this video. <a href="${esc(g.video.src)}">Download the film</a>.</video></div><p class="film-note"><strong>${esc(g.video.label)} · ${esc(g.video.duration)}</strong><span>${esc(g.video.note)}</span></p></section><div class="detail-content"><section aria-labelledby="premise-title"><h3 id="premise-title">The idea</h3><p class="detail-description">${esc(g.description)}</p><div class="detail-tags"><span>${esc(g.genre)}</span><span>${esc(g.players)}</span><span>${g.category==="Concept studies"?"Factory concept":"Development build"}</span></div></section><section aria-labelledby="loop-title"><h3 id="loop-title">${g.category==="Concept studies"?"The intended gameplay loop":"The gameplay loop"}</h3><ol class="loop">${g.loop.map(x=>`<li>${esc(x)}</li>`).join("")}</ol></section></div><section class="screenshot-section" aria-labelledby="screens-title"><div class="screenshot-heading"><h3 id="screens-title">Inside the frame</h3><span>SELECT A STILL TO ENLARGE ↗</span></div><div class="screenshots">${g.images.map((im,i)=>`<figure class="screenshot"><button data-photo="${i}" aria-label="Enlarge screenshot ${i+1}: ${esc(im.caption)}"><img src="${esc(im.src)}" alt="${esc(im.caption)}" loading="lazy"></button><figcaption>${esc(im.caption)}</figcaption></figure>`).join("")}</div></section><aside class="development-note"><strong>From the development notebook</strong>${esc(g.note)}</aside>`;
 if(!already){dialog.showModal();document.body.classList.add("modal-open");}
 dialog.scrollTop=0;
 if(writeHash&&location.hash!=="#"+id)history.pushState({project:id},"","#"+id);
 $("#share-project").addEventListener("click",copyLink);
 if(play)$("#detail-video").play().catch(()=>{});
}
function closeProject(){if(!dialog.open)return;closing=true;dialog.close();history.replaceState(null,"","#collection");closing=false;}
function updatePhoto(){
 const im=active.images[photoIndex]; $("#lightbox-image").src=im.src;$("#lightbox-image").alt=im.caption;$("#lightbox-caption").textContent=im.caption;$("#lightbox-position").textContent=`${photoIndex+1} / ${active.images.length}`;
}
function openPhoto(i){photoIndex=i;updatePhoto();imageDialog.showModal();}
function movePhoto(delta){photoIndex=(photoIndex+delta+active.images.length)%active.images.length;updatePhoto();}
async function copyLink(){
 const link=new URL(location.href);link.hash=active.id;
 try{await navigator.clipboard.writeText(link.href);toast("Project link copied");}
 catch{const input=document.createElement("textarea");input.value=link.href;input.style.position="fixed";input.style.opacity="0";dialog.append(input);input.select();let ok=false;try{ok=document.execCommand("copy");}catch{}input.remove();toast(ok?"Project link copied":"Use the address bar to copy this project link");}
}
let toastTimer;function toast(msg){$("#toast").textContent=msg;$("#toast").classList.add("visible");clearTimeout(toastTimer);toastTimer=setTimeout(()=>$("#toast").classList.remove("visible"),2500);}
document.addEventListener("click",e=>{const open=e.target.closest("[data-open]");if(open){openProject(open.dataset.open);return;}const photo=e.target.closest("[data-photo]");if(photo)openPhoto(Number(photo.dataset.photo));});
document.querySelectorAll(".filter").forEach(b=>b.addEventListener("click",()=>{filter=b.dataset.filter;document.querySelectorAll(".filter").forEach(x=>{x.classList.toggle("active",x===b);x.setAttribute("aria-pressed",String(x===b));});render();}));
search.addEventListener("input",render);
$("#reset").addEventListener("click",()=>{search.value="";document.querySelector('[data-filter="All"]').click();search.focus();});
$("#close-project").addEventListener("click",closeProject);
dialog.addEventListener("close",()=>{const v=dialog.querySelector("video");if(v){v.pause();v.removeAttribute("src");v.querySelectorAll("source").forEach(s=>s.removeAttribute("src"));v.load();}document.body.classList.remove("modal-open");if(!closing&&location.hash==="#"+active?.id)history.replaceState(null,"","#collection");lastFocus?.focus({preventScroll:true});});
$("#close-image").addEventListener("click",()=>imageDialog.close());
$("#prev-image").addEventListener("click",()=>movePhoto(-1));$("#next-image").addEventListener("click",()=>movePhoto(1));
imageDialog.addEventListener("keydown",e=>{if(e.key==="ArrowLeft"){e.preventDefault();movePhoto(-1);}if(e.key==="ArrowRight"){e.preventDefault();movePhoto(1);}});
for(const d of [dialog,imageDialog])d.addEventListener("click",e=>{if(e.target!==d)return;const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom){if(d===dialog)closeProject();else d.close();}});
window.addEventListener("hashchange",()=>{const id=location.hash.slice(1);if(projects.some(g=>g.id===id))openProject(id,false,false);else if(dialog.open)dialog.close();});
render();const initial=location.hash.slice(1);if(projects.some(g=>g.id===initial))openProject(initial,false,false);
})();