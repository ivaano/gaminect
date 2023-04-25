from typing import Any, List, Optional
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
    added: str
    added_segment: int
    age_rating_ids: Optional[List[str]]
    age_ratings: Optional[List[AgeRating]]
    background_image: Optional[str]
    categories: Any
    category_ids: Any
    community_score: Optional[int]
    community_score_group: int
    community_score_rating: int
    completion_status: CompletionStatus
    completion_status_id: str
    cover_image: Optional[str]
    critic_score: Optional[int]
    critic_score_group: int
    critic_score_rating: int
    description: Optional[str]
    developer_ids: Optional[List[str]]
    developers: Optional[List[Genre]]
    enable_system_hdr: bool
    favorite: bool
    feature_ids: Optional[List[str]]
    features: Optional[List[Feature]]
    game_actions: Any
    game_id: str
    game_started_script: Any
    genre_ids: Optional[List[str]]
    genres: Optional[List[Genre]]
    hidden: bool
    icon: Optional[str]
    id: str
    include_library_plugin_action: bool
    install_directory: Any
    install_size: Any
    install_size_group: int
    installation_status: int
    is_custom_game: bool
    is_installed: bool
    is_installing: bool
    is_launching: bool
    is_running: bool
    is_uninstalling: bool
    last_activity: Any
    last_activity_segment: int
    last_size_scan_date: Any
    links: Optional[List[Link]]
    manual: Any
    modified: str
    modified_segment: int
    name: str
    notes: Any
    override_install_state: bool
    platform_ids: Optional[List[str]]
    platforms: Optional[List[Platform]]
    play_count: int
    playtime: int
    playtime_category: int
    plugin_id: str
    post_script: Any
    pre_script: Any
    publisher_ids: Optional[List[str]]
    publishers: Optional[List[Genre]]
    recent_activity: str
    recent_activity_segment: int
    region_ids: Any
    regions: Any
    release_date: Optional[ReleaseDate]
    release_year: Optional[int]
    roms: Any
    series: Optional[List[Series]]
    series_ids: Optional[List[str]]
    sorting_name: Any
    source: Any
    source_id: str
    tag_ids: Any
    tags: Any
    use_global_game_started_script: bool
    use_global_post_script: bool
    use_global_pre_script: bool
    user_score: Any
    user_score_group: int
    user_score_rating: int
    version: Any


class Games(BaseModel):
    games: Optional[List[Game]] = None
