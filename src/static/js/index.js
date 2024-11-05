/**
 * Displays the add content button on all tabs
 * except statistics as this just displays stats
 * about the content state
 *
 * @param {string} value tab to show button under
 */
function displayAddContentButton(value) {
  const btn = document.getElementById("content-btn");
  if (value != "statistics") {
    btn.classList.remove("hidden");
  } else {
    btn.classList.add("hidden");
  }
}

/**
 * Hides the add content button
 */
function hideAddContentButton() {
  const btn = document.getElementById("content-btn");
  btn.classList.add("hidden");
}

/**
 * Hides the resource form
 */
function hideResourceForm() {
  const form = document.getElementById("resource-form");
  form.classList.add("hidden");
}

/**
 * Hides all content
 */
function hideAllContent() {
  const courses = document.getElementById("courses");
  const videos = document.getElementById("videos");
  const articles = document.getElementById("articles");
  const documents = document.getElementById("documentation");
  const content = [courses, videos, articles, documents];
  for (let topic of content) {
    topic.classList.add("hidden");
  }
}

/**
 * Clears the values in the name and url form
 * input fields
 */
function clearFormInputs() {
  const name = document.getElementById("resource-name");
  const url = document.getElementById("resource-url");
  if (name && url) {
    name.value = "";
    url.value = "";
  }
}

/**
 * Clears the values from the add section form
 *
 * @param {str} id
 */
function clearSectionForm(id) {
  // check local storage for courses with expanded sections
  const courses = window.localStorage.getItem("coursesWithOpenSections");
  if (courses) {
    // parse and update courses with ID if found
    const courseArray = JSON.parse(courses);
    if (!courseArray.includes(id)) {
      courseArray.push(id);
      window.localStorage.setItem(
        "coursesWithOpenSections",
        JSON.stringify(courseArray)
      );
    }
  } else {
    // create the courses array if not found
    window.localStorage.setItem(
      "coursesWithOpenSections",
      JSON.stringify([id])
    );
  }
  const number = document.getElementById(`sections-${id}-number`);
  const title = document.getElementById(`sections-${id}-title`);
  setInterval(() => {
    number.value = "";
    title.value = "";
  }, 500);
}

/**
 * Clears resource type radio buttons of the
 * checked attribute
 */
function clearChecked() {
  for (let i = 0; i < 4; i++) {
    const el = document.getElementById(`resource_type-${i}`);
    el.checked = false;
  }
}

/**
 * Gets the innerHTML value of the currently
 * selected content tab
 */
function getSelectedValue() {
  let value;
  let links = document.getElementById("cert-nav").children;
  // find selected element value
  for (let link of links) {
    if (link.classList.contains("selected")) {
      value = link.innerHTML.toLowerCase();
      break;
    }
  }
  return value;
}

/**
 * Displays the resource form to add content
 * to the cert dashboard
 */
function displayAddResourceForm() {
  let links = document.getElementById("cert-nav").children;
  // get value of selected content
  for (let link of links) {
    if (link.classList.contains("selected")) {
      type = link.innerHTML.toLowerCase();
    }
  }
  // hide other elements and only display form
  hideAllContent();
  hideAddContentButton();
  hideResourceForm();
  const form = document.getElementById("resource-form");
  form.classList.remove("hidden");
  // clear the input fields
  clearFormInputs();
}

/**
 * Displays the section form to add a section
 * to a course
 *
 * @param {str} id
 */
function displayAddSectionForm(id) {
  const sections = document.getElementById(`sections-${id}-form`);
  const addBtn = document.getElementById(`sections-${id}-btn`);
  const closeBtn = document.getElementById(`sections-${id}-close-btn`);
  sections.classList.remove("hidden");
  addBtn.classList.add("hidden");
  closeBtn.classList.remove("hidden");
}

/**
 * Updates the selected option in the select
 * drop down list
 *
 * @param {string} value Option to select
 */
function updateSelect(value) {
  const select_list = document.getElementById("content");
  select_list.value = value.toLowerCase();
}

/**
 * Updates the highlighting for the selected
 * content when selected from the nav bar
 *
 * @param {HTMLElement} el element to update
 */
function updateHighlightNav(el) {
  let links = document.getElementById("cert-nav").children;
  // remove selected class
  for (let link of links) {
    if (link.classList.contains("selected")) {
      link.classList.remove("selected");
    }
  }
  el.classList.add("selected");
  updateSelect(el.innerHTML);
}

/**
 * Updates the highlighting for the selected
 * content when selected from the select list
 *
 * @param {str} value
 */
function updateHighlightSelect(value) {
  let links = document.getElementById("cert-nav").children;
  // remove selected class
  for (let link of links) {
    if (link.innerHTML.toLowerCase() == value) {
      link.classList.add("selected");
    } else {
      link.classList.remove("selected");
    }
  }
}

/**
 * Displays the selected content
 *
 * @param {number} id element to display
 */
function displayContent(id) {
  const content = [
    "statistics",
    "courses",
    "videos",
    "articles",
    "documentation",
  ];
  for (let topic of content) {
    const el = document.getElementById(topic);
    if (topic == id) {
      el.classList.remove("hidden");
    } else {
      el.classList.add("hidden");
    }
  }
}

