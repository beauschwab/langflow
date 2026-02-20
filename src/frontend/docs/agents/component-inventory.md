# Comprehensive Frontend Component Inventory

Inventory generated from `src/frontend/src` TypeScript component files (`.ts`/`.tsx`).

## Summary counts

- `components`: **183** files
- `pages`: **112** files
- `modals`: **121** files
- `CustomNodes`: **50** files

## Inventory by area

### `components`

Reusable UI and feature components used across pages.

#### `components/authorization` (5 files)

- `components/authorization/authAdminGuard/index.tsx`
- `components/authorization/authGuard/index.tsx`
- `components/authorization/authLoginGuard/index.tsx`
- `components/authorization/authSettingsGuard/index.tsx`
- `components/authorization/storeGuard/index.tsx`

#### `components/common` (31 files)

- `components/common/GradientWrapper/index.tsx`
- `components/common/ImageViewer/index.tsx`
- `components/common/accordionComponent/composite/folderAccordionComponent/index.tsx`
- `components/common/accordionComponent/index.tsx`
- `components/common/animatedNumbers/index.tsx`
- `components/common/arrayReaderComponent/index.tsx`
- `components/common/catchAllRoutes/index.tsx`
- `components/common/crashErrorComponent/index.tsx`
- `components/common/fetchErrorComponent/index.tsx`
- `components/common/fetchIconComponent/index.tsx`
- `components/common/genericIconComponent/index.tsx`
- `components/common/horizontalScrollFadeComponent/index.tsx`
- `components/common/loadingComponent/index.tsx`
- `components/common/loadingTextComponent/index.tsx`
- `components/common/numberReader/index.tsx`
- `components/common/objectRender/index.tsx`
- `components/common/pageLayout/index.tsx`
- `components/common/paginatorComponent/index.tsx`
- `components/common/renderIconComponent/components/renderKey/index.tsx`
- `components/common/renderIconComponent/index.tsx`
- `components/common/sanitizedHTMLWrapper/index.tsx`
- `components/common/shadTooltipComponent/index.tsx`
- `components/common/skeletonCardComponent/index.tsx`
- `components/common/storeCardComponent/hooks/use-data-effect.ts`
- `components/common/storeCardComponent/hooks/use-handle-install.ts`
- `components/common/storeCardComponent/index.tsx`
- `components/common/storeCardComponent/utils/convert-test-name.tsx`
- `components/common/stringReaderComponent/index.tsx`
- `components/common/tagsSelectorComponent/index.tsx`
- `components/common/timeoutErrorComponent/index.tsx`
- `components/common/viewTriggers/chat/index.tsx`

#### `components/core` (103 files)

