from typing import Any, List, Optional, Union
from pydantic import BaseModel


class ReleaseDate(BaseModel):
    ReleaseDate: str


class Link(BaseModel):
    name: str
    url: str


class Genre(BaseModel):
    id: str
    name: str


class Developer(BaseModel):
    id: str
    name: str


class Publisher(BaseModel):
    id: str
    name: str


class Feature(BaseModel):
    id: str
    name: str


class Platform(BaseModel):
    background: Any
    cover: Any
    icon: Any
    id: str
    name: str
    specification_id: str


class Series(BaseModel):
    id: str
    name: str


class AgeRating(BaseModel):
    id: str
    name: str


class CompletionStatus(BaseModel):
    id: str
    name: str


class Game(BaseModel):
    added: Optional[str]
    added_segment: Optional[int]
    age_rating_ids: Optional[List[str]]
    age_ratings: Optional[List[AgeRating]]
    background_image: Optional[str]
    categories: Any
    category_ids: Any
    community_score: Optional[int]
    community_score_group: Optional[int]
    community_score_rating: Optional[int]
    completion_status: Optional[CompletionStatus]
    completion_status_id: Optional[str]
    cover_image: Optional[str]
    critic_score: Optional[int]
    critic_score_group: Optional[int]
    critic_score_rating: Optional[int]
    description: Optional[str]
    developer_ids: Optional[List[str]]
    developers: Optional[List[Genre]]
    enable_system_hdr: bool = False
    favorite: bool = False
    feature_ids: Optional[List[str]]
    features: Optional[List[Feature]]
    game_actions: Any
    game_id: Optional[str]
    game_started_script: Any
    genre_ids: Optional[List[str]]
    genres: Optional[List[Genre]]
    hidden: bool = False
    icon: Optional[str]
    id: str
    include_library_plugin_action: bool = False
    install_directory: Any
    install_size: Any
    install_size_group: Optional[int]
    installation_status: Optional[int]
    is_custom_game: bool = False
    is_installed: bool = False
    is_installing: bool = False
    is_launching: bool = False
    is_running: bool = False
    is_uninstalling: bool = False
    last_activity: Any
    last_activity_segment: Optional[int]
    last_size_scan_date: Any
    links: Optional[List[Link]]
    manual: Any
    modified: Optional[str]
    modified_segment: Optional[int]
    name: Optional[str]
    notes: Any
    override_install_state: bool = False
    platform_ids: Optional[List[str]]
    platforms: Optional[List[Platform]]
    play_count: Optional[int]
    playtime: Optional[int]
    playtime_category: Optional[int]
    plugin_id: Optional[str]
    post_script: Any
    pre_script: Any
    publisher_ids: Optional[List[str]]
    publishers: Optional[List[Genre]]
    recent_activity: Optional[str]
    recent_activity_segment: Optional[int]
    region_ids: Any
    regions: Any
    release_date: Optional[ReleaseDate]
    release_year: Optional[int]
    roms: Any
    series: Optional[List[Series]]
    series_ids: Optional[List[str]]
    sorting_name: Any
    source: Any
    source_id: Optional[str]
    tag_ids: Any
    tags: Any
    use_global_game_started_script: bool = False
    use_global_post_script: bool = False
    use_global_pre_script: bool = False
    user_score: Any
    user_score_group: Optional[int]
    user_score_rating: Optional[int]
    version: Any


class Games(BaseModel):
    games: Optional[List[Game]] = None