/**
 * Handles the cert content nav selection
 *
 * @param {HTMLElement} el
 */
function handleNav(el) {
  // hide any open forms
  hideResourceForm();
  // clear the radio buttons
  clearChecked();
  let id;
  if (el.tagName.toLowerCase() == "select") {
    displayAddContentButton(el.value);
    updateHighlightSelect(el.value);
    id = el.value;
  } else {
    const value = el.innerHTML.toLowerCase();
    displayAddContentButton(value);
    updateHighlightNav(el);
    id = value;
  }
  displayContent(id);
  // update local storage
  window.localStorage.setItem("currentNav", id);
}

/**
 * Closes the resource form and displays the content
 */
function closeForm() {
  const el = document.getElementById("resource-form");
  el.classList.add("hidden");
  // display the add content button
  const value = getSelectedValue();
  displayAddContentButton(value);
  // display the content
  displayContent(value);
}

/**
 * Updates local storage with the display state of the
 * resource form
 */
function updateResourceFormState(state) {
  window.localStorage.setItem("loadResourceForm", state);
}

/**
 * Closes the section form
 *
 * @param {number} id element ID
 */
function closeSectionForm(id) {
  const sections = document.getElementById(`sections-${id}-form`);
  const addBtn = document.getElementById(`sections-${id}-btn`);
  const closeBtn = document.getElementById(`sections-${id}-close-btn`);
  sections.classList.add("hidden");
  addBtn.classList.remove("hidden");
  closeBtn.classList.add("hidden");
}

/**
 * Displays course section data
 *
 * @param {number} id
 */
function displaySections(id) {
  const down = document.getElementById(`down-arrow-${id}`);
  const up = document.getElementById(`up-arrow-${id}`);
  const sections = document.getElementById(`sections-${id}`);
  if (down.classList.contains("hidden")) {
    down.classList.remove("hidden");
    up.classList.add("hidden");
    sections.classList.add("hidden");
    // update courses with expanded sections
    const courses = window.localStorage.getItem("coursesWithOpenSections");
    if (courses) {
      // parse and update courses with ID if found
      const courseArray = JSON.parse(courses);
      const index = courseArray.indexOf(id);
      if (index > -1) {
        courseArray.splice(index, 1);
        window.localStorage.setItem(
          "coursesWithOpenSections",
          JSON.stringify(courseArray)
        );
      }
    }
  } else {
    down.classList.add("hidden");
    up.classList.remove("hidden");
    sections.classList.remove("hidden");
  }
}

/**
 * Updates a list of section colours against
 * a single course in local storage
 *
 * @param {number} courseID
 * @param {number} sectionID
 * @param {str} colour
 */
function updateSectionsLocalStorage(courseID, sectionID, colour) {
  // check if sections array for the course already exists
  const courseArray =
    window.localStorage.getItem(`course-${courseID}-sections`) || null;
  if (courseArray) {
    // // if it does pull it out and add the new section/colour
    courseSections = JSON.parse(courseArray);
    let found = false;
    for (let section of courseSections) {
      if (section.id == sectionID) {
        section.colour = colour;
        found = true;
        break;
      }
    }
    if (!found) {
      courseSections.push({ id: sectionID, colour: colour });
    }
    // write it back to local storage
    window.localStorage.setItem(
      `course-${courseID}-sections`,
      JSON.stringify(courseSections)
    );
  } else {
    // create the array and write it as a JSON string to local storage
    window.localStorage.setItem(
      `course-${courseID}-sections`,
      JSON.stringify([{ id: sectionID, colour: colour }])
    );
  }
}

/**
 * Sets the colour of a section card based
 * on the checked form elements
 *
 * @param {number} courseID
 * @param {number} sectionID
 */
function updateSectionColour(courseID, sectionID) {
  const sectionCardsMade = document.getElementById(
    `course-${courseID}-section-${sectionID}-cards_made`
  );
  const sectionComplete = document.getElementById(
    `course-${courseID}-section-${sectionID}-complete`
  );
  const toDo = "bg-red-400";
  const inProgress = "bg-orange-400";
  const completed = "bg-lime-400";
  const section = document.getElementById(`section-${sectionID}-${courseID}`);
  if (sectionCardsMade.checked && sectionComplete.checked) {
    section.classList.remove(toDo);
    section.classList.remove(inProgress);
    section.classList.add(completed);
    updateSectionsLocalStorage(courseID, sectionID, completed);
    return;
  } else if (sectionCardsMade.checked || sectionComplete.checked) {
    section.classList.remove(toDo);
    section.classList.remove(completed);
    section.classList.add(inProgress);
    updateSectionsLocalStorage(courseID, sectionID, inProgress);
    return;
  } else {
    section.classList.remove(inProgress);
    section.classList.remove(completed);
    section.classList.add(toDo);
    updateSectionsLocalStorage(courseID, sectionID, toDo);
    return;
  }
}

/**
 * Delete a flashed message
 */
function deleteMsg() {
  const msgContainer = document.getElementById("msg-container");
  msgContainer.remove();
}
