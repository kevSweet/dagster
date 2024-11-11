import {execSync} from 'child_process';
import path from 'path';

const ASSET_SELECTION_GRAMMAR_FILE_PATH = path.resolve(
  '../../../../python_modules/dagster/dagster/_core/definitions/antlr_asset_selection/AssetSelection.g4',
);
execSync(
  `antlr4ts -visitor -o ./src/asset-selection/generated ${ASSET_SELECTION_GRAMMAR_FILE_PATH}`,
);

execSync(`yarn prettier ./src/asset-selection/generated/*.ts --write`);