- `components/core/GlobalVariableModal/GlobalVariableModal.tsx`
- `components/core/GlobalVariableModal/utils/sort-by-name.tsx`
- `components/core/appHeaderComponent/components/AccountMenu/index.tsx`
- `components/core/appHeaderComponent/components/FlowMenu/index.tsx`
- `components/core/appHeaderComponent/components/GithubStarButton/index.tsx`
- `components/core/appHeaderComponent/components/HeaderMenu/index.tsx`
- `components/core/appHeaderComponent/components/ProfileIcon/index.tsx`
- `components/core/appHeaderComponent/components/ThemeButtons/index.tsx`
- `components/core/appHeaderComponent/index.tsx`
- `components/core/border-trail.tsx`
- `components/core/canvasControlsComponent/index.tsx`
- `components/core/cardComponent/components/dragCardComponent/index.tsx`
- `components/core/cardComponent/hooks/use-handle-install.ts`
- `components/core/cardComponent/hooks/use-on-drag-start.tsx`
- `components/core/cardComponent/index.tsx`
- `components/core/cardComponent/utils/convert-test-name.tsx`
- `components/core/cardsWrapComponent/index.tsx`
- `components/core/chatComponents/ContentBlockDisplay.tsx`
- `components/core/chatComponents/ContentDisplay.tsx`
- `components/core/chatComponents/DurationDisplay.tsx`
- `components/core/codeTabsComponent/ChatCodeTabComponent.tsx`
- `components/core/codeTabsComponent/components/tweakComponent/index.tsx`
- `components/core/codeTabsComponent/components/tweaksComponent/index.tsx`
- `components/core/codeTabsComponent/index.tsx`
- `components/core/csvOutputComponent/helpers/convert-data-function.ts`
- `components/core/csvOutputComponent/index.tsx`
- `components/core/dataOutputComponent/index.tsx`
- `components/core/dateReaderComponent/index.tsx`
- `components/core/dropdownButtonComponent/index.tsx`
- `components/core/dropdownComponent/index.tsx`
- `components/core/editFlowSettingsComponent/index.tsx`
- `components/core/flowToolbarComponent/components/deploy-dropdown.tsx`
- `components/core/flowToolbarComponent/components/flow-toolbar-options.tsx`
- `components/core/flowToolbarComponent/components/playground-button.tsx`
- `components/core/flowToolbarComponent/index.tsx`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/components/add-folder-button.tsx`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/components/folder-select-item.tsx`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/components/header-buttons.tsx`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/components/input-edit-folder-name.tsx`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/components/select-options.tsx`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/components/upload-folder-button.tsx`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/helpers/handle-select-change.ts`
- `components/core/folderSidebarComponent/components/sideBarFolderButtons/index.tsx`
- `components/core/folderSidebarComponent/components/sidebarFolderSkeleton/index.tsx`
- `components/core/folderSidebarComponent/hooks/use-on-file-drop.ts`
- `components/core/jsonEditor/index.tsx`
- `components/core/jsonOutputComponent/json-output-view.tsx`
- `components/core/parameterRenderComponent/components/TableNodeComponent/index.tsx`
- `components/core/parameterRenderComponent/components/codeAreaComponent/index.tsx`
- `components/core/parameterRenderComponent/components/copyFieldAreaComponent/index.tsx`
- `components/core/parameterRenderComponent/components/dictComponent/index.tsx`
- `components/core/parameterRenderComponent/components/dropdownComponent/index.tsx`
- `components/core/parameterRenderComponent/components/emptyParameterComponent/index.tsx`
- `components/core/parameterRenderComponent/components/floatComponent/index.tsx`
- `components/core/parameterRenderComponent/components/inputComponent/components/helpers/get-icon-name.ts`
- `components/core/parameterRenderComponent/components/inputComponent/components/helpers/get-input-class-name.ts`
- `components/core/parameterRenderComponent/components/inputComponent/components/popover/index.tsx`
- `components/core/parameterRenderComponent/components/inputComponent/components/popoverObject/index.tsx`
- `components/core/parameterRenderComponent/components/inputComponent/index.tsx`
- `components/core/parameterRenderComponent/components/inputFileComponent/index.tsx`
- `components/core/parameterRenderComponent/components/inputGlobalComponent/index.tsx`
- `components/core/parameterRenderComponent/components/inputListComponent/components/button-input-list.tsx`
- `components/core/parameterRenderComponent/components/inputListComponent/components/delete-button-input-list.tsx`
- `components/core/parameterRenderComponent/components/inputListComponent/components/dropdown-menu.tsx`
- `components/core/parameterRenderComponent/components/inputListComponent/helpers/get-class-name.ts`
- `components/core/parameterRenderComponent/components/inputListComponent/helpers/get-test-id.ts`
- `components/core/parameterRenderComponent/components/inputListComponent/index.tsx`
- `components/core/parameterRenderComponent/components/intComponent/index.tsx`
- `components/core/parameterRenderComponent/components/keypairListComponent/index.tsx`
- `components/core/parameterRenderComponent/components/linkComponent/index.tsx`
- `components/core/parameterRenderComponent/components/multiselectComponent/index.tsx`
- `components/core/parameterRenderComponent/components/promptComponent/index.tsx`
- `components/core/parameterRenderComponent/components/refreshParameterComponent/index.tsx`
- `components/core/parameterRenderComponent/components/sliderComponent/components/slider-labels.tsx`
- `components/core/parameterRenderComponent/components/sliderComponent/helpers/build-color-by-name.ts`
- `components/core/parameterRenderComponent/components/sliderComponent/helpers/get-min-max-value.ts`
- `components/core/parameterRenderComponent/components/sliderComponent/index.tsx`
- `components/core/parameterRenderComponent/components/strRenderComponent/index.tsx`
- `components/core/parameterRenderComponent/components/tabComponent/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/ResetColumns/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/TableOptions/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/loadingOverlay/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/tableAdvancedToggleCellRender/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/tableAutoCellRender/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/tableDropdownCellEditor/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/tableNodeCellRender/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/tableToggleCellEditor/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/components/tableTooltipRender/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/index.tsx`
- `components/core/parameterRenderComponent/components/tableComponent/utils/reset-grid-columns.tsx`
- `components/core/parameterRenderComponent/components/textAreaComponent/index.tsx`
- `components/core/parameterRenderComponent/components/textInputComponent/index.tsx`
- `components/core/parameterRenderComponent/components/toggleShadComponent/index.tsx`
- `components/core/parameterRenderComponent/components/webhookFieldComponent/index.tsx`
- `components/core/parameterRenderComponent/helpers/get-placeholder-disabled.ts`
- `components/core/parameterRenderComponent/helpers/get-textarea-content-class.ts`
- `components/core/parameterRenderComponent/index.tsx`
- `components/core/parameterRenderComponent/types.ts`
- `components/core/pdfViewer/Error/index.tsx`
- `components/core/pdfViewer/index.tsx`
- `components/core/pdfViewer/noData/index.tsx`
- `components/core/sidebarComponent/index.tsx`
- `components/core/textOutputComponent/index.tsx`

#### `components/ui` (44 files)

- `components/ui/TextShimmer.tsx`
- `components/ui/accordion.tsx`
- `components/ui/alert.tsx`
- `components/ui/badge.tsx`
- `components/ui/border-beams.tsx`
- `components/ui/button.tsx`
- `components/ui/card.tsx`
- `components/ui/checkbox.tsx`
- `components/ui/checkmark.tsx`
- `components/ui/collapsible.tsx`
- `components/ui/combobox.tsx`
- `components/ui/command.tsx`
- `components/ui/custom-accordion.tsx`
- `components/ui/dialog-with-no-close.tsx`
- `components/ui/dialog.tsx`
- `components/ui/disclosure.tsx`
- `components/ui/dropdown-menu.tsx`
- `components/ui/form.tsx`
- `components/ui/input.tsx`
- `components/ui/label.tsx`
- `components/ui/loading.tsx`
- `components/ui/menubar.tsx`
- `components/ui/morphing-menu.tsx`
- `components/ui/popover.tsx`
- `components/ui/progress.tsx`
- `components/ui/refreshButton.tsx`
- `components/ui/rename-label.tsx`
- `components/ui/select-custom.tsx`
- `components/ui/select.tsx`
- `components/ui/separator.tsx`
- `components/ui/sheet.tsx`
- `components/ui/sidebar.tsx`
- `components/ui/skeleton.tsx`
- `components/ui/skeletonGroup.tsx`
- `components/ui/slider.tsx`
- `components/ui/switch.tsx`
- `components/ui/table.tsx`
- `components/ui/tabs-button.tsx`
- `components/ui/tabs.tsx`
- `components/ui/textAnimation.tsx`
- `components/ui/textarea.tsx`
- `components/ui/toggle.tsx`
- `components/ui/tooltip.tsx`
- `components/ui/xmark.tsx`

### `pages`

Route-level screens and page-specific component composition.

#### `pages/AdminPage` (2 files)

- `pages/AdminPage/LoginPage/index.tsx`
- `pages/AdminPage/index.tsx`

#### `pages/AppAuthenticatedPage` (1 files)

- `pages/AppAuthenticatedPage/index.tsx`

#### `pages/AppInitPage` (1 files)

- `pages/AppInitPage/index.tsx`

#### `pages/AppWrapperPage` (3 files)

- `pages/AppWrapperPage/components/GenericErrorComponent/index.tsx`
- `pages/AppWrapperPage/hooks/use-health-check.ts`
- `pages/AppWrapperPage/index.tsx`

#### `pages/DashboardWrapperPage` (1 files)

- `pages/DashboardWrapperPage/index.tsx`

#### `pages/DeleteAccountPage` (1 files)

- `pages/DeleteAccountPage/index.tsx`

#### `pages/FlowPage` (45 files)

- `pages/FlowPage/components/ConnectionLineComponent/index.tsx`
- `pages/FlowPage/components/DisclosureComponent/index.tsx`
- `pages/FlowPage/components/PageComponent/index.tsx`
- `pages/FlowPage/components/PageComponent/utils/get-random-name.tsx`
- `pages/FlowPage/components/PageComponent/utils/is-wrapped-with-class.tsx`
- `pages/FlowPage/components/ParentDisclosureComponent/index.tsx`
- `pages/FlowPage/components/SelectionMenuComponent/index.tsx`
- `pages/FlowPage/components/UpdateAllComponents/index.tsx`
- `pages/FlowPage/components/extraSidebarComponent/SidebarCategoryComponent/index.tsx`
- `pages/FlowPage/components/extraSidebarComponent/index.tsx`
- `pages/FlowPage/components/extraSidebarComponent/sideBarDraggableComponent/index.tsx`
- `pages/FlowPage/components/extraSidebarComponent/sideBarNoteComponent/index.tsx`
- `pages/FlowPage/components/extraSidebarComponent/sidebarFilterComponent/index.tsx`
- `pages/FlowPage/components/extraSidebarComponent/utils/sensitive-sort.tsx`
- `pages/FlowPage/components/extraSidebarComponent/utils.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/bundleItems/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/categoryDisclouse/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/categoryGroup/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/emptySearchComponent/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/featureTogglesComponent/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/searchInput/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/sidebarBundles/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/sidebarDraggableComponent/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/sidebarFooterButtons/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/sidebarHeader/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/components/sidebarItemsList/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/helpers/apply-beta-filter.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/apply-edge-filter.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/apply-legacy-filter.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/combined-results.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/disable-item.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/filtered-data.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/get-disabled-tooltip.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/normalize-string.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/search-on-metadata.ts`
- `pages/FlowPage/components/flowSidebarComponent/helpers/traditional-search-metadata.ts`
- `pages/FlowPage/components/flowSidebarComponent/index.tsx`
- `pages/FlowPage/components/flowSidebarComponent/types/index.ts`
- `pages/FlowPage/components/nodeToolbarComponent/components/toolbar-button.tsx`
- `pages/FlowPage/components/nodeToolbarComponent/components/toolbar-modals.tsx`
- `pages/FlowPage/components/nodeToolbarComponent/hooks/use-shortcuts.ts`
- `pages/FlowPage/components/nodeToolbarComponent/index.tsx`
- `pages/FlowPage/components/nodeToolbarComponent/shortcutDisplay/index.tsx`
- `pages/FlowPage/components/nodeToolbarComponent/toolbarSelectItem/index.tsx`
- `pages/FlowPage/index.tsx`

#### `pages/LoadingPage` (1 files)

- `pages/LoadingPage/index.tsx`

#### `pages/LoginPage` (1 files)

- `pages/LoginPage/index.tsx`

#### `pages/MainPage` (29 files)

- `pages/MainPage/components/dropdown/index.tsx`
- `pages/MainPage/components/grid/index.tsx`
- `pages/MainPage/components/gridSkeleton/index.tsx`
- `pages/MainPage/components/header/index.tsx`
- `pages/MainPage/components/inputSearchComponent/index.tsx`
- `pages/MainPage/components/list/index.tsx`
- `pages/MainPage/components/listSkeleton/index.tsx`
- `pages/MainPage/components/modalsComponent/index.tsx`
- `pages/MainPage/constants.ts`
- `pages/MainPage/entities/index.tsx`
- `pages/MainPage/hooks/use-description-modal.ts`
- `pages/MainPage/hooks/use-dropdown-options.ts`
- `pages/MainPage/hooks/use-filtered-flows.ts`
- `pages/MainPage/hooks/use-handle-duplicate.ts`
- `pages/MainPage/hooks/use-handle-select-all.ts`
- `pages/MainPage/hooks/use-on-file-drop.ts`
- `pages/MainPage/hooks/use-select-options-change.ts`
- `pages/MainPage/hooks/use-selected-flows.ts`
- `pages/MainPage/pages/emptyFolder/index.tsx`
- `pages/MainPage/pages/emptyPage/index.tsx`
- `pages/MainPage/pages/filesPage/components/dragWrapComponent/index.tsx`
- `pages/MainPage/pages/filesPage/index.tsx`
- `pages/MainPage/pages/homePage/index.tsx`
- `pages/MainPage/pages/index.tsx`
- `pages/MainPage/utils/get-name-by-type.ts`
- `pages/MainPage/utils/get-template-style.ts`
- `pages/MainPage/utils/handle-download-folder.ts`
- `pages/MainPage/utils/sort-flows.ts`
- `pages/MainPage/utils/time-elapse.ts`

#### `pages/Playground` (1 files)

- `pages/Playground/index.tsx`

#### `pages/ProfileSettingsPage` (1 files)

- `pages/ProfileSettingsPage/index.tsx`

#### `pages/SettingsPage` (22 files)

- `pages/SettingsPage/index.tsx`
- `pages/SettingsPage/pages/ApiKeysPage/components/ApiKeyHeader/index.tsx`
- `pages/SettingsPage/pages/ApiKeysPage/helpers/column-defs.ts`
- `pages/SettingsPage/pages/ApiKeysPage/helpers/get-modal-props.tsx`
- `pages/SettingsPage/pages/ApiKeysPage/index.tsx`
- `pages/SettingsPage/pages/GeneralPage/components/GeneralPageHeader/index.tsx`
- `pages/SettingsPage/pages/GeneralPage/components/PasswordForm/index.tsx`
- `pages/SettingsPage/pages/GeneralPage/components/ProfileGradientForm/index.tsx`
- `pages/SettingsPage/pages/GeneralPage/components/ProfilePictureForm/components/profilePictureChooserComponent/hooks/use-preload-images.ts`
- `pages/SettingsPage/pages/GeneralPage/components/ProfilePictureForm/components/profilePictureChooserComponent/index.tsx`
- `pages/SettingsPage/pages/GeneralPage/components/ProfilePictureForm/index.tsx`
- `pages/SettingsPage/pages/GeneralPage/index.tsx`
- `pages/SettingsPage/pages/GlobalVariablesPage/index.tsx`
- `pages/SettingsPage/pages/ShortcutsPage/CellRenderWrapper/index.tsx`
- `pages/SettingsPage/pages/ShortcutsPage/EditShortcutButton/index.tsx`
- `pages/SettingsPage/pages/ShortcutsPage/index.tsx`
- `pages/SettingsPage/pages/StoreApiKeyPage/components/StoreApiKeyForm.tsx`
- `pages/SettingsPage/pages/StoreApiKeyPage/index.tsx`
- `pages/SettingsPage/pages/StorePage/index.tsx`
- `pages/SettingsPage/pages/hooks/use-scroll-to-element.tsx`
- `pages/SettingsPage/pages/messagesPage/components/headerMessages/index.tsx`
- `pages/SettingsPage/pages/messagesPage/index.tsx`

#### `pages/SignUpPage` (1 files)

- `pages/SignUpPage/index.tsx`

#### `pages/StorePage` (1 files)

- `pages/StorePage/index.tsx`

#### `pages/ViewPage` (1 files)

- `pages/ViewPage/index.tsx`

### `modals`

Modal-based user interaction surfaces and workflows.

#### `modals/EmbedModal` (1 files)

- `modals/EmbedModal/embed-modal.tsx`

#### `modals/IOModal` (63 files)

- `modals/IOModal/components/IOFieldView/components/csv-selected.tsx`
- `modals/IOModal/components/IOFieldView/components/file-input.tsx`
- `modals/IOModal/components/IOFieldView/components/json-input.tsx`
- `modals/IOModal/components/IOFieldView/components/key-pair-input.tsx`
- `modals/IOModal/components/IOFieldView/components/session-selector.tsx`
- `modals/IOModal/components/IOFieldView/io-field-view.tsx`
- `modals/IOModal/components/chat-view-wrapper.tsx`
- `modals/IOModal/components/chatView/chatInput/chat-input.tsx`
- `modals/IOModal/components/chatView/chatInput/components/button-send-wrapper.tsx`
- `modals/IOModal/components/chatView/chatInput/components/input-wrapper.tsx`
- `modals/IOModal/components/chatView/chatInput/components/no-input.tsx`
- `modals/IOModal/components/chatView/chatInput/components/text-area-wrapper.tsx`
- `modals/IOModal/components/chatView/chatInput/components/upload-file-button.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/audio-settings-dialog.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/components/header.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/components/language-select.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/components/microphone-select.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/audio-settings/components/voice-select.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/settings-voice-button.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/components/voice-button.tsx`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/check-provider.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/format-time.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/streamProcessor.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/helpers/utils.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-bar-controls.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-handle-websocket-message.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-initialize-audio.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-interrupt-playback.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-play-next-audio-chunk.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-start-conversation.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-start-recording.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/hooks/use-stop-recording.ts`
- `modals/IOModal/components/chatView/chatInput/components/voice-assistant/voice-assistant.tsx`
- `modals/IOModal/components/chatView/chatInput/helpers/get-class-file-preview.ts`
- `modals/IOModal/components/chatView/chatInput/hooks/use-auto-resize-text-area.ts`
- `modals/IOModal/components/chatView/chatInput/hooks/use-drag-and-drop.ts`
- `modals/IOModal/components/chatView/chatInput/hooks/use-file-handler.ts`
- `modals/IOModal/components/chatView/chatInput/hooks/use-focus-unlock.ts`
- `modals/IOModal/components/chatView/chatInput/hooks/use-handle-file-change.ts`
- `modals/IOModal/components/chatView/chatInput/hooks/use-upload.ts`
- `modals/IOModal/components/chatView/chatMessage/chat-message.tsx`
- `modals/IOModal/components/chatView/chatMessage/components/chat-logo-icon.tsx`
- `modals/IOModal/components/chatView/chatMessage/components/code-block.tsx`
- `modals/IOModal/components/chatView/chatMessage/components/content-view.tsx`
- `modals/IOModal/components/chatView/chatMessage/components/edit-message-field.tsx`
- `modals/IOModal/components/chatView/chatMessage/components/edit-message.tsx`
- `modals/IOModal/components/chatView/chatMessage/components/file-card-wrapper.tsx`
- `modals/IOModal/components/chatView/chatMessage/components/message-options.tsx`
- `modals/IOModal/components/chatView/chatMessage/helpers/convert-files.ts`
- `modals/IOModal/components/chatView/components/chat-view.tsx`
- `modals/IOModal/components/chatView/fileComponent/components/download-button.tsx`
- `modals/IOModal/components/chatView/fileComponent/components/file-card.tsx`
- `modals/IOModal/components/chatView/fileComponent/components/file-preview.tsx`
- `modals/IOModal/components/chatView/fileComponent/utils/format-file-name.tsx`
- `modals/IOModal/components/chatView/fileComponent/utils/get-classes.tsx`
- `modals/IOModal/components/flow-running-squeleton.tsx`
- `modals/IOModal/components/selected-view-field.tsx`
- `modals/IOModal/components/session-view.tsx`
- `modals/IOModal/components/sidebar-open-view.tsx`
- `modals/IOModal/new-modal.tsx`
- `modals/IOModal/types/chat-view-wrapper.ts`
- `modals/IOModal/types/selected-view-field.ts`
- `modals/IOModal/types/sidebar-open-view.ts`

