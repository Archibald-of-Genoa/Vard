import React, { useState, useEffect } from "react";
import "./SearchBar.css";
import { ReactComponent as SearchIcon } from "./assets/icons/search.svg";
import { ReactComponent as CloseIcon } from "./assets/icons/close_default.svg";
import { ReactComponent as CloseHoverIcon } from "./assets/icons/close_hover-click.svg";
import { ReactComponent as FilterIcon } from "./assets/icons/filter_default.svg";
import { ReactComponent as FilterHoverIcon } from "./assets/icons/filter_hover-click.svg";

// Из общего: имеет смысл сразу выносить состояние наружу. Я предпочитаю RTK
// Query. Компонент получился большой. Надо декомпозировать. Но этим мы займёмся
// вместе. Подумаем, какие штучки имеет смысл, опять-таки, вынести наружу

// В зависимости от того, как долго выполняется фильтрация или поиск, может быть
// полезно предоставлять пользователю обратную связь о том, что у нас здесь происходит... Какой-нибудь вертухайчик поставить...


const SearchBar = ({ variation }) => {
  //  всего 5 вариаций
  const [searchQuery, setSearchQuery] = useState(""); //  default
  const [data, setData] = useState([]); //  connection

  // Текущая реализация фильтрует данные при каждом нажатии кнопки поиска.
  // Если набор данных большой, это может стать неэффективным.
  // Можно впендюрить useMemo и бахнуть как-нибудь так:
  // const filteredData = useMemo(() => {
  //     if (!searchQuery.trim()) return data;
  //     return data.filter(item => item.name.toLowerCase().includes(searchQuery.toLowerCase()));
  // }, [data, searchQuery]);

  // Или логику фильтрации вообще вынести отдельно

  const [filteredData, setFilteredData] = useState([]); //  files
  const [isLoading, setIsLoading] = useState(false); //  charts
  const [isCloseHovered, setIsCloseHovered] = useState(false); //  wiki
  const [isFilterHovered, setIsFilterHovered] = useState(false);


  // Асинхронные запросы лучше делать не через цепочку промисов, а через createApi, который в RTK уже есть.

  useEffect(() => {
    // Fetch data
    setIsLoading(true);
    fetch("") // не забыть поставить API
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setFilteredData(data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
      });
  }, [variation]);

  let searchBarClass = "search-bar";
  let placeholderText = "Search...";
  let hideSearchAndCloseIcon = true;

  switch (variation) {
    case "connection":
      placeholderText = "Search connection";
      break;
    case "files":
      placeholderText = "Search files";
      break;
    case "charts":
      placeholderText = "Search charts";
      break;
    case "wiki":
      placeholderText = "Search wiki";
      break;
    default:
      break;
  }

  if (variation !== "default") {
    searchBarClass += " nonDefault";
    hideSearchAndCloseIcon = false;
  }
// Возможно, имеет смысл сделать кастомные хуки. Допустим, на поведение крысы.
// Типа useHover()

  const handleCloseMouseEnter = () => {
    setIsCloseHovered(true);
  };

  const handleCloseMouseLeave = () => {
    setIsCloseHovered(false);
  };

  const handleFilterMouseEnter = () => {
    setIsFilterHovered(true);
  };

  const handleFilterMouseLeave = () => {
    setIsFilterHovered(false);
  };

  const handleSearch = () => {
    console.log("Search button clicked");
    if (!data || data.length === 0) {
      return;
    }
    if (searchQuery.trim() === "") {
      setFilteredData([]);
      return;
    }

    setIsLoading(true);
    const filtered = data.filter((item) =>
      item.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredData(filtered);
    setIsLoading(false);

    console.log("Search button clicked:", searchQuery);
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleClearSearch = () => {
    setSearchQuery("");
    setFilteredData([]);
    console.log("Clear button clicked");
  };

  const handleFilter = () => {
    console.log("Filter button clicked");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className={searchBarClass}>
      {hideSearchAndCloseIcon && (
        <SearchIcon onClick={handleSearch} className="search-icon" />
      )}

// Пропсы надо типизировать. Либо через TS (желательно), либо через propTypes,
// который уже есть в Реакте. Но последний вариант имеет смысл, если проект
// кастрированный и использование  тайпскрипта не подразумевается

      <input
        type="text"
        value={searchQuery}
        onChange={handleSearchChange}
        placeholder={placeholderText}
        onKeyDown={handleKeyDown}
      />
      <div
        className="filter-icon"
        onMouseEnter={handleFilterMouseEnter}
        onMouseLeave={handleFilterMouseLeave}
        onClick={handleFilter}
      >
        {isFilterHovered ? <FilterHoverIcon /> : <FilterIcon />}
      </div>
      {hideSearchAndCloseIcon && (
        <div
          className="close-icon"
          onMouseEnter={handleCloseMouseEnter}
          onMouseLeave={handleCloseMouseLeave}
          onClick={handleClearSearch}
        >
          {isCloseHovered ? <CloseHoverIcon /> : <CloseIcon />}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
