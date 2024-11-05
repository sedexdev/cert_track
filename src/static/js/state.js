(function () {
  const pathWhiteList = [
    // user defined routes will go here
  ];

  window.onload = () => {
    if (pathWhiteList.includes(window.location.pathname)) {
      console.log("Updating state...");
      if (localStorage.length > 0) {
        setCurrentNav(window.localStorage.getItem("currentNav"));
        setDisplayedContent(window.localStorage.getItem("currentNav"));
        setDisplayAddContentBtn(window.localStorage.getItem("currentNav"));
        setSectionColours();
        setExpandedSections();
        setResourceFormState();
      } else {
        const nav = document.getElementById("nav-statistics");
        nav.classList.add("selected");
        const content = document.getElementById("statistics");
        content.classList.remove("hidden");
      }
    }
  };
})();

/**
 * Sets both the nav bar and the select
 * menu on smaller screens to the last
 * selected tab
 *
 * @param {string} value
 */
function setCurrentNav(value) {
  // remove selected class from all nav elements
  const nav = document.getElementById("cert-nav");
  if (nav) {
    const links = nav.children;
    for (let link of links) {
      if (link.classList.contains("selected")) {
        link.classList.remove("selected");
      }
    }
    // update from local storage if it exists
    if (value) {
      // add selected to current nav
      const current = document.getElementById(`nav-${value}`);
      current.classList.add("selected");
      // do the same for the select menu
      const select_list = document.getElementById("content");
      select_list.value = value;
    }
  }
}

/**
 * Updates the displayed content
 *
 * @param {number} id element to update
 */
function setDisplayedContent(id) {
  const content = [
    "statistics",
    "courses",
    "videos",
    "articles",
    "documentation",
  ];
  const nav = document.getElementById("cert-nav");
  if (nav) {
    for (let topic of content) {
      const contentEl = document.getElementById(topic);
      contentEl.classList.add("hidden");
    }
    const el = document.getElementById(id);
    el.classList.remove("hidden");
  }
}

/**
 * Updates the add content button displayed
 *
 * @param {number} id element to update
 */
function setDisplayAddContentBtn(id) {
  const btn = document.getElementById("content-btn");
  if (btn) {
    if (id != "statistics") {
      btn.classList.remove("hidden");
    }
  }
}

/**
 * Sets the correct colours for each
 * course section
 */
function setSectionColours() {
  // apply colour to all sections from local storage
  for (let [key, _] of Object.entries(localStorage)) {
    if (key.includes("course") && key.includes("sections")) {
      const courseID = key.split("-")[1];
      const courseSections = JSON.parse(
        window.localStorage.getItem(`course-${courseID}-sections`)
      );
      for (let section of courseSections) {
        const el = document.getElementById(`section-${section.id}-${courseID}`);
        if (el) {
          el.classList.add(section.colour);
        }
      }
    }
  }
  // add bg-red-400 to any section without a colour
  // this will catch newly created sections
  const sections = document.querySelectorAll('[id^="section-"]');
  for (let section of sections) {
    let hasColour = false;
    for (let c of section.classList) {
      if (c.includes("bg-")) {
        hasColour = true;
        break;
      }
    }
    if (!hasColour) {
      section.classList.add("bg-red-400");
    }
  }
}

/**
 * Expands already open sections that have just
 * had a new section added to them
 */
function setExpandedSections() {
  const courses = window.localStorage.getItem("coursesWithOpenSections");
  if (courses) {
    const courseArray = JSON.parse(courses);
    for (let id of courseArray) {
      const down = document.getElementById(`down-arrow-${id}`);
      const up = document.getElementById(`up-arrow-${id}`);
      const el = document.getElementById(`sections-${id}`);
      down.classList.add("hidden");
      up.classList.remove("hidden");
      el.classList.remove("hidden");
    }
  }
}

/**
 * Opens the resource form again after a page
 * reload in the event that an Open Graph protocol
 * hit caused a reload
 */
function setResourceFormState() {
  const show = window.localStorage.getItem("loadResourceForm");
  if (show == "true") {
    const form = document.getElementById("resource-form");
    if (form) {
      form.classList.remove("hidden");
      const btn = document.getElementById("content-btn");
      btn.classList.add("hidden");
    }
  } else {
    const form = document.getElementById("resource-form");
    if (form) {
      form.classList.add("hidden");
    }
    window.localStorage.removeItem("loadResourceForm");
  }
}