#### `modals/apiModal` (11 files)

- `modals/apiModal/codeTabs/code-tabs.tsx`
- `modals/apiModal/index.tsx`
- `modals/apiModal/new-api-modal.tsx`
- `modals/apiModal/utils/get-changes-types.ts`
- `modals/apiModal/utils/get-curl-code.tsx`
- `modals/apiModal/utils/get-js-api-code.tsx`
- `modals/apiModal/utils/get-nodes-with-default-value.ts`
- `modals/apiModal/utils/get-python-api-code.tsx`
- `modals/apiModal/utils/get-python-code.tsx`
- `modals/apiModal/utils/get-widget-code.tsx`
- `modals/apiModal/utils/tabs-array.tsx`

#### `modals/baseModal` (2 files)

- `modals/baseModal/helpers/switch-case-size.ts`
- `modals/baseModal/index.tsx`

#### `modals/codeAreaModal` (1 files)

- `modals/codeAreaModal/index.tsx`

#### `modals/confirmationModal` (1 files)

- `modals/confirmationModal/index.tsx`

#### `modals/deleteConfirmationModal` (1 files)

- `modals/deleteConfirmationModal/index.tsx`

#### `modals/dictAreaModal` (1 files)

- `modals/dictAreaModal/index.tsx`

#### `modals/editNodeModal` (5 files)

- `modals/editNodeModal/components/editNodeComponent/index.tsx`
- `modals/editNodeModal/hooks/use-column-defs.ts`
- `modals/editNodeModal/hooks/use-handle-change-advanced.ts`
- `modals/editNodeModal/hooks/use-row-data.ts`
- `modals/editNodeModal/index.tsx`

#### `modals/exportModal` (1 files)

- `modals/exportModal/index.tsx`

#### `modals/fileManagerModal` (7 files)

- `modals/fileManagerModal/components/dragFilesComponent/index.tsx`
- `modals/fileManagerModal/components/filesContextMenuComponent/index.tsx`
- `modals/fileManagerModal/components/filesRendererComponent/components/fileRendererComponent/index.tsx`
- `modals/fileManagerModal/components/filesRendererComponent/index.tsx`
- `modals/fileManagerModal/components/importButtonComponent/index.tsx`
- `modals/fileManagerModal/components/recentFilesComponent/index.tsx`
- `modals/fileManagerModal/index.tsx`

#### `modals/flowLogsModal` (1 files)

- `modals/flowLogsModal/index.tsx`

#### `modals/flowSettingsModal` (1 files)

- `modals/flowSettingsModal/index.tsx`

#### `modals/newFlowModal` (3 files)

- `modals/newFlowModal/components/NewFlowCardComponent/index.tsx`
- `modals/newFlowModal/components/hooks/use-redirect-flow-card-click.tsx`
- `modals/newFlowModal/components/undrawCards/index.tsx`

#### `modals/nodeModal` (1 files)

- `modals/nodeModal/components/modalField/index.tsx`

#### `modals/promptModal` (2 files)

- `modals/promptModal/index.tsx`
- `modals/promptModal/utils/var-highlight-html.tsx`

#### `modals/saveChangesModal` (1 files)

- `modals/saveChangesModal/index.tsx`

#### `modals/secretKeyModal` (4 files)

- `modals/secretKeyModal/components/content-render.tsx`
- `modals/secretKeyModal/components/form-key-render.tsx`
- `modals/secretKeyModal/components/header-render.tsx`
- `modals/secretKeyModal/index.tsx`

#### `modals/shareModal` (2 files)

- `modals/shareModal/index.tsx`
- `modals/shareModal/utils/get-tags-ids.tsx`

#### `modals/tableModal` (1 files)

- `modals/tableModal/index.tsx`

#### `modals/templatesModal` (7 files)

- `modals/templatesModal/components/GetStartedComponent/index.tsx`
- `modals/templatesModal/components/TemplateCardComponent/index.tsx`
- `modals/templatesModal/components/TemplateCategoryComponent/index.tsx`
- `modals/templatesModal/components/TemplateContentComponent/index.tsx`
- `modals/templatesModal/components/TemplateGetStartedCardComponent/index.tsx`
- `modals/templatesModal/components/navComponent/index.tsx`
- `modals/templatesModal/index.tsx`

#### `modals/textAreaModal` (1 files)

- `modals/textAreaModal/index.tsx`

#### `modals/textModal` (2 files)

- `modals/textModal/components/textEditorArea/index.tsx`
- `modals/textModal/index.tsx`

#### `modals/userManagementModal` (1 files)

- `modals/userManagementModal/index.tsx`

### `CustomNodes`

Canvas node implementations and node-specific helpers/hooks.

#### `CustomNodes/GenericNode` (21 files)

- `CustomNodes/GenericNode/components/HandleTooltipComponent/index.tsx`
- `CustomNodes/GenericNode/components/NodeDescription/index.tsx`
- `CustomNodes/GenericNode/components/NodeDialogComponent/index.tsx`
- `CustomNodes/GenericNode/components/NodeInputField/index.tsx`
- `CustomNodes/GenericNode/components/NodeInputInfo/index.tsx`
- `CustomNodes/GenericNode/components/NodeName/index.tsx`
- `CustomNodes/GenericNode/components/NodeOutputParameter/index.tsx`
- `CustomNodes/GenericNode/components/NodeOutputfield/index.tsx`
- `CustomNodes/GenericNode/components/NodeStatus/components/build-status-display.tsx`
- `CustomNodes/GenericNode/components/NodeStatus/index.tsx`
- `CustomNodes/GenericNode/components/NodeStatus/utils/format-run-time.ts`
- `CustomNodes/GenericNode/components/OutputComponent/index.tsx`
- `CustomNodes/GenericNode/components/RenderInputParameters/index.tsx`
- `CustomNodes/GenericNode/components/handleRenderComponent/index.tsx`
- `CustomNodes/GenericNode/components/nodeIcon/index.tsx`
- `CustomNodes/GenericNode/components/outputModal/components/switchOutputView/components/index.tsx`
- `CustomNodes/GenericNode/components/outputModal/components/switchOutputView/helpers/convert-to-table-rows.ts`
- `CustomNodes/GenericNode/components/outputModal/components/switchOutputView/index.tsx`
- `CustomNodes/GenericNode/components/outputModal/index.tsx`
- `CustomNodes/GenericNode/hooks/use-get-build-status.ts`
- `CustomNodes/GenericNode/index.tsx`

#### `CustomNodes/NoteNode` (4 files)

- `CustomNodes/NoteNode/NoteToolbarComponent/index.tsx`
- `CustomNodes/NoteNode/components/color-picker-buttons.tsx`
- `CustomNodes/NoteNode/components/select-items.tsx`
- `CustomNodes/NoteNode/index.tsx`

#### `CustomNodes/helpers` (12 files)

- `CustomNodes/helpers/check-lucide-icons.ts`
- `CustomNodes/helpers/count-handles.ts`
- `CustomNodes/helpers/get-class-from-build-status.ts`
- `CustomNodes/helpers/get-class-toolbar-transform.ts`
- `CustomNodes/helpers/get-node-input-colors-name.ts`
- `CustomNodes/helpers/get-node-input-colors.ts`
- `CustomNodes/helpers/get-node-output-colors-name.ts`
- `CustomNodes/helpers/get-node-output-colors.ts`
- `CustomNodes/helpers/mutate-template.ts`
- `CustomNodes/helpers/process-node-advanced-fields.ts`
- `CustomNodes/helpers/sort-tool-mode-field.ts`
- `CustomNodes/helpers/update-hidden-outputs.ts`

#### `CustomNodes/hooks` (10 files)

- `CustomNodes/hooks/use-check-code-validity.ts`
- `CustomNodes/hooks/use-fetch-data-on-mount.ts`
- `CustomNodes/hooks/use-handle-new-value.ts`
- `CustomNodes/hooks/use-handle-node-class.ts`
- `CustomNodes/hooks/use-icons-status.tsx`
- `CustomNodes/hooks/use-merge-refs.ts`
- `CustomNodes/hooks/use-update-all-nodes.ts`
- `CustomNodes/hooks/use-update-node-code.ts`
- `CustomNodes/hooks/use-update-validation-status.ts`
- `CustomNodes/hooks/use-validation-status-string.ts`

#### `CustomNodes/utils` (3 files)

- `CustomNodes/utils/get-field-title.tsx`
- `CustomNodes/utils/get-handle-id.tsx`
- `CustomNodes/utils/sort-fields.tsx`
